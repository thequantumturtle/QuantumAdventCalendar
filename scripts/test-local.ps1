# PowerShell quick local smoke tests using Docker (host HTTP checks)
# Ensures containers are up and checks /health and /api/challenges

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$root\.."

Write-Host "Starting containers (build if needed)..."
docker-compose up -d --build

Start-Sleep -Seconds 3

$healthUrl = 'http://127.0.0.1:5000/health'
Write-Host "Checking health at $healthUrl"
try {
    $resp = Invoke-WebRequest -Uri $healthUrl -UseBasicParsing -TimeoutSec 10
    if ($resp.StatusCode -ne 200) {
        Write-Error "Health check failed: status $($resp.StatusCode)"
        exit 1
    }
    Write-Host "Health OK:" $resp.Content
} catch {
    Write-Error "Health check failed: $_"
    exit 1
}

$chUrl = 'http://127.0.0.1:5000/api/challenges/'
Write-Host "Checking challenges at $chUrl"
try {
    $resp = Invoke-WebRequest -Uri $chUrl -UseBasicParsing -TimeoutSec 10
    $data = $resp.Content | ConvertFrom-Json
    if (-not ($data -is [System.Array]) -or $data.Count -lt 1) {
        Write-Error "No challenges seeded (got $($data | Out-String))"
        exit 1
    }
    Write-Host "Challenges count:" $data.Count
} catch {
    Write-Error "Challenges endpoint failed: $_"
    exit 1
}

Write-Host "Smoke tests passed."
