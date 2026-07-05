// tests/scoring/test-momentum.mjs — Momentum (5 komponen)
import { runTest, lastVal, assert, summary } from './runner.mjs';

const src = `
// ── INPUT DATA ──
rsi_val = 55.0
pos52_val = 65.0
relStr6m_val = 10.0
relStr12m_val = 15.0
volatility_val = 35.0
maScore_val = 80.0   // dClose above all MAs → Bullish

// ── SKOR MOMENTUM ──
rsiScore  = f_scoreMid(rsi_val, 30, 60, 85)
posScore  = f_scoreHigher(pos52_val, 20, 90)
rs6Score  = f_scoreHigher(relStr6m_val, -20, 25)
rs12Score = f_scoreHigher(relStr12m_val, -25, 35)
volScore  = f_scoreLower(volatility_val, 10, 80)

maVolAvg = f_avg3(maScore_val, volScore, na)
momentumScore = f_avg5(rsiScore, posScore, rs6Score, rs12Score, maVolAvg)

// ── Edge cases ──
rsiOversold  = f_scoreMid(25.0, 30, 60, 85)   // < bad → 0
rsiOverbought = f_scoreMid(90.0, 30, 60, 85)  // > hi → 0
posExtreme    = f_scoreHigher(95.0, 20, 90)     // > good → 100
rsNegative    = f_scoreHigher(-30.0, -20, 25)   // < bad → 0
volNa         = f_scoreLower(na, 10, 80)        // na → na

// ── PLOTS ──
plot(rsiScore, "RSI")
plot(posScore, "POS")
plot(rs6Score, "RS6")
plot(rs12Score, "RS12")
plot(volScore, "VOL")
plot(maVolAvg, "MAVOL")
plot(momentumScore, "MOM")
plot(rsiOversold, "RSILOW")
plot(rsiOverbought, "RSIHI")
plot(posExtreme, "POSEX")
plot(rsNegative, "RSNEG")
`;

const t = { passed: 0, failed: 0 };
const r = await runTest(src);

assert(t, 'RSI         (x=55, 30-60-85)', lastVal(r, 'RSI'), 83.3);
assert(t, '52W Pos     (x=65, bad=20, good=90)', lastVal(r, 'POS'), 64.3);
assert(t, 'RS 6M       (x=10, bad=-20, good=25)', lastVal(r, 'RS6'), 66.7);
assert(t, 'RS 12M      (x=15, bad=-25, good=35)', lastVal(r, 'RS12'), 66.7);
assert(t, 'Vol         (x=35, good=10, bad=80)', lastVal(r, 'VOL'), 64.3);
assert(t, 'MA+Vol Avg  (80 + 64.3 / 2)', lastVal(r, 'MAVOL'), 72.1);

assert(t, 'Momentum Score', lastVal(r, 'MOM'), 70.6);

assert(t, 'RSI < bad → 0', lastVal(r, 'RSILOW'), 0);
assert(t, 'RSI > hi → 0', lastVal(r, 'RSIHI'), 0);
assert(t, 'Position > good → 100', lastVal(r, 'POSEX'), 100);
assert(t, 'RS < bad → 0', lastVal(r, 'RSNEG'), 0);

process.exit(summary(t) ? 0 : 1);
