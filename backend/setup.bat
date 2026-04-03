@echo off
REM Setup script for MahilaUdyam Daily Market Price Updates
REM This script runs all necessary steps to enable market price functionality

setlocal enabledelayedexpansion

cd /d "c:\Users\Rupali\OneDrive\Desktop\Villupuram_Hackathon\MahilaUdyam_claude\MahilaUdyam_claude\MahilaUdyam\backend"

echo.
echo =====================================================
echo  MahilaUdyam - Market Price Setup
echo =====================================================
echo.

REM Step 1: Create migrations
echo [1/4] Creating database migrations...
python manage.py makemigrations api
if errorlevel 1 (
    echo Error creating migrations!
    pause
    exit /b 1
)
echo ✓ Migrations created

echo.

REM Step 2: Apply migrations
echo [2/4] Applying migrations to database...
python manage.py migrate
if errorlevel 1 (
    echo Error applying migrations!
    pause
    exit /b 1
)
echo ✓ Migrations applied

echo.

REM Step 3: Run setup script
echo [3/4] Initializing price history...
python setup_market_updates.py
if errorlevel 1 (
    echo Error running setup!
    pause
    exit /b 1
)
echo ✓ Setup complete

echo.

REM Step 4: Run first update
echo [4/4] Running first price update...
python manage.py update_market_prices
if errorlevel 1 (
    echo Error running price update!
    pause
    exit /b 1
)
echo ✓ Price update complete

echo.
echo =====================================================
echo  ✓ Setup Complete!
echo =====================================================
echo.
echo Next steps:
echo 1. Start backend: python manage.py runserver 0.0.0.0:8000
echo 2. Start frontend: npm start (in frontend folder)
echo 3. Go to Market Price page - you should see prices!
echo.
echo Optional: Setup automated daily updates
echo   - See QUICKSTART.md for scheduler options
echo.
pause
