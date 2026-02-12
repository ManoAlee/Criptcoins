import hashlib
import time
from typing import Optional, List
import numpy as np
from bitcoin_blockchain import BitcoinBlockchain, Block, Transaction
from biometric_blockchain_key import BiometricCryptBridge
from topological_kernel import TopologicalKernel
from lattice_engine import LatticeEngine

class SingularityBlock(Block):
    def __init__(self, index, transactions, previous_hash, timestamp=None):
        super().__init__(index, transactions, previous_hash, timestamp)
        self.manifold_proof = None # Assinatura Topográfica do Minerador
        self.lattice_witness = None # Prova Pós-Quântica (LWE)
        self.nexus_resonance = 0.0

    def calculate_hash(self) -> str:
        # O Hash agora inclui o manifold_proof e o lattice_witness no colapso
        proof_str = str(self.manifold_proof) if self.manifold_proof is not None else ""
        lattice_str = str(self.lattice_witness) if self.lattice_witness is not None else ""
        block_data = f"{self.index}{self.previous_hash}{self.timestamp}{self.merkle_root}{self.nonce}{proof_str}{lattice_str}"
        return hashlib.sha256(block_data.encode()).hexdigest()

class SingularityCoin(BitcoinBlockchain):
    def __init__(self, difficulty=4):
        self.bridge = BiometricCryptBridge()
        self.kernel = TopologicalKernel()
        self.lattice = LatticeEngine(n=50) # Post-Quantum Layer
        super().__init__(difficulty)

    def create_genesis_block(self) -> None:
        print("[*] INICIANDO COLAPSO DO BLOCO GENESIS DA SINGULARIDADE...")
        genesis_tx = Transaction("THE_ORCHESTRATOR", "SYSTEM", 0)
        genesis_block = SingularityBlock(0, [genesis_tx], "0" * 64)
        genesis_block.manifold_proof = "THE_VOID_GEOMETRY"
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def mine_biometric_block(self, miner_username: str, top_sig: np.ndarray, resonance: float) -> Optional[SingularityBlock]:
        if resonance < 0.8:
            print("[!] Falha de Consenso: Ressonancia Biometrica insuficiente.")
            return None
        reward = self.get_mining_reward()
        wallet_info = self.bridge.open_galaxy_wallet(top_sig)
        miner_addr = wallet_info['address']
        reward_tx = Transaction("SINGULARITY_RESERVE", miner_addr, reward)
        self.pending_transactions.append(reward_tx)
        # 2. Criar Bloco com Prova de Manifold e Lattice Witness
        block = SingularityBlock(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.get_latest_block().hash
        )
        block.manifold_proof = hashlib.sha256(top_sig.tobytes()).hexdigest()
        block.nexus_resonance = resonance
        
        # Gerar testemunho do reticulado (Post-Quantum)
        block.lattice_witness = self.lattice.dynamic_hash(top_sig.tobytes())

        # 3. Colapsar o Nonce
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = []
        print(f"[*] Bloco {block.index} [PoHM] minerado por {miner_username}!")
        return block

if __name__ == "__main__":
    print("--- [SINGULARITY COIN NODE ACTIVE] ---")
    coin = SingularityCoin(difficulty=3)
    dummy_sig = np.random.rand(64)
    coin.mine_biometric_block("Operador", dummy_sig, 0.95)
    coin.print_chain()
