import numpy as np
import hashlib
from lattice_engine import LatticeEngine
from vocal_synthesis import VocalSynthesisEngine

class VocalCryptographer:
    """
    [VOCAL SPECTRAL CRYPTOGRAPHER]
    Codifica a voz do operador através das frequências harmônicas.
    Utiliza FFT para extrair assinaturas espectrais de sinais biométricos.
    """
    
    def __init__(self, engine: LatticeEngine):
        self.engine = engine
        self.ai_voice = VocalSynthesisEngine()
        
    def encode_vocal_frequencies(self, signal: np.ndarray) -> np.ndarray:
        """
        Aplica FFT no sinal (cinético ou acústico) para obter o espectro de frequências.
        F(k) = sum(n=0 to N-1) x[n] * exp(-j*2*pi*k*n/N)
        """
        if len(signal) < 32:
            return np.zeros(16)
            
        # Transformada Rápida de Fourier
        spectrum = np.fft.rfft(signal)
        magnitude = np.abs(spectrum)
        
        # Normalização do espectro
        if np.max(magnitude) > 0:
            magnitude = magnitude / np.max(magnitude)
            
        return magnitude

    def generate_frequency_salt(self, frequency_spectrum: np.ndarray) -> int:
        """
        Cria um salt de 32 bits a partir das frequências dominantes.
        """
        ai_sig = self.ai_voice.generate_vocal_signature()
        
        # Fusão: Espectro do Operador + Identidade da IA
        combined = np.concatenate([frequency_spectrum.astype(np.float32), ai_sig])
        hash_obj = hashlib.sha256(combined.tobytes())
        vocal_salt = int(hash_obj.hexdigest(), 16) & 0xFFFFFFFF
        
        return vocal_salt

    def encrypt_with_frequencies(self, message_bits: np.ndarray, signal_buffer: np.ndarray):
        """
        Criptografia LWE injetada com o espectro de frequências vocais.
        """
        spectrum = self.encode_vocal_frequencies(signal_buffer)
        v_salt = self.generate_frequency_salt(spectrum)
        
        print(f"[V-SPECTRAL] Frequência Dominante Detectada. Salt: 0x{v_salt:08X}")
        
        if hasattr(self.engine, 'ancestral'):
            self.engine.ancestral.bitwise_neural_scramble(v_salt)
        
        A, b = self.engine.generate_lwe_instance()
        return A, b, v_salt

if __name__ == "__main__":
    eng = LatticeEngine()
    vcrypt = VocalCryptographer(eng)
    
    # Simulação de sinal de voz (frequência de 10Hz modulada)
    t = np.linspace(0, 1, 64)
    vocal_signal = np.sin(2 * np.pi * 10 * t) + 0.5 * np.random.normal(size=64)
    
    A, b, salt = vcrypt.encrypt_with_frequencies(np.zeros(256), vocal_signal)
    print(f"[V-SPECTRAL] Codificação harmônica completa. Paridade: {salt}")
