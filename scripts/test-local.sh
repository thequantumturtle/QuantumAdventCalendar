#!/usr/bin/env bash
# Quick local smoke tests using Docker (POSIX)
# - Ensures containers are up
# - Runs a backend /health check via Flask test client
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

echo "Starting containers (build if needed)..."
docker-compose up -d --build

echo "Waiting 2s for services to start..."
sleep 2

echo "Running backend health check inside container..."
docker-compose exec backend python - <<'PY'
from app import app
with app.test_client() as c:
    r = c.get('/health')
    print('health status:', r.json)
    if r.status_code != 200:
        raise SystemExit('Health check failed')
PY

echo "Smoke tests passed."
