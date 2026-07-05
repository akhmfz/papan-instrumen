#!/usr/bin/env node
// tests/pinets-verify.mjs — verify PapanInstrumen utility functions via PineTS
// Usage: node tests/pinets-verify.mjs

import { PineTS } from 'pinets';

const candles = Array.from({ length: 20 }, (_, i) => ({
    open: 100 + i, high: 102 + i, low: 99 + i, close: 101 + i, volume: 1000,
    openTime: 1751673600000 + i * 86400000,
    closeTime: 1751673600000 + (i + 1) * 86400000,
}));

const src = `//@version=6
indicator("UtilVerify")
f_clamp(float x, float lo, float hi) =>
    math.max(lo, math.min(x, hi))
f_safeDiv(float a, float b) =>
    na(a) or na(b) or b == 0 ? na : a / b
f_scoreHigher(float v, float bad, float good) =>
    na(v) ? na : f_clamp((v - bad) / (good - bad) * 100, 0, 100)
f_scoreLower(float v, float good, float bad) =>
    na(v) ? na : f_clamp((bad - v) / (bad - good) * 100, 0, 100)
f_scoreLowerSafe(float v, float good, float bad) =>
    na(v) ? na : v <= 0 ? 0.0 : f_scoreLower(v, good, bad)
f_scoreMid(float v, float lo, float ideal, float hi) =>
    na(v) ? na : v <= ideal ? f_clamp((v - lo) / (ideal - lo) * 100, 0, 100) : f_clamp((hi - v) / (hi - ideal) * 100, 0, 100)
f_scorePositive(float v) =>
    na(v) ? na : v > 0 ? 100 : 0
f_avg5(float a, float b, float c, float d, float e) =>
    float sum = 0.0
    int n = 0
    if not na(a)
        sum += a
        n += 1
    if not na(b)
        sum += b
        n += 1
    if not na(c)
        sum += c
        n += 1
    if not na(d)
        sum += d
        n += 1
    if not na(e)
        sum += e
        n += 1
    n == 0 ? na : sum / n
f_avg3(float a, float b, float c) =>
    f_avg5(a, b, c, na, na)
plot(f_clamp(75, 0, 100), "C")
plot(f_clamp(-10, 0, 100), "C2")
plot(f_clamp(200, 0, 100), "C3")
plot(f_safeDiv(10, 3), "D")
plot(f_safeDiv(10, 0), "D2")
plot(f_scoreHigher(15, 5, 25), "H")
plot(f_scoreLower(10, 1, 20), "L")
plot(f_scoreLowerSafe(-5, 0, 10), "S")
plot(f_scoreMid(1.5, 0.5, 2, 5), "M")
plot(f_scorePositive(100), "P1")
plot(f_scorePositive(-100), "P2")
plot(f_avg3(50, 75, 100), "A")
`;

try {
    const r = await new PineTS(candles).run(src);
    const v = (x) => r.plots[x].data.at(-1).value;

    const tests = [
        ['f_clamp(75,0,100)', v('C'), 75],
        ['f_clamp(-10,0,100)', v('C2'), 0],
        ['f_clamp(200,0,100)', v('C3'), 100],
        ['f_safeDiv(10,3)', v('D'), 3.3333],
        ['f_safeDiv(10,0)', v('D2'), null, true], // na expected
        ['f_scoreHigher(15,5,25)', v('H'), 50],
        ['f_scoreLower(10,1,20)', v('L'), 52.6316],
        ['f_scoreLowerSafe(-5,0,10)', v('S'), 0],
        ['f_scoreMid(1.5, 0.5, 2, 5)', v('M'), 66.667],
        ['f_scorePositive(100)', v('P1'), 100],
        ['f_scorePositive(-100)', v('P2'), 0],
        ['f_avg3(50,75,100)', v('A'), 75],
    ];

    let passed = 0, failed = 0;
    for (const [name, actual, expected, isNa] of tests) {
        const match = isNa ? isNaN(actual) : Math.abs(actual - expected) < 0.1;
        if (match) {
            console.log(`  ✅ ${name} = ${isNaN(actual) ? 'na' : actual}`);
            passed++;
        } else {
            console.log(`  ❌ ${name}: expected ${isNa ? 'na' : expected}, got ${actual}`);
            failed++;
        }
    }

    console.log(`\n${passed}/${tests.length} passed, ${failed} failed`);
    process.exit(failed > 0 ? 1 : 0);
} catch (e) {
    console.log('❌ Crash:', e.message);
    process.exit(1);
}
