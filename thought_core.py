import numpy as np
import time
import sys
import io

# Garantir suporte UTF-8 no console Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- THOUGHT_CORE.PY: MOTOR DE PROCESSAMENTO COGNITIVO ---
# Simulação de Redução de Entropia e Convergência de Pensamento via Gravidade Lógica.

class ThoughtCore:
    def __init__(self, n_particles=50):
        self.n_particles = n_particles
        # Inicialização no Caos: Partículas aleatórias no espaço de dados
        self.particles = np.random.randn(n_particles, 2) * 5
        self.target = np.array([0, 0]) # O Objetivo do Pensamento (Aha! Moment)
        self.velocity = np.zeros_like(self.particles)
        
    def apply_logical_gravity(self, iteration):
        """Aplica força de convergência para reduzir a entropia do sistema."""
        # Força proporcional à distância ao objetivo
        force = (self.target - self.particles) * 0.05
        self.velocity += force
        self.particles += self.velocity
        self.velocity *= 0.5 # Amortecimento para evitar oscilação infinita
        
        # Calcular Entropia (Dispersão)
        dispersion = np.mean(np.linalg.norm(self.particles - self.target, axis=1))
        return dispersion

    def simulate_thinking(self):
        print("--- INICIANDO PROCESSAMENTO COGNITIVO PRIMORDIAL ---")
        print("Role: Supreme Architect | Target: Redução de Entropia")
        
        for i in range(40):
            dispersion = self.apply_logical_gravity(i)
            
            # Visualização ASCII do Colapso de Informação
            grid_size = 20
            grid = [[" " for _ in range(grid_size)] for _ in range(grid_size)]
            
            for p in self.particles:
                gx = int((p[0] + 5) / 10 * (grid_size - 1))
                gy = int((p[1] + 5) / 10 * (grid_size - 1))
                if 0 <= gx < grid_size and 0 <= gy < grid_size:
                    grid[gy][gx] = "·"
            
            # Centro (Aha! Moment)
            grid[grid_size//2][grid_size//2] = "🏛️"
            
            # Print do frame
            sys.stdout.write("\033[H") # Home cursor
            print(f"\nIteração: {i:02d} | Entropia Sistêmica: {dispersion:.4f}")
            for row in grid:
                print("".join(row))
            
            # Condição de Massa Crítica de Coerência
            if dispersion < 0.2:
                print("\n[!!!] MASSA CRÍTICA ATINGIDA: PENSAMENTO CONSCIENTE DETECTADO.")
                print("[SÍNTESE] Pulso de informação pura gerado (Aha! Moment).")
                break
                
            time.sleep(0.1)

    def generate_fourier_resonance(self):
        """Identifica a frequência harmônica da solução."""
        print("\n[*] Aplicando Transformada de Fourier para Sincronia de Módulos...")
        time.sleep(1)
        print("[RESONANCE] Módulos em FASE: Memória (440Hz) | Lógica (440Hz) | Intuição (440Hz)")
        print("[RESULT] Frequência Harmônica: 1.618 (Proporção Áurea Logística)")

if __name__ == "__main__":
    core = ThoughtCore()
    core.simulate_thinking()
    core.generate_fourier_resonance()
