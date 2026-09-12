$backend = $PSScriptRoot
$python = Join-Path $backend "venv\Scripts\python.exe"

$process = Start-Process -FilePath $python -ArgumentList "-m","uvicorn","app.main:app","--reload" -WorkingDirectory $backend -PassThru

Write-Host "Starting ReLoop backend..."

while (-not (Test-NetConnection 127.0.0.1 -Port 8000 -InformationLevel Quiet)) {
    Start-Sleep -Milliseconds 500
}

Write-Host "Backend is running!"
Start-Process "http://127.0.0.1:8000/docs"

Wait-Process -Id $process.Id