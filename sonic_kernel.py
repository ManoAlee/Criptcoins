import winsound
import time
import numpy as np
from vocal_synthesis import VocalSynthesisEngine

class SonicKernel:
    """
    [SONIC KERNEL]
    O coração auditivo do sistema. Traduz telemetria em frequências.
    Integra a Voz do Arquiteto com feedback musical algorítmico.
    """
    
    def __init__(self):
        self.base_freq = 440  # A4
        self.scale = [261, 293, 329, 349, 392, 440, 493, 523] # C Major
        self.vocal = VocalSynthesisEngine()
        
    def generative_melody(self, focus_score: float, entropy: float):
        """Transforma telemetria em sequências melódicas pentatônicas."""
        # Escala Pentatônica Major (C, D, E, G, A)
        pentatonic = [261, 293, 329, 392, 440]
        
        # Determinar complexidade baseada na entropia (mais entropia = mais notas)
        num_notes = int(3 + (entropy * 5))
        
        for _ in range(num_notes):
            # Escolher nota baseada no focus_score
            idx = int(focus_score * (len(pentatonic) - 1))
            note = pentatonic[idx]
            duration = int(40 + (random.random() * 60))
            
            try:
                winsound.Beep(note, duration)
            except:
                pass
            time.sleep(0.01)

    def architectural_alert(self, level: str, text: str = None):
        """Voz do Sistema: Alertas rítmicos e síntese vocal."""
        if text:
            self.vocal.speak(text)
            
        if level == "INFO":
            for f in [440, 554, 659]:
                winsound.Beep(f, 60)
        elif level == "WARNING":
            for _ in range(2):
                winsound.Beep(100, 150)
        elif level == "SINGULARITY":
            # Arpejo Pentatônico Rápido
            penta = [261, 329, 392, 523, 659]
            for f in penta:
                winsound.Beep(f, 30)

    def play_logic_sequence(self, bit_sequence: int):
        """Converte uma sequência de bits (Assembly Logic) em som."""
        for i in range(8):
            bit = (bit_sequence >> i) & 1
            freq = 800 if bit else 400
            winsound.Beep(freq, 30)

if __name__ == "__main__":
    import random
    sk = SonicKernel()
    print("[SONIC] Testando Melodias Generativas...")
    sk.architectural_alert("SINGULARITY", "Iniciando sinfonia algorítmica.")
    for _ in range(3):
        sk.generative_melody(random.random(), random.random())
    time.sleep(2)
