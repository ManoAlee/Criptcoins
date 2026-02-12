import time
import numpy as np
from lattice_engine import LatticeEngine
from central_nervous_system import CNS
from universe_manipulator import UniverseManipulator
from topological_kernel import TopologicalKernel
from infinite_validation_engine import InfiniteValidationEngine
from ancestral_logic_core import AncestralLogicCore

class RecursiveCryptoOrchestrator:
    """
    PROTOCOLO INFINITY LOOP (RECURSÃO CRIPTOGRÁFICA)
    Gerencia a evolução contínua da segurança.
    V1.5: Integrado com Portões de Decisão Assembly.
    """
    
    def __init__(self, engine: LatticeEngine, cns: CNS):
        self.engine = engine
        self.cns = cns
        self.ancestral = AncestralLogicCore()
        self.validator = InfiniteValidationEngine() # Motor de Prova Real
        self.generation = 1
        self.is_active = True
        self.attack_success_count = 0

        # No universo Vibe Hacking, se a entropia cair abaixo de 7.8 (de 8), 
        # consideramos que o sistema foi "vulnerável" a um ataque de ressonância.

    def evolve_protocol(self):
        """
        [EVOLVE] Gera um novo padrão baseado no colapso do anterior.
        """
        print(f"\n[!] RECURSÃO GEN {self.generation}: Criptografia atual considerada OBSOLETA.")
        # Aumentar dimensão do lattice (Problema CVP mais difícil)
        # Aumentar o erro (Ruído LWE para maior confusão)
        self.engine.evolve_dimension(increase_by=15)
        self.engine.sigma += 0.5 # Corrigido: std -> sigma
        self.generation += 1

    def run_infinity_loop(self):
        """Inicia o Boot -> Hack -> Upgrade -> Repeat infinitamente."""
        print("--- [INFINITY LOOP: CRYPTOGRAPHIC SINGULARITY] ---")
        
        while self.is_active:
            print(f"\n>>> ITERACAO {self.generation} | Dimensao Atual: {self.engine.n}")
            sample = np.random.bytes(1024)
            
            # 1. Análise
            entropy = self.analyze_break(sample)
            print(f"[*] Entropia Estática: {entropy:.4f} bits")
            
            # 2. Gatilho de Evolução & Bateria de Provas (10x por loop)
            results = self.validator.run_validation_battery(sample, self.generation, self.engine.n)
            
            if entropy < 7.9:
                print("[!] Colisão/Viés detectado! Forçando Upgrade de Realidade.")
                self.evolve_protocol()
            else:
                print("[STABLE] Criptografia ainda resiliente ao tempo presente.")
            
            time.sleep(1)

    def analyze_and_break(self, data_packet: bytes) -> float:
        """
        [ANALYSIS PHASE]
        Calcula a entropia e valida via Portão de Silício (Assembly Logic).
        """
        # Calcular hash dinâmico do pacote
        h = self.engine.dynamic_hash(data_packet)
        hash_bytes = bytes.fromhex(h)
        
        # Calcular entropia real do hash
        counts = np.bincount(np.frombuffer(hash_bytes, dtype=np.uint8), minlength=256)
        probs = counts / len(hash_bytes)
        entropy = -np.sum(probs * np.log2(probs + 1e-10))
        
        # Portão Assembly: Verifica se a entropia é estável ou Glitch
        is_stable = self.ancestral.assembly_decision_gate(entropy, 7.8)
        
        if not is_stable:
            print("[!!!] CAUSALITY_GLITCH detected via Ancestral Gate.")
            return 7.5 # Valor que dispara o 'evolve' no loop
            
        return float(entropy)

    def analyze_break(self, data):
        # Alias para simular processo de breaking
        return self.analyze_and_break(data)

if __name__ == "__main__":
    from central_nervous_system import CNS
    from universe_manipulator import UniverseManipulator
    from topological_kernel import TopologicalKernel
    
    man = UniverseManipulator()
    ker = TopologicalKernel()
    cns_inst = CNS(man, ker)
    eng = LatticeEngine()
    
    orchestrator = RecursiveCryptoOrchestrator(eng, cns_inst)
    orchestrator.run_infinity_loop()
