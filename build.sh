#!/bin/bash
# build.sh — concatenate modules into deployable PapanInstrumen.pine
set -e

MODULES="src/modules"
OUTPUT="src/PapanInstrumen.pine"
ORDER="01-base.pine 02-data.pine 03-ui.pine 04-scoring.pine"

echo "// Built from modules/ — edit modules, not this file" > "$OUTPUT"
for m in $ORDER; do
    cat "$MODULES/$m" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
done

echo "→ $OUTPUT built ($(wc -l < "$OUTPUT") lines)"
