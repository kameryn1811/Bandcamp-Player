@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ========================================
echo Building Bandcamp Player Launcher
echo ========================================
echo.

for /f "tokens=1-3 delims=/: " %%a in ("%time%") do set TIMESTAMP=%%a:%%b:%%c
echo [%TIMESTAMP%] [0/5] Checking Python version...
python --version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo.
for /f "tokens=1-3 delims=/: " %%a in ("%time%") do set TIMESTAMP=%%a:%%b:%%c
echo [%TIMESTAMP%] Checking if Python version is 3.11...
python -c "import sys; exit(0 if sys.version_info >= (3, 11) and sys.version_info < (3, 12) else 1)"
if errorlevel 1 (
    echo.
    echo WARNING: Python version check failed!
    echo.
    echo The launcher must be built with Python 3.11 for Windows 7 compatibility.
    echo Python 3.12+ does NOT support Windows 7.
    echo.
    echo Current Python version: 
    python --version
    echo.
    echo Please ensure you are using Python 3.11.x
    echo You can download it from: https://www.python.org/downloads/release/python-3110/
    echo.
    set /p CONTINUE="Continue anyway? (y/N): "
    if /i not "!CONTINUE!"=="y" (
        echo Build cancelled.
        pause
        exit /b 1
    )
)
for /f "tokens=1-3 delims=/: " %%a in ("%time%") do set TIMESTAMP=%%a:%%b:%%c
echo [%TIMESTAMP%] Python version OK for Windows 7 compatibility.
echo.

for /f "tokens=1-3 delims=/: " %%a in ("%time%") do set TIMESTAMP=%%a:%%b:%%c
echo [%TIMESTAMP%] [1/5] Installing/upgrading PyInstaller...
echo This may take a minute if PyInstaller needs to be downloaded...
python -m pip install --upgrade pyinstaller --quiet --progress-bar off
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)
for /f "tokens=1-3 delims=/: " %%a in ("%time%") do set TIMESTAMP=%%a:%%b:%%c
echo [%TIMESTAMP%] PyInstaller installation complete.
echo.

for /f "tokens=1-3 delims=/: " %%a in ("%time%") do set TIMESTAMP=%%a:%%b:%%c
echo [%TIMESTAMP%] [2/5] Installing/upgrading required dependencies...
echo Installing requests...
python -m pip install --upgrade requests --quiet --progress-bar off
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
for /f "tokens=1-3 delims=/: " %%a in ("%time%") do set TIMESTAMP=%%a:%%b:%%c
echo [%TIMESTAMP%] Dependencies installation complete.
echo.

for /f "tokens=1-3 delims=/: " %%a in ("%time%") do set TIMESTAMP=%%a:%%b:%%c
echo [%TIMESTAMP%] [3/5] Verifying PyInstaller version...
pyinstaller --version
echo.

for /f "tokens=1-3 delims=/: " %%a in ("%time%") do set TIMESTAMP=%%a:%%b:%%c
echo [%TIMESTAMP%] [4/5] Cleaning previous build artifacts...
if exist "build" (
    echo Removing build directory...
    rmdir /s /q "build" 2>nul
)
if exist "dist\BandcampPlayer.exe" (
    echo Removing previous executable...
    del /q "dist\BandcampPlayer.exe" 2>nul
)
for /f "tokens=1-3 delims=/: " %%a in ("%time%") do set TIMESTAMP=%%a:%%b:%%c
echo [%TIMESTAMP%] Cleanup complete.
echo.

for /f "tokens=1-3 delims=/: " %%a in ("%time%") do set TIMESTAMP=%%a:%%b:%%c
echo [%TIMESTAMP%] [5/5] Building launcher with PyInstaller...
echo This will bundle Python %PYTHON_VERSION% into the executable.
echo.
echo NOTE: This step can take 5-15 minutes depending on your system.
echo PyInstaller is analyzing dependencies, bundling files, and compressing...
echo.
echo Progress indicators:
echo   - Analyzing dependencies... (may take 1-3 minutes)
echo   - Collecting files... (may take 2-5 minutes)
echo   - Compressing executable... (may take 2-7 minutes)
echo.
echo You will see detailed output below as PyInstaller works:
echo.

:: Start timer
set START_TIME=%time%

:: Run PyInstaller with verbose output and progress indicators
:: --log-level=INFO shows detailed progress
:: --noconfirm skips prompts (faster)
:: --clean removes old build files (already done, but ensures clean state)
pyinstaller launcher.spec --clean --log-level=INFO --noconfirm
if errorlevel 1 (
    echo.
    echo ERROR: Build failed
    echo Check the output above for details.
    pause
    exit /b 1
)

for /f "tokens=1-3 delims=/: " %%a in ("%time%") do set TIMESTAMP=%%a:%%b:%%c
echo [%TIMESTAMP%] Build step completed.

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.

if exist "dist\BandcampPlayer.exe" (
    for %%A in ("dist\BandcampPlayer.exe") do (
        set FILE_SIZE=%%~zA
        set /a FILE_SIZE_MB=!FILE_SIZE!/1048576
        for /f "tokens=1-3 delims=/: " %%a in ("%time%") do set TIMESTAMP=%%a:%%b:%%c
        echo [%TIMESTAMP%] Executable size: !FILE_SIZE_MB! MB
    )
) else (
    echo WARNING: Executable not found in dist folder!
)

echo.
echo IMPORTANT: The EXE was built with Python %PYTHON_VERSION%
echo This version %PYTHON_VERSION% is compatible with Windows 7.
echo.
echo The launcher.exe is located in: dist\BandcampPlayer.exe
echo.
pause
exit /b 0

