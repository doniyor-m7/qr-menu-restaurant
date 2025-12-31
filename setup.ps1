# QR Menu - PowerShell Setup Script
# Run this in PowerShell: .\setup.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "QR Menu - Setup Script (PowerShell)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[*] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Python not found. Please install Python 3.8+" -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Remove old venv if exists
if (Test-Path "venv") {
    Write-Host "[*] Removing old virtual environment..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
    Write-Host "✓ Old venv removed" -ForegroundColor Green
}

# Create virtual environment
Write-Host ""
Write-Host "[1/7] Creating virtual environment..." -ForegroundColor Yellow
try {
    python -m venv venv
    if ($LASTEXITCODE -ne 0) { throw "Failed to create venv" }
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Failed to create virtual environment" -ForegroundColor Red
    Write-Host "Try running PowerShell as Administrator" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate virtual environment
Write-Host ""
Write-Host "[2/7] Activating virtual environment..." -ForegroundColor Yellow
try {
    & .\venv\Scripts\Activate.ps1
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "You may need to run: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Upgrade pip
Write-Host ""
Write-Host "[3/7] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "✓ Pip upgraded" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "[4/7] Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray
try {
    pip install -r requirements.txt --quiet
    if ($LASTEXITCODE -ne 0) { throw "Failed to install dependencies" }
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Run migrations
Write-Host ""
Write-Host "[5/7] Creating database..." -ForegroundColor Yellow
try {
    python manage.py makemigrations restaurant --noinput
    python manage.py migrate --noinput
    if ($LASTEXITCODE -ne 0) { throw "Failed to create database" }
    Write-Host "✓ Database created" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Failed to create database" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Populate sample data
Write-Host ""
Write-Host "[6/7] Loading sample data..." -ForegroundColor Yellow
try {
    python manage.py populate_sample_data
    if ($LASTEXITCODE -ne 0) { throw "Failed to load sample data" }
    Write-Host "✓ Sample data loaded" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Failed to load sample data" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Generate QR codes
Write-Host ""
Write-Host "[7/7] Generating QR codes..." -ForegroundColor Yellow
try {
    python manage.py generate_qr_codes
    if ($LASTEXITCODE -ne 0) { throw "Failed to generate QR codes" }
    Write-Host "✓ QR codes generated" -ForegroundColor Green
} catch {
    Write-Host "✗ WARNING: Failed to generate QR codes (optional)" -ForegroundColor Yellow
}

# Collect static files
Write-Host ""
Write-Host "[*] Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput --clear | Out-Null
Write-Host "✓ Static files collected" -ForegroundColor Green

# Success message
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ Setup completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Default credentials:" -ForegroundColor Yellow
Write-Host "  Admin:   admin / admin123" -ForegroundColor White
Write-Host "  Kitchen: kitchen / kitchen123" -ForegroundColor White
Write-Host "  Waiter:  waiter / waiter123" -ForegroundColor White
Write-Host ""
Write-Host "To start the server, run:" -ForegroundColor Yellow
Write-Host "  .\run.ps1" -ForegroundColor Cyan
Write-Host "  OR" -ForegroundColor Gray
Write-Host "  python manage.py runserver" -ForegroundColor Cyan
Write-Host ""
Write-Host "Then open: http://localhost:8000" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"
