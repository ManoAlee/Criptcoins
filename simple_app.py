#!/usr/bin/env python3
"""
Simple App - Front-end Profissional com Bitcoin Real
Sistema Bitcoin com Câmera Real, Voz e Dados de API
"""
from flask import Flask, render_template, Response, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import cv2
import threading
import time
import hashlib
from datetime import datetime
import numpy as np
import logging

# Importar APIs Bitcoin reais
try:
    from bitcoin_api import BitcoinAPI, TradingEngine
    HAS_BITCOIN_API = True
except:
    print("[⚠️] bitcoin_api.py não encontrado - usando modo simulado")
    HAS_BITCOIN_API = False

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sistema Bitcoin Simplificado Integrado
class SimpleWallet:
    def __init__(self, name: str):
        self.name = name
        self.address = hashlib.sha256(f"{name}{time.time()}".encode()).hexdigest()[:40]

class SimpleTransaction:
    def __init__(self, sender: str, recipient: str, amount: float):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()
        self.tx_hash = hashlib.sha256(f"{sender}{recipient}{amount}{self.timestamp}".encode()).hexdigest()

class SimpleBlock:
    def __init__(self, index: int, transactions: list, previous_hash: str):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = ""
    
    def calculate_hash(self):
        data = f"{self.index}{self.timestamp}{len(self.transactions)}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def mine_block(self, difficulty: int):
        target = '0' * difficulty
        logger.info(f"⛏️ Minerando bloco #{self.index}...")
        start = time.time()
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        elapsed = time.time() - start
        logger.info(f"✅ Bloco minerado! Tempo: {elapsed:.2f}s, Nonce: {self.nonce}")

class SimpleBlockchain:
    def __init__(self, difficulty: int = 2):
        self.chain = []
        self.difficulty = difficulty
        self.pending_transactions = []
        self.mining_reward = 50.0
        
        genesis = SimpleBlock(0, [], "0")
        genesis.mine_block(self.difficulty)
        self.chain.append(genesis)
    
    def add_transaction(self, transaction: SimpleTransaction):
        if transaction.sender != "SYSTEM":
            balance = self.get_balance(transaction.sender)
            if balance < transaction.amount:
                return False
        self.pending_transactions.append(transaction)
        return True
    
    def mine_pending_transactions(self, miner_address: str):
        block = SimpleBlock(len(self.chain), self.pending_transactions, self.chain[-1].hash)
        block.mine_block(self.difficulty)
        self.chain.append(block)
        
        reward = SimpleTransaction("SYSTEM", miner_address, self.mining_reward)
        self.pending_transactions = [reward]
    
    def get_balance(self, address: str) -> float:
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address:
                    balance -= tx.amount
                if tx.recipient == address:
                    balance += tx.amount
        for tx in self.pending_transactions:
            if tx.sender == address:
                balance -= tx.amount
            if tx.recipient == address:
                balance += tx.amount
        return balance

class SimpleBitcoinSystem:
    def __init__(self, difficulty: int = 2):
        self.blockchain = SimpleBlockchain(difficulty)
        self.system_wallets = {}
        
        # Inicializar API Bitcoin real se disponível
        if HAS_BITCOIN_API:
            self.bitcoin_api = BitcoinAPI()
            self.trading_engine = TradingEngine(self.bitcoin_api)
            self.real_btc_price = None
            
            # Iniciar WebSocket para preços em tempo real
            def price_callback(price, data):
                self.real_btc_price = price
                # Emitir via SocketIO se disponível
                if hasattr(self, 'socketio'):
                    self.socketio.emit('price_update', {
                        'price': price,
                        'timestamp': time.time()
                    })
            
            self.bitcoin_api.start_websocket(price_callback)
        else:
            self.bitcoin_api = None
            self.trading_engine = None
            self.real_btc_price = None
    
    def create_user_wallet(self, name: str):
        if name in self.system_wallets:
            return self.system_wallets[name]
        wallet = SimpleWallet(name)
        self.system_wallets[name] = wallet
        
        # Dar saldo inicial
        initial_tx = SimpleTransaction("SYSTEM", wallet.address, 100.0)
        self.blockchain.add_transaction(initial_tx)
        
        return wallet
    
    def create_validated_transaction(self, sender_name: str, recipient_name: str, amount: float):
        if sender_name not in self.system_wallets or recipient_name not in self.system_wallets:
            return None
        sender_wallet = self.system_wallets[sender_name]
        recipient_wallet = self.system_wallets[recipient_name]
        return SimpleTransaction(sender_wallet.address, recipient_wallet.address, amount)
    
    def mine_block_with_ai(self, miner_name: str):
        if miner_name not in self.system_wallets:
            return
        miner_wallet = self.system_wallets[miner_name]
        self.blockchain.mine_pending_transactions(miner_wallet.address)


# Inicializar Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = hashlib.sha256(str(time.time()).encode()).hexdigest()
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Sistema Global
bitcoin_system = SimpleBitcoinSystem(difficulty=2)
bitcoin_system.socketio = socketio
bitcoin_system.create_user_wallet('User')
bitcoin_system.create_user_wallet('Miner')
bitcoin_system.create_user_wallet('Trader')

# Estado da Câmera
camera = None
camera_lock = threading.Lock()
camera_active = False
current_user = "Guest"
face_detected = False
voice_command = ""

def get_camera():
    """Obtém câmera de forma segura com fallback"""
    global camera, camera_active
    
    if camera is not None and camera.isOpened():
        return camera
    
    # Tentar diferentes métodos de captura
    for backend in [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]:
        for device_id in range(3):  # Tentar 3 dispositivos
            try:
                cam = cv2.VideoCapture(device_id, backend)
                if cam.isOpened():
                    # Configurar câmera
                    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    cam.set(cv2.CAP_PROP_FPS, 30)
                    
                    # Testar leitura
                    ret, _ = cam.read()
                    if ret:
                        camera = cam
                        camera_active = True
                        logger.info(f"✅ Câmera {device_id} ativada com backend {backend}")
                        return camera
                cam.release()
            except Exception as e:
                logger.debug(f"Falha ao abrir câmera {device_id} com backend {backend}: {e}")
                continue
    
    camera_active = False
    logger.warning("⚠️ Nenhuma câmera disponível - usando modo placeholder")
    return None

def generate_frames():
    """Gera frames da câmera com detecção facial REAL"""
    global face_detected, camera_active
    
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    frame_count = 0
    last_camera_check = 0
    
    while True:
        try:
            with camera_lock:
                # Verificar câmera periodicamente
                current_time = time.time()
                if current_time - last_camera_check > 5:
                    cam = get_camera()
                    last_camera_check = current_time
                else:
                    cam = camera
                
                if cam is None or not cam.isOpened():
                    # Gerar placeholder profissional
                    frame = np.zeros((480, 640, 3), dtype=np.uint8)
                    
                    # Fundo gradiente
                    for i in range(480):
                        color = int(30 + (i / 480) * 30)
                        frame[i, :] = [color, color, color + 20]
                    
                    # Texto informativo
                    cv2.putText(frame, '📷 CAMERA OFFLINE', (180, 200),
                               cv2.FONT_HERSHEY_DUPLEX, 1, (255, 100, 100), 2)
                    cv2.putText(frame, 'Conectando...', (230, 280),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 1)
                    
                    # Ícone de câmera (retângulo estilizado)
                    cv2.rectangle(frame, (280, 320), (360, 380), (100, 100, 255), 2)
                    cv2.circle(frame, (320, 350), 15, (100, 100, 255), 2)
                    
                    face_detected = False
                    camera_active = False
                    
                    ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                    time.sleep(0.2)
                    continue
                
                # Câmera ativa - ler frame
                success, frame = cam.read()
                if not success:
                    continue
                
                frame_count += 1
                
                # Detectar face (otimizado - não em todo frame)
                if frame_count % 3 == 0:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                    
                    face_detected = len(faces) > 0
                    
                    # Desenhar retângulos e informações
                    for (x, y, w, h) in faces:
                        # Retângulo principal
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        
                        # Retângulos nos cantos (estilo futurista)
                        corner_len = 20
                        thickness = 3
                        color = (0, 255, 255)
                        
                        # Canto superior esquerdo
                        cv2.line(frame, (x, y), (x+corner_len, y), color, thickness)
                        cv2.line(frame, (x, y), (x, y+corner_len), color, thickness)
                        
                        # Canto superior direito
                        cv2.line(frame, (x+w, y), (x+w-corner_len, y), color, thickness)
                        cv2.line(frame, (x+w, y), (x+w, y+corner_len), color, thickness)
                        
                        # Canto inferior esquerdo
                        cv2.line(frame, (x, y+h), (x+corner_len, y+h), color, thickness)
                        cv2.line(frame, (x, y+h), (x, y+h-corner_len), color, thickness)
                        
                        # Canto inferior direito
                        cv2.line(frame, (x+w, y+h), (x+w-corner_len, y+h), color, thickness)
                        cv2.line(frame, (x+w, y+h), (x+w, y+h-corner_len), color, thickness)
                        
                        # Nome do usuário
                        cv2.putText(frame, f'👤 {current_user}', (x, y-10),
                                   cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 255), 2)
                
                # Overlay de informações
                height, width = frame.shape[:2]
                
                # Barra superior com info
                overlay = frame.copy()
                cv2.rectangle(overlay, (0, 0), (width, 70), (0, 0, 0), -1)
                cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
                
                # Textos informativos
                cv2.putText(frame, f'🌌 GALAXY BITCOIN SYSTEM', (10, 25),
                           cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
                cv2.putText(frame, f'User: {current_user}', (10, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
                
                # Status face
                face_status = f"✅ {len(faces)} face(s)" if face_detected else "❌ No face"
                cv2.putText(frame, face_status, (width - 150, 25),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0) if face_detected else (100, 100, 255), 1)
                
                # FPS
                cv2.putText(frame, f'FPS: 30', (width - 150, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
                
                # Codificar e enviar
                ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
                frame_bytes = buffer.tobytes()
                
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        except Exception as e:
            logger.error(f"Erro no generate_frames: {e}")
            time.sleep(0.1)
        
        time.sleep(0.033)  # ~30 FPS

@app.route('/')
def index():
    """Página principal"""
    return render_template('simple_index.html')

@app.route('/video_feed')
def video_feed():
    """Stream de vídeo"""
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/status')
def get_status():
    """Retorna status do sistema com dados reais"""
    chain = bitcoin_system.blockchain
    user_wallet = bitcoin_system.system_wallets.get('User')
    miner_wallet = bitcoin_system.system_wallets.get('Miner')
    
    return jsonify({
        'user': current_user,
        'face_detected': face_detected,
        'voice_command': voice_command,
        'blockchain': {
            'blocks': len(chain.chain),
            'pending_tx': len(chain.pending_transactions),
            'difficulty': chain.difficulty
        },
        'wallets': {
            'User': {
                'address': user_wallet.address if user_wallet else 'N/A',
                'balance': chain.get_balance(user_wallet.address) if user_wallet else 0
            },
            'Miner': {
                'address': miner_wallet.address if miner_wallet else 'N/A',
                'balance': chain.get_balance(miner_wallet.address) if miner_wallet else 0
            }
        },
        'timestamp': datetime.now().isoformat(),
        'system_online': True
    })

@app.route('/api/wallets')
def get_wallets():
    """Lista todas as carteiras"""
    wallets = {}
    for name, wallet in bitcoin_system.system_wallets.items():
        wallets[name] = {
            'name': name,
            'address': wallet.address,
            'balance': bitcoin_system.blockchain.get_balance(wallet.address)
        }
    
    return jsonify(wallets)

@app.route('/api/blockchain')
def get_blockchain():
    """Retorna informações da blockchain"""
    chain = bitcoin_system.blockchain
    blocks = []
    
    for block in chain.chain[-10:]:  # Últimos 10 blocos
        blocks.append({
            'index': block.index,
            'timestamp': block.timestamp,
            'transactions': len(block.transactions),
            'hash': block.hash[:16] + '...' if block.hash else 'Mining...',
            'nonce': block.nonce
        })
    
    return jsonify({
        'total_blocks': len(chain.chain),
        'recent_blocks': blocks,
        'pending_tx': len(chain.pending_transactions)
    })

@app.route('/api/bitcoin/price')
def get_bitcoin_price():
    """Obtém preço real do Bitcoin"""
    if HAS_BITCOIN_API and bitcoin_system.bitcoin_api:
        market_data = bitcoin_system.bitcoin_api.get_market_data()
        if market_data:
            return jsonify(market_data)
    
    return jsonify({'error': 'API não disponível', 'price_usd': 0})

@app.route('/api/bitcoin/stats')
def get_bitcoin_stats():
    """Obtém estatísticas da blockchain Bitcoin real"""
    if HAS_BITCOIN_API and bitcoin_system.bitcoin_api:
        stats = bitcoin_system.bitcoin_api.get_blockchain_stats()
        if stats:
            return jsonify(stats)
    
    return jsonify({'error': 'API não disponível'})

@app.route('/api/transaction', methods=['POST'])
def create_transaction():
    """Cria uma transação"""
    data = request.json
    sender = data.get('sender', 'User')
    recipient = data.get('recipient', 'Miner')
    amount = float(data.get('amount', 1.0))
    
    tx = bitcoin_system.create_validated_transaction(sender, recipient, amount)
    if tx:
        success = bitcoin_system.blockchain.add_transaction(tx)
        if success:
            # Emitir evento via WebSocket
            socketio.emit('transaction_created', {
                'tx_hash': tx.tx_hash,
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
                'timestamp': tx.timestamp
            })
            
            return jsonify({
                'success': True,
                'tx_hash': tx.tx_hash,
                'message': f'Transação criada: {amount} BTC de {sender} para {recipient}'
            })
    
    return jsonify({
        'success': False,
        'message': 'Falha ao criar transação (saldo insuficiente ou carteira inválida)'
    }), 400

@app.route('/api/mine', methods=['POST'])
def mine_block():
    """Minera um novo bloco"""
    data = request.json
    miner = data.get('miner', 'Miner')
    
    def mine_async():
        bitcoin_system.mine_block_with_ai(miner)
        
        # Emitir evento de bloco minerado
        socketio.emit('block_mined', {
            'block_number': len(bitcoin_system.blockchain.chain) - 1,
            'miner': miner,
            'reward': bitcoin_system.blockchain.mining_reward,
            'timestamp': time.time()
        })
    
    thread = threading.Thread(target=mine_async, daemon=True)
    thread.start()
    
    return jsonify({
        'success': True,
        'message': f'Mineração iniciada por {miner}'
    })

@app.route('/api/wallet/create', methods=['POST'])
def create_wallet():
    """Cria uma nova carteira"""
    data = request.json
    name = data.get('name', f'User{len(bitcoin_system.system_wallets)}')
    
    if name in bitcoin_system.system_wallets:
        return jsonify({
            'success': False,
            'message': 'Carteira já existe'
        }), 400
    
    wallet = bitcoin_system.create_user_wallet(name)
    
    return jsonify({
        'success': True,
        'wallet': {
            'name': name,
            'address': wallet.address,
            'balance': bitcoin_system.blockchain.get_balance(wallet.address)
        }
    })

@app.route('/api/camera/status')
def camera_status():
    """Status da câmera"""
    return jsonify({
        'active': camera_active,
        'face_detected': face_detected,
        'current_user': current_user
    })

@app.route('/api/camera/user', methods=['POST'])
def set_camera_user():
    """Define usuário da câmera"""
    global current_user
    data = request.json
    current_user = data.get('user', 'Guest')
    return jsonify({'success': True, 'user': current_user})


# WebSocket Events
@socketio.on('connect')
def handle_connect():
    """Cliente conectado"""
    logger.info('🔌 Cliente WebSocket conectado')
    emit('connected', {'message': 'Conectado ao Galaxy Bitcoin System'})

@socketio.on('disconnect')
def handle_disconnect():
    """Cliente desconectado"""
    logger.info('🔌 Cliente WebSocket desconectado')

@socketio.on('request_update')
def handle_request_update():
    """Cliente solicitou atualização"""
    emit('status_update', {
        'blockchain': {
            'blocks': len(bitcoin_system.blockchain.chain),
            'pending_tx': len(bitcoin_system.blockchain.pending_transactions)
        },
        'timestamp': time.time()
    })


def cleanup_camera():
    """Limpa recursos da câmera"""
    global camera
    if camera is not None:
        try:
            camera.release()
        except:
            pass
        camera = None

if __name__ == '__main__':
    try:
        logger.info("🌌 Iniciando Galaxy Bitcoin System...")
        logger.info("📡 Servidor: http://localhost:5000")
        logger.info("🎥 Câmera: Inicializando...")
        logger.info("⛓️ Blockchain: Ativo")
        
        if HAS_BITCOIN_API:
            logger.info("💹 API Bitcoin: Conectado")
        else:
            logger.info("💹 API Bitcoin: Modo simulado")
        
        # Iniciar servidor com SocketIO
        socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
    
    except KeyboardInterrupt:
        logger.info("\n👋 Encerrando sistema...")
        cleanup_camera()
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        cleanup_camera()
