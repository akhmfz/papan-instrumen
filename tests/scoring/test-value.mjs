// tests/scoring/test-value.mjs — Valuasi (10 rasio, Non-Finansial)
import { runTest, lastVal, assert, summary } from './runner.mjs';

const src = `
// ── INPUT DATA (simulasi BBCA — bank besar IDX) ──
pe_val = 15.0
peg_val = 1.2
ps_val = 3.0
pb_val = 2.5
evEbitda_val = 10.0
evSales_val = 2.0
earnYield_val = 6.7
opEarnYield_val = 8.0
grahamUpside_val = 15.0

// ── SKOR VALUASI (Non-Finansial Umum) ──
peScore        = f_scoreLowerSafe(pe_val, 8, 45)
psScore        = f_scoreLowerSafe(ps_val, 1, 15)
pbScore        = f_scoreLowerSafe(pb_val, 1, 12)
pegScore       = f_scoreLowerSafe(peg_val, 0.5, 3.5)
evScore        = f_scoreLowerSafe(evEbitda_val, 5, 30)
evSalesScore   = f_scoreLowerSafe(evSales_val, 1, 15)
earnYieldScore = f_scoreHigher(earnYield_val, 2, 12)
opYieldScore   = f_scoreHigher(opEarnYield_val, 3, 15)
grahamScore    = f_scoreHigher(grahamUpside_val, -30, 50)

// Non-Finansial: bobot default (1:1:1:1:1:3:1.5:1.5:3)
valueVals = array.from(peScore, pegScore, psScore, pbScore, evScore, evSalesScore, earnYieldScore, opYieldScore, grahamScore)
valueWts  = array.from(1.0, 1.0, 1.0, 1.0, 1.0, 3.0, 1.5, 1.5, 3.0)
valueScore = f_wavgArr(valueVals, valueWts)

// ── EDGE CASES ──
peNegative = f_scoreLowerSafe(-5.0, 8, 45)   // laba rugi → skor 0
peNa       = f_scoreLowerSafe(na, 8, 45)      // data missing → na
evZero     = f_scoreLowerSafe(0.0, 5, 30)     // ev=0 → risky → 0
earnNa     = f_scoreHigher(na, 2, 12)         // na → na

// ── Financial sector: wPb*1.5, wPe*1.3, wPeg*0.5, wGraham*0.3 ──
finVals = array.from(peScore, pegScore, psScore, pbScore, evScore, evSalesScore, earnYieldScore, opYieldScore, grahamScore)
finWts  = array.from(1.3, 0.5, 1.0, 1.5, 1.0, 3.0, 1.5, 1.5, 0.9)
finScore = f_wavgArr(finVals, finWts)

// ── PLOTS ──
plot(peScore, "PE")
plot(pegScore, "PEG")
plot(psScore, "PS")
plot(pbScore, "PB")
plot(evScore, "EV")
plot(evSalesScore, "EVS")
plot(earnYieldScore, "EY")
plot(opYieldScore, "OY")
plot(grahamScore, "GR")
plot(valueScore, "VALUE")
plot(finScore, "FIN")
plot(peNegative, "PENEG")
plot(peNa ? 999 : 0, "PENA")
plot(evZero, "EVZERO")
`;

const t = { passed: 0, failed: 0 };

const r = await runTest(src);

// Individual ratio scores
assert(t, 'PE    (x=15, bad=8, good=45)', lastVal(r, 'PE'), 81.1);
assert(t, 'PEG   (x=1.2, bad=0.5, good=3.5)', lastVal(r, 'PEG'), 76.7);
assert(t, 'PS    (x=3, bad=1, good=15)', lastVal(r, 'PS'), 85.7);
assert(t, 'PB    (x=2.5, bad=1, good=12)', lastVal(r, 'PB'), 86.4);
assert(t, 'EV    (x=10, bad=5, good=30)', lastVal(r, 'EV'), 80.0);
assert(t, 'EVS   (x=2, bad=1, good=15)', lastVal(r, 'EVS'), 92.9);
assert(t, 'EY    (x=6.7, bad=2, good=12)', lastVal(r, 'EY'), 47.0);
assert(t, 'OY    (x=8, bad=3, good=15)', lastVal(r, 'OY'), 41.7);
assert(t, 'GR    (x=15, bad=-30, good=50)', lastVal(r, 'GR'), 56.3);

// Composite score (weighted average of 9 ratios)
assert(t, 'Value Score (Non-Finansial)', lastVal(r, 'VALUE'), 70.7);

// Financial sector composite (different weights → different score)
assert(t, 'Fin Score (different weights)', lastVal(r, 'FIN'), 73.9);

// Edge cases
assert(t, 'PE negative → 0', lastVal(r, 'PENEG'), 0);
assert(t, 'PE na → na', lastVal(r, 'PENA'), 0); // plot(na?999:0) if na → 0
assert(t, 'EV zero → 0', lastVal(r, 'EVZERO'), 0);

process.exit(summary(t) ? 0 : 1);
