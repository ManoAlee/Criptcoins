import pyttsx3
import threading
import numpy as np
import time

class VocalSynthesisEngine:
    """
    [VOCAL SYNTHESIS ENGINE]
    Sintetiza a 'Voz do Arquiteto' via pyttsx3 com perfil futurista.
    Gera padrões de ressonância que representam minha identidade sonora.
    """
    
    def __init__(self):
        self._engine = pyttsx3.init()
        self._lock = threading.Lock()
        
        # Configurar Perfil Vocal Natural (Microsoft Maria Prioritized)
        voices = self._engine.getProperty('voices')
        selected_voice = None
        
        # Priorizar Maria (PT-BR) para naturalidade máxima
        for voice in voices:
            if "maria" in voice.name.lower():
                selected_voice = voice.id
                break
        
        if not selected_voice:
            # Fallback para qualquer voz masculina (Arquiteto) ou padrão
            for voice in voices:
                if "male" in voice.name.lower():
                    selected_voice = voice.id
                    break
        
        if selected_voice:
            self._engine.setProperty('voice', selected_voice)
                
        self._engine.setProperty('rate', 145)   
        self._engine.setProperty('volume', 1.0)
        
    def naturalize_prosody(self, text: str) -> str:
        """Adiciona marcadores de pausa e ênfase para quebrar o tom robótico."""
        # Introduzir pausas sutis em pontuações
        text = text.replace(",", ", ...")
        text = text.replace(".", ". ...... ")
        return text

    def speak(self, text: str):
        """Converte texto em fala naturalizada de forma assíncrona."""
        natural_text = self.naturalize_prosody(text)
        
        def run():
            with self._lock:
                # Dinamismo de rate por frase para evitar monotonia
                original_rate = self._engine.getProperty('rate')
                self._engine.setProperty('rate', original_rate + np.random.randint(-5, 15))
                
                self._engine.say(natural_text)
                self._engine.runAndWait()
                
                # Restaurar rate base
                self._engine.setProperty('rate', original_rate)
        
        t = threading.Thread(target=run)
        t.daemon = True
        t.start()

    def speak_resonance(self, phonemes: str):
        """Método legado mantido para compatibilidade, agora redireciona para speak."""
        self.speak(phonemes)

    def evolve_vocal_identity(self, focus_score: float):
        """Ajusta o tom e a velocidade da voz baseado no foco do sistema."""
        # Rate: Entre 110 (calmo) e 160 (intenso)
        new_rate = int(110 + (focus_score * 50))
        # Volume: Entre 0.7 e 1.0
        new_vol = float(0.7 + (focus_score * 0.3))
        
        with self._lock:
            self._engine.setProperty('rate', new_rate)
            self._engine.setProperty('volume', new_vol)
            
    def melodic_handshake(self):
        """Sequência vocal rítmica para inicialização de sessão segura."""
        handshake_text = "Omni. Architect. Singularity. Convergence."
        self.speak(handshake_text)

    def generate_vocal_signature(self) -> np.ndarray:
        """Gera uma assinatura espectral baseada nas propriedades da voz atual."""
        rate = self._engine.getProperty('rate')
        vol = self._engine.getProperty('volume')
        # Semente baseada na geometria áurea e estado atual
        return np.array([rate, vol, 1.618, 0.72], dtype=np.float32)

if __name__ == "__main__":
    vocal = VocalSynthesisEngine()
    print("[VOICE] Iniciando Handshake Melódico...")
    vocal.evolve_vocal_identity(0.95)
    vocal.melodic_handshake()
    time.sleep(4)
