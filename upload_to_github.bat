@echo off
REM 🌌 Galaxy Bitcoin System - Git Upload Script
REM Faz upload automático para seu repositório GitHub

setlocal enabledelayedexpansion

cls
echo.
echo ==============================================================
echo     GALAXY BITCOIN SYSTEM - Git Upload Automatico
echo ==============================================================
echo.

set REPO_URL=https://github.com/ManoAlee/Criptcoins.git
set BRANCH=main

echo Repository: %REPO_URL%
echo Branch: %BRANCH%
echo.

REM Verificar Git
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git nao encontrado!
    echo Por favor instale Git de: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [OK] Git encontrado!
echo.

REM Inicializar repositório se necessário
if not exist .git (
    echo [1/5] Inicializando repositorio Git...
    git init
    echo [OK] Repositorio inicializado
) else (
    echo [1/5] Repositorio Git ja existe
)

echo.

REM Configurar usuário Git
echo [2/5] Verificando configuracao de usuario Git...
git config user.email >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Configurando usuario Git...
    set /p GIT_EMAIL=Email: 
    set /p GIT_NAME=Nome: 
    git config user.email "%GIT_EMAIL%"
    git config user.name "%GIT_NAME%"
    echo [OK] Usuario configurado
) else (
    echo [OK] Usuario ja configurado
)

echo.

REM Adicionar arquivos
echo [3/5] Adicionando arquivos ao Git...
git add .
echo [OK] Arquivos adicionados

echo.

REM Commit
echo [4/5] Criando commit...
git commit -m "🌌 Galaxy Bitcoin System v1.0 - Complete Implementation" --no-verify
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Nenhuma mudanca para commitar
) else (
    echo [OK] Commit criado
)

echo.

REM Configurar remote
echo [5/5] Fazendo push para GitHub...

git remote -v | findstr origin >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Atualizando remote...
    git remote set-url origin %REPO_URL%
) else (
    echo Adicionando remote...
    git remote add origin %REPO_URL%
)

REM Criar branch main
git branch -M main

echo.
echo Iniciando push... (pode pedir login no GitHub)
pause

REM Push
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ==============================================================
    echo     [SUCCESS] UPLOAD CONCLUIDO COM SUCESSO!
    echo ==============================================================
    echo.
    echo Acesse seu repositorio:
    echo    https://github.com/ManoAlee/Criptcoins
    echo.
    echo Documentacao disponivel em:
    echo    - README.md
    echo    - START_HERE.md
    echo    - PROJECT_SUMMARY.md
    echo    - DEPLOYMENT.md
    echo.
) else (
    echo.
    echo ==============================================================
    echo     [WARNING] Erro ao fazer push
    echo ==============================================================
    echo.
    echo Possivel motivo: Credenciais do GitHub incorretas
    echo.
    echo Solucao:
    echo 1. Abra GitHub em seu navegador
    echo 2. Crie um novo repositorio chamado "Criptcoins"
    echo 3. Configure SSH ou HTTPS
    echo 4. Tente novamente: git push -u origin main
    echo.
)

echo.
pause
