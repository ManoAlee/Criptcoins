@echo off
chcp 65001 > nul
title Galaxy Bitcoin - Interface Minimalista
color 0B

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║     🌌 GALAXY BITCOIN SYSTEM - Interface Minimalista      ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo 🚀 Iniciando sistema...
echo.

REM Verificar Python
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Instale Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

REM Verificar dependências
echo 📦 Verificando dependências...
pip show flask > nul 2>&1
if errorlevel 1 (
    echo ⚠️  Flask não instalado. Instalando...
    pip install flask opencv-python SpeechRecognition pyaudio
)

echo ✅ Dependências OK
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo 📱 O sistema vai abrir em: http://localhost:5000
echo.
echo 📹 Câmera: Ativa
echo 🎤 Voz: Ativa  
echo ⛓️  Blockchain: Online
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo 💡 Pressione Ctrl+C para parar o servidor
echo.

REM Abrir navegador após 3 segundos
start "" timeout /t 3 /nobreak ^&^& start http://localhost:5000

REM Iniciar servidor
python simple_app.py

pause
