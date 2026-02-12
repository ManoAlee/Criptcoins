import numpy as np
import time
import sys
import io
import math
import random

# Suporte UTF-8 para Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class EntropyOptimizer:
    """
    --- ENTROPY_OPTIMIZER.PY: DECAY_DYNAMICS ---
    Role: Entropic Engineer // personification of the Second Law
    Objective: Crystallize Order from Chaos via Simulated Annealing
    """
    def __init__(self):
        self.temperature = 100.0
        self.cooling_rate = 0.95
        self.state = 0.0 # Estado inicial (Caos)
        self.target = 1.61803398875 # Proporção Áurea (A Meta)
        self.energy = float('inf')

    def calculate_energy(self, current_state):
        """Calcula quão longe estamos da perfeição axiomática."""
        return abs(current_state - self.target)

    def transition_probability(self, new_energy, old_energy, temp):
        """Lógica de Boltzmann para aceitar estados piores (evitar mínimos locais)."""
        if new_energy < old_energy:
            return 1.0
        return math.exp((old_energy - new_energy) / temp)

    def run_annealing(self):
        print("--- [ENTROPY_ENGINEER] INICIANDO DISSIPAÇÃO LÓGICA ---")
        print(f"Temperatura Inicial: {self.temperature} | Alvo: {self.target}\n")
        
        step = 0
        while self.temperature > 0.01:
            step += 1
            # Gerar uma "mutação" estocástica (ruído)
            noise = random.uniform(-self.temperature / 10, self.temperature / 10)
            candidate_state = self.state + noise
            
            new_energy = self.calculate_energy(candidate_state)
            old_energy = self.calculate_energy(self.state)
            
            # Decisão baseada na Segunda Lei da Termodinâmica
            if self.transition_probability(new_energy, old_energy, self.temperature) > random.random():
                self.state = candidate_state
                self.energy = new_energy
            
            # Resfriamento Simulado
            self.temperature *= self.cooling_rate
            
            # Mudança de visualização baseada na entropia (Dissipação)
            entropy_bar = "▓" * int(self.temperature / 2) + "░" * (50 - int(self.temperature / 2))
            sys.stdout.write(f"\r[PASSO {step:03d}] TEMP: {self.temperature:7.3f} | STATE: {self.state:.5f} | ENERGY: {self.energy:.5f} | {entropy_bar}")
            sys.stdout.flush()
            
            time.sleep(0.1)
            
        print(f"\n\n[CRISTALIZAÇÃO] SUCESSO. Estado estável encontrado em {step} passos.")
        print(f"[!] ESTADO FINAL: {self.state:.10f} (ERRO: {self.energy:.10f})")
        print("[!] A desordem serviu ao propósito. A estrutura emergiu do vácuo.")

if __name__ == "__main__":
    optimizer = EntropyOptimizer()
    optimizer.run_annealing()
