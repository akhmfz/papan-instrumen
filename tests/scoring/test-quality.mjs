// tests/scoring/test-quality.mjs — Profitability/Kualitas (9 rasio, 3 sektor)
import { runTest, lastVal, assert, summary } from './runner.mjs';

const src = `
// ── INPUT DATA (simulasi ICBP — consumer goods) ──
roe_val = 18.0
roa_val = 10.0
roic_val = 15.0
grossM_val = 45.0
opM_val = 20.0
netM_val = 12.0
ebitdaM_val = 28.0
fcfMargin_val = 8.0
piotroski_val = 7.0

// ── SKOR KUALITAS (Non-Finansial Umum) ──
roeScore       = f_scoreHigher(roe_val, 5, 25)
roaScore       = f_scoreHigher(roa_val, 2, 15)
roicScore      = f_scoreHigher(roic_val, 5, 25)
grossScore     = f_scoreHigher(grossM_val, 20, 60)
opScore        = f_scoreHigher(opM_val, 5, 30)
netScore       = f_scoreHigher(netM_val, 3, 25)
ebitdaScore    = f_scoreHigher(ebitdaM_val, 8, 35)
fcfMarginScore = f_scoreHigher(fcfMargin_val, 0, 20)
piotroskiScore = f_clamp(piotroski_val / 9 * 100, 0, 100)

// Default bobot (Non-Finansial / Consumer): 1:1:1:1:1:1:1.5:1.5:3
qualityVals = array.from(roeScore, roaScore, roicScore, grossScore, opScore, netScore, ebitdaScore, fcfMarginScore, piotroskiScore)
qualityWts  = array.from(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.5, 1.5, 3.0)
qualityScore = f_wavgArr(qualityVals, qualityWts)

// ── Bank: margin di-skip, ROE/ROA prioritas ──
bankVals = array.from(roeScore, roaScore, roicScore, grossScore, opScore, netScore, ebitdaScore, fcfMarginScore, piotroskiScore)
bankWts  = array.from(1.5, 1.3, 1.2, 0, 0, 0, 0, 0, 3.6)
bankScore = f_wavgArr(bankVals, bankWts)

// ── Edge cases ──
piotroskiMin  = f_clamp(0.0 / 9 * 100, 0, 100)   // Piotroski 0 → 0
piotroskiMax  = f_clamp(9.0 / 9 * 100, 0, 100)   // Piotroski 9 → 100
roeNegative   = f_scoreHigher(-5.0, 5, 25)         // ROE negatif → 0 (below bad)
roeNa         = f_scoreHigher(na, 5, 25)            // na → na

// ── PLOTS ──
plot(roeScore, "ROE")
plot(roaScore, "ROA")
plot(roicScore, "ROIC")
plot(grossScore, "GROSS")
plot(opScore, "OP")
plot(netScore, "NET")
plot(ebitdaScore, "EBITDA")
plot(fcfMarginScore, "FCFM")
plot(piotroskiScore, "PIOT")
plot(qualityScore, "QUALITY")
plot(bankScore, "BANK")
plot(piotroskiMin, "PMIN")
plot(piotroskiMax, "PMAX")
plot(roeNegative, "ROENEG")
plot(roeNa ? 999 : 0, "ROENA")
`;

const t = { passed: 0, failed: 0 };
const r = await runTest(src);

assert(t, 'ROE       (x=18,  bad=5,  good=25)', lastVal(r, 'ROE'), 65.0);
assert(t, 'ROA       (x=10,  bad=2,  good=15)', lastVal(r, 'ROA'), 61.5);
assert(t, 'ROIC      (x=15,  bad=5,  good=25)', lastVal(r, 'ROIC'), 50.0);
assert(t, 'Gross M   (x=45,  bad=20, good=60)', lastVal(r, 'GROSS'), 62.5);
assert(t, 'Op M      (x=20,  bad=5,  good=30)', lastVal(r, 'OP'), 60.0);
assert(t, 'Net M     (x=12,  bad=3,  good=25)', lastVal(r, 'NET'), 40.9);
assert(t, 'EBITDA M  (x=28,  bad=8,  good=35)', lastVal(r, 'EBITDA'), 74.1);
assert(t, 'FCF M     (x=8,   bad=0,  good=20)', lastVal(r, 'FCFM'), 40.0);
assert(t, 'Piotroski (7/9)', lastVal(r, 'PIOT'), 77.8);

assert(t, 'Quality Score (Consumer)', lastVal(r, 'QUALITY'), 62.0);
assert(t, 'Bank Score (different weights)', lastVal(r, 'BANK'), 68.1);

assert(t, 'Piotroski 0  → 0', lastVal(r, 'PMIN'), 0);
assert(t, 'Piotroski 9  → 100', lastVal(r, 'PMAX'), 100);
assert(t, 'ROE negatif  → 0', lastVal(r, 'ROENEG'), 0);
assert(t, 'ROE na → na', lastVal(r, 'ROENA'), 0);

process.exit(summary(t) ? 0 : 1);
