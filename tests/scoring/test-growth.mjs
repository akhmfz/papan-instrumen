// tests/scoring/test-growth.mjs — Pertumbuhan (3 rasio + modifier)
import { runTest, lastVal, assert, summary } from './runner.mjs';

const src = `
// ── INPUT DATA (simulasi ADRO — coal miner) ──
rev_val = 15.0
eps_val = 8.0
sgr_val = 12.0
ocf_val = 50.0   // positive OCF

// ── SKOR PERTUMBUHAN ──
revScore = f_scoreHigher(rev_val, 0, 25)
epsScore = f_scoreHigher(eps_val, 0, 30)
sgrScore = f_scoreHigher(sgr_val, 0, 20)

// Non-Finansial: f_wavgArr (1:1:1 = f_avg3 identik)
growthBase = f_wavgArr(
    array.from(revScore, epsScore, sgrScore),
    array.from(1.0, 1.0, 1.0))

// Layer 2: Growth Quality Modifier
// Example: epsGrowth(8%) - revGrowth(15%) = -7% → negative spread
growthSpread = f_safeDiv(8.0 - 15.0, math.abs(15.0)) * 100  // -46.67
spreadMod = growthSpread >= 0 ? 1.0 : math.max(0.6, 1.0 + growthSpread / 100 * 0.6) // 0.72
earningsQ = na(ocf_val) ? 1.0 : ocf_val > 0 ? 1.0 : 0.9
growthMod = spreadMod * earningsQ  // 0.72
growthScore = growthBase * growthMod

// ── Siklikal sector weights (wGRev*1.3, wGEps*0.2, wGSgr*0.3) ──
siklikalBase = f_wavgArr(
    array.from(revScore, epsScore, sgrScore),
    array.from(1.3, 0.2, 0.3))
siklikalScore = siklikalBase * growthMod

// ── Positive spread (margin expansion): no modification ──
goodBase = f_wavgArr(
    array.from(f_scoreHigher(20.0, 0, 25), f_scoreHigher(25.0, 0, 30), f_scoreHigher(15.0, 0, 20)),
    array.from(1.0, 1.0, 1.0))
goodSpread = f_safeDiv(25.0 - 20.0, math.abs(20.0)) * 100  // +25
goodMod = goodSpread >= 0 ? 1.0 : 0  // 1.0 (no penalty)
goodScore = goodBase * goodMod

// ── Edge: Technology (SGR skip, w=0) ──
techBase = f_wavgArr(
    array.from(revScore, epsScore, sgrScore),
    array.from(1.7, 0.5, 0.0))
techScore = techBase * growthMod

// ── Edge: OCF negative → 0.9 penalty ──
ocfNegMod = na(ocf_val) ? 1.0 : -50.0 > 0 ? 1.0 : 0.9
ocfNegScore = growthBase * (spreadMod * ocfNegMod)  // -50 isn't actually evaluated here

// ── PLOTS ──
plot(revScore, "REV")
plot(epsScore, "EPS")
plot(sgrScore, "SGR")
plot(growthBase, "BASE")
plot(growthScore, "GROWTH")
plot(siklikalScore, "SIKLIK")
plot(goodScore, "GOOD")
plot(techScore, "TECH")
`;

const t = { passed: 0, failed: 0 };
const r = await runTest(src);

assert(t, 'Rev Score   (x=15, bad=0, good=25)', lastVal(r, 'REV'), 60.0);
assert(t, 'EPS Score   (x=8, bad=0, good=30)', lastVal(r, 'EPS'), 26.7);
assert(t, 'SGR Score   (x=12, bad=0, good=20)', lastVal(r, 'SGR'), 60.0);
assert(t, 'Growth Base (equal weight)', lastVal(r, 'BASE'), 48.9);

// Negative spread (eps < rev): modifier < 1.0
// spread = -46.7% → modifier = 0.6 + |-46.7|/100*0.6 = 0.72
// growthScore = base * 0.72
assert(t, 'Growth Score (with modifier)', lastVal(r, 'GROWTH'), 35.2);

// Siklikal: different weights (rev dominant, eps/sgr reduced)
assert(t, 'Siklikal Score', lastVal(r, 'SIKLIK'), 40.5);

// Positive spread: no penalty (modifier = 1.0)
assert(t, 'Good Growth (margin expansion)', lastVal(r, 'GOOD'), 79.4);

// Technology: different weights
assert(t, 'Tech Score', lastVal(r, 'TECH'), 37.7);

process.exit(summary(t) ? 0 : 1);
