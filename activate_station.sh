#!/bin/bash
# NEURO-HACKING STATION: AUTOMATIC ACTIVATION SCRIPT

echo "[*] Iniciando Gênese da Estação..."

# 1. Instalar ZSH e Oh-My-Zsh (Silencioso)
sudo apt update && sudo apt install -y zsh git curl
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
fi

# 2. Configurar Powerlevel10k
if [ ! -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k" ]; then
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
    sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="powerlevel10k\/powerlevel10k"/' ~/.zshrc
fi

# 3. Preparar Lab
mkdir -p ~/workspace
echo "[*] Infraestrutura pronta. Reinicie o terminal para ativar o link neural (ZSH)."
