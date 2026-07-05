#!/bin/bash
# tests/transpile.sh — Pine Script syntax validation via PineTS
# Uses LuxAlgo/PineTS (npm: pinets) — open-source Pine Script runtime
# https://github.com/LuxAlgo/PineTS

PINE_FILE="${1:-src/PapanInstrumen.pine}"

echo "🔬 PineTS Syntax Validation"
echo ""

node -e "require('pinets')" 2>/dev/null || {
    echo "⏭  pinets not installed locally"
    echo "   Run: npm install pinets"
    exit 0
}

node --input-type=module -e "
import { PineTS } from 'pinets';
import { readFileSync } from 'fs';

const d = [{
    open: 100, high: 102, low: 99, close: 101, volume: 1000,
    openTime: Date.now() - 86400000, closeTime: Date.now()
}];

try {
    await new PineTS(d).run(readFileSync('$PINE_FILE', 'utf8'));
} catch (e) {
    const m = e.message || '';
    if (m.includes('tickerid') || m.includes('syminfo') || m.includes('request.financial')) {
        console.log('✅ Syntax valid');
        console.log('   Runtime error (expected): ' + m.substring(0, 80) + '...');
        console.log('   PineTS does not support syminfo/request.financial');
    } else if (m.includes('parse') || m.includes('Syntax') || m.includes('Unexpected')) {
        console.log('❌ Parse error: ' + m);
        process.exit(1);
    } else {
        console.log('❌ Unexpected: ' + m);
        process.exit(1);
    }
}
" 2>&1

STATUS=$?
echo ""
[ $STATUS -eq 0 ] && echo "✅ PineTS validation passed" || echo "❌ PineTS validation failed"
exit $STATUS
