# Hospital Management System - Setup Script
# Run this script to set up the complete system

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Hospital Management System - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python installation
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Step 2: Install requirements
Write-Host ""
Write-Host "[2/5] Installing required packages..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Packages installed successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install packages. Please check requirements.txt" -ForegroundColor Red
    exit 1
}

# Step 3: Initialize database
Write-Host ""
Write-Host "[3/5] Initializing database..." -ForegroundColor Yellow
python database.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Database initialized successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to initialize database." -ForegroundColor Red
    exit 1
}

# Step 4: Verify files
Write-Host ""
Write-Host "[4/5] Verifying project files..." -ForegroundColor Yellow
$requiredFiles = @("app.py", "database.py", "privacy.py", "requirements.txt", "Assignment4.ipynb")
$allFilesExist = $true

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file (missing)" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if (-not $allFilesExist) {
    Write-Host "✗ Some required files are missing!" -ForegroundColor Red
    exit 1
}

# Step 5: Display credentials
Write-Host ""
Write-Host "[5/5] Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Default Login Credentials:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Admin:        admin / admin123" -ForegroundColor White
Write-Host "Doctor:       Dr.Bob / doc123" -ForegroundColor White
Write-Host "Receptionist: Alice_recep / rec123" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "To start the application, run:" -ForegroundColor Cyan
Write-Host "  streamlit run app.py" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to start the application now..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Start the application
Write-Host ""
Write-Host "Starting Hospital Management System..." -ForegroundColor Yellow
streamlit run app.py
