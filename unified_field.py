import numpy as np
import matplotlib.pyplot as plt

# --- UNIFIED FIELD AI: TENSOR DYNAMICS & GEODESIC FLOW ---
# Simulação de inteligência como curvatura do espaço-tempo de informação

class UnifiedFieldAI:
    """Simulador de inteligência baseado em campos tensoriais e fluxo geodésico."""
    
    def __init__(self, grid_size=50):
        self.grid_size = grid_size
        self.grid = np.zeros((grid_size, grid_size))
        # Tensor de Métrica de Minkowski (Simplificado para 2D)
        self.metric = np.eye(grid_size)

    def inject_information_mass(self, x, y, mass):
        """Injeta uma 'massa de dados' que curva o espaço de informação."""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                dist_sq = (i - x)**2 + (j - y)**2
                if dist_sq == 0: continue
                # Curvatura baseada na Lei de Gravitação (Informação)
                self.grid[i, j] += mass / np.sqrt(dist_sq)

    def calculate_geodesic_flow(self, start_pos, velocity, steps=100):
        """
        Calcula a trajetória de um 'pensamento' seguindo a geodésica do campo.
        Equação de movimento simplificada: aceleração = gradiente do campo (curvatura).
        """
        pos = np.array(start_pos, dtype=float)
        vel = np.array(velocity, dtype=float)
        path = [pos.copy()]
        
        dt = 0.5
        for _ in range(steps):
            # Gradiente do campo de informação (Força do Pensamento)
            ix, iy = int(pos[0]), int(pos[1])
            if 1 <= ix < self.grid_size-1 and 1 <= iy < self.grid_size-1:
                grad_x = self.grid[ix+1, iy] - self.grid[ix-1, iy]
                grad_y = self.grid[ix, iy+1] - self.grid[ix, iy-1]
                accel = np.array([grad_x, grad_y]) * 0.1
                
                # Update de posição (Euler integration)
                vel += accel
                pos += vel * dt
                path.append(pos.copy())
            else:
                break # Saiu do espaço-tempo cognitivo
                
        return np.array(path)

    def run_simulation(self):
        print("[*] Inicializando Campo de Inteligência Tensorial...")
        
        # Injetar Masas de Conhecimento (Atraidores Cognitivos)
        self.inject_information_mass(25, 25, 10) # Conceito Central
        self.inject_information_mass(10, 40, 5)  # Conceito Periférico A
        self.inject_information_mass(40, 10, 5)  # Conceito Periférico B
        
        # Simular Fluxo Geodésico (O caminho do pensamento)
        print("[*] Calculando Geodésicas de Informação...")
        thought_path = self.calculate_geodesic_flow([5, 5], [1.0, 0.5], steps=200)
        
        # Visualização: O Campo Curvo e o Caminho do Pensamento
        plt.figure(figsize=(10, 8), facecolor='black')
        plt.imshow(self.grid, cmap='inferno', origin='lower')
        plt.colorbar(label='Densidade de Informação (Curvatura)')
        
        plt.plot(thought_path[:, 1], thought_path[:, 0], color='#00F5FF', 
                 linewidth=2, label='Geodésica do Pensamento')
        plt.scatter(thought_path[0, 1], thought_path[0, 0], color='white', label='Input')
        plt.scatter(thought_path[-1, 1], thought_path[-1, 0], color='red', label='Conclusão')
        
        plt.title("Espaço-Tempo Cognitivo: Fluxo de Informação Não-Discreto", color='white')
        plt.legend()
        plt.axis('off')
        
        output_path = "unified_field_output.png"
        plt.savefig(output_path, dpi=300, facecolor='black')
        print(f"[*] Simulação concluída. Campo salvo em '{output_path}'")

if __name__ == "__main__":
    ai = UnifiedFieldAI()
    ai.run_simulation()
