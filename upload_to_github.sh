#!/bin/bash
# 🌌 Galaxy Bitcoin System - Git Upload Script
# Faz upload automático para seu repositório GitHub

set -e

echo ""
echo "=============================================================="
echo "🌌 GALAXY BITCOIN SYSTEM - Git Upload Automático"
echo "=============================================================="
echo ""

# Configurações
REPO_URL="https://github.com/ManoAlee/Criptcoins.git"
BRANCH="main"

echo "Repository: $REPO_URL"
echo "Branch: $BRANCH"
echo ""

# Verificar Git
if ! command -v git &> /dev/null; then
    echo "❌ Git não encontrado. Por favor instale Git."
    exit 1
fi

echo "✅ Git encontrado"
echo ""

# Inicializar repositório se necessário
if [ ! -d ".git" ]; then
    echo "[1/5] Inicializando repositório Git..."
    git init
    echo "✅ Repositório inicializado"
else
    echo "[1/5] Repositório Git já existe"
fi

echo ""

# Configurar usuário Git (se não estiver configurado)
if ! git config user.email &> /dev/null; then
    echo "[2/5] Configurando usuário Git..."
    read -p "Email: " GIT_EMAIL
    read -p "Nome: " GIT_NAME
    git config user.email "$GIT_EMAIL"
    git config user.name "$GIT_NAME"
    echo "✅ Usuário configurado"
else
    echo "[2/5] Usuário Git já configurado"
fi

echo ""

# Adicionar arquivos
echo "[3/5] Adicionando arquivos ao Git..."
git add .
echo "✅ Arquivos adicionados"

echo ""

# Commit
echo "[4/5] Criando commit inicial..."
git commit -m "🌌 Galaxy Bitcoin System v1.0 - Complete Implementation

🚀 Features:
- Sistema Bitcoin completo funcional
- Blockchain com Proof of Work real
- Reconhecimento facial com OpenCV
- APIs Bitcoin reais integradas
- Dashboard profissional moderno
- WebSocket para tempo real
- Sistema de carteiras completo
- Trading engine
- Criptografia AES-256-GCM
- Autenticação biométrica

📚 Documentação completa:
- README principal
- Guias de instalação
- Deployment em produção
- Git e GitHub
- Troubleshooting
- API Reference
- Arquitetura do sistema
- Exemplos de uso

🔒 Segurança:
- Assinaturas ECDSA
- Derivação de chaves PBKDF2
- Merkle Trees
- Validação de cadeia

✨ Setup:
- Instalação automática
- Validação automática
- Configuração Git automática
- Deploy simplificado

Made with ❤️ and Bitcoin" || true

echo "✅ Commit criado"

echo ""

# Configurar remote
echo "[5/5] Fazendo push para GitHub..."

if git remote | grep -q origin; then
    echo "Atualizando remote..."
    git remote set-url origin "$REPO_URL"
else
    echo "Adicionando remote..."
    git remote add origin "$REPO_URL"
fi

# Criar branch main se não existir
git branch -M main

# Push
git push -u origin main

echo ""
echo "=============================================================="
echo "✅ UPLOAD CONCLUÍDO COM SUCESSO!"
echo "=============================================================="
echo ""
echo "🌐 Acesse seu repositório:"
echo "   https://github.com/ManoAlee/Criptcoins"
echo ""
echo "📖 Documentação disponível em:"
echo "   - README.md"
echo "   - START_HERE.md"
echo "   - PROJECT_SUMMARY.md"
echo "   - DEPLOYMENT.md"
echo "   - GIT_GUIDE.md"
echo ""
echo "🎉 Parabéns! Seu repositório está online!"
echo ""
