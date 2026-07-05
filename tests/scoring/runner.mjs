// tests/scoring/runner.mjs — shared test runner for scoring dimension tests
import { PineTS } from 'pinets';

export function dummyCandles(count = 20) {
    return Array.from({ length: count }, (_, i) => ({
        open: 100 + i,
        high: 102 + i,
        low: 99 + i,
        close: 101 + i,
        volume: 1000000 + i * 1000,
        openTime: 1751673600000 + i * 86400000,
        closeTime: 1751673600000 + (i + 1) * 86400000,
    }));
}

// Pine Script utility function definitions (shared header for all test scripts)
export const UTILS_HEADER = `
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
f_avg3(float a, float b, float c) =>
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
    n == 0 ? na : sum / n
f_avg4(float a, float b, float c, float d) =>
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
    n == 0 ? na : sum / n
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
f_avg6(float a, float b, float c, float d, float e, float f) =>
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
    if not na(f)
        sum += f
        n += 1
    n == 0 ? na : sum / n
f_wavgArr(array<float> vals, array<float> wts) =>
    float sum = 0.0
    float wsum = 0.0
    int i = 0
    while i < array.size(vals)
        v = array.get(vals, i)
        w = array.get(wts, i)
        if not na(v) and w > 0
            sum += v * w
            wsum += w
        i += 1
    wsum == 0 ? na : sum / wsum
`;

export async function runTest(pineSrc) {
    const pineTS = new PineTS(dummyCandles(20));
    const result = await pineTS.run(`//@version=6
indicator("ScoringTest")
${UTILS_HEADER}
${pineSrc}
`);
    return result;
}

// Helper: get last plotted value by plot name
export function lastVal(result, plotName) {
    const data = result.plots[plotName]?.data;
    if (!data || data.length === 0) return NaN;
    return data[data.length - 1].value;
}

// Helper: assert approximate equality
export function assert(t, name, actual, expected, tolerance = 0.1) {
    const match = isNaN(expected) ? isNaN(actual) : Math.abs(actual - expected) < tolerance;
    if (match) {
        t.passed++;
        console.log(`  ✅ ${name} = ${isNaN(actual) ? 'na' : actual.toFixed(1)}`);
    } else {
        t.failed++;
        console.log(`  ❌ ${name}: expected ${isNaN(expected) ? 'na' : expected}, got ${isNaN(actual) ? 'na' : actual.toFixed(1)}`);
    }
}

export function summary(t) {
    const total = t.passed + t.failed;
    console.log(`\n${t.passed}/${total} passed, ${t.failed} failed`);
    return t.failed === 0;
}
