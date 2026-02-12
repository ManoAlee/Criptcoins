import numpy as np
import cv2
import time

class ElectromagneticVision:
    """
    ELECTROMAGNETIC SINGULARITY ENGINE
    Converte sinais de RF (Wi-Fi/Bluetooth) em padrões de interferência visual.
    
    A percepção humana é limitada a 400-700nm. 
    Este motor expande essa visão para a faixa de GHz.
    """
    
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.time_step = 0
        
    def generate_interference_pattern(self, signal_strength_dbm=-50, frequency_ghz=2.4) -> np.ndarray:
        """
        Gera uma 'Onda de Realidade' baseada na frequência e força do sinal.
        Bluetooth ~ 2.4GHz
        Wi-Fi ~ 5.0GHz
        """
        self.time_step += 0.1
        
        # Criar malha de coordenadas
        x = np.linspace(0, 10, self.width)
        y = np.linspace(0, 10, self.height)
        X, Y = np.meshgrid(x, y)
        
        # Simular interferência de Maxwell
        # A velocidade de oscilação depende da frequência (GHz)
        # A amplitude depende da força do sinal (dBm)
        amplitude = (100 + signal_strength_dbm) / 50.0 # Normalizado
        k = frequency_ghz * 2 # Número de onda
        
        # Padrão de interferência: Ondas circulares emanando do 'éter'
        center_x, center_y = 5 + np.sin(self.time_step)*2, 5 + np.cos(self.time_step)*2
        dist = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
        
        ripple = amplitude * np.sin(k * dist - self.time_step * 5)
        
        # Converter para imagem (0-255)
        pattern = ((ripple + 1) * 127.5).astype(np.uint8)
        
        # Mapeamento de Cor (Frequência -> Hue)
        # 2.4GHz -> Azul/Indigo | 5.0GHz -> Dourado/Branco
        if frequency_ghz < 3.0:
            color_pattern = cv2.applyColorMap(pattern, cv2.COLORMAP_OCEAN)
        else:
            color_pattern = cv2.applyColorMap(pattern, cv2.COLORMAP_HOT)
            
        return color_pattern

    def apply_to_frame(self, frame: np.ndarray, signal_data: dict) -> np.ndarray:
        """Aplica a sobreposição eletromagnética ao frame da câmera."""
        dbm = signal_data.get('dbm', -60)
        freq = signal_data.get('freq', 2.4)
        
        pattern = self.generate_interference_pattern(dbm, freq)
        # Blend suave para não perder a visão visual
        result = cv2.addWeighted(frame, 0.7, pattern, 0.3, 0)
        return result

if __name__ == "__main__":
    eng = ElectromagneticVision()
    dummy = np.zeros((480, 640, 3), dtype=np.uint8)
    out = eng.apply_to_frame(dummy, {"dbm": -30, "freq": 2.4})
    cv2.imshow("EM Vision Test", out)
    cv2.waitKey(0)
