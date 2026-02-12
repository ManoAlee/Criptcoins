import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Configurações da Simulação do Buraco Branco (Astro-Computacional Antigravity)
RS = 1.0  # Raio de Schwarzschild (Normalizado)
NUM_PARTICULAS = 50
TEMPO_SIM = 100
DR_REPULSAO = 0.2 # Força de aceleração repulsiva

class WhiteHoleSim:
    def __init__(self):
        # Spawna partículas logo acima do horizonte de anti-eventos (r > Rs)
        angles = np.random.uniform(0, 2 * np.pi, NUM_PARTICULAS)
        radii = np.random.uniform(RS, RS + 0.1, NUM_PARTICULAS)
        
        self.x = radii * np.cos(angles)
        self.y = radii * np.sin(angles)
        
        # Velocidade inicial puramente radial para fora
        self.vx = 0.5 * np.cos(angles)
        self.vy = 0.5 * np.sin(angles)

    def update(self):
        r = np.sqrt(self.x**2 + self.y**2)
        
        # Lógica de Campo Repulsivo (Simetria-T do Buraco Negro)
        # No Buraco Branco, a "gravidade" age como uma força de ejeção para r > Rs
        ax = DR_REPULSAO * (self.x / r**3)
        ay = DR_REPULSAO * (self.y / r**3)
        
        self.vx += ax
        self.vy += ay
        self.x += self.vx
        self.y += self.vy
        
        # Reset de partículas que saem do campo de visão (Simulando fluxo contínuo)
        mask_out = (np.abs(self.x) > 10) | (np.abs(self.y) > 10)
        num_reset = np.sum(mask_out)
        if num_reset > 0:
            angles = np.random.uniform(0, 2 * np.pi, num_reset)
            self.x[mask_out] = RS * np.cos(angles)
            self.y[mask_out] = RS * np.sin(angles)
            self.vx[mask_out] = 0.2 * np.cos(angles)
            self.vy[mask_out] = 0.2 * np.sin(angles)

def animate_sim():
    sim = WhiteHoleSim()
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='#0D0D0D')
    ax.set_facecolor('#0D0D0D')
    
    # Desenha o Horizonte de Anti-Eventos (Zona Proibida de Entrada)
    circle = plt.Circle((0, 0), RS, color='#00F5FF', fill=True, alpha=0.3, label='Anti-Event Horizon')
    ax.add_artist(circle)
    
    # Grid de Campo Vetorial (Repulsão)
    Y, X = np.mgrid[-5:5:20j, -5:5:20j]
    R = np.sqrt(X**2 + Y**2)
    U = (X / R**3) * 0.5
    V = (Y / R**3) * 0.5
    ax.quiver(X, Y, U, V, color='#BD93F9', alpha=0.4)

    particles, = ax.plot([], [], 'o', color='#FF6E6E', markersize=3, label='Matter Ejection')
    
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.axis('off')
    ax.set_title("SIMULAÇÃO DE BURACO BRANCO: LOCAL BIG BANG", color='#00F5FF', fontsize=14)
    ax.legend(facecolor='#0D0D0D', edgecolor='#00F5FF', labelcolor='white')

    def update_plot(frame):
        sim.update()
        particles.set_data(sim.x, sim.y)
        return particles,

    ani = FuncAnimation(fig, update_plot, frames=TEMPO_SIM, interval=50, blit=True)
    plt.savefig('white_hole_simulation.png')
    print("Simulação salva em 'white_hole_simulation.png'")
    # plt.show() # Desativado para ambiente agentic

if __name__ == "__main__":
    animate_sim()
