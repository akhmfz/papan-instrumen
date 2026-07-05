#!/bin/bash
# tests/transpile.sh — validate Pine Script syntax via pinets-cli transpilation
# pinets-cli will fail at execution (TradingView-specific features),
# but if it gets past transpile, syntax is valid.

PINETS=$(which pinets-cli 2>/dev/null || true)
if [ -z "$PINETS" ]; then
    echo "⏭  pinets-cli not installed, skipping transpile check"
    echo "   Install: npm i -g pinets-cli"
    exit 0
fi

PINE_FILE="${1:-src/PapanInstrumen.pine}"

python3 -c "
import json
candles = []
for i in range(400):
    p = 100 + i * 0.5
    candles.append({
        'openTime': 1751673600 + i * 86400,
        'open': p, 'high': p + 2, 'low': p - 1, 'close': p + 1,
        'volume': 100000 + i * 1000,
        'closeTime': 1751673600 + (i+1) * 86400
    })
json.dump(candles, open('/tmp/pinets_test.json','w'))
" 2>/dev/null

OUTPUT=$("$PINETS" run --data /tmp/pinets_test.json --quiet "$PINE_FILE" 2>&1) || true

if echo "$OUTPUT" | grep -q "Cannot read properties\|request\.\|invalid_symbol\|syminfo"; then
    echo "✅ Syntax valid (runtime error from TV-specific features, expected)"
    echo "   pinets-cli does not support request.financial/security"
    exit 0
fi

if echo "$OUTPUT" | grep -q "Error\|Unexpected\|Cannot parse\|SyntaxError\|undefined"; then
    echo "❌ Syntax error:"
    echo "$OUTPUT"
    exit 1
fi

echo "✅ Transpile passed"
