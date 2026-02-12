# 🌐 GIT SETUP & GITHUB GUIDE

## 🚀 Como Subir o Projeto no GitHub

### Método 1: Automático (Recomendado)

#### Windows
```bash
# Execute o script automático
setup_git.bat
```

#### Linux/macOS
```bash
# Dê permissões e execute
chmod +x setup_git.sh
./setup_git.sh
```

O script irá:
1. ✅ Inicializar repositório Git
2. ✅ Adicionar todos os arquivos
3. ✅ Criar commit inicial
4. ✅ Conectar com GitHub
5. ✅ Fazer push

---

### Método 2: Manual

#### 1. Criar Repositório no GitHub

1. Acesse https://github.com
2. Clique em **"New Repository"**
3. Nome: `galaxy-bitcoin-system`
4. Descrição: `🌌 Advanced Bitcoin Trading Platform with AI & Biometric Security`
5. **Não** inicialize com README
6. Clique em **"Create Repository"**

#### 2. Configurar Git Local

```bash
# Inicializar repositório
git init

# Configurar usuário (primeira vez)
git config --global user.name "Seu Nome"
git config --global user.email "seu-email@example.com"

# Adicionar todos os arquivos
git add .

# Criar commit inicial
git commit -m "🌌 Initial commit: Galaxy Bitcoin System v1.0

- Complete Bitcoin trading system
- Biometric authentication
- Real-time face recognition
- Real Bitcoin APIs integrated
- Professional dashboard
- WebSocket real-time data
- Functional blockchain with PoW
- Voice commands
- Wallet system
- Trading engine"

# Conectar com GitHub
git remote add origin https://github.com/SEU-USUARIO/galaxy-bitcoin-system.git

# Criar branch main
git branch -M main

# Push inicial
git push -u origin main
```

---

## 📝 Comandos Git Essenciais

### Operações Básicas

```bash
# Ver status
git status

# Adicionar arquivos
git add .                    # Todos
git add arquivo.py          # Específico
git add *.py                # Por extensão

# Commit
git commit -m "Mensagem"

# Push (enviar para GitHub)
git push

# Pull (baixar do GitHub)
git pull

# Ver histórico
git log --oneline --graph
```

### Branches

```bash
# Criar nova branch
git checkout -b feature/nova-funcionalidade

# Trocar de branch
git checkout main

# Listar branches
git branch -a

# Deletar branch
git branch -d nome-branch

# Merge
git checkout main
git merge feature/nova-funcionalidade
```

### Desfazer Mudanças

```bash
# Descartar mudanças locais
git checkout -- arquivo.py

# Desfazer último commit (mantém mudanças)
git reset --soft HEAD~1

# Desfazer último commit (descarta mudanças)
git reset --hard HEAD~1

# Reverter commit específico
git revert <commit-hash>
```

---

## 🔐 Autenticação GitHub

### SSH (Recomendado)

```bash
# Gerar chave SSH
ssh-keygen -t ed25519 -C "seu-email@example.com"

# Copiar chave pública
# Windows
type %USERPROFILE%\.ssh\id_ed25519.pub | clip

# Linux/macOS
cat ~/.ssh/id_ed25519.pub | xclip -selection clipboard

# Adicionar no GitHub:
# Settings > SSH and GPG keys > New SSH key
```

Mudar URL para SSH:
```bash
git remote set-url origin git@github.com:SEU-USUARIO/galaxy-bitcoin-system.git
```

### Personal Access Token

1. GitHub Settings > Developer settings > Personal access tokens
2. Generate new token (classic)
3. Selecione: `repo`, `workflow`
4. Copie o token

Configurar:
```bash
# Windows
git config --global credential.helper wincred

# Linux/macOS
git config --global credential.helper cache

# Usar token como senha no próximo push
```

---

## 📋 .gitignore Essencial

O arquivo `.gitignore` já está configurado, mas importante verificar:

```gitignore
# Nunca commit isso!
.env
*.key
*.pem
secrets.json
api_keys.txt

# Dados sensíveis
face_db/
blockchain_data/
wallets/
*.enc
*.npz

# Ambiente
venv/
__pycache__/
*.pyc
```

---

## 🏷️ Tags e Releases

### Criar Tag

```bash
# Tag simples
git tag v1.0.0

# Tag anotada (recomendado)
git tag -a v1.0.0 -m "Release 1.0.0 - Initial Release"

# Push tag
git push origin v1.0.0

# Push todas as tags
git push origin --tags
```

### Criar Release no GitHub

1. Vá para o repositório no GitHub
2. Clique em **"Releases"** > **"Create a new release"**
3. Tag: `v1.0.0`
4. Title: `Galaxy Bitcoin System v1.0.0`
5. Descrição:
```markdown
## 🌌 Galaxy Bitcoin System v1.0.0

### ✨ Features
- ✅ Complete Bitcoin trading platform
- ✅ Biometric authentication
- ✅ Real-time face recognition
- ✅ Real Bitcoin APIs
- ✅ Professional dashboard
- ✅ WebSocket live data
- ✅ Blockchain with PoW
- ✅ Voice commands

### 📦 Installation
\`\`\`bash
git clone https://github.com/SEU-USUARIO/galaxy-bitcoin-system.git
cd galaxy-bitcoin-system
pip install -r requirements.txt
python quick_start.py
\`\`\`

### 📖 Full Changelog
- Initial release
```

---

## 🔄 Workflow Recomendado

### 1. Desenvolvimento Local

```bash
# Criar branch para feature
git checkout -b feature/nova-funcionalidade

# Fazer mudanças
# ... código ...

# Commit
git add .
git commit -m "✨ Add nova funcionalidade"

# Push
git push origin feature/nova-funcionalidade
```

### 2. Pull Request

1. Vá para GitHub
2. Clique em **"Compare & pull request"**
3. Preencha descrição
4. Clique em **"Create pull request"**

### 3. Review e Merge

1. Revisar código
2. Aprovar
3. **"Merge pull request"**
4. Deletar branch

### 4. Atualizar Main Local

```bash
git checkout main
git pull origin main
git branch -d feature/nova-funcionalidade
```

---

## 📊 Configurações Avançadas

### GitHub Actions (CI/CD)

O arquivo `.github/workflows/ci.yml` já está configurado para:
- ✅ Executar testes
- ✅ Verificar código
- ✅ Deploy automático

### Badges no README

Adicione ao `README.md`:

```markdown
![Build Status](https://img.shields.io/github/actions/workflow/status/SEU-USUARIO/galaxy-bitcoin-system/ci.yml?branch=main)
![Stars](https://img.shields.io/github/stars/SEU-USUARIO/galaxy-bitcoin-system)
![Forks](https://img.shields.io/github/forks/SEU-USUARIO/galaxy-bitcoin-system)
![Issues](https://img.shields.io/github/issues/SEU-USUARIO/galaxy-bitcoin-system)
![License](https://img.shields.io/github/license/SEU-USUARIO/galaxy-bitcoin-system)
```

### GitHub Pages (Documentação)

```bash
# Criar branch gh-pages
git checkout --orphan gh-pages
git rm -rf .
echo "# Galaxy Bitcoin System Docs" > index.md
git add index.md
git commit -m "Initial docs"
git push origin gh-pages

# Configurar no GitHub:
# Settings > Pages > Source: gh-pages
```

---

## 🐛 Troubleshooting Git

### Erro: "Permission denied (publickey)"

```bash
# Verificar chave SSH
ssh -T git@github.com

# Se falhar, adicionar chave:
ssh-add ~/.ssh/id_ed25519
```

### Erro: "fatal: not a git repository"

```bash
# Inicializar repositório
git init
```

### Erro: "Updates were rejected"

```bash
# Pull primeiro
git pull origin main --rebase

# Depois push
git push origin main
```

### Conflitos de Merge

```bash
# Ver conflitos
git status

# Resolver manualmente nos arquivos
# Depois:
git add .
git commit -m "Resolve conflicts"
git push
```

---

## 📚 Recursos

### Documentação
- [Git Book](https://git-scm.com/book/pt-br/v2)
- [GitHub Docs](https://docs.github.com)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

### Tutoriais
- [Learn Git Branching](https://learngitbranching.js.org/?locale=pt_BR)
- [Git Tutorial - Atlassian](https://www.atlassian.com/git/tutorials)

### Ferramentas
- [GitHub Desktop](https://desktop.github.com/)
- [GitKraken](https://www.gitkraken.com/)
- [SourceTree](https://www.sourcetreeapp.com/)

---

## ✅ Checklist Git

- [ ] Git instalado
- [ ] Usuário configurado
- [ ] Repositório GitHub criado
- [ ] Repositório local inicializado
- [ ] Remote configurado
- [ ] `.gitignore` configurado
- [ ] Commit inicial feito
- [ ] Push para GitHub
- [ ] README atualizado
- [ ] License adicionada

---

**🌐 Seu projeto está pronto para o GitHub!**

Repository: `https://github.com/SEU-USUARIO/galaxy-bitcoin-system`
