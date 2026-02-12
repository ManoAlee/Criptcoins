# 🌌 Galaxy Bitcoin System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Bitcoin](https://img.shields.io/badge/Bitcoin-Ready-orange.svg)](https://bitcoin.org)
[![AI Powered](https://img.shields.io/badge/AI-Powered-green.svg)]()

## 🚀 Sistema Avançado de Trading Bitcoin com IA e Biometria

Sistema completo de negociação Bitcoin com:
- ✅ **Blockchain real** integrado
- 🎥 **Reconhecimento facial** para segurança
- 🎤 **Comandos de voz** para trading
- 📊 **Dashboard profissional** em tempo real
- 🔐 **Autenticação biométrica** multi-fator
- 💹 **Trading automatizado** com IA
- 🌐 **APIs REST e WebSocket**

---

## 🚀 Instalação Rápida

### Windows
```bash
git clone https://github.com/seu-usuario/galaxy-bitcoin-system.git
cd galaxy-bitcoin-system
install_and_run_windows.bat
```

### Linux/MacOS
```bash
git clone https://github.com/seu-usuario/galaxy-bitcoin-system.git
cd galaxy-bitcoin-system
chmod +x install_and_run_unix.sh
./install_and_run_unix.sh
```

### Manual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/MacOS
pip install -r requirements.txt
python quick_start.py
```

Sistema disponível em: `http://localhost:5000`

---

## ✨ Características

### 🔐 Segurança
- Autenticação biométrica facial
- Criptografia AES-256-GCM
- ECDSA (secp256k1)
- PBKDF2 com 200k iterações

### ⛓️ Blockchain
- Proof of Work completo
- Merkle Trees
- Transações assinadas
- Validação de cadeia

### 💹 Trading
- APIs Bitcoin reais
- WebSocket em tempo real
- Análise técnica
- Stop loss / Take profit

### 🎥 Visão Computacional
- Reconhecimento facial
- Detecção de vivacidade
- Análise topológica

### 🎤 Comandos de Voz
```
"Criar carteira Alice"
"Transferir 10 bitcoins de Alice para Bob"
"Minerar bloco"
"Mostrar saldo de Alice"
```

---

## 💻 Uso

### API REST
```python
# Criar transação
POST /api/transaction
{"sender": "Alice", "recipient": "Bob", "amount": 10.5}

# Minerar bloco
POST /api/mine
{"miner": "Alice"}

# Status
GET /api/status
```

### WebSocket
```javascript
const socket = io('http://localhost:5000');
socket.on('blockchain_update', (data) => console.log(data));
```

---

## 🏗️ Arquitetura

```
galaxy-bitcoin-system/
├── 🔐 Core Security
│   ├── bitcoin_crypto.py
│   ├── biometric_key.py
│   └── face_recog.py
├── ⛓️ Blockchain
│   ├── bitcoin_blockchain.py
│   └── bitcoin_p2p_network.py
├── 💹 Trading
│   ├── bitcoin_api.py
│   └── trading_engine.py
├── 🌐 Web
│   ├── simple_app.py
│   └── templates/
└── 🧠 AI
    ├── central_nervous_system.py
    └── topological_kernel.py
```

---

## 🧪 Testes

```bash
pytest                    # Todos os testes
python test_simple.py     # Teste simples
python health_check.py    # Health check
```

---

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/Feature`)
3. Commit (`git commit -m 'Add Feature'`)
4. Push (`git push origin feature/Feature`)
5. Abra Pull Request

---

## 📝 Licença

MIT License - veja [LICENSE](LICENSE)

---

## ⚖️ Disclaimer

Software educacional. Use por sua conta e risco. Não nos responsabilizamos por perdas.

---

**Made with ❤️ and Bitcoin**
