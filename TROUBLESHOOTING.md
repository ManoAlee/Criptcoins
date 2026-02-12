# 🔧 Troubleshooting Guide - Galaxy Bitcoin System

## Problemas Comuns e Soluções

### 🐍 Python

#### Erro: Python version too old
```
[❌] Python 3.6 detectado
[!] Python 3.7+ é necessário
```

**Solução:**
```bash
# Windows
python --version
# Se < 3.7, baixe de python.org

# Linux
sudo apt update
sudo apt install python3.9

# Mac
brew install python@3.9
```

---

### 📦 Dependências

#### Erro: ModuleNotFoundError: No module named 'ecdsa'
```python
ModuleNotFoundError: No module named 'ecdsa'
```

**Solução:**
```bash
# Instalar todas as dependências
pip install -r requirements.txt

# Ou individual
pip install ecdsa base58 numpy matplotlib scipy networkx
```

#### Erro: pip não encontrado
```
'pip' is not recognized as an internal or external command
```

**Solução:**
```bash
# Use python -m pip
python -m pip install -r requirements.txt

# Ou instale pip
python -m ensurepip --upgrade
```

---

### 🔗 Blockchain

#### Erro: Mineração muito lenta
```
[⛏️] Minerando bloco #1 (dificuldade: 6)...
  Nonce: 10,000,000 | Hash: 00000abc...
  # Demora muito tempo
```

**Solução:**
```python
# Reduza a dificuldade
blockchain = BitcoinBlockchain(difficulty=3)  # Em vez de 6

# Ou use quick_demo.py para dificuldade 2
```

#### Erro: Blockchain inválida
```
[❌] Bloco #2: Hash inválido
```

**Solução:**
```python
# Verifique se está alterando blocos após mineração
# Blocos devem ser imutáveis após mineração

# Re-mine o bloco
block.mine_block(difficulty)
```

---

### 🔐 Criptografia

#### Erro: Invalid signature
```
[❌] Assinatura INVÁLIDA!
```

**Solução:**
```python
# Certifique-se de usar mesma chave pública
wallet = BitcoinWallet()
wallet.create_new_wallet()

message = "Test"
signature = wallet.sign_transaction(message)

# Use wallet.public_key, não outra chave
crypto.verify_signature(message, signature, wallet.public_key)
```

#### Erro: Address generation failed
```
TypeError: string argument without an encoding
```

**Solução:**
```python
# Certifique-se de usar bytes
public_key_bytes = bytes.fromhex(public_key_hex)
# Não: public_key_bytes = public_key_hex
```

---

### 🌐 Rede P2P

#### Erro: Port already in use
```
[❌] Erro ao iniciar servidor: [Errno 48] Address already in use
```

**Solução:**
```python
# Use porta diferente
node = P2PNode(port=9999)  # Em vez de 8333

# Ou mate processo usando a porta
# Windows
netstat -ano | findstr :8333
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8333
kill -9 <PID>
```

#### Erro: Connection refused
```
[❌] Erro ao conectar a localhost:8333: Connection refused
```

**Solução:**
```python
# Certifique-se de que servidor está rodando
node1 = P2PNode(port=8333)
node1.start_server()  # Deve rodar primeiro
time.sleep(1)  # Espere servidor iniciar

# Então conecte
node2.connect_to_peer('localhost', 8333)
```

---

### 🎨 Visualizações

#### Erro: matplotlib not showing plots
```
# Nada aparece na tela
```

**Solução:**
```python
# Adicione plt.show() no final
plt.savefig('output.png')
plt.show()  # Adicione isso

# Ou use modo não-interativo
import matplotlib
matplotlib.use('Agg')
```

#### Erro: networkx layouts fail
```
KeyError: 'node not found'
```

**Solução:**
```python
# Certifique-se de que grafo tem nós
if G.number_of_nodes() == 0:
    print("Grafo vazio!")
    return

pos = nx.spring_layout(G)
```

---

### 🧠 Neural Network

#### Erro: Matrix dimension mismatch
```
ValueError: shapes (20,10) and (5,1) not aligned
```

**Solução:**
```python
# Certifique-se de input_size correto
nn = NeuralNetwork(input_nodes=10, hidden_nodes=20, output_nodes=5)

# Input deve ter 10 elementos
input_data = np.random.rand(10)  # Correto
# input_data = np.random.rand(5)  # Errado!
```

---

### ✅ Validação

#### Erro: Entropy too low
```
[❌] Transação rejeitada: entropia insuficiente
```

**Solução:**
```python
# Use dados mais variados
# Não: tx_data = "AAA"
# Sim: tx_data = "Alice123Bob456"

# Ou desabilite validação de entropia (desenvolvimento)
# Comente a verificação no código
```

#### Erro: Turing test fails
```
[!!!] HIPÓTESE REJEITADA: 3 inconsistências detectadas.
```

**Solução:**
```python
# Verifique variáveis de teste
# Devem ser consistentes com hipótese

# Use menos variáveis para teste rápido
variables = [f"var_{i}" for i in range(5)]  # Em vez de 10
```

---

### 💾 Sistema Integrado

#### Erro: Wallet not found
```
[❌] Carteira não encontrada
```

**Solução:**
```python
system = GalaxyBitcoinSystem()

# Crie carteiras ANTES de usar
system.create_user_wallet("Alice")
system.create_user_wallet("Bob")

# Então use
tx = system.create_validated_transaction("Alice", "Bob", 10.0)
```

#### Erro: Insufficient balance
```
[❌] Saldo insuficiente: 0.00 BTC < 10.00 BTC
```

**Solução:**
```python
# Mine um bloco primeiro para Alice receber recompensa
system.mine_block_with_ai("Alice")

# Agora Alice tem saldo (50 BTC de recompensa)
tx = system.create_validated_transaction("Alice", "Bob", 10.0)
```

---

### 🖥️ Ambiente

#### Windows: UTF-8 encoding errors
```
UnicodeEncodeError: 'charmap' codec can't encode character
```

**Solução:**
```python
# Adicione no início do arquivo
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Ou use
print("✅", flush=True)  # Em vez de print("✅")
```

#### Linux: Permission denied
```
[Errno 13] Permission denied: 'wallet.json'
```

**Solução:**
```bash
# Dê permissão ao diretório
chmod 755 .
chmod 644 *.py

# Ou rode com sudo (não recomendado)
```

---

### 📊 Performance

#### Problema: Sistema muito lento

**Diagnóstico:**
```python
import time

start = time.time()
blockchain.mine_pending_transactions("Miner")
elapsed = time.time() - start
print(f"Tempo: {elapsed:.2f}s")
```

**Soluções:**

1. **Reduzir dificuldade**
```python
blockchain = BitcoinBlockchain(difficulty=3)  # Mais rápido
```

2. **Menos transações por bloco**
```python
# Adicione apenas 1-2 transações
blockchain.add_transaction(tx1)
# blockchain.add_transaction(tx2)  # Comente extras
```

3. **Desabilitar validações pesadas**
```python
# Em desenvolvimento, comente validações Turing
# system.validate_blockchain_integrity()
```

---

### 🔍 Debug

#### Modo debug

```python
# Adicione prints para debug
print(f"[DEBUG] Block hash: {block.hash}")
print(f"[DEBUG] Nonce: {block.nonce}")
print(f"[DEBUG] Difficulty: {self.difficulty}")

# Use logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"Mining block {block.index}")
```

#### Verificar estado

```python
# Blockchain
blockchain.print_chain()

# Wallet
wallet.print_wallet_info(show_private=True)

# Sistema
system.print_system_status()

# Rede
node.print_network_status()
```

---

### 🆘 Ajuda Adicional

#### Comandos úteis

```bash
# Verificar saúde do sistema
python health_check.py

# Executar testes
python install_and_test.py

# Ver exemplos
python api_examples.py

# Menu interativo
python launch.py
```

#### Logs

```python
# Salvar logs em arquivo
import sys
sys.stdout = open('output.log', 'w')

# Executar script
python galaxy_bitcoin_system.py

# Ver log
cat output.log  # Linux/Mac
type output.log  # Windows
```

---

### 📚 Recursos

- **Documentação**: `BITCOIN_README.md`
- **Guia rápido**: `QUICKSTART.md`
- **Changelog**: `CHANGELOG.md`
- **Exemplos**: `api_examples.py`

---

### ❓ FAQ

**Q: Posso usar em produção?**  
A: Não, é apenas educacional. Use bibliotecas estabelecidas para produção.

**Q: É seguro?**  
A: Usa criptografia real, mas não foi auditado. Não use para valores reais.

**Q: Quanto tempo demora para minerar?**  
A: Com difficulty=4, cerca de 2-10 segundos por bloco.

**Q: Posso mudar a dificuldade?**  
A: Sim: `BitcoinBlockchain(difficulty=3)` (mais fácil)

**Q: Funciona em Windows?**  
A: Sim, mas pode ter problemas com UTF-8. Veja soluções acima.

**Q: Precisa de internet?**  
A: Não, tudo roda localmente.

---

### 🐛 Reportar Bugs

Se encontrar um bug:

1. Verifique este troubleshooting
2. Execute `python health_check.py`
3. Execute `python install_and_test.py`
4. Veja logs/stack trace completo
5. Teste com exemplo mínimo

---

**Última atualização**: 2024  
**Versão**: 4.0.0

🌌 *"Debug is a journey, not a destination"* 🌌
