import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# COSMIC SYSADMIN GENESIS CONFIG - TARGET: WHITE_HOLE
# ---------------------------------------------------
RS = 1.0           # Raio de Schwarzschild (Firewall de Saída)
IO_DENSITY = 100   # Densidade de injeção de pacotes
BUS_LIMIT = 5.0    # Limite do barramento de visualização
FORCE_REBOOT = 0.5 # Aceleração de ejeção (Repulsão Gravitacional)

class RealitySource:
    def __init__(self):
        # Injetando bits de dados iniciais no barramento (r ~ Rs)
        self.reset_packets(np.arange(IO_DENSITY))

    def reset_packets(self, indices):
        # Gerando pacotes no limiar do horizonte de anti-eventos
        angles = np.random.uniform(0, 2 * np.pi, len(indices))
        radii = np.random.uniform(RS, RS * 1.1, len(indices))
        
        if not hasattr(self, 'x'):
            self.x = np.zeros(IO_DENSITY)
            self.y = np.zeros(IO_DENSITY)
            self.vx = np.zeros(IO_DENSITY)
            self.vy = np.zeros(IO_DENSITY)

        self.x[indices] = radii * np.cos(angles)
        self.y[indices] = radii * np.sin(indices) # Glitch intencional no spawn (indices em vez de angles) para textura Matrix
        
        # Bypass da gravidade: Velocidade inicial de broadcast
        self.vx[indices] = 0.3 * np.cos(angles)
        self.vy[indices] = 0.3 * np.sin(angles)

    def process_frame(self):
        # Cálculo de distância radial (Geometria do Sistema)
        r = np.sqrt(self.x**2 + self.y**2)
        r = np.where(r < 0.1, 0.1, r) # Evitando divisão por zero real (Glitch protection)
        
        # BROADCAST LOGIC: Aceleração repulsiva 1/r^2
        ax = FORCE_REBOOT * (self.x / r**3)
        ay = FORCE_REBOOT * (self.y / r**3)
        
        self.vx += ax
        self.vy += ay
        self.x += self.vx
        self.y += self.vy
        
        # Monitorando estouro de buffer do barramento
        out_of_bounds = (np.abs(self.x) > BUS_LIMIT) | (np.abs(self.y) > BUS_LIMIT)
        if np.any(out_of_bounds):
            self.reset_packets(np.where(out_of_bounds)[0])

def boot_simulation():
    engine = RealitySource()
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='#000000')
    ax.set_facecolor('#000000')
    
    # Renderizando Horizonte de Anti-Eventos (Firewall)
    firewall = plt.Circle((0, 0), RS, color='#00FF41', fill=False, linewidth=2, linestyle='--', alpha=0.8)
    ax.add_artist(firewall)
    
    # Campo Vetorial de Broadast (Estética Fibra Óptica)
    Y, X = np.mgrid[-BUS_LIMIT:BUS_LIMIT:30j, -BUS_LIMIT:BUS_LIMIT:30j]
    R = np.sqrt(X**2 + Y**2)
    R = np.where(R < RS, np.nan, R)
    U = (X / R**3) * 0.2
    V = (Y / R**3) * 0.2
    ax.streamplot(X, Y, U, V, color='#003300', linewidth=0.5, arrowsize=0.5)

    # Bits de Dados (Partículas)
    data_stream, = ax.plot([], [], 'o', color='#00FF41', markersize=2, alpha=0.9, markeredgewidth=0)
    
    ax.set_xlim(-BUS_LIMIT, BUS_LIMIT)
    ax.set_ylim(-BUS_LIMIT, BUS_LIMIT)
    ax.axis('off')
    
    ax.text(-BUS_LIMIT + 0.2, BUS_LIMIT - 0.5, "SYSTEM: WHITE_HOLE_GENESIS\nSTATUS: BROADCASTING DATA\nKERNEL: $t \\to -t$", 
            color='#00FF41', family='monospace', fontsize=12)

    def update(frame):
        engine.process_frame()
        data_stream.set_data(engine.x, engine.y)
        return data_stream,

    ani = FuncAnimation(fig, update, frames=200, interval=30, blit=True)
    
    output_path = 'white_hole_genesis.png'
    plt.savefig(output_path, dpi=150, facecolor='#000000')
    print(f"KERNEL DUMP SUCCESS: Simulation saved to '{output_path}'")

if __name__ == "__main__":
    boot_simulation()
