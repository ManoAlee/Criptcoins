import numpy as np
import time

class CNS:
    """
    CENTRAL NERVOUS SYSTEM (Brain Layer)
    
    Orquestra as camadas de hardware e software, reagindo autonomamente
    à entropia e à variação do sinal biométrico.
    """
    
    def __init__(self, manipulator, kernel):
        self.manipulator = manipulator
        self.kernel = kernel
        
        # Parâmetros de Estado
        self.entropy_threshold = 4.5 # Bits (abaixo disso, sinal é pobre)
        self.stability_history = []
        self.current_recommendation = "STABLE"
        self.autonomous_lock = False # Se o sistema está em auto-correção

    def analyze_situation(self, raw_frame, face_roi_gray):
        """
        Analisa o ambiente e decide o melhor modo de operação.
        """
        # Calcular Entropia Global (do frame) ou Local (da face)
        h, w = face_roi_gray.shape
        # Sub-amostragem para velocidade no CNS
        small_face = face_roi_gray[::4, ::4]
        counts = np.bincount(small_face.flatten(), minlength=256)
        probs = counts / small_face.size
        p = probs[probs > 0]
        local_entropy = -np.sum(p * np.log2(p))
        
        # Feedback Loop: Ajuste de Hardware/Filtros
        actions = []
        if local_entropy < self.entropy_threshold:
            actions.append("EMIT_LOG_MAPPING")
            actions.append("INCREASE_EXPOSURE_EMULATED")
            self.current_recommendation = "LOW_SIGNAL_RECOVERY"
        elif local_entropy > 7.5: # Muito ruído
            actions.append("APPLY_SVD_DENOISING")
            self.current_recommendation = "HIGH_NOISE_REFLUX"
        else:
            self.current_recommendation = "STABLE"
            
        return local_entropy, actions

    def record_heartbeat(self, confidence_score):
        """Registra a estabilidade do reconhecimento para detecção de anomalias."""
        self.stability_history.append(float(confidence_score))
        if len(self.stability_history) > 100:
            self.stability_history.pop(0)
            
        # Analisar variância do reconhecimento (Se varia muito, algo está errado)
        if len(self.stability_history) > 10:
            var = np.var(self.stability_history[-10:])
            if var > 500: # Instabilidade alta (flutuação de identidade)
                return "UNSTABLE_GEOMETRY"
        return "STABLE_FIELD"

if __name__ == "__main__":
    print("[*] CNS: Central Nervous System Initialized.")
    # Exemplo de loop de consciência
    from universe_manipulator import UniverseManipulator
    from topological_kernel import TopologicalKernel
    
    cns = CNS(UniverseManipulator(), TopologicalKernel())
    dummy_face = np.random.randint(0, 50, (100, 100), dtype=np.uint8) # Low entropy
    entropy, actions = cns.analyze_situation(None, dummy_face)
    print(f"[CNS] Entropia Detectada: {entropy:.2f} bits.")
    print(f"[CNS] Ações Recomendadas: {actions}")
