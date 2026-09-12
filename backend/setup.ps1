# ReLoop backend setup for Windows PowerShell.
# Run this from the backend/ folder:   .\setup.ps1
#
# This deliberately never relies on "venv\Scripts\Activate.ps1" -- that
# script commonly gets silently blocked by PowerShell's execution policy,
# which was the root cause of the "alembic not recognized" / "module not
# found" errors. Instead every command below calls the venv's python.exe
# directly by path, which always works regardless of activation state or
# execution policy.

$ErrorActionPreference = "Stop"

Write-Host "== ReLoop backend setup ==" -ForegroundColor Cyan

# 1. Create .env if it doesn't exist yet.
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host ""
    Write-Host "Created .env from .env.example." -ForegroundColor Yellow
    Write-Host "Open backend\.env now and fill in:" -ForegroundColor Yellow
    Write-Host "  DATABASE_URL      (your real Postgres connection string)"
    Write-Host "  TELEGRAM_BOT_TOKEN (your real bot token from BotFather)"
    Write-Host ""
    Write-Host "Re-run .\setup.ps1 after you've edited .env." -ForegroundColor Yellow
    exit 0
}

# 2. Check .env still has placeholder values before doing anything that needs them.
$envContent = Get-Content ".env" -Raw
$dbStillPlaceholder = $envContent -match "user:password@localhost"
$tokenStillPlaceholder = $envContent -match "your_telegram_bot_token_here"

if ($dbStillPlaceholder -or $tokenStillPlaceholder) {
    Write-Host ""
    Write-Host "backend\.env still has placeholder values:" -ForegroundColor Red
    if ($dbStillPlaceholder) { Write-Host "  - DATABASE_URL is still the example placeholder" -ForegroundColor Red }
    if ($tokenStillPlaceholder) { Write-Host "  - TELEGRAM_BOT_TOKEN is still the example placeholder" -ForegroundColor Red }
    Write-Host "Fill these in, then re-run .\setup.ps1" -ForegroundColor Red
    exit 1
}

# 3. Fresh virtual environment.
if (Test-Path "venv") {
    Write-Host "Removing existing venv to start clean..."
    Remove-Item -Recurse -Force "venv"
}
Write-Host "Creating virtual environment..."
python -m venv venv

$venvPython = ".\venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "venv creation failed -- venv\Scripts\python.exe not found." -ForegroundColor Red
    Write-Host "Check that 'python --version' works in this shell at all." -ForegroundColor Red
    exit 1
}

# 4. Install dependencies straight into that interpreter -- no activation needed.
Write-Host "Installing dependencies (this can take a minute)..."
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r requirements.txt

# 5. Run the migration.
Write-Host ""
Write-Host "Running Alembic migration..." -ForegroundColor Cyan
& $venvPython -m alembic upgrade head

# 6. Seed collectors (still demo data unless you've edited seed_collectors.py).
Write-Host ""
Write-Host "Seeding collector profiles..." -ForegroundColor Cyan
& $venvPython -m app.db.seed_collectors

# 7. Run tests.
Write-Host ""
Write-Host "Running backend test suite..." -ForegroundColor Cyan
& $venvPython -m pytest -q

Write-Host ""
Write-Host "== Done. ==" -ForegroundColor Green
Write-Host "From now on, always call the backend using the venv's python.exe directly, e.g.:"
Write-Host "  .\venv\Scripts\python.exe -m uvicorn app.main:app --reload"
Write-Host "  .\venv\Scripts\python.exe -m pytest"
Write-Host "(No need to activate the venv -- calling python.exe by path works the same way.)"
