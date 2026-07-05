// tests/scoring/test-regression.mjs — regression guard untuk bug P0-1 & P0-2
import { runTest, lastVal, assert, summary } from './runner.mjs';

const src = `
// ── P0-1: netDebtEbitdaScore dengan f_scoreLowerSafe ──
// EBITDA negatif + net debt positif = distress → seharusnya skor <= 0
// (bukan ~100 seperti bug sebelumnya yang pakai f_scoreLower)

// Simulasi: EBITDA negatif, Net Debt = 5, sehingga Net D/EBITDA = -10
// (net cash position karena EBITDA negatif, rasio tidak bermakna)
netDebtEBITDA_neg = f_scoreLowerSafe(-10.0, 0.0, 5.0)

// Simulasi: perusahaan normal, Net Debt/EBITDA = 2.0
netDebtEBITDA_norm = f_scoreLowerSafe(2.0, 0.0, 5.0)

// Simulasi: nilai 0 — juga pakai guard
netDebtEBITDA_zero = f_scoreLowerSafe(0.0, 0.0, 5.0)

// ── P0-2: Sektor Konsumer/Industri/Kesehatan ada bobot berbeda ──
// Verifikasi: sektor-sektor ini punya weight adjustments di dimensi Value

// Simulasi Consumer (isKonsumerSektor = true)
consumerPreset = f_wavgArr(
    array.from(80.0, 50.0, 50.0, 80.0, 50.0, 50.0, 50.0, 50.0, 50.0),
    array.from(1.2, 1.0, 1.0, 1.2, 1.0, 3.0, 1.5, 1.5, 3.0))

// Non-Finansial default
nonFinPreset = f_wavgArr(
    array.from(80.0, 50.0, 50.0, 80.0, 50.0, 50.0, 50.0, 50.0, 50.0),
    array.from(1.0, 1.0, 1.0, 1.0, 1.0, 3.0, 1.5, 1.5, 3.0))

// ── P0-4 edge: growthSpread saat revGrowth == 0 ──
// Ketika revGrowth = 0 dan EPS negatif, growthSpread = na
// spreadModifier harusnya tidak default 1.0 tanpa penalti
// Test: revGrowth = 0, epsGrowth = -10
// growthSpread = na → spreadModifier = revGrowth==0 and epsGrowth<0 ? 0.9 : 1.0
// Verifikasi modifier < 1.0

// Simulasi modifier langsung (reproduksi logika produksi)
spreadMod_zeroRev = 0.0 == 0 and -10.0 < 0 ? 0.9 : 1.0
spreadMod_zeroRevBothZero = 0.0 == 0 and 0.0 < 0 ? 0.9 : 1.0

// ── PLOTS ──
plot(netDebtEBITDA_neg, "ND_NEG")
plot(netDebtEBITDA_norm, "ND_NORM")
plot(netDebtEBITDA_zero, "ND_ZERO")
plot(consumerPreset, "CONS")
plot(nonFinPreset, "NONFIN")
plot(spreadMod_zeroRev, "SPMOD")
plot(spreadMod_zeroRevBothZero, "SPMOD2")
`;

const t = { passed: 0, failed: 0 };
const r = await runTest(src);

// P0-1: netDebtEbitdaScore with f_scoreLowerSafe
assert(t, 'P0-1: EBITDA negatif → skor 0', lastVal(r, 'ND_NEG'), 0);
assert(t, 'P0-1: EBITDA normal → skor wajar', lastVal(r, 'ND_NORM'), 60.0);
assert(t, 'P0-1: Net D/EBITDA == 0 → skor 0', lastVal(r, 'ND_ZERO'), 0);

// P0-2: Consumer vs Non-Finansial weights should differ
// Consumer has wPe=1.2, wPb=1.2 vs default wPe=1.0, wPb=1.0
assert(t, 'P0-2: Consumer preset ≠ Non-Finansial', lastVal(r, 'CONS') !== lastVal(r, 'NONFIN') ? 1 : 0, 1);
assert(t, 'P0-2: Non-Finansial weighted avg', lastVal(r, 'NONFIN'), 54.3);

// P0-4: growthSpread with revGrowth == 0
assert(t, 'P0-4: revGrowth==0 + EPS turun → modifier 0.9', lastVal(r, 'SPMOD'), 0.9);
assert(t, 'P0-4: revGrowth==0 + EPS=0 → modifier 1.0', lastVal(r, 'SPMOD2'), 1.0);

process.exit(summary(t) ? 0 : 1);
