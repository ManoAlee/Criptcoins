@echo off
REM 🌌 Galaxy Bitcoin System - All-in-One Setup & Deploy
REM Este script faz TUDO automaticamente

title Galaxy Bitcoin System - Complete Setup

echo ================================================================
echo     GALAXY BITCOIN SYSTEM - Complete Setup ^& Deploy
echo ================================================================
echo.
echo Este script ira:
echo   1. Verificar Python e Git
echo   2. Criar ambiente virtual
echo   3. Instalar dependencias
echo   4. Validar sistema
echo   5. Configurar Git
echo   6. Subir para GitHub
echo   7. Iniciar sistema
echo.
echo ================================================================
echo.

pause

REM ============================================================================
REM STEP 1: Verificar Python
REM ============================================================================
echo.
echo [1/7] Verificando Python...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python nao encontrado!
    echo Por favor, instale Python 3.8+ de https://python.org
    pause
    exit /b 1
)
echo [OK] Python encontrado!

REM ============================================================================
REM STEP 2: Verificar Git
REM ============================================================================
echo.
echo [2/7] Verificando Git...
git --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Git nao encontrado! Instalacao sera pulada.
    set GIT_AVAILABLE=0
) else (
    echo [OK] Git encontrado!
    set GIT_AVAILABLE=1
)

REM ============================================================================
REM STEP 3: Criar Ambiente Virtual
REM ============================================================================
echo.
echo [3/7] Criando ambiente virtual...
if exist venv (
    echo [INFO] Ambiente virtual ja existe
) else (
    python -m venv venv
    echo [OK] Ambiente virtual criado
)

REM ============================================================================
REM STEP 4: Ativar e Instalar Dependencias
REM ============================================================================
echo.
echo [4/7] Instalando dependencias...
call venv\Scripts\activate.bat

python -m pip install --upgrade pip --quiet

echo [INFO] Instalando dependencias principais...
pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [WARNING] Alguns pacotes falharam (pode ser PyAudio)
    echo Continuando mesmo assim - sistema funcionara sem esses pacotes
    echo [TIP] Para instalar pacotes opcionais depois: pip install -r requirements-optional.txt
)

echo.
echo [OK] Dependencias principais instaladas

REM ============================================================================
REM STEP 5: Validar Sistema
REM ============================================================================
echo.
echo [5/7] Validando sistema...
python validate_system.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [WARNING] Validacao encontrou problemas
    echo Deseja continuar mesmo assim? (s/n)
    set /p CONTINUE="> "
    if /i not "%CONTINUE%"=="s" (
        echo Setup cancelado
        pause
        exit /b 1
    )
)

REM ============================================================================
REM STEP 6: Configurar Git (Opcional)
REM ============================================================================
if %GIT_AVAILABLE%==1 (
    echo.
    echo [6/7] Configurar Git e subir para GitHub?
    echo (s) Sim, configurar agora
    echo (n) Nao, pular esta etapa
    set /p SETUP_GIT="> "
    
    if /i "%SETUP_GIT%"=="s" (
        echo.
        echo Configurando Git...
        
        REM Verificar se ja e um repo git
        if exist .git (
            echo [INFO] Repositorio Git ja inicializado
        ) else (
            git init
            echo [OK] Repositorio inicializado
        )
        
        REM Adicionar arquivos
        git add .
        
        REM Commit
        git commit -m "🌌 Galaxy Bitcoin System v1.0 - Complete Setup"
        
        REM Configurar remote
        echo.
        echo Digite o nome do repositorio GitHub:
        set /p REPO_NAME="> "
        echo Digite seu usuario GitHub:
        set /p GITHUB_USER="> "
        
        git remote remove origin 2>nul
        git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git
        
        git branch -M main
        
        echo.
        echo [INFO] Fazendo push para GitHub...
        echo Voce precisara fazer login no GitHub
        pause
        
        git push -u origin main
        
        if %ERRORLEVEL% EQU 0 (
            echo.
            echo ================================================================
            echo [SUCCESS] Projeto subido para GitHub!
            echo URL: https://github.com/%GITHUB_USER%/%REPO_NAME%
            echo ================================================================
        ) else (
            echo [WARNING] Falha ao fazer push. Configure manualmente depois.
        )
    )
) else (
    echo.
    echo [6/7] Git nao disponivel - pulando configuracao
)

REM ============================================================================
REM STEP 7: Iniciar Sistema
REM ============================================================================
echo.
echo [7/7] Iniciar o sistema agora? (s/n)
set /p START_NOW="> "

if /i "%START_NOW%"=="s" (
    echo.
    echo ================================================================
    echo     Iniciando Galaxy Bitcoin System...
    echo ================================================================
    echo.
    echo Sistema disponivel em: http://localhost:5000
    echo Pressione Ctrl+C para parar
    echo.
    
    REM Aguardar 3 segundos e abrir navegador
    timeout /t 3 /nobreak >nul
    start http://localhost:5000
    
    python simple_app.py
) else (
    echo.
    echo ================================================================
    echo     Setup Concluido!
    echo ================================================================
    echo.
    echo Para iniciar o sistema:
    echo   1. Ative o ambiente virtual: venv\Scripts\activate
    echo   2. Execute: python quick_start.py
    echo   ou execute: python simple_app.py
    echo.
    echo Sistema estara disponivel em: http://localhost:5000
    echo.
)

echo.
echo ================================================================
echo     Obrigado por usar Galaxy Bitcoin System!
echo ================================================================
echo.

pause
