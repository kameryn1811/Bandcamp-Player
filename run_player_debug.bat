@echo off
REM Bandcamp Player - Direct Runner (keeps console open on error)
REM Use this to run bandcamp_pl_gui.py directly and see any errors

echo Bandcamp Player - Direct Runner
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.11.6 from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM Show Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python version: %PYTHON_VERSION%
echo.

REM Change to script directory
cd /d "%~dp0"

REM Run the script and capture errors
echo Starting Bandcamp Player...
echo.
python bandcamp_pl_gui.py

REM Check exit code
if errorlevel 1 (
    echo.
    echo ========================
    echo Player failed to start.
    echo Check the error message above.
    echo ========================
    echo.
)

REM Always pause so user can see any errors
pause

