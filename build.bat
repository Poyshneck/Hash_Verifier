@echo off
setlocal enabledelayedexpansion

REM Get the directory where the script is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Set up logging
set "LOG_FILE=build_log.txt"
echo Build started at %date% %time% > "%LOG_FILE%"
echo ============================ >> "%LOG_FILE%"

REM Function to log messages
call :log "File Hash Verifier Build Script"
call :log "============================"
call :log ""

REM Check if running as administrator
net session >nul 2>&1
if %errorlevel% == 0 (
    call :log "WARNING: Running as administrator"
    call :log "While this is not recommended by PyInstaller, it may be necessary"
    call :log "in some cases to resolve permission issues."
    call :log ""
    call :log "Press any key to continue with administrator privileges..."
    pause >nul
)

call :log "Checking Python installation..."
REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    call :log "ERROR: Python is not installed or not in PATH."
    call :log "Please install Python from https://www.python.org/downloads/"
    call :log "Make sure to check 'Add Python to PATH' during installation."
    pause
    exit /b 1
)
call :log "Python found."

call :log "Checking tkinter..."
REM Check if tkinter is available
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    call :log "ERROR: tkinter is not installed."
    call :log "Please reinstall Python and make sure to check 'tcl/tk and IDLE' during installation."
    pause
    exit /b 1
)
call :log "tkinter found."

call :log "Checking requirements.txt..."
REM Check if requirements.txt exists
if not exist "requirements.txt" (
    call :log "ERROR: requirements.txt not found in the current directory."
    call :log "Current directory: %CD%"
    call :log "Please make sure you're running this script from the correct directory."
    pause
    exit /b 1
)
call :log "requirements.txt found."

call :log "Installing requirements..."
REM Install PyInstaller if not already installed
pip install -r requirements.txt >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    call :log "ERROR: Failed to install requirements."
    pause
    exit /b 1
)
call :log "Requirements installed successfully."

call :log "Creating version file..."
REM Create version file using Python script
python create_version.py >> "%LOG_FILE%" 2>&1

if errorlevel 1 (
    call :log "ERROR: Failed to create version.txt using Python script"
    call :log "Python error code: %errorlevel%"
    pause
    exit /b 1
)

if not exist "version.txt" (
    call :log "ERROR: version.txt was not created"
    call :log "Current directory: %CD%"
    call :log "Please check if you have write permissions in this directory"
    pause
    exit /b 1
)

call :log "Version file created successfully at: %CD%\version.txt"

call :log ""
call :log "Building executable..."
call :log "This may take a few minutes..."
call :log ""

call :log "Checking for running instances..."
REM Force close any running instances
taskkill /F /IM "FileHashVerifier.exe" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    call :log "No running instances found."
) else (
    call :log "Closed running instances."
)

REM Wait a moment for processes to close
timeout /t 2 /nobreak >nul

call :log "Setting up build directories..."
REM Set up build directories with shorter paths
set "BUILD_ROOT=C:\PyBuild"
set "DIST_PATH=%BUILD_ROOT%\dist"
set "WORK_PATH=%BUILD_ROOT%\build"

REM Create build directories if they don't exist
if not exist "%BUILD_ROOT%" (
    call :log "Creating build root directory..."
    mkdir "%BUILD_ROOT%" >> "%LOG_FILE%" 2>&1
)
if not exist "%DIST_PATH%" (
    call :log "Creating dist directory..."
    mkdir "%DIST_PATH%" >> "%LOG_FILE%" 2>&1
)
if not exist "%WORK_PATH%" (
    call :log "Creating work directory..."
    mkdir "%WORK_PATH%" >> "%LOG_FILE%" 2>&1
)

call :log "Cleaning up previous build artifacts..."
REM Clean up previous build artifacts
if exist "FileHashVerifier.spec" del /f /q "FileHashVerifier.spec" >> "%LOG_FILE%" 2>&1

call :log "Running PyInstaller..."
REM Build the executable with additional options to reduce false positives
pyinstaller --noconfirm --onefile --windowed --icon=NONE --name "FHV" ^
    --add-data "README.md;." ^
    --add-data "BUILD_INSTRUCTIONS.md;." ^
    --add-data "help.html;." ^
    --version-file version.txt ^
    --distpath "%DIST_PATH%" ^
    --workpath "%WORK_PATH%" ^
    file_hash_verifier.py >> "%LOG_FILE%" 2>&1

if errorlevel 1 (
    call :log "ERROR: PyInstaller failed with error code %errorlevel%"
    call :log "Check build_log.txt for details"
    pause
    exit /b 1
)

call :log ""
if exist "%DIST_PATH%\FHV.exe" (
    call :log "Build successful! Moving executable to final location..."
    
    REM Create dist directory if it doesn't exist
    if not exist "dist" mkdir "dist" >> "%LOG_FILE%" 2>&1
    
    REM Move the executable to the final location
    move /Y "%DIST_PATH%\FHV.exe" "dist\" >> "%LOG_FILE%" 2>&1
    
    if exist "dist\FHV.exe" (
        call :log "The executable has been created in the 'dist' folder."
        call :log "You can find it at: %CD%\dist\FHV.exe"
        call :log ""
        call :log "NOTE: Some antivirus software may flag this executable as suspicious."
        call :log "This is a false positive because the executable is not digitally signed."
        call :log "You can safely add it to your antivirus exclusion list."
        call :log ""
        call :log "To verify the executable is safe:"
        call :log "1. The source code is available in file_hash_verifier.py"
        call :log "2. The executable was built from this source code"
        call :log "3. No external dependencies were added during the build"
    ) else (
        call :log "Failed to move executable to final location."
        call :log "The executable is available at: %DIST_PATH%\FHV.exe"
    )
) else (
    call :log "Build failed. Please check the error messages above."
    call :log ""
    call :log "Common issues:"
    call :log "1. The executable is currently running - close it and try again"
    call :log "2. Antivirus is blocking the build - temporarily disable it"
    call :log "3. Insufficient permissions - try running as administrator"
    call :log "4. Wrong directory - make sure you're in the correct directory"
    call :log "5. File is locked - close any applications that might be using it"
    call :log ""
    call :log "Troubleshooting steps:"
    call :log "1. Close all instances of the File Hash Verifier"
    call :log "2. Temporarily disable your antivirus"
    call :log "3. Try running as administrator if permission issues persist"
    call :log "4. Make sure you have write permissions to the directory"
    call :log "5. Try running the script from a different directory"
    call :log "6. Check if any antivirus is blocking file operations"
)

call :log "Cleaning up..."
REM Clean up
del /f /q version.txt >> "%LOG_FILE%" 2>&1
rmdir /s /q build >> "%LOG_FILE%" 2>&1
rmdir /s /q __pycache__ >> "%LOG_FILE%" 2>&1

call :log ""
call :log "Build completed at %date% %time%"
call :log "Check build_log.txt for detailed information"
echo.
echo Build completed. Check build_log.txt for details.
pause
exit /b 0

:log
echo %~1
echo %~1 >> "%LOG_FILE%"
exit /b 0 