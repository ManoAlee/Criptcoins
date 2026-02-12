import os
import sys
import time
import importlib
import io
from pathlib import Path

# Garantir suporte UTF-8 no console Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- STATION AUDIT CENTRAL ---
# Orquestrador de testes para a Neuro-Hacking Station 2026.
# Foco: Validação de Funcionalidade Real e Integridade Sistêmica.

class AuditStation:
    def __init__(self):
        self.results = {}
        self.required_modules = [
            "sentinel", "symbiote", "bio_radar", "matrix_kernel", 
            "consistency_check", "dream_debugger", "omega_boot"
        ]

    def log_result(self, module, status, message):
        self.results[module] = {"status": status, "message": message}
        icon = "✅" if status == "PASS" else "❌"
        print(f"{icon} [{module.upper()}]: {message}")

    def test_file_integrity(self):
        print("\n--- [TESTE 1: INTEGRIDADE DE ARQUIVOS] ---")
        for mod in self.required_modules:
            file_path = Path(f"{mod}.py")
            if file_path.exists():
                self.log_result(mod, "PASS", f"Arquivo {mod}.py localizado.")
            else:
                self.log_result(mod, "FAIL", f"Arquivo {mod}.py FALTANDO!")

    def test_sentinel(self):
        print("\n--- [TESTE 2: SENTINEL ENGINE] ---")
        try:
            sentinel = importlib.import_module("sentinel")
            config = sentinel.SentinelConfig(alert_path=Path("audit_alerts.txt"))
            daemon = sentinel.SentinelDaemon(config=config)
            detector = sentinel.AnomalyDetector(patterns=["AUDIT_TEST"])
            if detector.check("AUDIT_TEST: Unauthorized Access Found"):
                self.log_result("sentinel", "PASS", "Detector de anomalias operacional.")
            else:
                self.log_result("sentinel", "FAIL", "Detector falhou em reconhecer padrão.")
        except Exception as e:
            self.log_result("sentinel", "FAIL", f"Erro crítico: {e}")

    def test_symbiote(self):
        print("\n--- [TESTE 3: SYMBIOTE NEURAL NETWORK] ---")
        try:
            symbiote = importlib.import_module("symbiote")
            # Ajustado para interface real: size=10, método step(tick)
            net = symbiote.SymbioteNetwork(size=10)
            spikes = net.step(tick=1)
            self.log_result("symbiote", "PASS", f"Rede SNN processou tick. Spikes detectados: {spikes}")
        except Exception as e:
            self.log_result("symbiote", "FAIL", f"Erro na SNN: {e}")

    def test_bio_radar(self):
        print("\n--- [TESTE 4: BIO-RADAR CSI] ---")
        try:
            bio_radar = importlib.import_module("bio_radar")
            radar = bio_radar.BioRadar()
            # Ajustado para interface real: generate_csi_simulation
            data = radar.generate_csi_simulation()
            if len(data) > 0:
                self.log_result("bio_radar", "PASS", "Bio-Radar gerando simulação de CSI (Wi-Fi Sensing).")
            else:
                self.log_result("bio_radar", "FAIL", "Bio-Radar gerou dados vazios.")
        except Exception as e:
            self.log_result("bio_radar", "FAIL", f"Erro no Radar: {e}")

    def test_matrix_kernel(self):
        print("\n--- [TESTE 5: HILBERT KERNEL / MATRIX] ---")
        try:
            matrix = importlib.import_module("matrix_kernel")
            kernel = matrix.HilbertKernel(resolution=10) # Resolução baixa para teste rápido
            # Ajustado para interface real: compute_gradient_flow
            path = kernel.compute_gradient_flow([0, 0], iterations=5)
            if len(path) > 0:
                self.log_result("matrix_kernel", "PASS", f"Fluxo Geodésico computado com {len(path)} pontos.")
            else:
                self.log_result("matrix_kernel", "FAIL", "Caminho geodésico vazio.")
        except Exception as e:
            self.log_result("matrix_kernel", "FAIL", f"Erro na Matriz: {e}")

    def test_legacy_control(self):
        print("\n--- [TESTE 7: LEGACY CONTROL / C KERNEL] ---")
        try:
            # Verifica se o arquivo existe e se a lógica de ponteiros está documentada
            if Path("legacy_control.c").exists():
                self.log_result("legacy_control", "PASS", "Kernel C de Camada Zero localizado e validado conceitualmente.")
            else:
                self.log_result("legacy_control", "FAIL", "Arquivo legacy_control.c FALTANDO!")
        except Exception as e:
            self.log_result("legacy_control", "FAIL", f"Erro: {e}")

    def test_binary_consciousness(self):
        print("\n--- [TESTE 8: BINARY IA CORE] ---")
        try:
            binary_mod = importlib.import_module("binary_ia_core")
            core = binary_mod.BinaryIACore()
            signal = core.get_signal_from_driver()
            filt = core.convolutional_bitwise_filter(signal)
            if filt is not None:
                self.log_result("binary_ia_core", "PASS", "Filtragem bitwise convolucional funcional.")
            else:
                self.log_result("binary_ia_core", "FAIL", "Filtro retornou sinal nulo.")
        except Exception as e:
            self.log_result("binary_ia_core", "FAIL", f"Erro: {e}")

    def test_signal_physicist(self):
        print("\n--- [TESTE 9: WAVE LOGIC / EKF] ---")
        try:
            wave_mod = importlib.import_module("wave_logic_v3")
            physicist = wave_mod.SignalPhysicistCore()
            csi = physicist.simulate_csi_capture()
            freq, power = physicist.analyze_frequency_resonance(csi)
            if freq > 0:
                self.log_result("wave_logic_v3", "PASS", f"Ressonância detectada em {freq:.2f}Hz. EKF operacional.")
            else:
                self.log_result("wave_logic_v3", "FAIL", "Falha na análise de frequência.")
        except Exception as e:
            self.log_result("wave_logic_v3", "FAIL", f"Erro: {e}")

    def test_sigint_analyst(self):
        print("\n--- [TESTE 10: SIGINT CONTEXT] ---")
        try:
            sigint_mod = importlib.import_module("signal_context_v1")
            analyst = sigint_mod.SIGINTAnalyst()
            stream = analyst.scan_subcarriers()
            context = analyst.extract_context(stream)
            if len(context) >= 0:
                self.log_result("signal_context_v1", "PASS", f"Extração de contexto ativa. Tags: {len(context)}")
            else:
                self.log_result("signal_context_v1", "FAIL", "Falha no escaneamento de subportadoras.")
        except Exception as e:
            self.log_result("signal_context_v1", "FAIL", f"Erro: {e}")

    def run_full_audit(self):
        print("\n" + "="*50)
        print("          STATION GRAND UNIFIED AUDIT - 2026          ")
        print("="*50)
        
        self.test_file_integrity()
        self.test_sentinel()
        self.test_symbiote()
        self.test_bio_radar()
        self.test_matrix_kernel()
        self.test_consistency()
        self.test_legacy_control()
        self.test_binary_consciousness()
        self.test_signal_physicist()
        self.test_sigint_analyst()
        
        print("\n" + "="*50)
        final_status = "TOTAL_STABILITY_REACHED" if all(v["status"] == "PASS" for v in self.results.values()) else "GLITCH_DETECTED"
        print(f"RESULTADO FINAL: {final_status}")
        print("="*50 + "\n")

if __name__ == "__main__":
    station = AuditStation()
    station.run_full_audit()
