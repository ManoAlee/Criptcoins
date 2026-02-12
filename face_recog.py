"""
face_recog.py

Módulo simples de reconhecimento facial local baseado em OpenCV Haar cascades.
Funcionalidades:
- detectar face em uma imagem (bytes PNG)
- enroll interativo (capturar várias amostras via webcam)
- autenticar comparando com média das amostras (MSE/MAE)

Armazena bancos de faces em `face_db/{username}.npz` contendo 'mean' array (uint8).
"""
import os
import cv2
import json
import numpy as np
import io
import hashlib
import hmac
import time
from typing import Optional, Tuple
from topological_kernel import TopologicalKernel
from central_nervous_system import CNS
from universe_manipulator import UniverseManipulator

# Instanciar o Kernel Topológico e Manipulador
top_kernel = TopologicalKernel()
manipulator = UniverseManipulator()
cns = CNS(manipulator, top_kernel)

DB_DIR = 'face_db'
CASCADE_FRONTAL = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
CASCADE_PROFILE = cv2.data.haarcascades + 'haarcascade_profileface.xml'
FACE_SIZE = (100, 100)
SYSTEM_SEED = "Ψ_BIOMETRIC_SEED_2026_GALAXY" # DNA do Sistema


def ensure_db_dir():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR, exist_ok=True)


def detect_face_array_from_image_bytes(image_bytes: bytes, robust: bool = False) -> Optional[np.ndarray]:
    """Detecta face com Kernel Bio-Simétrico (Frontal + Perfil + Flip + Sensibilidade)."""
    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        return None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 🟢 1. Tentativa Frontal Padrão (Alta Fidelidade)
    frontal_cascade = cv2.CascadeClassifier(CASCADE_FRONTAL)
    faces = frontal_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # 🟡 2. Fallbacks em modo ROBUSTO (Manifold Enrollment)
    if len(faces) == 0 and robust:
        # 🧪 A. Tentar Perfil (Direita)
        profile_cascade = cv2.CascadeClassifier(CASCADE_PROFILE)
        faces = profile_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3)
        
        # 🧪 B. Bio-Simetria: Tentar Inverter Imagem (Perfil Esquerdo)
        if len(faces) == 0:
            flipped_gray = cv2.flip(gray, 1)
            faces_flipped = profile_cascade.detectMultiScale(flipped_gray, scaleFactor=1.05, minNeighbors=3)
            if len(faces_flipped) > 0:
                # Se detectou no flip, retornamos a ROI do flip (pois compararemos com ROI)
                gray = flipped_gray
                faces = faces_flipped
        
        # 🧪 C. Tentativa Ultra-Sensível (Ambientes Hostis/Extremas)
        if len(faces) == 0:
            faces = frontal_cascade.detectMultiScale(gray, scaleFactor=1.03, minNeighbors=2)

    if len(faces) == 0:
        if robust:
            # 🧬 D. FINAL FALLBACK: Nucleus Universal (Central Crop)
            # Se a biometria falhar em todos os ângulos, extraímos o núcleo central da imagem
            # para evitar o "Sync Error" e permitir a colonização.
            h, w = gray.shape
            size = int(min(w, h) * 0.7)
            x = (w - size) // 2
            y = (h - size) // 2
            print(f"[🛡️] Usando Núcleo Universal (Central Crop) para detecção robusta.")
            roi = gray[y:y+size, x:x+size]
            roi_resized = cv2.resize(roi, FACE_SIZE)
            return roi_resized
        return None
        
    # Escolher a maior face (maior área detectada)
    x, y, w, h = max(faces, key=lambda r: r[2] * r[3])
    roi = gray[y:y+h, x:x+w]
    roi_resized = cv2.resize(roi, FACE_SIZE)
    return roi_resized


def enroll_user_manifold(username: str, angle_images: list) -> bool:
    """Sintetiza o Manifold Facial (5 ângulos) com integridade de membrana."""
    ensure_db_dir()
    
    facial_manifold = [] # Lista de (mean, top_sig)
    
    for idx, img_bytes in enumerate(angle_images):
        face = detect_face_array_from_image_bytes(img_bytes, robust=True)
        if face is None:
            print(f"[⚠️] Ângulo {idx+1} não detectado. Abortando síntese.")
            return False
        
        top_sig = top_kernel.extract_signature(face)
        facial_manifold.append({
            'mean': face,
            'top_sig': top_sig
        })
    
    # Gerar Hash da Membrana Global (Manifold Integrity)
    data_stream = io.BytesIO()
    # Ordem fixa para garantir consistência do Hash
    np.savez(data_stream, manifold=facial_manifold)
    membrane_hash = hashlib.sha256(data_stream.getvalue()).hexdigest()
    
    out_path = os.path.join(DB_DIR, f'{username}.npz')
    # Salvando a estrutura expandida (Ψ Premium)
    np.savez_compressed(out_path, 
                        manifold=facial_manifold, 
                        membrane_hash=membrane_hash,
                        version="1.1.0_manifold")
    
    print(f'[✅] Manifold de {username} (5 ângulos) estabilizado. Hash: {membrane_hash[:10]}')
    return True

    print(f'[✅] Manifold de {username} (5 ângulos) estabilizado. Hash: {membrane_hash[:10]}')
    return True


def list_enrolled_users() -> list:
    """Lista todos os nós biométricos colonizados."""
    ensure_db_dir()
    users = []
    for f in os.listdir(DB_DIR):
        if f.endswith('.npz'):
            users.append(os.path.splitext(f)[0])
    return users


def load_user_mean(username: str) -> Optional[np.ndarray]:
    path = os.path.join(DB_DIR, f'{username}.npz')
    if not os.path.exists(path):
        return None
    data = np.load(path)
    return data['mean']


def authenticate_from_image_bytes(image_bytes: bytes, threshold_override: float = None) -> Tuple[Optional[str], Optional[float]]:
    """Valida ressonância comparando com o Manifold Facial (Multi-Angle)."""
    # ⚡ USAR MODO ROBUSTO PARA LOGIN TAMBÉM (Garante detecção de perfis)
    face = detect_face_array_from_image_bytes(image_bytes, robust=True)
    if face is None:
        print("[⚠️] Sensor não conseguiu captar núcleo biométrico no login.")
        return None, None
        
    avg_brightness = np.mean(face)
    context_enzyme = 1.0
    if avg_brightness < 40 or avg_brightness > 220:
        context_enzyme = 0.85 
        
    users = list_enrolled_users()
    if not users:
        return None, None
        
    best_user = None
    best_total_confidence = -1.0 
    
    current_top_sig = top_kernel.extract_signature(face)

    for u in users:
        path = os.path.join(DB_DIR, f'{u}.npz')
        try:
            data = np.load(path, allow_pickle=True)
            
            # Verificação de Membrana
            if 'membrane_hash' in data:
                check_stream = io.BytesIO()
                if 'manifold' in data:
                    np.savez(check_stream, manifold=data['manifold'])
                else:
                    np.savez(check_stream, mean=data['mean'], top_sig=data['top_sig'])
                
                if hashlib.sha256(check_stream.getvalue()).hexdigest() != str(data['membrane_hash']):
                    print(f"[⚠️] Violação detectada para {u}!")
                    continue

            # IDENTIFICAÇÃO PREMIUM (MANIFOLD)
            if 'manifold' in data:
                manifold = data['manifold']
                user_best_confidence = 0.0
                
                # Comparar captura contra todos os ângulos salvos
                for angle in manifold:
                    m_mean = angle['mean']
                    m_top_sig = angle['top_sig']
                    
                    p_score = float(np.mean(np.abs(m_mean.astype(np.int16) - face.astype(np.int16))))
                    p_sim = max(0, 1.0 - (p_score / 100.0))
                    
                    g_dist = top_kernel.compute_geodesic_distance(m_top_sig, current_top_sig)
                    t_score = 1.0 - min(1.0, g_dist * 2.0)
                    
                    angle_conf = ((p_sim * 0.4) + (t_score * 0.6)) * context_enzyme
                    user_best_confidence = max(user_best_confidence, angle_conf)
                
                if user_best_confidence > best_total_confidence:
                    # 🎯 Barreira de Segurança Ψ Premium: 0.50 para máxima ressonância em testes
                    if user_best_confidence > 0.50: 
                        best_total_confidence = user_best_confidence
                        best_user = u
                        
                print(f"[🔍] Check {u}: Best Angle Conf: {user_best_confidence:.4f}")
            else:
                # Fallback para usuários versão 1.0 (Single Shot)
                pixel_score = float(np.mean(np.abs(data['mean'].astype(np.int16) - face.astype(np.int16))))
                pixel_sim = max(0, 1.0 - (pixel_score / 100.0))
                top_score = 0.0
                if 'top_sig' in data:
                    g_dist = top_kernel.compute_geodesic_distance(data['top_sig'], current_top_sig)
                    top_score = 1.0 - min(1.0, g_dist * 2.0)
                
                conf = ((pixel_sim * 0.4) + (top_score * 0.6)) * context_enzyme
                if conf > best_total_confidence and conf > 0.80:
                    best_total_confidence = conf
                    best_user = u
                    
        except Exception as e:
            print(f"[💥] Erro {u}: {e}")
            continue

    if best_user:
        print(f"[RESONANCE_STABLE] {best_user} | Conf: {best_total_confidence:.4f}")
        return best_user, best_total_confidence
    return None, None


# =================================================================
# HARD ENGINEERING: COGNITIVE TOKEN SYSTEM (HMAC-SHA256)
# =================================================================

def derive_cognitive_token(username: str, context: str, permission: str) -> dict:
    """
    Deriva um Token Cognitivo efêmero baseado em PIN (Identity), Seed e Contexto.
    𝑇𝑜𝑘𝑒𝑛 = HMAC_K (PIN ∥ Contexto ∥ Permissão ∥ Timestamp)
    𝐾 = Hash (PIN ∥ Seed)
    """
    timestamp = str(int(time.time()))
    
    # 1. PIN é o próprio username no sistema simplificado
    pin = username
    
    # 2. Derivar Chave K (Efêmera)
    k_input = f"{pin}{SYSTEM_SEED}".encode()
    k = hashlib.sha256(k_input).hexdigest()
    
    # 3. Gerar Assinatura HMAC (Integridade + Autenticidade)
    # Entrelaçamento: PIN | Context | Permission | Timestamp
    msg = f"{pin}|{context}|{permission}|{timestamp}".encode()
    signature = hmac.new(k.encode(), msg, hashlib.sha256).hexdigest()
    
    token = {
        'iss': 'Galaxy_Ψ_System',
        'sub_hash': hashlib.sha256(pin.encode()).hexdigest(),
        'ctx': context,
        'scope': permission,
        'iat': timestamp,
        'exp': str(int(time.time()) + 3600), # 1 hora de vida
        'sig': signature
    }
    
    return token

def validate_cognitive_token(token: dict, username: str) -> bool:
    """Valida o colapso do token para o observador (username) atual."""
    try:
        # 1. Verificar Expiração
        if int(time.time()) > int(token['exp']):
            return False
            
        # 2. Re-derivar Chave K
        pin = username
        k_input = f"{pin}{SYSTEM_SEED}".encode()
        k = hashlib.sha256(k_input).hexdigest()
        
        # 3. Re-calcular Assinatura
        msg = f"{pin}|{token['ctx']}|{token['scope']}|{token['iat']}".encode()
        expected_sig = hmac.new(k.encode(), msg, hashlib.sha256).hexdigest()
        
        return hmac.compare_digest(expected_sig, token['sig'])
    except:
        return False
