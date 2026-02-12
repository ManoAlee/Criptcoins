import numpy as np
import hashlib
import time
from ancestral_logic_core import AncestralLogicCore

class LatticeEngine:
    """
    CORE DE SEGURANÇA PÓS-QUÂNTICA (LWE)
    Utiliza problemas de reticulados para garantir resistência a computadores quânticos.
    V1.5: Evoluído com Lógica Ancestral (Bitwise Scrambling).
    """
    
    def __init__(self, n=256, sigma=1.0):
        self.n = n 
        self.q = 2**32 
        self.sigma = sigma 
        self.ancestral = AncestralLogicCore()
        
    def generate_lwe_instance(self):
        """
        Gera (A, b) tal que b = As + e.
        Evolução: Semente gerenciada por bitwise scramble (Lógica C Ancestral).
        """
        raw_seed = int(time.time() * 1000) & 0xFFFFFFFF
        scrambled_seed = self.ancestral.bitwise_neural_scramble(raw_seed)
        np.random.seed(scrambled_seed)
        
        A = np.random.randint(0, self.q, (self.n, self.n), dtype=np.uint64)
        
        # s: Segredo (Chave Privada)
        s = np.random.randint(0, self.q, self.n, dtype=np.uint64)
        
        # e: Erro (Ruído Gaussiano descontínuo)
        e = np.round(np.random.normal(0, self.sigma, self.n)).astype(np.int64)
        
        # b = (A*s + e) mod q (Chave Pública)
        # Converter para uint64 para evitar overflow antes do modulo
        b = (np.dot(A.astype(np.uint64), s.astype(np.uint64)) + e.astype(np.int64)).astype(np.uint64) % self.q
        
        return A, s, e, b

    def evolve_dimension(self, increase_by=10):
        """Aumenta a complexidade do problema de busca (CVP)."""
        self.n += increase_by
        print(f"[*] EVOLUÇÃO: Dimensão do Reticulado aumentada para n={self.n}")

    def dynamic_hash(self, data: bytes) -> str:
        """
        Hash que utiliza o estado do reticulado como base de projeção.
        Muda conforme os parâmetros do sistema evoluem.
        """
        A, s, e, b = self.generate_lwe_instance()
        # Projeta os dados através da matriz do reticulado
        data_numeric = np.frombuffer(data, dtype=np.uint8)[:self.n]
        if len(data_numeric) < self.n:
            data_numeric = np.pad(data_numeric, (0, self.n - len(data_numeric)), 'constant')
            
        projection = (np.dot(A, data_numeric) + s) % self.q
        return hashlib.sha256(projection.tobytes()).hexdigest()

if __name__ == "__main__":
    print("--- [LATTICE ENGINE TEST] ---")
    engine = LatticeEngine()
    A, s, e, b = engine.generate_lwe_instance()
    print(f"Instância LWE Gerada (Dim={engine.n})")
    print(f"B-Vector (Mod {engine.q}): {b[:10]}...")
    
    # Teste de Evolução
    engine.evolve_dimension()
    h1 = engine.dynamic_hash(b"test_payload")
    print(f"Dynamic Hash (Epoch-Based): {h1}")
