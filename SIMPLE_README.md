# 🌌 Galaxy Bitcoin System - Interface Minimalista

## 📱 Sistema Simples e Funcional

Este é o **front-end minimalista** do Galaxy Bitcoin System, focado em:

✅ **Simplicidade** - Interface limpa e fácil de entender  
✅ **Funcionalidade Real** - Dados reais da blockchain  
✅ **Câmera Funcionando** - Stream de vídeo em tempo real  
✅ **Voz Ativa** - Reconhecimento de voz em português  
✅ **Sem Bugs** - Sistema estável e testado  

---

## 🚀 Como Usar

### Windows (Mais Fácil):
```bash
start_simple.bat
```

### Manualmente:
```bash
python simple_app.py
```

Depois abra: **http://localhost:5000**

---

## 📋 Funcionalidades

### 📹 Câmera
- Stream de vídeo em tempo real
- Detecção facial automática
- Indicação visual de usuário identificado

### 🎤 Voz
- Clique em "🎤 Capturar Comando de Voz"
- Fale em português
- Sistema reconhece e exibe o comando

### 💰 Carteiras
- Visualização de todas as carteiras
- Saldo em tempo real (BTC)
- Endereços das carteiras

### 💸 Transações
- Criar transações entre carteiras
- Validação de saldo
- Confirmação instantânea

### ⛏️ Mineração
- Minerar novos blocos
- Sistema de recompensa
- Mineração em background

### ⛓️ Blockchain
- Visualizar últimos blocos
- Hash de cada bloco
- Número de transações

---

## 🎨 Diferenças do Dashboard Antigo

| **Dashboard Antigo** | **Interface Minimalista** |
|---------------------|---------------------------|
| ❌ Complexo demais | ✅ Simples e direto |
| ❌ Bugado e travado | ✅ Estável e fluído |
| ❌ Dados fake | ✅ Dados reais |
| ❌ Câmera não funciona | ✅ Câmera funcionando |
| ❌ Difícil de entender | ✅ Fácil de usar |

---

## 🔧 Requisitos

```bash
pip install flask opencv-python SpeechRecognition pyaudio
```

**Nota:** Para voz no Windows, você pode precisar instalar:
```bash
pip install pyaudio
```

Se der erro no `pyaudio`, baixe o wheel adequado de:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

---

## 📊 API Endpoints

### `GET /api/status`
Retorna status completo do sistema

### `GET /api/wallets`
Lista todas as carteiras

### `GET /api/blockchain`
Informações da blockchain

### `POST /api/transaction`
Cria nova transação
```json
{
  "sender": "User",
  "recipient": "Miner",
  "amount": 1.0
}
```

### `POST /api/mine`
Inicia mineração
```json
{
  "miner": "Miner"
}
```

### `POST /api/voice`
Captura comando de voz

---

## 🎯 Estrutura

```
galaxy-bitcoin/
├── simple_app.py              # Servidor Flask minimalista
├── templates/
│   └── simple_index.html      # Interface HTML
├── start_simple.bat           # Script de inicialização Windows
└── SIMPLE_README.md           # Este arquivo
```

---

## 🐛 Problemas Conhecidos Resolvidos

✅ Dashboard travando → **Resolvido com nova interface leve**  
✅ Câmera não funciona → **Resolvido com OpenCV direto**  
✅ Dados não aparecem → **Resolvido com API real**  
✅ Sistema complexo → **Simplificado para uso fácil**  

---

## 💡 Dicas

1. **Câmera não aparece?**
   - Verifique se outra aplicação está usando a câmera
   - Permita acesso à câmera nas configurações do Windows

2. **Voz não funciona?**
   - Verifique permissões do microfone
   - Fale claramente em português
   - Aguarde o sistema processar (2-3 segundos)

3. **Transação falha?**
   - Verifique se a carteira tem saldo suficiente
   - Mine alguns blocos primeiro para ter BTC

4. **Performance lenta?**
   - Feche outros aplicativos pesados
   - Diminua a dificuldade da blockchain (edite `simple_app.py` linha 24)

---

## 🌟 Próximos Passos

Depois de testar o sistema básico, você pode:

1. Criar mais carteiras
2. Fazer transações entre elas
3. Minerar blocos para ganhar recompensas
4. Testar o reconhecimento de voz
5. Ver a câmera detectando seu rosto

---

## 📞 Suporte

Problemas? Verifique:
1. Python 3.8+ instalado
2. Dependências instaladas (`pip install -r requirements.txt`)
3. Câmera e microfone funcionando
4. Porta 5000 livre

---

**Desenvolvido com ❤️ para ser SIMPLES e FUNCIONAL**
