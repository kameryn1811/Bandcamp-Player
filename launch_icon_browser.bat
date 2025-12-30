@echo off
REM ============================================================================
REM QtAwesome Icon Browser Launcher
REM ============================================================================
REM This script launches the QtAwesome icon browser (qta-browser)
REM which allows you to browse and preview all available FontAwesome icons
REM ============================================================================

echo.
echo QtAwesome Icon Browser Launcher
echo =================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 or later
    pause
    exit /b 1
)

echo Python found: 
python --version
echo.

REM Try to launch qta-browser using Python module
echo Launching QtAwesome Icon Browser...
echo.

REM Method 1: Try as Python module (most reliable)
python -m qtawesome.browser 2>nul
if errorlevel 1 (
    echo.
    echo Attempting alternative method...
    REM Method 2: Try direct command (if installed as script)
    qta-browser 2>nul
    if errorlevel 1 (
        echo.
        echo ERROR: Could not launch QtAwesome browser
        echo.
        echo QtAwesome may not be installed. Attempting to install...
        python -m pip install qtawesome --quiet
        if errorlevel 1 (
            echo.
            echo ERROR: Failed to install qtawesome
            echo Please install manually: pip install qtawesome
            pause
            exit /b 1
        )
        echo.
        echo QtAwesome installed! Launching browser...
        python -m qtawesome.browser
    )
)

if errorlevel 1 (
    echo.
    echo ERROR: Failed to launch QtAwesome browser
    echo.
    echo Troubleshooting:
    echo 1. Make sure qtawesome is installed: pip install qtawesome
    echo 2. Try running manually: python -m qtawesome.browser
    echo.
    pause
    exit /b 1
)

echo.
echo Icon browser closed.
pause

