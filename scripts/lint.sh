#!/bin/bash
# lint.sh — Pine Script v6 linter
set -e

PINE="src/PapanInstrumen.pine"
ERR=0

ok()  { echo "  ✅ $1"; }
err() { echo "  ❌ $1"; ERR=$((ERR + 1)); }

echo "🔍 Linting $PINE"
echo ""

# structural
grep -q '//@version=6' "$PINE" && ok "version=6 header" || err "Missing //@version=6"
grep -q 'indicator('      "$PINE" && ok "indicator() declaration" || err "Missing indicator()"

# safety
grep -q 'f_safeDiv' "$PINE" && ok "f_safeDiv helper" || err "Missing f_safeDiv — divide-by-zero risk"

# bare security() check — count lines with security( but NOT request.security
BARE=$(grep 'security(' "$PINE" 2>/dev/null | grep -cv 'request\.security' 2>/dev/null) || BARE=0
[ "$BARE" -eq 0 ] && ok "no bare security()" || err "Found $BARE bare security() — use request.security()"

# deprecated
! grep -q 'study(' "$PINE" && ok "no deprecated study()" || err "Found deprecated study() — use indicator()"

# budget — hard limit 40, safety warning at 36+
REQ=$(grep -cE 'request\.(financial|security)\b' "$PINE" 2>/dev/null) || REQ=0
[ "$REQ" -le 40 ] && ok "request budget: $REQ/40" || err "request budget exceeded: $REQ > 40"
[ "$REQ" -ge 36 ] && echo "  ⚠️  WARNING: $REQ/40 requests used — only 4-5 slots left for new fields"

echo ""
if [ "$ERR" -eq 0 ]; then
    echo "✅ All checks passed"
else
    echo "❌ $ERR issue(s)"
    exit 1
fi
