#!/bin/bash
# Run the Production Validation Pipeline
# Usage: ./tests/production/run.sh [--scenario NAME] [--json] [--update-golden]

cd "$(dirname "$0")/../.." || exit 1
exec node tests/production/pipeline.mjs "$@"
