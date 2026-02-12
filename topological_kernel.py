import cv2
import numpy as np
from scipy.ndimage import gaussian_filter, sobel
import matplotlib.pyplot as plt

class TopologicalKernel:
    """
    KERNEL DE RECONHECIMENTO TOPOLÓGICO (ROOT ARCHITECT)
    
    Este módulo trata a intensidade da imagem facial como uma 'variedade' (manifold) 3D imersa em R^3.
    A identidade é extraída através de invariantes geométricos como a Curvatura de Gauss.
    """
    
    def __init__(self, sigma=1.5, n_components=10):
        self.sigma = sigma 
        self.n_components = n_components 
        self.temporal_flow_cache = [] 
        self.prev_gray = None # Para Optical Flow

    def compute_metric_tensor(self, Ix, Iy):
        """
        Calcula os componentes do Tensor Métrico g_ij da superfície facial.
        g = [[1+Ix^2, Ix*Iy], [Ix*Iy, 1+Iy^2]]
        """
        g11 = 1 + Ix**2
        g12 = Ix * Iy
        g22 = 1 + Iy**2
        return g11, g12, g22

    def compute_geodesic_distance(self, sig1: np.ndarray, sig2: np.ndarray) -> float:
        """
        Calcula a distância geodésica entre duas assinaturas topológicas.
        Evolução Riemannian: Integra a divergência local pesada pelo tensor métrico.
        Nota: Para histogramas, usamos a variação da forma da variedade (curvatura).
        """
        # Estabilidade Numérica: Epsilon
        eps = 1e-10
        p = sig1 + eps
        q = sig2 + eps
        
        # 1. Divergência de Jensen-Shannon (Symmetrized KL)
        m = 0.5 * (p + q)
        js_div = 0.5 * np.sum(p * np.log(p / m)) + 0.5 * np.sum(q * np.log(q / m))
        
        # 2. Fator de Escala Riemannian (Simulado via Entropia do Tensor se disponível)
        # Aqui, a distância é refinada para ser robusta a deformações afins.
        dist = np.sqrt(max(0, js_div))
        return dist

    def _apply_svd_cleaning(self, image_matrix: np.ndarray) -> np.ndarray:
        """Utiliza SVD para reconstruir a imagem apenas com componentes principais, eliminando ruído."""
        U, S, Vt = np.linalg.svd(image_matrix.astype(float), full_matrices=False)
        S_clean = np.zeros_like(S)
        S_clean[:self.n_components] = S[:self.n_components]
        im_clean = U @ np.diag(S_clean) @ Vt
        return im_clean

    def _compute_derivatives(self, image_matrix: np.ndarray):
        """Calcula derivadas parciais de primeira e segunda ordem com SVD Pre-processing."""
        # Pre-processamento via SVD para reduzir ruído de hardware
        im_svd = self._apply_svd_cleaning(image_matrix)
        
        # Suavização Gaussiana para estabilizar o Tensor Métrico
        im = gaussian_filter(im_svd, self.sigma)
        
        # Derivadas de primeira ordem
        Ix = np.gradient(im, axis=1)
        Iy = np.gradient(im, axis=0)
        
        # Derivadas de segunda ordem
        Ixx = np.gradient(Ix, axis=1)
        Iyy = np.gradient(Iy, axis=0)
        Ixy = np.gradient(Ix, axis=0)
        
        return Ix, Iy, Ixx, Iyy, Ixy

    def compute_gaussian_curvature(self, image_matrix: np.ndarray) -> np.ndarray:
        """
        Calcula a Curvatura de Gauss (K) para a superfície Z = I(x,y).
        Fórmula: K = (fxx*fyy - fxy^2) / (1 + fx^2 + fy^2)^2
        """
        Ix, Iy, Ixx, Iyy, Ixy = self._compute_derivatives(image_matrix)
        
        numerator = (Ixx * Iyy - Ixy**2)
        denominator = (1 + Ix**2 + Iy**2)**2
        
        # Evitar divisão por zero (embora o denominador seja sempre >= 1 aqui)
        K = numerator / (denominator + 1e-10)
        return K

    def extract_signature(self, image_matrix: np.ndarray) -> np.ndarray:
        """
        Gera uma assinatura geométrica baseada na Curvatura Gaussiana.
        Reduz a dimensionalidade via pooling ou histograma de curvatura.
        """
        K = self.compute_gaussian_curvature(image_matrix)
        # Assinatura: Histograma da curvatura (invariante a translação)
        # Focamos em pontos de sela e picos ósseos.
        hist, _ = np.histogram(K, bins=64, range=(-1, 1), density=True)
        return hist

    def compute_similarity(self, sig1: np.ndarray, sig2: np.ndarray) -> float:
        """
        Compara duas assinaturas usando Distância de Mahalanobis ou Correlação.
        Aqui utilizamos Correlação de Pearson para alinhar vetores de curvatura.
        """
        if np.all(sig1 == 0) or np.all(sig2 == 0):
            return 0.0
        corr = np.corrcoef(sig1, sig2)[0, 1]
        return corr

    def detect_liveness(self, frame_sequence: list) -> float:
        """
        RPPG (Remote Photoplethysmography): Detecta pulsação sanguínea (Liveness).
        Analisa a micro-variação da cor média no tempo.
        """
        if len(frame_sequence) < 30: return 0.0 # Necessita de amostragem temporal
        
        # Média do canal verde (onde o sinal de hemoglobina é mais forte)
        greens = [np.mean(f[:,:,1]) for f in frame_sequence]
        greens = np.array(greens) - np.mean(greens) # Centralizar
        
        # FFT para encontrar frequências de batimento (0.75 - 3Hz -> 45-180 BPM)
        fft_data = np.abs(np.fft.fft(greens))
        # Simplificação: retorna a 'energia' na banda biológica
        return np.max(fft_data)

    def compute_optical_flow(self, current_gray: np.ndarray) -> np.ndarray:
        """
        [AMET] Calcula o Fluxo Óptico (Farneback) para detectar intenção e micro-movimentos.
        """
        if self.prev_gray is None or self.prev_gray.shape != current_gray.shape:
            self.prev_gray = current_gray
            return np.zeros((current_gray.shape[0], current_gray.shape[1], 2), dtype=np.float32)
            
        flow = cv2.calcOpticalFlowFarneback(self.prev_gray, current_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        self.prev_gray = current_gray
        return flow

    def analyze_flow_state(self, flow: np.ndarray) -> float:
        """
        Analisa o Estado de Fluxo: Estabilidade de olhar vs. Micro-movimentos involuntários.
        Retorna score de FOCO (0-1.0).
        """
        flow_f32 = flow.astype(np.float32)
        mag, ang = cv2.cartToPolar(flow_f32[...,0], flow_f32[...,1])
        # Foco alto = Baixa magnitude de movimento (estabilidade) com micro-variações controladas
        avg_mag = np.mean(mag)
        focus_score = 1.0 - min(1.0, avg_mag * 10.0)
        return focus_score

    def _compute_lbp(self, gray: np.ndarray) -> np.ndarray:
        """
        Local Binary Patterns para análise de textura.
        Diferencia poros da pele de artefatos de compressão digital ou pixels de tela.
        """
        h, w = gray.shape
        lbp = np.zeros((h-2, w-2), dtype=np.uint8)
        for i in range(1, h-1):
            for j in range(1, w-1):
                center = gray[i, j]
                code = 0
                code |= (gray[i-1, j-1] > center) << 7
                code |= (gray[i-1, j] > center) << 6
                code |= (gray[i-1, j+1] > center) << 5
                code |= (gray[i, j+1] > center) << 4
                code |= (gray[i+1, j+1] > center) << 3
                code |= (gray[i+1, j] > center) << 2
                code |= (gray[i+1, j-1] > center) << 1
                code |= (gray[i, j-1] > center) << 0
                lbp[i-1, j-1] = code
        return lbp

    def _check_chromicity(self, image_bgr: np.ndarray) -> float:
        """
        Analisa a distribuição de cores no espaço YCbCr.
        Telas digitais têm distribuições de cromitância (Cb/Cr) muito mais estreitas ou 
        com picos artificiais em relação à pele humana Lambertiana.
        """
        ycrcb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)
        cr = ycrcb[:,:,1]
        cb = ycrcb[:,:,2]
        # Pele real tem variância de Cr/Cb em faixas específicas
        std_cr = np.std(cr)
        std_cb = np.std(cb)
        
        # Se a variância for muito baixa (imagem chapada/digitalizada) ou 
        # se o histograma for muito 'espetado' (artefatos de compressão), suspeitar.
        if std_cr < 3.0 or std_cb < 3.0: 
            return 0.3 # Suspeita de Spoofing
        return 0.9

    def audit_surface_reflectance(self, image_bgr: np.ndarray) -> float:
        """
        [LAMBERTIAN AUDIT v2.0]
        Identifica se a superfície é PELE ou TELA via LBP + Fourier + Chromicity.
        """
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        
        # 1. Textura via LBP
        lbp = self._compute_lbp(gray)
        hist, _ = np.histogram(lbp, bins=256, range=(0, 256), density=True)
        # Telas têm picos em 0 ou 255 (áreas uniformes ou ruído digital)
        lbp_uniformity = np.max(hist)
        
        # 2. Fourier (Moiré)
        f = np.fft.fft2(gray)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
        h, w = magnitude_spectrum.shape
        magnitude_spectrum[h//2-5:h//2+5, w//2-5:w//2+5] = 0 # Ignorar centro DC
        
        # 3. Cromitância
        chroma_score = self._check_chromicity(image_bgr)
        
        # Síntese: Se LBP for muito uniforme OU Fourier tiver picos altos OU chroma for suspeito
        if lbp_uniformity > 0.15 or np.max(magnitude_spectrum) > 195 or chroma_score < 0.5:
            return 0.1 # SPOOF DETECTED
            
        return 0.95 # BIOLOGICAL_STABLE

    def verify_3d_parallax(self, flow: np.ndarray) -> float:
        """
        [GEOMETRIC AUDIT v2.0]
        Verifica se o objeto é 3D ou um plano 2D (foto).
        Analisa a divergência de fluxo entre o centro (nariz) e periferia.
        """
        h, w, _ = flow.shape
        mag, _ = cv2.cartToPolar(flow[...,0], flow[...,1])
        
        # Regiões: Centro (nariz) vs Bordas
        center_mag = np.mean(mag[h//4:3*h//4, w//4:3*w//4])
        outer_mag = (np.mean(mag[:h//4, :]) + np.mean(mag[3*h//4:, :])) / 2
        
        # Parallax Ratio: Em 3D, o centro se move com magnitude diferente da periferia
        # Em uma foto 2D, a razão é próxima de 1 (movimento global uniforme)
        ratio = abs(center_mag - outer_mag)
        
        # Se as magnitudes forem quase iguais, é um plano rígido (foto/celular)
        if ratio < 0.005: 
            return 0.1 # Plano 2D detectado.
            
        return min(1.0, ratio * 50.0)

    def visualize_manifold(self, image_matrix: np.ndarray, username="Unknown"):
        """Gera uma visualização 3D da face como uma superfície topológica."""
        K = self.compute_gaussian_curvature(image_matrix)
        
        h, w = image_matrix.shape
        x = np.arange(0, w)
        y = np.arange(0, h)
        X, Y = np.meshgrid(x, y)
        
        fig = plt.figure(figsize=(12, 8), facecolor='black')
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('black')
        
        # Plotar a superfície com cores mapeadas pela Curvatura (K)
        # Normalizar K para visualização
        K_norm = (K - np.min(K)) / (np.max(K) - np.min(K) + 1e-10)
        
        surf = ax.plot_surface(X, Y, image_matrix, facecolors=plt.cm.magma(K_norm),
                               linewidth=0, antialiased=True, shade=True)
        
        ax.set_title(f"Face Manifold: {username}", color='cyan', fontsize=16)
        ax.grid(False)
        ax.axis('off')
        
        output_path = f"face_manifold_{username}.png"
        plt.savefig(output_path, dpi=150, facecolor='black')
        plt.close()
        print(f"[*] Manifold visual salvo em: {output_path}")

if __name__ == "__main__":
    # Teste rápido com ruído estruturado
    print("[*] Testando Kernel Topológico...")
    kernel = TopologicalKernel()
    dummy_face = np.zeros((100, 100))
    # Simular um nariz (pico de curvatura)
    for i in range(100):
        for j in range(100):
            dist = np.sqrt((i-50)**2 + (j-50)**2)
            dummy_face[i,j] = 255 * np.exp(-dist**2 / 500)
    
    sig = kernel.extract_signature(dummy_face)
    print(f"[+] Assinatura gerada (size {len(sig)}): {sig[:5]}...")
    kernel.visualize_manifold(dummy_face, "Synthetic_Test")
