// tests/scoring/test-health.mjs — Financial Health (11 rasio, Non-Finansial + Bank)
import { runTest, lastVal, assert, summary } from './runner.mjs';

const src = `
// ── INPUT DATA (simulasi JSMR — infrastructure) ──
debtEq_val        = 2.0
debtAsset_val     = 0.4
debtEbitda_val    = 3.0
netDebtEbitda_val = 2.5
cashDebt_val      = 0.8
interestCover_val = 8.0
currRatio_val     = 1.5
quickRatio_val    = 1.2
altmanZ_val       = 2.0
ocf_val           = 100.0
fcf_val           = 50.0

// ── SKOR KESEHATAN (Non-Finansial Umum defaults) ──
debtEqG = 0.0
debtEqB = 2.5
debtEbitdaG = 0.0
debtEbitdaB = 6.0
netDebtEbitdaG = 0.0
netDebtEbitdaB = 5.0
currL = 0.5
currI = 2.0
currH = 5.0
quickL = 0.3
quickI = 1.5
quickH = 4.0
intBad = 5.0
intGood = 50.0
altmanBad = 1.1
altmanGood = 2.6

debtEqScore = debtEq_val < 0 ? 0.0 : f_scoreLower(debtEq_val, debtEqG, debtEqB)
debtAssetScore     = f_scoreLowerSafe(debtAsset_val, 0, 0.8)
debtEbitdaScore    = f_scoreLowerSafe(debtEbitda_val, debtEbitdaG, debtEbitdaB)
netDebtEbitdaScore = f_scoreLower(netDebtEbitda_val, netDebtEbitdaG, netDebtEbitdaB)
cashDebtScore      = f_scoreHigher(cashDebt_val, 0, 1.5)
currScore          = f_scoreMid(currRatio_val, currL, currI, currH)
quickScore         = f_scoreMid(quickRatio_val, quickL, quickI, quickH)
interestScore      = f_scoreHigher(interestCover_val, intBad, intGood)
altmanScore        = f_scoreHigher(altmanZ_val, altmanBad, altmanGood)
ocfScore           = f_scorePositive(ocf_val)
fcfScore           = f_scorePositive(fcf_val)

// Default bobot Non-Finansial: 1:1:1:1:1:1:1.5:1.5:3:1.5:1.5
healthVals = array.from(debtEqScore, debtAssetScore, debtEbitdaScore, netDebtEbitdaScore,
    cashDebtScore, interestScore, currScore, quickScore, altmanScore, ocfScore, fcfScore)
healthWts  = array.from(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.5, 1.5, 3.0, 1.5, 1.5)
healthScore = f_wavgArr(healthVals, healthWts)

// ── Bank: different weights (most leverage ratios = 0) ──
bankVals = array.from(debtEqScore, debtAssetScore, debtEbitdaScore, netDebtEbitdaScore,
    cashDebtScore, interestScore, currScore, quickScore, altmanScore, ocfScore, fcfScore)
bankWts  = array.from(0, 0, 0, 0, 0, 1.5, 0, 0, 0, 1.5, 1.5)
bankScore = f_wavgArr(bankVals, bankWts)

// ── Edge cases ──
debtNeg = -2.0 < 0 ? 0.0 : f_scoreLower(-2.0, 0.0, 2.5)
altmanLow = f_scoreHigher(0.5, 1.1, 2.6)  // < bad → 0
altmanHigh = f_scoreHigher(4.0, 1.1, 2.6)  // > good → 100

// ── PLOTS ──
plot(debtEqScore, "DE")
plot(debtAssetScore, "DA")
plot(debtEbitdaScore, "DEB")
plot(netDebtEbitdaScore, "NDEB")
plot(cashDebtScore, "CD")
plot(interestScore, "IC")
plot(currScore, "CR")
plot(quickScore, "QR")
plot(altmanScore, "ALT")
plot(ocfScore, "OCF")
plot(fcfScore, "FCF")
plot(healthScore, "HEALTH")
plot(bankScore, "BANK")
plot(debtNeg, "DNEG")
plot(altmanLow, "ALOW")
plot(altmanHigh, "AHI")
`;

const t = { passed: 0, failed: 0 };
const r = await runTest(src);

assert(t, 'D/E          (x=2.0, good=0, bad=2.5)', lastVal(r, 'DE'), 20.0);
assert(t, 'D/A          (x=0.4, good=0, bad=0.8)', lastVal(r, 'DA'), 50.0);
assert(t, 'D/EBITDA     (x=3.0, good=0, bad=6.0)', lastVal(r, 'DEB'), 50.0);
assert(t, 'Net D/EBITDA (x=2.5, good=0, bad=5.0)', lastVal(r, 'NDEB'), 50.0);
assert(t, 'Cash/Debt    (x=0.8, bad=0, good=1.5)', lastVal(r, 'CD'), 53.3);
assert(t, 'Int Cover    (x=8, bad=5, good=50)', lastVal(r, 'IC'), 6.7);
assert(t, 'Current R    (x=1.5, lo=0.5, ideal=2, hi=5)', lastVal(r, 'CR'), 66.7);
assert(t, 'Quick R      (x=1.2, lo=0.3, ideal=1.5, hi=4)', lastVal(r, 'QR'), 75.0);
assert(t, 'Altman Z     (x=2.0, bad=1.1, good=2.6)', lastVal(r, 'ALT'), 60.0);
assert(t, 'OCF          (positive → 100)', lastVal(r, 'OCF'), 100);
assert(t, 'FCF          (positive → 100)', lastVal(r, 'FCF'), 100);

assert(t, 'Health Score (Non-Finansial)', lastVal(r, 'HEALTH'), 61.5);
assert(t, 'Bank Score   (limited ratios)', lastVal(r, 'BANK'), 68.9);

assert(t, 'Negative D/E (guard) → 0', lastVal(r, 'DNEG'), 0);
assert(t, 'Altman < bad → 0', lastVal(r, 'ALOW'), 0);
assert(t, 'Altman > good → 100', lastVal(r, 'AHI'), 100);

process.exit(summary(t) ? 0 : 1);
