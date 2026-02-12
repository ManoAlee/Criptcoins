import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# --- BIO-RADAR PROTOCOL: WI-FI SENSING (CSI) ---
# Simulação de detecção biológica via perturbação de sinais RF

class BioRadar:
    """Simulador de detecção de sinais vitais via Channel State Information (CSI)."""
    
    def __init__(self, sampling_rate=20):
        self.fs = sampling_rate  # Amostragem de 20Hz
        self.duration = 30       # 30 segundos de captura
        self.t = np.linspace(0, self.duration, self.duration * self.fs)

    def generate_csi_simulation(self):
        """
        Simula dados brutos de CSI:
        Ruído de fundo + Estática (móveis) + Sinal Biológico (respiração).
        """
        # 1. Ruído do Canal (Gaussian Noise)
        noise = np.random.normal(0, 0.05, len(self.t))
        
        # 2. Interferência de Objetos Estáticos (DC offset)
        static_environment = 1.0 
        
        # 3. Sinal Biológico: Respiração (0.2 Hz a 0.3 Hz)
        # O movimento do peito causa uma pequena variação de fase/amplitude
        breathing_freq = 0.25 # 15 respirações por minuto
        breathing_signal = 0.1 * np.sin(2 * np.pi * breathing_freq * self.t)
        
        # Sinal CSI Recebido: Y = H*X + N
        csi_amplitude = static_environment + breathing_signal + noise
        return csi_amplitude

    def apply_bio_filter(self, data):
        """Aplica filtro de Butterworth para isolar a frequência respiratória (0.1 - 0.5 Hz)."""
        nyquist = 0.5 * self.fs
        low = 0.1 / nyquist
        high = 0.5 / nyquist
        b, a = butter(4, [low, high], btype='batch')
        return filtfilt(b, a, data)

    def extract_vitals(self, filtered_data):
        """Extrai a frequência dominante usando FFT (Fast Fourier Transform)."""
        n = len(filtered_data)
        freqs = np.fft.fftfreq(n, d=1/self.fs)
        fft_values = np.abs(np.fft.fft(filtered_data))
        
        # Pegar apenas a metade positiva do espectro
        half_n = n // 2
        pos_freqs = freqs[:half_n]
        pos_fft = fft_values[:half_n]
        
        # Encontrar o pico na banda de respiração
        peak_idx = np.argmax(pos_fft)
        vitals_bpm = pos_freqs[peak_idx] * 60
        return pos_freqs, pos_fft, vitals_bpm

    def run_scan(self):
        print("[*] Iniciando varredura Bio-Radar (Wi-Fi Sensing)...")
        raw_csi = self.generate_csi_simulation()
        filtered_csi = self.apply_bio_filter(raw_csi)
        freqs, spectrum, bpm = self.extract_vitals(filtered_csi)
        
        print(f"[*] Detecção Concluída: Humano Identificado.")
        print(f"[*] Ritmo Respiratório Estimado: {bpm:.2f} BPM")
        
        # Visualização do Radar
        plt.figure(figsize=(12, 6), facecolor='black')
        
        # Time Domain
        plt.subplot(2, 1, 1)
        plt.plot(self.t, raw_csi, color='gray', alpha=0.5, label='Raw CSI (Noise)')
        plt.plot(self.t, filtered_csi + 1.0, color='#00F5FF', label='Filtered Bio-Signal')
        plt.title("Onda de Perturbação Eletromagnética (Zonas de Fresnel)", color='white')
        plt.legend()
        plt.gca().set_facecolor('#050505')
        
        # Frequency Domain (The Signature)
        plt.subplot(2, 1, 2)
        plt.plot(freqs, spectrum, color='#BD93F9')
        plt.fill_between(freqs, spectrum, color='#BD93F9', alpha=0.3)
        plt.title("Espectro de Frequência Biológica (Assinatura Vital)", color='white')
        plt.xlabel("Frequência (Hz)", color='white')
        plt.xlim(0, 1.0)
        plt.gca().set_facecolor('#050505')
        
        plt.tight_layout()
        plt.savefig("bio_radar_output.png")
        print("[*] Dados espectrais salvos em 'bio_radar_output.png'")

if __name__ == "__main__":
    radar = BioRadar()
    radar.run_scan()
