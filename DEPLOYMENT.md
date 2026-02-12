# 🚀 DEPLOYMENT GUIDE - Galaxy Bitcoin System

## 📋 Pré-requisitos

### Sistema Operacional
- ✅ Windows 10/11
- ✅ Ubuntu 20.04+ / Debian 11+
- ✅ macOS 11+

### Software
- Python 3.8 ou superior
- Git (opcional, para versionamento)
- Webcam (opcional, para biometria)
- Microfone (opcional, para comandos de voz)

---

## ⚡ Quick Start (Recomendado)

### Windows
```bash
# 1. Download do projeto
git clone https://github.com/seu-usuario/galaxy-bitcoin-system.git
cd galaxy-bitcoin-system

# 2. Executar instalador automático
install_and_run_windows.bat
```

### Linux/macOS
```bash
# 1. Download do projeto
git clone https://github.com/seu-usuario/galaxy-bitcoin-system.git
cd galaxy-bitcoin-system

# 2. Dar permissões e executar
chmod +x install_and_run_unix.sh
./install_and_run_unix.sh
```

---

## 🔧 Instalação Manual

### 1. Criar Ambiente Virtual

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Validar Sistema

```bash
python validate_system.py
```

### 4. Iniciar Sistema

```bash
python quick_start.py
```

---

## 🌐 Configuração de Produção

### 1. Variáveis de Ambiente

Crie um arquivo `.env`:

```env
# Server
DEBUG=False
HOST=0.0.0.0
PORT=5000
SECRET_KEY=your-super-secret-key-here

# Bitcoin API
BITCOIN_API_ENABLED=True
BITCOIN_API_TIMEOUT=10

# Security
REQUIRE_BIOMETRIC_AUTH=True
ENCRYPTION_ALGORITHM=AES-256-GCM
```

### 2. HTTPS/SSL

Para produção, use HTTPS:

```bash
# Gerar certificado self-signed (desenvolvimento)
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

Modificar `simple_app.py`:

```python
if __name__ == '__main__':
    socketio.run(app, 
                host='0.0.0.0', 
                port=5000,
                ssl_context=('cert.pem', 'key.pem'))
```

### 3. Servidor de Produção (Gunicorn)

Instalar:
```bash
pip install gunicorn eventlet
```

Executar:
```bash
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 simple_app:app
```

### 4. Nginx Reverse Proxy

`/etc/nginx/sites-available/galaxy-bitcoin`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /socket.io {
        proxy_pass http://127.0.0.1:5000/socket.io;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Ativar:
```bash
sudo ln -s /etc/nginx/sites-available/galaxy-bitcoin /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🐳 Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    libopencv-dev \
    libportaudio2 \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Expor porta
EXPOSE 5000

# Comando de inicialização
CMD ["python", "simple_app.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  galaxy-bitcoin:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./face_db:/app/face_db
      - ./blockchain_data:/app/blockchain_data
    environment:
      - DEBUG=False
      - BITCOIN_API_ENABLED=True
    restart: unless-stopped
    devices:
      - /dev/video0:/dev/video0  # Câmera (Linux)
```

Executar:
```bash
docker-compose up -d
```

---

## 🔐 Segurança

### Checklist de Segurança

- [ ] **Alterar SECRET_KEY** em produção
- [ ] **Usar HTTPS/SSL** obrigatoriamente
- [ ] **Firewall configurado** (apenas porta 443/80)
- [ ] **Rate limiting** ativo
- [ ] **Backups automáticos** das chaves
- [ ] **Logs configurados** e monitorados
- [ ] **Atualizações** regulares
- [ ] **Senha forte** para servidor
- [ ] **2FA habilitado** no GitHub/servidor
- [ ] **Dados biométricos** criptografados

### Hardening

```bash
# Firewall (UFW - Ubuntu)
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Fail2ban (proteção contra brute force)
sudo apt-get install fail2ban
sudo systemctl enable fail2ban
```

---

## 📊 Monitoramento

### Logs

Configurar em `config.py`:

```python
LOG_LEVEL = 'INFO'
LOG_FILE = '/var/log/galaxy-bitcoin/app.log'
LOG_MAX_BYTES = 10485760  # 10MB
LOG_BACKUP_COUNT = 5
```

### Systemd Service (Linux)

`/etc/systemd/system/galaxy-bitcoin.service`:

```ini
[Unit]
Description=Galaxy Bitcoin System
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/galaxy-bitcoin-system
Environment="PATH=/opt/galaxy-bitcoin-system/venv/bin"
ExecStart=/opt/galaxy-bitcoin-system/venv/bin/python simple_app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Ativar:
```bash
sudo systemctl daemon-reload
sudo systemctl enable galaxy-bitcoin
sudo systemctl start galaxy-bitcoin
sudo systemctl status galaxy-bitcoin
```

---

## 🧪 Testes

### Testes Unitários
```bash
pytest tests/
```

### Testes de Integração
```bash
pytest tests/integration/
```

### Teste de Carga
```bash
pip install locust
locust -f tests/load_test.py
```

---

## 🚀 CI/CD

### GitHub Actions

`.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.10
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          python validate_system.py
      
      - name: Deploy to server
        run: |
          # Seu script de deploy aqui
          echo "Deploying..."
```

---

## 🔄 Backup e Restore

### Backup

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/galaxy-bitcoin"

mkdir -p $BACKUP_DIR

# Backup dos dados
tar -czf $BACKUP_DIR/data_$DATE.tar.gz \
    face_db/ \
    blockchain_data/ \
    wallets/ \
    *.json \
    *.enc

# Manter apenas últimos 30 dias
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "✅ Backup concluído: $BACKUP_DIR/data_$DATE.tar.gz"
```

Agendar com cron:
```bash
# Backup diário às 2h
0 2 * * * /opt/galaxy-bitcoin-system/backup.sh
```

### Restore

```bash
#!/bin/bash
# restore.sh
BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Uso: ./restore.sh <arquivo_backup.tar.gz>"
    exit 1
fi

tar -xzf $BACKUP_FILE
echo "✅ Restore concluído"
```

---

## 📈 Escalabilidade

### Load Balancer (Nginx)

```nginx
upstream galaxy_backend {
    least_conn;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}

server {
    listen 80;
    location / {
        proxy_pass http://galaxy_backend;
    }
}
```

### Redis para Cache

```python
# config.py
REDIS_URL = 'redis://localhost:6379/0'
CACHE_TYPE = 'redis'
```

---

## 🐛 Troubleshooting

### Problemas Comuns

#### Câmera não funciona
```bash
# Linux: verificar permissões
ls -l /dev/video0
sudo usermod -a -G video $USER
```

#### Porta já em uso
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux
lsof -ti:5000 | xargs kill -9
```

#### Dependências faltando
```bash
pip install -r requirements.txt --force-reinstall
```

---

## 📞 Suporte

- 📧 Email: support@galaxy-bitcoin.com
- 💬 Discord: https://discord.gg/galaxy-bitcoin
- 📖 Docs: https://docs.galaxy-bitcoin.com
- 🐛 Issues: https://github.com/user/galaxy-bitcoin-system/issues

---

## ✅ Checklist Final

- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas
- [ ] Validação executada com sucesso
- [ ] Configurações de produção aplicadas
- [ ] HTTPS configurado
- [ ] Firewall ativo
- [ ] Backups configurados
- [ ] Logs configurados
- [ ] Monitoramento ativo
- [ ] Documentação lida

---

**🌌 Galaxy Bitcoin System está pronto para produção!**
