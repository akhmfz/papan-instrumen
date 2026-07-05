// tests/scoring/test-income.mjs — Dividend/Income (4 rasio)
import { runTest, lastVal, assert, summary } from './runner.mjs';

const src = `
// ── INPUT DATA (simulasi UNVR — high dividend consumer) ──
divYield_val = 4.5
payout_val = 60.0
fcfYield_val = 5.0
dps_val = 120.0

// ── SKOR DIVIDEN ──
yieldScore    = f_scoreHigher(divYield_val, 3, 8)
payoutScore   = f_scoreMid(payout_val, 0, 40, 100)
fcfYieldScore = f_scoreHigher(fcfYield_val, 0, 8)
dpsScore      = f_scorePositive(dps_val)

incomeScore = f_avg4(yieldScore, payoutScore, fcfYieldScore, dpsScore)

// ── Edge cases ──
yieldLow  = f_scoreHigher(1.0, 3, 8)     // below bad → 0
yieldHigh = f_scoreHigher(10.0, 3, 8)    // above good → 100
yieldZero = f_scoreHigher(0.0, 3, 8)     // no dividend → 0
payoutHigh = f_scoreMid(150.0, 0, 40, 100) // >100% payout
dpsZero    = f_scorePositive(0)            // no DPS → 0
naIncome   = f_avg4(na, payoutScore, fcfYieldScore, dpsScore) // missing yield

// ── PLOTS ──
plot(yieldScore, "YIELD")
plot(payoutScore, "PAYOUT")
plot(fcfYieldScore, "FCFY")
plot(dpsScore, "DPS")
plot(incomeScore, "INCOME")
plot(yieldLow, "YLOW")
plot(yieldHigh, "YHI")
plot(payoutHigh, "PHI")
plot(dpsZero, "DZERO")
plot(naIncome, "NAINC")
`;

const t = { passed: 0, failed: 0 };
const r = await runTest(src);

assert(t, 'Yield   (x=4.5, bad=3, good=8)', lastVal(r, 'YIELD'), 30.0);
assert(t, 'Payout  (x=60, 0-40-100)', lastVal(r, 'PAYOUT'), 66.7);
assert(t, 'FCF Yld (x=5.0, bad=0, good=8)', lastVal(r, 'FCFY'), 62.5);
assert(t, 'DPS     (>0 → 100)', lastVal(r, 'DPS'), 100);

assert(t, 'Income Score (avg 4)', lastVal(r, 'INCOME'), 64.8);

assert(t, 'Yield < bad → 0', lastVal(r, 'YLOW'), 0);
assert(t, 'Yield > good → 100', lastVal(r, 'YHI'), 100);
assert(t, 'Payout > 100% (mid formula)', lastVal(r, 'PHI'), 0.0);
assert(t, 'DPS = 0 → 0', lastVal(r, 'DZERO'), 0);
assert(t, 'Missing yield (avg of 3)', lastVal(r, 'NAINC'), 76.4);

process.exit(summary(t) ? 0 : 1);
