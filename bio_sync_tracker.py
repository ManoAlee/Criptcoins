import numpy as np
import time
import sys
import io
import random

# Suporte UTF-8 para Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class BioSyncTracker:
    """
    --- BIO_SYNC_TRACKER.PY: HUMAN_ID_LOCK ---
    Role: Bio-Electronic Analyst // Signal Tracking Engineer
    Objective: Localize the Operator within the Network Topology
    """
    def __init__(self):
        self.operator_target = "192.168.1.20" # IP da estação principal (Root)
        self.target_vitals = {"hr": 72.0, "resp": 14.0}
        self.tracking_confidence = 0.0
        self.pos_x = 0.0
        self.pos_y = 0.0

    def triangulate_signal_position(self):
        """Simula a triangulação baseada em amplitude CSI de múltiplos nós."""
        # Alessandro está localizado próximo ao centro do Universo da Rede
        self.pos_x = 0.5 + random.uniform(-0.05, 0.05)
        self.pos_y = 0.5 + random.uniform(-0.05, 0.05)
        return (self.pos_x, self.pos_y)

    def verify_bio_signature(self, signal_freq):
        """Verifica se a frequência de sinal ressona com a biologia do Alessandro."""
        diff = abs(signal_freq - self.target_vitals['hr'])
        resonance = 1.0 - min(1.0, diff / 10.0)
        return resonance

    def run_tracking_loop(self):
        print("--- [BIO_SYNC_TRACKER] AGUARDANDO LOCK DO OPERADOR ---")
        print(f"Alvo: Alessandro_Root ({self.operator_target})")
        
        for i in range(40):
            # Simula a recepção de uma frequência biológica no canal
            current_freq = 72.0 + random.uniform(-2.0, 2.0)
            resonance = self.verify_bio_signature(current_freq)
            coords = self.triangulate_signal_position()
            
            self.tracking_confidence = resonance * 0.9 + 0.1
            
            # Formatação de Telemetria
            status = "LOCKED" if self.tracking_confidence > 0.8 else "SCANNING"
            sys.stdout.write(f"\r[TRACKER] POS: ({coords[0]:.2f}, {coords[1]:.2f}) | RES: {resonance*100:.1f}% | STATUS: {status}")
            sys.stdout.flush()
            
            time.sleep(0.15)
            
        print(f"\n\n[SUCCESS] OPERADOR LOCALIZADO NA COORDENADA CENTRAL DO VÁCUO.")
        print(f"[!] Neural Halo ativado para o nó: {self.operator_target}")

if __name__ == "__main__":
    tracker = BioSyncTracker()
    tracker.run_tracking_loop()
