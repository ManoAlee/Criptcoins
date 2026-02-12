# ✅ CHECKLIST DE VALIDAÇÃO - Interface Minimalista

## 📋 Antes de Começar

- [ ] Python 3.8+ instalado
- [ ] Pip funcionando
- [ ] Porta 5000 disponível

## 🔧 Instalação

```bash
# Teste as dependências
python test_simple.py

# Se tudo OK, instale
pip install flask opencv-python SpeechRecognition pyaudio
```

## 🚀 Inicialização

### Método 1: Automático (Windows)
```bash
start_simple.bat
```

### Método 2: Manual
```bash
python simple_app.py
```

O navegador deve abrir automaticamente em: http://localhost:5000

## ✅ Validação das Funcionalidades

### 1. Interface Carrega?
- [ ] Página principal aparece
- [ ] Design gradiente roxo/azul visível
- [ ] Cards são exibidos corretamente
- [ ] Status mostra "Sistema Online"

### 2. Câmera Funciona?
- [ ] Stream de vídeo aparece
- [ ] Imagem está atualizada em tempo real
- [ ] Seu rosto é detectado com retângulo verde
- [ ] Nome do usuário aparece sobre o rosto
- [ ] Se câmera não disponível, mostra placeholder

### 3. Status do Sistema
- [ ] Número de blocos é exibido (mínimo: 1 - genesis)
- [ ] Dificuldade mostra "2"
- [ ] TX Pendentes é exibido
- [ ] Dados atualizam a cada 2 segundos

### 4. Carteiras
- [ ] Carteira "User" aparece
- [ ] Carteira "Miner" aparece
- [ ] Endereços são mostrados (truncados)
- [ ] Saldos são exibidos (inicialmente 0.0 BTC)

### 5. Criar Transação
- [ ] Campos de entrada funcionam
- [ ] Botão "Criar Transação" responde
- [ ] Se sem saldo: mostra erro vermelho
- [ ] Se com saldo: mostra sucesso verde
- [ ] Transação aparece como pendente

### 6. Mineração
- [ ] Campo "Nome do Minerador" aceita texto
- [ ] Botão "Minerar Novo Bloco" funciona
- [ ] Mostra mensagem "Minerando..."
- [ ] Após mineração: saldo do minerador aumenta 50 BTC
- [ ] Número de blocos incrementa

### 7. Blockchain
- [ ] Lista de blocos recentes aparece
- [ ] Cada bloco mostra:
  - [ ] Número do bloco
  - [ ] Hash truncado
  - [ ] Número de transações
  - [ ] Nonce
- [ ] Lista atualiza após mineração

### 8. Reconhecimento de Voz
- [ ] Botão "🎤 Capturar Comando de Voz" existe
- [ ] Ao clicar: mostra "Escutando..."
- [ ] Após falar: mostra o texto reconhecido
- [ ] Se erro: mostra mensagem de erro
- [ ] Suporta português brasileiro

## 🧪 Teste Completo - Passo a Passo

### Cenário 1: Primeira Mineração
1. [ ] Abra http://localhost:5000
2. [ ] Veja saldos: User = 0, Miner = 0
3. [ ] Clique "Minerar Novo Bloco"
4. [ ] Aguarde (5-30 segundos dependendo do PC)
5. [ ] Veja saldo do Miner aumentar para 50 BTC
6. [ ] Número de blocos deve ser 2 (genesis + novo)

### Cenário 2: Transação e Mineração
1. [ ] Com Miner tendo 50 BTC
2. [ ] Crie transação: Miner → User, 20 BTC
3. [ ] Veja "TX Pendentes" aumentar para 1
4. [ ] Mine outro bloco (pode ser User)
5. [ ] Após mineração:
   - [ ] User tem ~20 BTC
   - [ ] Miner tem ~30 BTC + recompensa
   - [ ] TX Pendentes volta para 0

### Cenário 3: Câmera e Detecção
1. [ ] Posicione-se na frente da câmera
2. [ ] Retângulo verde deve aparecer no seu rosto
3. [ ] Nome "Guest" deve aparecer
4. [ ] Contador "Faces: 1" deve estar visível

### Cenário 4: Voz
1. [ ] Clique no botão de voz
2. [ ] Fale claramente: "Olá sistema"
3. [ ] Texto reconhecido deve aparecer
4. [ ] Mensagem verde confirma sucesso

## 🐛 Problemas Comuns

### Câmera não aparece
- **Causa**: Outra aplicação usando câmera
- **Solução**: Feche Zoom, Skype, etc.
- **Fallback**: Sistema mostra placeholder automático

### Voz não funciona
- **Causa 1**: pyaudio não instalado
  ```bash
  pip install pyaudio
  ```
- **Causa 2**: Microfone não permitido
  - Vá em Configurações → Privacidade → Microfone
- **Causa 3**: Sem internet (Google Speech API)
  - Precisa de conexão para reconhecimento

### Transação falha
- **Causa**: Saldo insuficiente
- **Solução**: Mine blocos primeiro para ganhar BTC

### Mineração muito lenta
- **Causa**: Dificuldade alta para seu PC
- **Solução**: Edite `simple_app.py` linha 24:
  ```python
  bitcoin_system = SimpleBitcoinSystem(difficulty=1)  # Mude de 2 para 1
  ```

### Página não carrega
- **Causa 1**: Porta 5000 ocupada
  ```bash
  netstat -ano | findstr :5000
  taskkill /PID [numero] /F
  ```
- **Causa 2**: Erro no Python
  - Veja mensagens no terminal

## 📊 Métricas de Sucesso

### Mínimo Aceitável:
- ✅ Interface carrega
- ✅ Pelo menos 1 carteira visível
- ✅ Consegue minerar 1 bloco
- ✅ Blockchain tem 2+ blocos

### Funcionamento Completo:
- ✅ Câmera mostra vídeo
- ✅ Detecção facial funciona
- ✅ Transações são criadas
- ✅ Mineração gera recompensas
- ✅ Saldos atualizam corretamente
- ✅ Blockchain valida todos os blocos

### Excelência:
- ✅ Voz reconhece comandos
- ✅ Performance suave (sem travamentos)
- ✅ 3+ carteiras criadas
- ✅ 5+ blocos minerados
- ✅ 10+ transações processadas

## 🎯 Validação Final

Execute este teste completo:

```bash
python test_simple.py
```

Se todos os testes passarem e você conseguir:
1. ✅ Ver a interface
2. ✅ Minerar um bloco
3. ✅ Criar uma transação
4. ✅ Ver a câmera (ou placeholder)

**SISTEMA VALIDADO E FUNCIONAL!** 🎉

## 📞 Suporte

Se algo não funcionar:
1. Execute `python test_simple.py`
2. Leia `SOLUTION.md` para troubleshooting
3. Veja `SIMPLE_README.md` para documentação completa
4. Cheque logs no terminal onde rodou `simple_app.py`

---

**Última atualização:** Sistema validado e testado ✅
