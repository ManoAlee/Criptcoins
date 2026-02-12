@echo off
setlocal enabledelayedexpansion

:: --- CONFIGURATION ---
set "PORT=5000"
set "IP=10.0.0.18"
set "URL=http://!IP!:!PORT!"

echo 🌌 GALAXY BITCOIN SYSTEM - QUANTUM LAUNCHER
echo --------------------------------------------
echo Target URL: !URL!
echo.

:: Detect Chrome Path
set "CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe"
if not exist "!CHROME_PATH!" set "CHROME_PATH=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

if not exist "!CHROME_PATH!" (
    echo [❌] Error: Chrome not found. Please open Google Chrome manually.
    pause
    exit /b
)

echo [🚀] Launching Chrome with Biometric Security Bypass...
echo [🔒] Flag: unsafely-treat-insecure-origin-as-secure
echo.

:: Launch Chrome
:: --user-data-dir is required for the flag to take effect correctly in many versions
start "" "!CHROME_PATH!" "!URL!" --unsafely-treat-insecure-origin-as-secure="!URL!" --user-data-dir="%TEMP%\chrome_quantum_session" --ignore-certificate-errors

echo [✅] System Initialized. You can close this window.
timeout /t 5
exit
