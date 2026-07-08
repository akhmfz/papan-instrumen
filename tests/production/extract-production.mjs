// extract-production.mjs — Reads actual production .pine source files
// and extracts scoring logic into PineTS-compatible format.
// This is the core of P1-1: tests use PRODUCTION code, not copies.

import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = join(__dirname, '..', '..');

export function readSource(module) {
    const path = join(PROJECT_ROOT, 'src', 'modules', module);
    return readFileSync(path, 'utf8');
}

// Extract top-level function definitions from 01-base.pine.
// These are safe for PineTS — no syminfo/request.financial dependencies.
export function extractUtilities() {
    const src = readSource('01-base.pine');
    const lines = src.split('\n');
    const fns = [];
    let inFn = false;
    let buf = [];
    let braceDepth = 0;

    for (const raw of lines) {
        const line = raw;
        const trimmed = line.trim();

        // Detect top-level function start: `name(params) =>`
        const fnMatch = trimmed.match(/^(\w[\w\d]*)\s*\(.*\)\s*=>\s*$/);
        if (fnMatch && braceDepth === 0) {
            if (buf.length > 0) fns.push(buf.join('\n'));
            buf = [line];
            inFn = true;
            braceDepth += (line.match(/{/g) || []).length;
            braceDepth -= (line.match(/}/g) || []).length;
            if (braceDepth === 0 && !line.trim().endsWith('=>')) {
                inFn = false;
            }
            continue;
        }

        // Detect multiline function continuation
        if (inFn) {
            // Check for closing `=>` block — ends when we hit next fn or indentation drops
            buf.push(line);
            braceDepth += (line.match(/{/g) || []).length;
            braceDepth -= (line.match(/}/g) || []).length;

            // Detect end: next top-level item (not indented, not comment, not empty)
            if (braceDepth === 0) {
                const nextIsFn = trimmed.match(/^(\w[\w\d]*)\s*\(.*\)\s*=>/);
                const nextIsComment = trimmed.startsWith('//');
                const nextIsEmpty = trimmed === '';
                const nextIsImport = trimmed.startsWith('import');
                const nextIsVar = trimmed.startsWith('var ');
                if (!nextIsFn && !nextIsComment && !nextIsEmpty && !nextIsImport && !nextIsVar) {
                    // Still inside fn body
                } else if (nextIsFn || nextIsImport || nextIsVar) {
                    fns.push(buf.join('\n'));
                    buf = [];
                    inFn = false;
                }
            }
            continue;
        }

        // Single-line fn: `name(params) => expr`
        const oneLiner = trimmed.match(/^(\w[\w\d]*)\s*\(.*\)\s*=>\s*(.+)$/);
        if (oneLiner && !trimmed.startsWith('//')) {
            fns.push(line);
            continue;
        }
    }
    if (buf.length > 0) fns.push(buf.join('\n'));

    // Filter: only include valid function definitions
    const valid = fns.filter(f => /=>/.test(f) && !f.trim().startsWith('//'));
    return valid.join('\n');
}

// Extract the scoring logic from 04-scoring.pine (inside `if barstate.islast`).
// Strips render/UI code (table.*, f_row, f_section, etc.) that PineTS can't run.
export function extractScoringLogic() {
    const src = readSource('04-scoring.pine');
    const lines = src.split('\n');

    // Find `if barstate.islast` block
    let inBlock = false;
    let blockLines = [];
    let depth = 0;
    let started = false;

    for (const raw of lines) {
        const trimmed = raw.trim();

        if (!started && /^\s*if\s+barstate\.islast\s*$/.test(trimmed)) {
            started = true;
            inBlock = true;
            depth = 1;
            continue;
        }

        if (inBlock) {
            // Stop at render section — everything after is UI code (tables, formatting)
            if (trimmed.includes('RENDER KE TABEL') || trimmed.includes('RENDER TO TABLE')) {
                break;
            }

            depth += (trimmed.match(/\bif\b/g) || []).length;
            depth += (trimmed.match(/\bfor\b/g) || []).length;
            depth += (trimmed.match(/\bwhile\b/g) || []).length;
            depth += (trimmed.match(/\belse\b/g) || []).length;
            depth -= (trimmed.match(/^[^/]*\bend\b/g) || []).length;
            depth -= (trimmed.match(/^[^/]*\bendfor\b/g) || []).length;
            depth -= (trimmed.match(/^[^/]*\bendwhile\b/g) || []).length;

            blockLines.push(raw);

            if (depth <= 0 && trimmed.length > 0 && !trimmed.startsWith('//') && !trimmed.startsWith('if ') && !trimmed.startsWith('for ')) {
                break;
            }
        }
    }

    // Dedent: remove leading 4-space indent (was inside `if barstate.islast`)
    const dedented = blockLines.map(line => {
        const trimmed = line.trimStart();
        const indent = line.length - trimmed.length;
        return indent >= 4 ? line.slice(4) : line;
    });

    if (dedented.length > 0) {
        return dedented.join('\n');
    }
    return blockLines.join('\n');
}


// Generate a complete Pine Script for PineTS from a scenario
export function generatePineScript(scenario) {
    const utilities = extractUtilities();
    const scoringLogic = extractScoringLogic();

    // Build variable declarations from scenario inputs
    const varDecls = [];
    for (const [key, val] of Object.entries(scenario.inputs)) {
        if (typeof val === 'boolean') {
            varDecls.push(`bool ${key} = ${val}`);
        } else if (typeof val === 'string') {
            varDecls.push(`string ${key} = "${val}"`);
        } else if (val === null || val === undefined) {
            varDecls.push(`float ${key} = na`);
        } else {
            varDecls.push(`float ${key} = ${val}`);
        }
    }

    // Build sector flag declarations (all false unless specified)
    // Note: isSiklikalLike is computed from other flags inside scoring block,
    // so it must NOT be declared here — let the scoring code define it.
    const sectorFlags = [
        'isSiklikalSektor', 'isBatubaraSektor', 'isCPOSektor',
        'isFinancialSector', 'isBankSektor', 'isAsuransiSektor',
        'isSekuritasSektor', 'isPropertySektor', 'isInfrastrukturSektor',
        'isTechnologySektor', 'isTransportasiSektor', 'isKonsumerSektor',
        'isIndustriSektor', 'isKesehatanSektor',
    ];
    for (const flag of sectorFlags) {
        if (!(flag in scenario.inputs)) {
            varDecls.push(`bool ${flag} = false`);
        }
    }

    // Build toggle declarations (reasonable defaults)
    const toggles = {
        tampilIndonesia: false, tampilRisikoGorengan: true,
        tampilRingkasan: true, tampilValuasi: true,
        tampilCompact: false, tampilDividen: true,
        tampilKualitas: true, tampilPertumbuhan: true,
        tampilKesehatan: true, tampilMomentum: true,
    };
    for (const [key, val] of Object.entries(toggles)) {
        if (!(key in scenario.inputs)) {
            varDecls.push(`bool ${key} = ${val}`);
        }
    }

    // Bank inputs (always needed for scoring code that references them)
    if (!('carInput' in scenario.inputs)) varDecls.push('float carInput = -1.0');
    if (!('nplInput' in scenario.inputs)) varDecls.push('float nplInput = -1.0');
    if (!('ldrInput' in scenario.inputs)) varDecls.push('float ldrInput = -1.0');
    if (!('presetBobot' in scenario.inputs)) varDecls.push('string presetBobot = "Equal"');
    if (!('gunakanBobotKustom' in scenario.inputs)) varDecls.push('bool gunakanBobotKustom = false');
    if (!('bobotValue' in scenario.inputs)) varDecls.push('float bobotValue = 1.0');
    if (!('bobotQuality' in scenario.inputs)) varDecls.push('float bobotQuality = 1.0');
    if (!('bobotGrowth' in scenario.inputs)) varDecls.push('float bobotGrowth = 1.0');
    if (!('bobotHealth' in scenario.inputs)) varDecls.push('float bobotHealth = 1.0');
    if (!('bobotMomentum' in scenario.inputs)) varDecls.push('float bobotMomentum = 1.0');
    if (!('bobotIncome' in scenario.inputs)) varDecls.push('float bobotIncome = 1.0');
    if (!('bobotIndonesia' in scenario.inputs)) varDecls.push('float bobotIndonesia = 1.0');
    // Theme variables (referenced but not used in scoring)
    if (!('warnaTema' in scenario.inputs)) varDecls.push('string warnaTema = "Gelap"');
    if (!('tampilKelengkapan' in scenario.inputs)) varDecls.push('bool tampilKelengkapan = false');
    // Derived constants from 01-base.pine (needed by scoring logic)
    if (!('pakaiBobotTertimbang' in scenario.inputs)) varDecls.push('bool pakaiBobotTertimbang = false');

    // Build plot statements for each expected output
    const plots = [];
    if (scenario.expected) {
        for (const key of Object.keys(scenario.expected)) {
            plots.push(`plot(${key}, "${key}")`);
        }
    }

    return `//@version=6
indicator("ProdTest")
// --- UTILITY FUNCTIONS (from 01-base.pine) ---
${utilities}

// --- INPUT VARIABLES ---
${varDecls.join('\n')}

// --- SCORING LOGIC (from 04-scoring.pine) ---
${scoringLogic}

// --- PLOTS ---
${plots.join('\n')}
`;
}

// Default export for convenience
export default { readSource, extractUtilities, extractScoringLogic, generatePineScript };
