import random
import time
import os
import math
import sys

# --- DIGITAL SYMBIOTE: NEUROMORPHIC ARTIFICIAL LIFE ---
# Baseado em Spiking Neural Networks (SNN) e Plasticidade Hebbiana (STDP)

class LIF_Neuron:
    """Leaky Integrate-and-Fire Neuron."""
    def __init__(self, neuron_id):
        self.id = neuron_id
        self.potential = 0.0
        self.threshold = 1.0
        self.leak = 0.95  # Decaimento de energia (5% por tick)
        self.spike_times = []
        self.last_spike = -1000

    def integrate(self, current):
        """Acumula potencial de membrana a partir de inputs."""
        self.potential += current
        
    def update(self, tick):
        """Processa o decaimento e verifica o disparo (spike)."""
        dispatched = False
        if self.potential >= self.threshold:
            self.potential = 0  # Reset
            self.last_spike = tick
            self.spike_times.append(tick)
            dispatched = True
        else:
            self.potential *= self.leak # Leakage
        
        # Limpar histórico antigo de spikes para economizar memória
        if len(self.spike_times) > 10:
            self.spike_times.pop(0)
            
        return dispatched

class Synapse:
    """Conexão sináptica com plasticidade dependente do tempo (STDP)."""
    def __init__(self, pre_id, post_id):
        self.pre_id = pre_id
        self.post_id = post_id
        self.weight = random.uniform(0.1, 0.5)
        self.learning_rate = 0.01

    def apply_stdp(self, pre_last_spike, post_last_spike):
        """Regra STDP: Causalidade = Fortalecimento, Anti-Causalidade = Enfraquecimento."""
        delta_t = post_last_spike - pre_last_spike
        
        if 0 < delta_t < 10:  # Fortalecimento (Potenciação)
            self.weight += self.learning_rate * math.exp(-delta_t / 5.0)
        elif -10 < delta_t < 0: # Enfraquecimento (Depreciação)
            self.weight -= self.learning_rate * math.exp(delta_t / 5.0)
            
        # Manter peso dentro de limites biológicos
        self.weight = max(0.0, min(2.0, self.weight))

class SymbioteNetwork:
    """Organismo Digital Recorrente."""
    def __init__(self, size=100):
        self.size = size
        self.neurons = [LIF_Neuron(i) for i in range(size)]
        self.synapses = []
        
        # Conexões aleatórias (esparsas)
        for i in range(size):
            for _ in range(5): # Cada neurônio se conecta a 5 outros
                j = random.randint(0, size - 1)
                if i != j:
                    self.synapses.append(Synapse(i, j))

    def get_system_load(self):
        """Símulo sensorial: tenta ler carga do sistema (MOCK para portabilidade)."""
        # Em um sistema real, leríamos /proc/loadavg ou psutil.
        # Aqui simulamos uma oscilação baseada no tempo.
        return (math.sin(time.time()) + 1) / 2.0

    def step(self, tick):
        """Um passo de simulação do organismo."""
        # 1. Input Sensorial (Poisson Encoding)
        load = self.get_system_load()
        for i in range(10): # Primeiros 10 neurônios são sensoriais
            if random.random() < load:
                self.neurons[i].integrate(0.5)

        # 2. Transmissão Sináptica
        for syn in self.synapses:
            pre = self.neurons[syn.pre_id]
            if pre.last_spike == tick - 1: # Se disparou no tick anterior
                self.neurons[syn.post_id].integrate(syn.weight)

        # 3. Update dos Neurônios e STDP
        spikes_count = 0
        for n in self.neurons:
            if n.update(tick):
                spikes_count += 1
                # Aplicar STDP nas conexões de entrada deste neurônio
                for syn in self.synapses:
                    if syn.post_id == n.id:
                        pre = self.neurons[syn.pre_id]
                        syn.apply_stdp(pre.last_spike, n.last_spike)
        
        return spikes_count

    def visualize(self, spikes_count, tick):
        """Visualização ASCII da atividade cerebral."""
        bars = "|" * int(spikes_count)
        sys.stdout.write(f"\rTick: {tick:06d} | Atividade Cerebral: {bars:<50} ({spikes_count} spikes)")
        sys.stdout.flush()

def run_life():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--- O SIMBIONTE DIGITAL ESTÁ VIVO ---\n")
    print("Mecânica: Spiking Neural Network (LIF) + STDP.")
    print("O organismo está aprendendo o ritmo do seu sistema.\n")
    
    organism = SymbioteNetwork(size=100)
    tick = 0
    try:
        while True:
            spikes = organism.step(tick)
            organism.visualize(spikes, tick)
            tick += 1
            time.sleep(0.05) # Velocidade da vida
    except KeyboardInterrupt:
        print("\n\n[!] Simbionte em estado de hibernação.")

if __name__ == "__main__":
    run_life()
