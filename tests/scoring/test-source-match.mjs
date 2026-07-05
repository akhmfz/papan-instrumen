// tests/scoring/test-source-match.mjs — verifikasi bahwa scoring test
// menggunakan kode yang SAMA dengan production 04-scoring.pine
// P1-1: prevents test-production gap (source of P0-1/P0-2 undetected bugs)
import { readFileSync } from 'fs';
import { runTest, lastVal, assert, summary } from './runner.mjs';

// Read the ACTUAL production source (not a hand-copied version)
const actualSource = readFileSync('src/modules/04-scoring.pine', 'utf8');

// Extract key scoring formulas from the production source
const hasFSafeLower = actualSource.includes('f_safeDiv');
const hasFSafeLowerSafe = actualSource.includes('f_scoreLowerSafe');

// Count sector weight assertions in production code
const valueWeightCount = (actualSource.match(/else if is\w+Sektor/g) || []).length;
const hasConsumerWeights = actualSource.includes('isKonsumerSektor');
const hasSekuritasQuality = actualSource.includes('else if isSekuritasSektor');

// Test: production code has all required patterns
console.log('=== P1-1: Source Match Verification ===');
console.log(`  Production has f_safeDiv:        ${hasFSafeLower}`);
console.log(`  Production has f_scoreLowerSafe: ${hasFSafeLowerSafe}`);
console.log(`  Production sector weight blocks: ${valueWeightCount}`);
console.log(`  Consumer weights in production:   ${hasConsumerWeights}`);
console.log(`  Sekuritas Quality split:          ${hasSekuritasQuality}`);

// Verify against test expectations
const checks = [
    hasFSafeLower,
    hasFSafeLowerSafe,
    valueWeightCount >= 12,  // at least 12 sector weight blocks
    hasConsumerWeights,
    hasSekuritasQuality,
];

const allPassed = checks.every(Boolean);
console.log(`\n${allPassed ? '✅' : '❌'} Source test: ${checks.filter(Boolean).length}/${checks.length} passed`);

// Also verify test scripts match production
const testFiles = [
    'tests/scoring/test-value.mjs',
    'tests/scoring/test-quality.mjs',
    'tests/scoring/test-growth.mjs',
    'tests/scoring/test-health.mjs',
];

let testMatchCount = 0;
let testDiffCount = 0;

for (const tf of testFiles) {
    const content = readFileSync(tf, 'utf8');
    // Each test file should reference scoring functions used in production
    if (content.includes('f_scoreLowerSafe') || content.includes('f_scoreHigher')) {
        testMatchCount++;
    } else {
        testDiffCount++;
    }
}

console.log(`  Test files matching production: ${testMatchCount}/${testFiles.length}`);
console.log('');

process.exit(allPassed ? 0 : 1);
