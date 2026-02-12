@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ==================================================
echo Galaxy Bitcoin - Install and Run (Windows)
echo ==================================================

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Python not found in PATH. Please install Python 3.7+ and add to PATH.
  pause
  exit /b 1
)

REM Create virtual environment
if not exist .venv (
  echo Creating virtual environment .venv...
  python -m venv .venv
  if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
  )
) else (
  echo Virtual environment .venv already exists.
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
  echo [ERROR] Failed to activate virtual environment.
  pause
  exit /b 1
)

echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel --quiet

REM Install dependencies from requirements.txt
if exist requirements.txt (
  echo Installing Python requirements from requirements.txt...
  pip install -r requirements.txt
) else (
  echo [WARN] requirements.txt not found, installing core deps.
  pip install numpy matplotlib scipy ecdsa base58 networkx pytest
)

REM Ensure biometric dependencies
echo Installing biometric dependencies (opencv-python, cryptography)...
pip install opencv-python cryptography --quiet

echo Running basic install_and_test.py to verify setup...
python install_and_test.py

echo ==================================================
echo If the tests passed, running biometric utility now.
echo ==================================================

set /p runnow="Run biometric_key.py now? [Y/n]: "
if /i "%runnow%"=="n" (
  echo Skipping biometric utility. You can run it later with: python biometric_key.py
  pause
  exit /b 0
)

REM Run biometric utility
python biometric_key.py

echo Done.
pause
