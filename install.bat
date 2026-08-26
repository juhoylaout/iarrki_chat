@echo off
cd /d "%~dp0"

REM Check whether python is installed and the py command is usable
echo Checking python installation...
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.12 is not installed or the py command is not usable. Please install Python 3.12 via python.org
    exit /b 1
)

REM Attempt to create a python virtual environment if it does not exist already
echo Creating a virtual environment...
if not exist .venv (
    py -3.12 -m venv .venv
)
if errorlevel 1 (
    echo Failed to create virtual environment.
    exit /b 1
)

REM Install required packages
echo Installing required python packages...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt

REM Attempt to create a shortcut to the program on the Desktop
echo Creating a shortcut to the desktop...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0CreateShortcut.ps1"
if errorlevel 1 (
    echo Failed to create a shortcut. Resuming installation.
) else (
    echo Shortcut created on the Desktop.
)

echo Installation complete.
pause