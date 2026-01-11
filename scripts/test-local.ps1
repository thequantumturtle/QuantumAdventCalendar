# PowerShell quick local smoke tests using Docker
# - Ensures containers are up
# - Runs a backend /health check via Flask test client
param()

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root\..\

Write-Host "Starting containers (build if needed)..."
docker-compose up -d --build

Start-Sleep -Seconds 2

Write-Host "Running backend health check inside container..."
docker-compose exec backend python - <<'PY'
from app import app
with app.test_client() as c:
    r = c.get('/health')
    print('health status:', r.json)
    if r.status_code != 200:
        raise SystemExit('Health check failed')
PY

Write-Host "Smoke tests passed." 
