import cv2
import time
import numpy as np

def run_hardware_audit():
    print("--- [CAMERA_AUDIT] INICIANDO DIAGNÓSTICO DE HARDWARE ---")
    
    # 1. Teste de Abertura (DirectShow)
    print("[*] Testando driver CAP_DSHOW...")
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    if not cam.isOpened():
        print("[FAIL] CAP_DSHOW não conseguiu abrir a câmera.")
        return False
    
    print("[OK] CAP_DSHOW inicializado.")
    
    # 2. Teste de Resolução e Frame
    ret, frame = cam.read()
    if ret:
        h, w, c = frame.shape
        print(f"[OK] Frame capturado: {w}x{h} | Canais: {c}")
    else:
        print("[FAIL] Câmera aberta, mas falha na leitura do frame.")
        cam.release()
        return False

    # 3. Teste de Latência (10 frames)
    start = time.time()
    for _ in range(10):
        cam.read()
    end = time.time()
    avg_latency = (end - start) / 10
    print(f"[OK] Latência média por frame: {avg_latency*1000:.2f}ms (~{1/avg_latency:.1f} FPS)")

    # 4. Verificação de Dependências do Sistema
    print("\n--- [SYSTEM_DEPENDENCY_CHECK] ---")
    dependencies = {
        "activate_omega.py": "CAP_DSHOW" in open("activate_omega.py", encoding="utf-8").read(),
        "topological_validator_gui.py": "CAP_DSHOW" in open("topological_validator_gui.py", encoding="utf-8").read(),
        "face_recog.py": "CAP_DSHOW" in open("face_recog.py", encoding="utf-8").read()
    }
    
    for file, status in dependencies.items():
        print(f"[{'OK' if status else '!!'}] {file:<30} | {'Configurado com CAP_DSHOW' if status else 'Usando driver padrão (risco de instabilidade)'}")

    cam.release()
    print("\n[AUDIT_COMPLETE] Hardware validado com sucesso.")
    return True

if __name__ == "__main__":
    run_hardware_audit()
