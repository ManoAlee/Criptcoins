import cv2
import time
import sys
import os
from TOTAL_STATION_ROOT import TotalStationRoot
from face_recog import authenticate_from_image_bytes

def activate_everything():
    station = TotalStationRoot()
    
    # 1. Boot Subsystems
    station.boot_all_subsystems()
    
    # 2. Telemetry Pulse
    station.run_telemetry_loop()
    
    print("\n\n" + "="*80)
    print(" [HANDSHAKE] INICIANDO PROTOCOLO DE IDENTIDADE TOPOLÓGICA ".center(80))
    print("="*80)
    
    # 3. Camera Activation & Handshake
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cam.isOpened():
        print("[❌] Erro: Câmera não detectada. Pulando validação visual.")
        return

    print("[ℹ️] Olhando para a câmera para colapsar a função de onda...")
    time.sleep(1)
    
    try:
        authenticated = False
        for i in range(10): # Tentar por 10 frames
            ret, frame = cam.read()
            if not ret: break
            
            # Codificar frame para bytes (PNG) para o authenticate_from_image_bytes
            _, buffer = cv2.imencode('.png', frame)
            user, score = authenticate_from_image_bytes(buffer.tobytes())
            
            if user:
                print(f"\n[✨] HANDSHAKE COMPLETO: Operador {user} validado matematicamente.")
                print(f"[MATHEMATICAL_LOCK] Acesso Root Concedido. Estabilidade: 100%.")
                authenticated = True
                break
            else:
                sys.stdout.write(f"\r[SCANNING] Tentativa {i+1}/10 - Geometria não coincidente...")
                sys.stdout.flush()
                time.sleep(0.5)
        
        if not authenticated:
            print("\n[⚠️] Falha na sincronização topográfica. Modo de Segurança Ativado.")
            
    finally:
        cam.release()
        cv2.destroyAllWindows()

    # 4. Final Audit
    station.final_audit()
    print("\n[FINAL] SISTEMA OPERACIONAL. BEM-VINDO AO NÚCLEO, OPERADOR.")

if __name__ == "__main__":
    activate_everything()
