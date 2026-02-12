#!/bin/bash
# 🌌 Galaxy Bitcoin System - All-in-One Setup & Deploy
# Este script faz TUDO automaticamente

set -e  # Exit on error

echo "================================================================"
echo "   GALAXY BITCOIN SYSTEM - Complete Setup & Deploy"
echo "================================================================"
echo ""
echo "Este script irá:"
echo "  1. Verificar Python e Git"
echo "  2. Criar ambiente virtual"
echo "  3. Instalar dependências"
echo "  4. Validar sistema"
echo "  5. Configurar Git"
echo "  6. Subir para GitHub"
echo "  7. Iniciar sistema"
echo ""
echo "================================================================"
echo ""

read -p "Pressione ENTER para continuar..."

# ============================================================================
# STEP 1: Verificar Python
# ============================================================================
echo ""
echo "[1/7] Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION encontrado"
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo "✅ $PYTHON_VERSION encontrado"
    PYTHON_CMD=python
else
    echo "❌ Python não encontrado!"
    echo "Por favor, instale Python 3.8+ de https://python.org"
    exit 1
fi

# ============================================================================
# STEP 2: Verificar Git
# ============================================================================
echo ""
echo "[2/7] Verificando Git..."
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    echo "✅ $GIT_VERSION encontrado"
    GIT_AVAILABLE=1
else
    echo "⚠️  Git não encontrado! Instalação do Git será pulada."
    GIT_AVAILABLE=0
fi

# ============================================================================
# STEP 3: Criar Ambiente Virtual
# ============================================================================
echo ""
echo "[3/7] Criando ambiente virtual..."
if [ -d "venv" ]; then
    echo "ℹ️  Ambiente virtual já existe"
else
    $PYTHON_CMD -m venv venv
    echo "✅ Ambiente virtual criado"
fi

# ============================================================================
# STEP 4: Ativar e Instalar Dependências
# ============================================================================
echo ""
echo "[4/7] Instalando dependências..."
source venv/bin/activate

$PYTHON_CMD -m pip install --upgrade pip --quiet

echo "ℹ️  Instalando dependências principais..."
if ! pip install -r requirements.txt; then
    echo ""
    echo "⚠️  Alguns pacotes falharam (pode ser PyAudio)"
    echo "Sistema funcionará mesmo assim - você pode instalar pacotes opcionais depois:"
    echo "pip install -r requirements-optional.txt"
fi

echo ""
echo "✅ Dependências instaladas"

# ============================================================================
# STEP 5: Validar Sistema
# ============================================================================
echo ""
echo "[5/7] Validando sistema..."
if ! $PYTHON_CMD validate_system.py; then
    echo ""
    echo "⚠️  Validação encontrou problemas"
    read -p "Deseja continuar mesmo assim? (s/n): " CONTINUE
    if [ "$CONTINUE" != "s" ] && [ "$CONTINUE" != "S" ]; then
        echo "Setup cancelado"
        exit 1
    fi
fi

# ============================================================================
# STEP 6: Configurar Git (Opcional)
# ============================================================================
if [ $GIT_AVAILABLE -eq 1 ]; then
    echo ""
    echo "[6/7] Configurar Git e subir para GitHub?"
    echo "(s) Sim, configurar agora"
    echo "(n) Não, pular esta etapa"
    read -p "> " SETUP_GIT
    
    if [ "$SETUP_GIT" = "s" ] || [ "$SETUP_GIT" = "S" ]; then
        echo ""
        echo "Configurando Git..."
        
        # Verificar se já é um repo git
        if [ -d ".git" ]; then
            echo "ℹ️  Repositório Git já inicializado"
        else
            git init
            echo "✅ Repositório inicializado"
        fi
        
        # Adicionar arquivos
        git add .
        
        # Commit
        git commit -m "🌌 Galaxy Bitcoin System v1.0 - Complete Setup" || true
        
        # Configurar remote
        echo ""
        read -p "Digite o nome do repositório GitHub: " REPO_NAME
        read -p "Digite seu usuário GitHub: " GITHUB_USER
        
        git remote remove origin 2>/dev/null || true
        git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
        
        git branch -M main
        
        echo ""
        echo "ℹ️  Fazendo push para GitHub..."
        echo "Você precisará fazer login no GitHub"
        read -p "Pressione ENTER para continuar..."
        
        if git push -u origin main; then
            echo ""
            echo "================================================================"
            echo "✅ Projeto subido para GitHub!"
            echo "URL: https://github.com/$GITHUB_USER/$REPO_NAME"
            echo "================================================================"
        else
            echo "⚠️  Falha ao fazer push. Configure manualmente depois."
        fi
    fi
else
    echo ""
    echo "[6/7] Git não disponível - pulando configuração"
fi

# ============================================================================
# STEP 7: Iniciar Sistema
# ============================================================================
echo ""
read -p "[7/7] Iniciar o sistema agora? (s/n): " START_NOW

if [ "$START_NOW" = "s" ] || [ "$START_NOW" = "S" ]; then
    echo ""
    echo "================================================================"
    echo "   Iniciando Galaxy Bitcoin System..."
    echo "================================================================"
    echo ""
    echo "Sistema disponível em: http://localhost:5000"
    echo "Pressione Ctrl+C para parar"
    echo ""
    
    # Aguardar 3 segundos e abrir navegador
    sleep 3
    
    # Tentar abrir navegador (funciona em sistemas com desktop)
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:5000 &
    elif command -v open &> /dev/null; then
        open http://localhost:5000 &
    fi
    
    $PYTHON_CMD simple_app.py
else
    echo ""
    echo "================================================================"
    echo "   ✅ Setup Concluído!"
    echo "================================================================"
    echo ""
    echo "Para iniciar o sistema:"
    echo "  1. Ative o ambiente virtual: source venv/bin/activate"
    echo "  2. Execute: python quick_start.py"
    echo "  ou execute: python simple_app.py"
    echo ""
    echo "Sistema estará disponível em: http://localhost:5000"
    echo ""
fi

echo ""
echo "================================================================"
echo "   🌌 Obrigado por usar Galaxy Bitcoin System!"
echo "================================================================"
echo ""
