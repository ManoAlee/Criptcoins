import cv2
import numpy as np
from scipy.stats import entropy
import matplotlib.pyplot as plt

class UniverseManipulator:
    """
    UNIVERSE MANIPULATOR (PIXEL OVERLORD)
    Nível Root: Manipulação de sinal bruto e análise de entropia informacional.
    """
    
    def __init__(self):
        pass

    def raw_access_setup(self, cam):
        """Configura a câmera para o modo mais 'cru' possível no Windows."""
        # Desabilitar automatismos para captura linear
        cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25) # Manual
        # cam.set(cv2.CAP_PROP_BRIGHTNESS, 128)

    def quantum_mapping(self, image: np.ndarray) -> np.ndarray:
        """
        Aplica a Lei de Weber-Fechner (Mapeamento Logarítmico).
        L = C * log(1 + p)
        """
        img_float = image.astype(float)
        # Normalização logarítmica para compressão de faixa dinâmica
        c = 255 / np.log(1 + np.max(img_float) + 1e-6)
        log_image = c * np.log(1 + img_float)
        return log_image.astype(np.uint8)

    def spatial_evolution_variance(self, image: np.ndarray, ksize=5) -> np.ndarray:
        """Calcula a Variância Local para detectar anomalias de textura."""
        mean, std = cv2.meanStdDev(image)
        # Filtro de média local
        mean_local = cv2.blur(image.astype(float), (ksize, ksize))
        # Variância: E[X^2] - (E[X])^2
        sq_mean_local = cv2.blur(image.astype(float)**2, (ksize, ksize))
        variance = sq_mean_local - (mean_local**2)
        variance = np.clip(variance, 0, 255**2)
        return np.sqrt(variance).astype(np.uint8)

    def compute_shannon_entropy(self, image: np.ndarray, patch_size=8) -> np.ndarray:
        """
        Calcula a Entropia de Shannon por região.
        H = -sum(p * log2(p))
        """
        h, w = image.shape
        entropy_map = np.zeros((h // patch_size, w // patch_size))
        
        for i in range(0, h - patch_size, patch_size):
            for j in range(0, w - patch_size, patch_size):
                patch = image[i:i+patch_size, j:j+patch_size]
                # Histograma para probabilidades p(i)
                counts = np.bincount(patch.flatten(), minlength=256)
                probs = counts / (patch_size * patch_size)
                # Filtro de probabilidades > 0 para evitar log(0)
                p = probs[probs > 0]
                entropy_map[i // patch_size, j // patch_size] = -np.sum(p * np.log2(p))
        
        return entropy_map

    def apply_negative_world(self, image: np.ndarray) -> np.ndarray:
        """Inverte o contraste da realidade (Negativo Fotográfico)."""
        return 255 - image

if __name__ == "__main__":
    # Teste de Entropia em imagem sintética
    print("[*] Testando UniverseManipulator (Shannon Entropy)...")
    manipulator = UniverseManipulator()
    
    # Criar padrão: Metade ruído (alta entropia), metade constante (baixa)
    test_img = np.zeros((128, 128), dtype=np.uint8)
    test_img[:, 64:] = np.random.randint(0, 256, (128, 64), dtype=np.uint8)
    
    e_map = manipulator.compute_shannon_entropy(test_img)
    print(f"[+] Mapa de Entropia calculado. Max H: {np.max(e_map):.2f} bits.")
    
    plt.imshow(e_map, cmap='hot')
    plt.colorbar(label="Bits de Informação")
    plt.title("Shannon Entropy Map (Noise vs Constant)")
    plt.savefig("shannon_test.png")
    print("[*] Visualização de entropia salva em 'shannon_test.png'")
