#!/bin/bash
# 🌌 Galaxy Bitcoin System - Git Setup & Upload (Unix)

echo "================================================"
echo "   GALAXY BITCOIN SYSTEM - Git Setup"
echo "================================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git não encontrado! Por favor instale:"
    echo "  Ubuntu/Debian: sudo apt-get install git"
    echo "  MacOS: brew install git"
    exit 1
fi

echo "✅ Git encontrado: $(git --version)"
echo ""

# Initialize git repository
echo "[1/7] Inicializando repositório Git..."
git init

# Add all files
echo "[2/7] Adicionando arquivos..."
git add .

# First commit
echo "[3/7] Criando commit inicial..."
git commit -m "🌌 Initial commit: Galaxy Bitcoin System v1.0

- Sistema completo de trading Bitcoin
- Autenticação biométrica
- Reconhecimento facial em tempo real
- APIs Bitcoin reais integradas
- Dashboard profissional
- WebSocket para dados em tempo real
- Blockchain funcional com PoW
- Comandos de voz
- Sistema de carteiras
- Trading engine"

echo ""
echo "[4/7] Configurar repositório remoto"
echo ""
read -p "Digite o nome do seu repositório (ex: galaxy-bitcoin-system): " REPO_NAME
echo ""
read -p "Digite seu usuário GitHub: " GITHUB_USER
echo ""

# Set remote
echo "[5/7] Configurando remote..."
git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"

# Create and push to main branch
echo "[6/7] Criando branch main..."
git branch -M main

echo ""
echo "[7/7] Fazendo push para GitHub..."
echo ""
echo "⚠️  IMPORTANTE: Você precisará fazer login no GitHub"
echo ""
read -p "Pressione ENTER para continuar..."

git push -u origin main

echo ""
echo "================================================"
echo "           ✅ UPLOAD CONCLUÍDO!"
echo "================================================"
echo ""
echo "🌐 Seu repositório está em:"
echo "   https://github.com/$GITHUB_USER/$REPO_NAME"
echo ""
echo "================================================"
echo ""
