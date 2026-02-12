# 📡 API REFERENCE - Galaxy Bitcoin System

## 🌐 REST API Endpoints

### Base URL
```
http://localhost:5000
```

### 🔑 Authentication
Atualmente não requer autenticação. Em produção, adicione JWT tokens.

---

## 📝 Endpoints

### 1️⃣ **Dashboard**

#### GET `/`
Retorna a página principal do dashboard.

**Resposta**: HTML (simple_index.html)

```bash
curl http://localhost:5000/
```

---

### 2️⃣ **Video Feed**

#### GET `/video_feed`
Stream de vídeo da câmera com detecção facial.

**Tipo**: Multipart MJPEG stream

```bash
# Em um navegador:
<img src="http://localhost:5000/video_feed">

# Ou via ffplay:
ffplay http://localhost:5000/video_feed
```

---

### 3️⃣ **Status & Info**

#### GET `/api/status`
Retorna o status completo do sistema.

**Resposta**:
```json
{
  "user": "Guest",
  "face_detected": false,
  "voice_command": "",
  "blockchain": {
    "blocks": 1,
    "pending_tx": 0,
    "difficulty": 2
  },
  "wallets": {
    "User": {
      "address": "abc123...",
      "balance": 100.0
    },
    "Miner": {
      "address": "def456...",
      "balance": 0.0
    }
  },
  "timestamp": "2024-01-15T10:30:00",
  "system_online": true
}
```

```bash
curl http://localhost:5000/api/status | jq
```

---

### 4️⃣ **Wallets**

#### GET `/api/wallets`
Lista todas as carteiras.

**Resposta**:
```json
{
  "User": {
    "name": "User",
    "address": "abc123...",
    "balance": 100.0
  },
  "Miner": {
    "name": "Miner",
    "address": "def456...",
    "balance": 50.0
  }
}
```

```bash
curl http://localhost:5000/api/wallets | jq
```

---

#### POST `/api/wallet/create`
Cria uma nova carteira.

**Request**:
```json
{
  "name": "Alice"
}
```

**Resposta**:
```json
{
  "success": true,
  "wallet": {
    "name": "Alice",
    "address": "xyz789...",
    "balance": 100.0
  }
}
```

```bash
curl -X POST http://localhost:5000/api/wallet/create \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice"}'
```

---

### 5️⃣ **Blockchain**

#### GET `/api/blockchain`
Informações da blockchain.

**Resposta**:
```json
{
  "total_blocks": 2,
  "recent_blocks": [
    {
      "index": 0,
      "timestamp": 1234567890,
      "transactions": 1,
      "hash": "0abc123...",
      "nonce": 9
    },
    {
      "index": 1,
      "timestamp": 1234567900,
      "transactions": 1,
      "hash": "def456...",
      "nonce": 2
    }
  ],
  "pending_tx": 0
}
```

```bash
curl http://localhost:5000/api/blockchain | jq
```

---

### 6️⃣ **Transações**

#### POST `/api/transaction`
Cria uma nova transação.

**Request**:
```json
{
  "sender": "User",
  "recipient": "Miner",
  "amount": 10.5
}
```

**Resposta**:
```json
{
  "success": true,
  "tx_hash": "abc123def456...",
  "message": "Transação criada: 10.5 BTC de User para Miner"
}
```

```bash
curl -X POST http://localhost:5000/api/transaction \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "User",
    "recipient": "Miner",
    "amount": 10.5
  }'
```

---

### 7️⃣ **Mining**

#### POST `/api/mine`
Inicia mineração de um novo bloco.

**Request**:
```json
{
  "miner": "Miner"
}
```

**Resposta**:
```json
{
  "success": true,
  "message": "Mineração iniciada por Miner"
}
```

```bash
curl -X POST http://localhost:5000/api/mine \
  -H "Content-Type: application/json" \
  -d '{"miner":"Miner"}'
```

---

### 8️⃣ **Bitcoin Data**

#### GET `/api/bitcoin/price`
Preço atual do Bitcoin de APIs reais.

**Resposta**:
```json
{
  "price_usd": 42500.00,
  "price_brl": 213500.00,
  "market_cap": 830000000000,
  "volume_24h": 25000000000,
  "change_24h": 2.5,
  "change_7d": 5.2,
  "change_30d": -3.1,
  "high_24h": 43000.00,
  "low_24h": 41500.00,
  "ath": 69000.00,
  "circulating_supply": 21000000
}
```

```bash
curl http://localhost:5000/api/bitcoin/price | jq
```

---

#### GET `/api/bitcoin/stats`
Estatísticas da blockchain Bitcoin real.

**Resposta**:
```json
{
  "hash_rate": 500000000,
  "difficulty": 32500000000,
  "total_btc": 21000000,
  "n_btc_mined": 21000000,
  "miners_revenue": 75000,
  "market_price": 42500,
  "total_transactions": 500000000,
  "blocks_size": 350000000,
  "avg_block_size": 1400
}
```

```bash
curl http://localhost:5000/api/bitcoin/stats | jq
```

---

### 9️⃣ **Camera**

#### GET `/api/camera/status`
Status da câmera.

**Resposta**:
```json
{
  "active": true,
  "face_detected": false,
  "current_user": "Guest"
}
```

```bash
curl http://localhost:5000/api/camera/status | jq
```

---

#### POST `/api/camera/user`
Define usuário para a câmera.

**Request**:
```json
{
  "user": "Alice"
}
```

**Resposta**:
```json
{
  "success": true,
  "user": "Alice"
}
```

```bash
curl -X POST http://localhost:5000/api/camera/user \
  -H "Content-Type: application/json" \
  -d '{"user":"Alice"}'
```

---

## 🔌 WebSocket Events

### Connection
```javascript
const socket = io('http://localhost:5000');

socket.on('connect', () => {
  console.log('Conectado ao servidor');
});
```

### Eventos Recebidos

#### `connected`
Quando o cliente se conecta.

```javascript
socket.on('connected', (data) => {
  console.log(data.message);
});
```

#### `price_update`
Atualização de preço Bitcoin em tempo real.

```javascript
socket.on('price_update', (data) => {
  console.log(`Preço: $${data.price}`);
  console.log(`Timestamp: ${data.timestamp}`);
});
```

#### `transaction_created`
Nova transação criada.

```javascript
socket.on('transaction_created', (data) => {
  console.log(`TX: ${data.amount} BTC`);
  console.log(`De: ${data.sender}`);
  console.log(`Para: ${data.recipient}`);
});
```

#### `block_mined`
Novo bloco minerado.

```javascript
socket.on('block_mined', (data) => {
  console.log(`Bloco #${data.block_number} minerado!`);
  console.log(`Minerador: ${data.miner}`);
  console.log(`Recompensa: ${data.reward} BTC`);
});
```

#### `status_update`
Atualização de status do sistema.

```javascript
socket.on('status_update', (data) => {
  console.log(`Blocos: ${data.blockchain.blocks}`);
  console.log(`Tx Pendentes: ${data.blockchain.pending_tx}`);
});
```

### Eventos Enviados

#### `request_update`
Solicitar atualização de status.

```javascript
socket.emit('request_update');
```

---

## 🛡️ Error Handling

### Erro de Transação
```bash
curl -X POST http://localhost:5000/api/transaction \
  -H "Content-Type: application/json" \
  -d '{"sender":"Invalid","recipient":"Miner","amount":10}'
```

**Resposta**:
```json
{
  "success": false,
  "message": "Falha ao criar transação (saldo insuficiente ou carteira inválida)"
}
```

**Status Code**: `400 Bad Request`

---

## 📊 Exemplo Completo (Python)

```python
import requests
import json

BASE_URL = "http://localhost:5000"

# 1. Criar carteira
response = requests.post(f"{BASE_URL}/api/wallet/create", 
    json={"name": "Alice"})
print(response.json())

# 2. Ver status
response = requests.get(f"{BASE_URL}/api/status")
print(json.dumps(response.json(), indent=2))

# 3. Criar transação
response = requests.post(f"{BASE_URL}/api/transaction",
    json={
        "sender": "User",
        "recipient": "Alice",
        "amount": 25.0
    })
print(response.json())

# 4. Minerar bloco
response = requests.post(f"{BASE_URL}/api/mine",
    json={"miner": "Miner"})
print(response.json())

# 5. Ver blockchain
response = requests.get(f"{BASE_URL}/api/blockchain")
print(json.dumps(response.json(), indent=2))

# 6. Preço Bitcoin
response = requests.get(f"{BASE_URL}/api/bitcoin/price")
print(json.dumps(response.json(), indent=2))
```

---

## 📊 Exemplo Completo (JavaScript)

```javascript
// Função auxiliar para requisições
async function apiCall(endpoint, method = 'GET', data = null) {
  const options = {
    method: method,
    headers: {'Content-Type': 'application/json'}
  };
  
  if (data) options.body = JSON.stringify(data);
  
  const response = await fetch(`/api${endpoint}`, options);
  return response.json();
}

// 1. Criar carteira
const wallet = await apiCall('/wallet/create', 'POST', {name: 'Bob'});
console.log(wallet);

// 2. Ver status
const status = await apiCall('/status');
console.log(status);

// 3. Criar transação
const tx = await apiCall('/transaction', 'POST', {
  sender: 'User',
  recipient: 'Bob',
  amount: 15.0
});
console.log(tx);

// 4. Minerar
const mine = await apiCall('/mine', 'POST', {miner: 'Miner'});
console.log(mine);

// 5. Ver blockchain
const blockchain = await apiCall('/blockchain');
console.log(blockchain);
```

---

## 🔗 Rate Limiting

Atualmente sem rate limiting. Em produção, adicione:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/status')
@limiter.limit("10 per minute")
def get_status():
    ...
```

---

## 🔐 Segurança

### CORS
Habilitado para `*` em desenvolvimento. Em produção:

```python
CORS(app, origins=['https://seu-dominio.com'])
```

### HTTPS
Em produção, sempre use HTTPS:

```python
ssl_context = ('cert.pem', 'key.pem')
socketio.run(app, ssl_context=ssl_context)
```

### Validação de Input
Todos os inputs são validados antes de processar.

---

## 📈 Status Codes

| Code | Significado |
|------|-------------|
| 200 | OK |
| 400 | Bad Request |
| 404 | Not Found |
| 500 | Server Error |

---

## 🚀 Deploy

Para deploy em produção:

```bash
gunicorn --worker-class eventlet -w 1 simple_app:app
```

---

**Made with ❤️ and Bitcoin**

API Version: 1.0.0
Last Updated: 2024
