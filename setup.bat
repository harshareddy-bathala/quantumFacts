@echo off
REM Setup script for Windows

echo ========================================
echo  Viral Shorts Generator - Setup
echo ========================================
echo.

REM Check Python
echo Checking Python...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.9+ from python.org
    pause
    exit /b 1
)
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo .env file created. Please edit it with your API keys.
) else (
    echo .env file already exists.
)
echo.

REM Create directories
echo Creating directories...
if not exist "assets\music" mkdir assets\music
if not exist "output" mkdir output
if not exist "temp" mkdir temp
if not exist "logs" mkdir logs
echo Directories created.
echo.

REM Run setup check
echo Running setup verification...
python setup_check.py
echo.

echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Edit .env file with your API keys
echo   2. Add background music to assets/music/
echo   3. Run: python src\viral_shorts\main.py
echo.
pause
