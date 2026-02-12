#!/bin/bash
# 🌌 Galaxy Bitcoin System - Unix Installer & Launcher

echo "=================================================="
echo "🌌 GALAXY BITCOIN SYSTEM - Unix Installer"
echo "=================================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8+"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Criando ambiente virtual..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Atualizando pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Instalando dependências..."
pip install -r requirements.txt

echo ""
echo "=================================================="
echo "✅ Instalação concluída!"
echo "=================================================="
echo ""
echo "🚀 Iniciando Galaxy Bitcoin System..."
echo ""

# Run the application
python3 quick_start.py

# Deactivate on exit
deactivate
