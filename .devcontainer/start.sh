#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
python3 compiler/compiler.py

if ! pgrep -f "python3 -m http.server 8000" >/dev/null 2>&1; then
  nohup python3 -m http.server 8000 > /tmp/airport-opportunity-compiler.log 2>&1 &
fi

echo "Airport Opportunity Compiler is available on forwarded port 8000."
