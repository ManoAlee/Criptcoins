@echo off
REM 🌌 Galaxy Bitcoin System - Git Setup

echo ================================================
echo     GALAXY BITCOIN SYSTEM - Git Setup
echo ================================================
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git nao encontrado! Por favor instale:
    echo https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [OK] Git encontrado!
echo.

REM Initialize git repository
echo [1/7] Inicializando repositorio Git...
git init

REM Add all files
echo [2/7] Adicionando arquivos...
git add .

REM First commit
echo [3/7] Criando commit inicial...
git commit -m "🌌 Initial commit: Galaxy Bitcoin System v1.0

- Sistema completo de trading Bitcoin
- Autenticacao biometrica
- Reconhecimento facial em tempo real
- APIs Bitcoin reais integradas
- Dashboard profissional
- WebSocket para dados em tempo real
- Blockchain funcional com PoW
- Comandos de voz
- Sistema de carteiras
- Trading engine"

echo.
echo [4/7] Configurar repositorio remoto
echo.
echo Digite o nome do seu repositorio (ex: galaxy-bitcoin-system):
set /p REPO_NAME="> "
echo.
echo Digite seu usuario GitHub:
set /p GITHUB_USER="> "
echo.

REM Set remote
echo [5/7] Configurando remote...
git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git

REM Create and push to main branch
echo [6/7] Criando branch main...
git branch -M main

echo.
echo [7/7] Fazendo push para GitHub...
echo.
echo IMPORTANTE: Voce precisara fazer login no GitHub
echo.
pause

git push -u origin main

echo.
echo ================================================
echo             UPLOAD CONCLUIDO!
echo ================================================
echo.
echo Seu repositorio esta em:
echo https://github.com/%GITHUB_USER%/%REPO_NAME%
echo.
echo ================================================
echo.

pause
