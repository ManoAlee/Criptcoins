import hashlib
import json
import time
from typing import List, Dict, Any, Optional
import numpy as np

# --- BITCOIN BLOCKCHAIN CORE ---
# Implementação de blockchain inspirada no Bitcoin
# Integrado com o sistema genesis/matrix

class Transaction:
    """Transação criptográfica com assinatura digital."""
    
    def __init__(self, sender: str, recipient: str, amount: float, timestamp: Optional[float] = None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp or time.time()
        self.signature = None
        self.tx_hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calcula hash SHA-256 da transação."""
        tx_data = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}"
        return hashlib.sha256(tx_data.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'tx_hash': self.tx_hash,
            'signature': self.signature
        }


class Block:
    """Bloco da blockchain com Proof of Work."""
    
    def __init__(self, index: int, transactions: List[Transaction], 
                 previous_hash: str, timestamp: Optional[float] = None):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.merkle_root = self.calculate_merkle_root()
        self.hash = None
    
    def calculate_merkle_root(self) -> str:
        """Calcula Merkle Root das transações (como no Bitcoin)."""
        if not self.transactions:
            return hashlib.sha256(b'').hexdigest()
        
        tx_hashes = [tx.tx_hash for tx in self.transactions]
        
        while len(tx_hashes) > 1:
            if len(tx_hashes) % 2 != 0:
                tx_hashes.append(tx_hashes[-1])
            
            new_hashes = []
            for i in range(0, len(tx_hashes), 2):
                combined = tx_hashes[i] + tx_hashes[i + 1]
                new_hash = hashlib.sha256(combined.encode()).hexdigest()
                new_hashes.append(new_hash)
            
            tx_hashes = new_hashes
        
        return tx_hashes[0]
    
    def calculate_hash(self) -> str:
        """Calcula hash do bloco."""
        block_data = f"{self.index}{self.previous_hash}{self.timestamp}{self.merkle_root}{self.nonce}"
        return hashlib.sha256(block_data.encode()).hexdigest()
    
    def mine_block(self, difficulty: int) -> None:
        """Minera o bloco com Proof of Work (como no Bitcoin)."""
        target = '0' * difficulty
        print(f"[*] Minerando bloco #{self.index} (dificuldade: {difficulty})...")
        
        start_time = time.time()
        while not self.hash or not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
            
            if self.nonce % 100000 == 0:
                print(f"  Nonce: {self.nonce:,} | Hash: {self.hash[:20]}...")
        
        elapsed = time.time() - start_time
        print(f"[*] Bloco minerado! Nonce: {self.nonce:,} | Tempo: {elapsed:.2f}s")
        print(f"    Hash: {self.hash}")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'index': self.index,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'merkle_root': self.merkle_root,
            'hash': self.hash
        }


class BitcoinBlockchain:
    """Blockchain completa com consenso Proof of Work."""
    
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Transaction] = []
        self.mining_reward = 50.0
        self.halving_interval = 210000  # Como no Bitcoin
        
        # Genesis Block
        self.create_genesis_block()
    
    def create_genesis_block(self) -> None:
        """Cria o bloco gênesis (primeiro bloco)."""
        print("[*] CRIANDO GENESIS BLOCK...")
        genesis_tx = Transaction(
            sender="GENESIS",
            recipient="SYSTEM",
            amount=0,
            timestamp=1231006505  # Timestamp do Genesis Block real do Bitcoin
        )
        genesis_block = Block(0, [genesis_tx], "0" * 64, timestamp=1231006505)
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        print("[*] Genesis Block criado!")
    
    def get_latest_block(self) -> Block:
        """Retorna o último bloco da cadeia."""
        return self.chain[-1]
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """Adiciona transação ao pool de transações pendentes."""
        if not transaction.sender or not transaction.recipient:
            print("[❌] Transação inválida: falta sender ou recipient")
            return False
        
        self.pending_transactions.append(transaction)
        print(f"[*] Transacao adicionada: {transaction.sender[:8]}... -> {transaction.recipient[:8]}... ({transaction.amount})")
        return True
    
    def mine_pending_transactions(self, miner_address: str) -> None:
        """Minera as transações pendentes (cria novo bloco)."""
        if not self.pending_transactions:
            print("[⚠️] Nenhuma transação pendente para minerar - criando bloco apenas com recompensa")
            # Continue: still award mining reward even if there are no pending transactions
        
        # Adiciona recompensa de mineração
        reward = self.get_mining_reward()
        reward_tx = Transaction("SYSTEM", miner_address, reward)
        self.pending_transactions.append(reward_tx)
        
        # Cria novo bloco
        block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.get_latest_block().hash
        )
        
        # Minera o bloco
        block.mine_block(self.difficulty)
        
        # Adiciona à cadeia
        self.chain.append(block)
        
        print(f"[*] Bloco #{block.index} adicionado a blockchain!")
        print(f"[*] Recompensa mineracao: {reward} BTC -> {miner_address[:16]}...")
        
        # Limpa transações pendentes
        self.pending_transactions = []
    
    def get_mining_reward(self) -> float:
        """Calcula recompensa de mineração com halving."""
        halvings = len(self.chain) // self.halving_interval
        return self.mining_reward / (2 ** halvings)
    
    def is_chain_valid(self) -> bool:
        """Valida a integridade da blockchain."""
        print("\n[🔍] VALIDANDO BLOCKCHAIN...")
        
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verifica hash do bloco
            if current_block.hash != current_block.calculate_hash():
                print(f"[❌] Bloco #{i}: Hash inválido")
                return False
            
            # Verifica ligação com bloco anterior
            if current_block.previous_hash != previous_block.hash:
                print(f"[❌] Bloco #{i}: Ligação quebrada com bloco anterior")
                return False
            
            # Verifica Proof of Work
            if not current_block.hash.startswith('0' * self.difficulty):
                print(f"[❌] Bloco #{i}: Proof of Work inválido")
                return False
            
            # Verifica Merkle Root
            if current_block.merkle_root != current_block.calculate_merkle_root():
                print(f"[❌] Bloco #{i}: Merkle Root inválido")
                return False
        
        print("[✅] Blockchain válida! Integridade: 100%")
        return True
    
    def get_balance(self, address: str) -> float:
        """Calcula saldo de um endereço."""
        balance = 0.0
        
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address:
                    balance -= tx.amount
                if tx.recipient == address:
                    balance += tx.amount
        
        return balance
    
    def print_chain(self) -> None:
        """Imprime a blockchain completa."""
        print("\n" + "="*80)
        print("BLOCKCHAIN COMPLETA".center(80))
        print("="*80)
        
        for block in self.chain:
            print(f"\n🔗 BLOCO #{block.index}")
            print(f"   Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp))}")
            print(f"   Hash: {block.hash}")
            print(f"   Hash Anterior: {block.previous_hash}")
            print(f"   Merkle Root: {block.merkle_root}")
            print(f"   Nonce: {block.nonce:,}")
            print(f"   Transações: {len(block.transactions)}")
            
            for i, tx in enumerate(block.transactions, 1):
                print(f"      {i}. {tx.sender[:8]}... → {tx.recipient[:8]}... | {tx.amount} BTC")
        
        print("\n" + "="*80)
        print(f"Total de blocos: {len(self.chain)}")
        print(f"Dificuldade: {self.difficulty}")
        print("="*80 + "\n")


def demo_bitcoin_blockchain():
    """Demonstração do sistema blockchain."""
    print("╔" + "="*78 + "╗")
    print("║" + " BITCOIN BLOCKCHAIN INTEGRATION - GENESIS EDITION ".center(78) + "║")
    print("╚" + "="*78 + "╝\n")
    
    # Criar blockchain
    blockchain = BitcoinBlockchain(difficulty=4)
    
    # Endereços
    alice = "Alice_" + hashlib.sha256(b"alice").hexdigest()[:16]
    bob = "Bob_" + hashlib.sha256(b"bob").hexdigest()[:16]
    charlie = "Charlie_" + hashlib.sha256(b"charlie").hexdigest()[:16]
    
    print(f"\n👤 Participantes:")
    print(f"   Alice:   {alice}")
    print(f"   Bob:     {bob}")
    print(f"   Charlie: {charlie}\n")
    
    # Bloco 1: Transações iniciais
    print("\n" + "─"*80)
    print("📦 BLOCO #1: Transações Iniciais")
    print("─"*80)
    blockchain.add_transaction(Transaction(alice, bob, 25.0))
    blockchain.add_transaction(Transaction(bob, charlie, 10.0))
    blockchain.mine_pending_transactions(alice)
    
    # Bloco 2: Mais transações
    print("\n" + "─"*80)
    print("📦 BLOCO #2: Segunda Rodada")
    print("─"*80)
    blockchain.add_transaction(Transaction(charlie, alice, 5.0))
    blockchain.add_transaction(Transaction(alice, bob, 15.0))
    blockchain.add_transaction(Transaction(bob, charlie, 8.0))
    blockchain.mine_pending_transactions(bob)
    
    # Bloco 3: Consolidação
    print("\n" + "─"*80)
    print("📦 BLOCO #3: Consolidação")
    print("─"*80)
    blockchain.add_transaction(Transaction(charlie, bob, 20.0))
    blockchain.mine_pending_transactions(charlie)
    
    # Imprimir blockchain
    blockchain.print_chain()
    
    # Validar blockchain
    blockchain.is_chain_valid()
    
    # Mostrar saldos
    print("\n💰 SALDOS FINAIS:")
    print(f"   Alice:   {blockchain.get_balance(alice):.2f} BTC")
    print(f"   Bob:     {blockchain.get_balance(bob):.2f} BTC")
    print(f"   Charlie: {blockchain.get_balance(charlie):.2f} BTC")
    
    return blockchain


if __name__ == "__main__":
    demo_bitcoin_blockchain()
