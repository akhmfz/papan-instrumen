// pipeline.mjs — Production Validation Pipeline (P1-1)
//
// Loads scenarios from JSON → extracts actual production Pine Script source →
// generates PineTS-compatible test scripts → runs via PineTS → validates outputs.
//
// Adding a new scenario:
//   1. Add an entry to data/scenarios.json with:
//      - name, description, inputs (all financial/flag variables), expected (score name → value)
//      - See existing entries for format reference
//   2. Run: node tests/production/pipeline.mjs --update-golden
//      This re-generates golden/scenarios.json with actual outputs as baseline
//   3. Verify: node tests/production/pipeline.mjs --scenario YOUR_SCENARIO
//
// Usage:
//   node tests/production/pipeline.mjs                    # run all scenarios
//   node tests/production/pipeline.mjs --scenario BBCA    # run specific scenario
//   node tests/production/pipeline.mjs --json             # JSON output
//   node tests/production/pipeline.mjs --update-golden    # regenerate golden snapshots

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { PineTS } from 'pinets';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = join(__dirname, '..', '..');
const DATA_DIR = join(__dirname, 'data');
const GOLDEN_DIR = join(__dirname, 'golden');

// Import our production source extractor
const { extractUtilities, extractScoringLogic, generatePineScript } = await import(
    join(__dirname, 'extract-production.mjs')
);

// ── Helpers ──

function dummyCandles(count = 20) {
    return Array.from({ length: count }, (_, i) => ({
        open: 100 + i, high: 102 + i, low: 99 + i,
        close: 101 + i, volume: 1000000 + i * 1000,
        openTime: 1751673600000 + i * 86400000,
        closeTime: 1751673600000 + (i + 1) * 86400000,
    }));
}

function stripVolatile(obj) {
    if (typeof obj !== 'object' || obj === null) return obj;
    if (Array.isArray(obj)) return obj.map(stripVolatile);
    const clean = {};
    for (const [k, v] of Object.entries(obj)) {
        if (!['generated_at', 'parse_time_ms'].includes(k)) {
            clean[k] = stripVolatile(v);
        }
    }
    return clean;
}

// ── Core: run a single scenario ──

async function runScenario(scenario) {
    const pineScript = generatePineScript(scenario);

    const t0 = Date.now();
    const pineTS = new PineTS(dummyCandles(20));

    let result;
    try {
        result = await pineTS.run(pineScript);
    } catch (err) {
        return {
            scenario: scenario.name,
            status: 'ERROR',
            error: err.message,
            parse_time_ms: Date.now() - t0,
        };
    }

    const parseTime = Date.now() - t0;
    const plots = result.plots || {};

    // Extract scores from plots
    const actual = {};
    for (const [key] of Object.entries(scenario.expected || {})) {
        const plotData = plots[key];
        if (plotData && plotData.data && plotData.data.length > 0) {
            const val = plotData.data[plotData.data.length - 1].value;
            actual[key] = typeof val === 'number' ? Math.round(val * 10) / 10 : val;
        } else {
            actual[key] = null;
        }
    }

    // Compare against expected
    const mismatches = [];
    for (const [key, expectedVal] of Object.entries(scenario.expected || {})) {
        const actualVal = actual[key];
        if (actualVal === null || actualVal === undefined) {
            mismatches.push({ key, expected: expectedVal, actual: null });
        } else {
            const tolerance = 5.0; // ±5 points tolerance for PineTS floating point
            let expectedNum = typeof expectedVal === 'number' ? expectedVal : parseFloat(expectedVal);
            if (Math.abs(actualVal - expectedNum) > tolerance) {
                mismatches.push({ key, expected: expectedNum, actual: actualVal });
            }
        }
    }

    const passed = mismatches.length === 0;

    return {
        scenario: scenario.name,
        status: passed ? 'PASS' : 'FAIL',
        description: scenario.description,
        parse_time_ms: parseTime,
        checks: Object.keys(scenario.expected || {}).length,
        passed_checks: Object.keys(scenario.expected || {}).length - mismatches.length,
        mismatches: passed ? [] : mismatches,
        actual,
    };
}

// ── Main ──

async function main() {
    const args = process.argv.slice(2);
    const filterScenario = args.includes('--scenario') ? args[args.indexOf('--scenario') + 1] : null;
    const outputJson = args.includes('--json');
    const updateGolden = args.includes('--update-golden');

    // Load scenarios
    const scenarios = JSON.parse(readFileSync(join(DATA_DIR, 'scenarios.json'), 'utf8'));
    const toRun = filterScenario
        ? scenarios.filter(s => s.name.toLowerCase().includes(filterScenario.toLowerCase()))
        : scenarios;

    if (toRun.length === 0) {
        console.error(`No scenarios match filter: ${filterScenario}`);
        process.exit(1);
    }

    // Verify production source can be extracted
    let utils, scoring;
    try {
        utils = extractUtilities();
        scoring = extractScoringLogic();
        if (!utils || !scoring) throw new Error('Empty extraction');
    } catch (err) {
        console.error(`❌ Production source extraction FAILED: ${err.message}`);
        console.error('   Cannot proceed — the pipeline requires valid production source.');
        process.exit(2);
    }

    const results = [];
    let totalPassed = 0;
    let totalFailed = 0;
    let totalErrors = 0;

    console.log(`\n${'='.repeat(60)}`);
    console.log(`  Production Validation Pipeline — P1-1`);
    console.log(`  ${toRun.length} scenario(s) — ${new Date().toISOString()}`);
    console.log(`  Source: src/modules/01-base.pine + 04-scoring.pine (${(utils + scoring).split('\n').length} lines)`);
    console.log(`${'='.repeat(60)}\n`);

    for (const scenario of toRun) {
        const result = await runScenario(scenario);
        results.push(result);

        const icon = result.status === 'PASS' ? '✅' : result.status === 'ERROR' ? '❌' : '❌';
        console.log(`  ${icon} ${scenario.name}`);
        console.log(`     Status: ${result.status}`);

        if (result.parse_time_ms) {
            console.log(`     Parse:  ${result.parse_time_ms}ms`);
        }

        if (result.status === 'PASS') {
            console.log(`     Checks: ${result.passed_checks}/${result.checks} passed`);
            totalPassed++;
        } else if (result.status === 'FAIL') {
            console.log(`     Checks: ${result.passed_checks}/${result.checks} passed`);
            for (const m of (result.mismatches || [])) {
                console.log(`     ✗ ${m.key}: expected ${typeof m.expected === 'number' ? m.expected.toFixed(1) : m.expected}, got ${m.actual !== null && m.actual !== undefined ? (typeof m.actual === 'number' ? m.actual.toFixed(1) : m.actual) : 'na'}`);
            }
            totalFailed++;
        } else {
            console.log(`     Error: ${result.error}`);
            totalErrors++;
        }
        console.log('');
    }

    // Summary
    console.log(`${'='.repeat(60)}`);
    const total = totalPassed + totalFailed + totalErrors;
    console.log(`  Results: ${totalPassed}/${total} passed, ${totalFailed} failed, ${totalErrors} errors`);
    console.log(`${'='.repeat(60)}\n`);

    // Update golden snapshots if requested
    if (updateGolden) {
        if (!existsSync(GOLDEN_DIR)) mkdirSync(GOLDEN_DIR, { recursive: true });
        const golden = results.map(r => ({
            scenario: r.scenario,
            actual: stripVolatile(r.actual),
            status: r.status,
        }));
        writeFileSync(join(GOLDEN_DIR, 'scenarios.json'), JSON.stringify(golden, null, 2));
        console.log(`  ✏️  Golden snapshots written to ${GOLDEN_DIR}/scenarios.json`);
    }

    // JSON output
    if (outputJson) {
        console.log(JSON.stringify({ results, summary: { total, passed: totalPassed, failed: totalFailed, errors: totalErrors } }, null, 2));
    }

    process.exit(totalFailed > 0 || totalErrors > 0 ? 1 : 0);
}

main();
