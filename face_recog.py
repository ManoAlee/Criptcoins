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
from typing import Optional, Tuple
from topological_kernel import TopologicalKernel
from central_nervous_system import CNS
from universe_manipulator import UniverseManipulator

# Instanciar o Kernel Topológico e Manipulador
top_kernel = TopologicalKernel()
manipulator = UniverseManipulator()
cns = CNS(manipulator, top_kernel)

DB_DIR = 'face_db'
CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
FACE_SIZE = (100, 100)


def ensure_db_dir():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR, exist_ok=True)


def detect_face_array_from_image_bytes(image_bytes: bytes) -> Optional[np.ndarray]:
    """Detecta a maior face na imagem PNG bytes e retorna ROI grayscale 100x100 array."""
    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        return None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(CASCADE_PATH)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    if len(faces) == 0:
        return None
    # choose largest face
    x, y, w, h = max(faces, key=lambda r: r[2] * r[3])
    roi = gray[y:y+h, x:x+w]
    roi_resized = cv2.resize(roi, FACE_SIZE)
    return roi_resized


def enroll_user_interactive(username: str, samples: int = 5) -> bool:
    """Interativo: abre webcam e captura `samples` rostos para o usuário, salva média."""
    ensure_db_dir()
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cam.isOpened():
        print('[❌] Não foi possível abrir a webcam para enrolamento.')
        return False

    print(f'[ℹ️] Enrolando usuário: {username}. Pressione ESPAÇO para capturar cada amostra; q para cancelar.')
    samples_collected = []

    while len(samples_collected) < samples:
        ret, frame = cam.read()
        if not ret:
            print('[❌] Falha ao ler frame da webcam.')
            break
        display = frame.copy()
        cv2.putText(display, f'Samples: {len(samples_collected)}/{samples}', (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0),2)
        cv2.imshow('Enroll - press SPACE to capture, q to quit', display)
        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):
            ret2, buf = cv2.imencode('.png', frame)
            if not ret2:
                print('[❌] Falha ao codificar imagem.')
                continue
            face = detect_face_array_from_image_bytes(buf.tobytes())
            if face is None:
                print('[⚠️] Nenhuma face detectada. Ajuste a posição e tente novamente.')
                continue
            samples_collected.append(face.astype(np.uint8))
            print(f'[✅] Amostra coletada: {len(samples_collected)}/{samples}')

        if key == ord('q'):
            print('[⚠️] Enrolamento cancelado pelo usuário.')
            break

    cam.release()
    cv2.destroyAllWindows()

    if not samples_collected:
        return False

    mean_face = np.mean(np.stack(samples_collected), axis=0).astype(np.uint8)
    # Gerar assinatura topológica (Curvatura de Gauss)
    top_sig = top_kernel.extract_signature(mean_face)
    
    out_path = os.path.join(DB_DIR, f'{username}.npz')
    np.savez_compressed(out_path, mean=mean_face, top_sig=top_sig)
    print(f'[✅] Usuário {username} enrolado. Dados (Topológicos + Pixels) salvos em: {out_path}')
    return True


def list_enrolled_users() -> list:
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


def authenticate_from_image_bytes(image_bytes: bytes, threshold: float = 40.0) -> Tuple[Optional[str], Optional[float]]:
    """Detecta face na imagem e compara com usuários enrolados. Retorna (username, distance) ou (None, None)."""
    face = detect_face_array_from_image_bytes(image_bytes)
    if face is None:
        return None, None
    users = list_enrolled_users()
    if not users:
        return None, None
    best_user = None
    best_score = float('inf')
    best_top_score = -1.0 # Correlação topológica
    
    # Extrair assinatura topológica da face capturada
    current_top_sig = top_kernel.extract_signature(face)

    for u in users:
        path = os.path.join(DB_DIR, f'{u}.npz')
        data = np.load(path)
        mean = data['mean']
        
        # Comparação Legada (Pixels)
        pixel_score = float(np.mean(np.abs(mean.astype(np.int16) - face.astype(np.int16))))
        
        # Comparação Topológica (Se existir no arquivo)
        top_score = 0.0
        if 'top_sig' in data:
            # Evolução Level 2: Distância Geodésica (Jensen-Shannon)
            # Menor distância = Maior similaridade
            geo_dist = top_kernel.compute_geodesic_distance(data['top_sig'], current_top_sig)
            # Normalizar para Score (0 a 1)
            top_score = 1.0 - min(1.0, geo_dist * 2.0)
        
        # Lógica Híbrida Inteligente
        if pixel_score < best_score or top_score > best_top_score:
            if top_score > 0.88 or pixel_score <= threshold:
                best_score = pixel_score
                best_top_score = top_score
                best_user = u

    if best_user:
        # Notificar o CNS da estabilidade
        cns.record_heartbeat(best_top_score * 100)
        print(f"[GEODESIC_SYNC] {best_user} | Geo_Score: {best_top_score:.4f}")
        return best_user, best_score
    return None, best_score
