Write-Host "=========================================="
Write-Host "       Starting XENO AI-Native CRM        "
Write-Host "=========================================="
Write-Host ""

# Create Virtual Environment if it doesn't exist
if (-Not (Test-Path "venv")) {
    Write-Host "-> Creating Python Virtual Environment..."
    py -3.12 -m venv venv
}

# Activate venv
Write-Host "-> Activating venv and installing dependencies..."
.\venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
pip install -r channel-service/requirements.txt

$root = $PSScriptRoot
$pythonExe = Join-Path $root "venv\Scripts\python.exe"

# Run Data Ingestion if needed
Write-Host "-> Ingesting BeanBox Seed Data..."
& $pythonExe (Join-Path $root "seed\ingest.py")

# Start Channel Service (Background)
Write-Host "-> Starting Channel Service on port 8001..."
Start-Process -NoNewWindow -FilePath $pythonExe -ArgumentList "-m uvicorn app.main:app --host 0.0.0.0 --port 8001" -WorkingDirectory (Join-Path $root "channel-service")
Start-Sleep -Seconds 2

# Start Backend API (Background)
Write-Host "-> Starting Backend API on port 8000..."
Start-Process -NoNewWindow -FilePath $pythonExe -ArgumentList "-m uvicorn app.main:app --host 0.0.0.0 --port 8000" -WorkingDirectory (Join-Path $root "backend")
Start-Sleep -Seconds 2

# Start Frontend (Interactive)
Write-Host "-> Starting Next.js Frontend on port 3000..."
Set-Location (Join-Path $root "frontend")
npm run dev
