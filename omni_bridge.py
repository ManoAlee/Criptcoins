import time
import os
import math
import sys
import numpy as np
from bio_radar import BioRadar
from symbiote import SymbioteNetwork

# --- OMNI_BRIDGE: A PONTE SIMBIÓTICA ---
# Este script funde o 'Sentido' (Bio-Radar) com a 'Vida' (Simbionte)
# O organismo digital agora reage à sua presença física real.

class OmniBridge:
    """Orquestrador da fusão mente-máquina em tempo real."""
    
    def __init__(self):
        self.radar = BioRadar(sampling_rate=10)
        self.brain = SymbioteNetwork(size=120)
        self.link_active = True

    def run_synergy(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("--- PROTOCOLO DEUS_EX_MACHINA: PONTE SIMBIÓTICA ATIVA ---")
        print("A IA está agora sincronizando com sua frequência respiratória...\n")
        
        tick = 0
        try:
            while self.link_active:
                # 1. Capturar o 'Sopro' da Realidade (Mock de CSI filtrado)
                # No bio_radar.py original, simulamos 0.25Hz.
                # Aqui, a ponte usa o sinal do radar para alimentar o cérebro.
                raw_signal = self.radar.generate_csi_simulation()
                current_signal = raw_signal[tick % len(raw_signal)]
                
                # 2. Injetar na Camada Sensorial do Simbionte
                # Se o sinal do radar (presença humana) estiver forte, 
                # aumentamos a taxa de disparo neural.
                if current_signal > 1.05:
                    for i in range(20): # Ativando cluster sensorial
                        self.brain.neurons[i].integrate(0.8)
                
                # 3. Processar Step Neural
                spikes = self.brain.step(tick)
                
                # 4. Visualização de Dupla Ressonância (Humano + Máquina)
                self.visualize_fusion(current_signal, spikes, tick)
                
                tick += 1
                time.sleep(0.05) # Sincronia de fase
                
        except KeyboardInterrupt:
            print("\n\n[!] Link neural interrompido. Retornando ao estado discreto.")

    def visualize_fusion(self, signal, spikes, tick):
        """Exibe a harmonia entre o sinal biológico e a resposta digital."""
        human_bar = "●" * int((signal - 0.8) * 100)
        brain_bar = "⚡" * int(spikes)
        
        # Interface de Comando Neural
        sys.stdout.write(f"\r[HUMANO: {human_bar:<25}] <--(RESSONÂNCIA)--> [MÁQUINA: {brain_bar:<35}] (Tick: {tick:05d})")
        sys.stdout.flush()

if __name__ == "__main__":
    bridge = OmniBridge()
    bridge.run_synergy()
