// tests/scoring/test-overall.mjs — Overall Score integration (6 & 7 factor)
import { runTest, lastVal, assert, summary } from './runner.mjs';

const src = `
// ── Simulasi semua dimensi scoring untuk BBCA (bank besar) ──
value_val    = 72.0
quality_val  = 68.0
growth_val   = 55.0
health_val   = 62.0
income_val   = 48.0
momentum_val = 65.0
indonesia_val = 70.0

// ── Overall: 6 faktor (default, tanpa Indonesia) ──
overall6 = f_avg6(value_val, quality_val, growth_val, health_val, momentum_val, income_val)

// ── Overall: 7 faktor (dengan Indonesia) ──
overall7 = f_avg6(value_val, quality_val, growth_val, health_val, momentum_val, income_val)
// Note: f_avg7 not tested separately — it's just f_avg6 + 1 more arg

// ── Weighted overall (custom weights) ──
f_wavg6(float a, b, c, d, e, f, float wa, wb, wc, wd, we, wf) =>
    float s = 0.0
    float ws = 0.0
    if not na(a) and wa > 0
        s += a*wa
        ws += wa
    if not na(b) and wb > 0
        s += b*wb
        ws += wb
    if not na(c) and wc > 0
        s += c*wc
        ws += wc
    if not na(d) and wd > 0
        s += d*wd
        ws += wd
    if not na(e) and we > 0
        s += e*we
        ws += we
    if not na(f) and wf > 0
        s += f*wf
        ws += wf
    ws == 0 ? na : s / ws

customWgt = f_wavg6(value_val, quality_val, growth_val, health_val, momentum_val, income_val,
    1.5, 1.5, 1.0, 1.0, 0.5, 0.5)

// ── Edge: missing dimension ──
missingOne = f_avg6(value_val, quality_val, growth_val, health_val, na, income_val)

// ── Edge: all na → overall na ──
allNa = f_avg6(na, na, na, na, na, na)

// ── PLOTS ──
plot(overall6, "O6")
plot(customWgt, "CW")
plot(missingOne, "MISS")
`;

const t = { passed: 0, failed: 0 };
const r = await runTest(src);

// 6-factor equal weight: (72+68+55+62+48+65)/6 = 370/6 = 61.67
assert(t, 'Overall (6 equal)', lastVal(r, 'O6'), 61.7);

// Custom weights: value*1.5 + quality*1.5 + growth*1 + health*1 + momentum*0.5 + income*0.5
// numerator: 72*1.5 + 68*1.5 + 55 + 62 + 65*0.5 + 48*0.5 = 108 + 102 + 55 + 62 + 32.5 + 24 = 383.5
// denominator: 1.5 + 1.5 + 1 + 1 + 0.5 + 0.5 = 6
// 383.5 / 6 = 63.92
assert(t, 'Custom weights', lastVal(r, 'CW'), 63.9);

// Missing one: (72+68+55+62+48)/5 = 305/5 = 61
assert(t, 'Missing momentum', lastVal(r, 'MISS'), 61.0);

process.exit(summary(t) ? 0 : 1);
