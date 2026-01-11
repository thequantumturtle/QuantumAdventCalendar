#!/usr/bin/env bash
# Quick POSIX smoke tests using Docker (host HTTP checks)
# - Ensures containers are up
# - Checks /health and /api/challenges on the host HTTP endpoint

set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

echo "Starting containers (build if needed)..."
docker-compose up -d --build

sleep 3

HEALTH_URL="http://127.0.0.1:5000/health"
CH_URL="http://127.0.0.1:5000/api/challenges/"

echo "Checking $HEALTH_URL"
resp=$(curl -sS -f "$HEALTH_URL") || { echo "Health check failed" >&2; exit 1; }
echo "Health response: $resp"

echo "Checking $CH_URL"
resp=$(curl -sS -f "$CH_URL") || { echo "Challenges endpoint failed" >&2; exit 1; }
count=$(printf '%s' "$resp" | python -c 'import sys,json; print(len(json.load(sys.stdin)))')
if [ "$count" -lt 1 ]; then
    echo "No challenges seeded" >&2
    exit 1
fi
echo "Challenges count: $count"

echo "Smoke tests passed."
