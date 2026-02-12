#!/usr/bin/env python3
"""
GALAXY BITCOIN SYSTEM - Visualização Gráfica
Cria visualizações da blockchain, rede e transações
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import numpy as np
import networkx as nx
from typing import List, Dict
import time

try:
    from bitcoin_blockchain import BitcoinBlockchain, Transaction
    from bitcoin_crypto import BitcoinWallet
except ImportError:
    print("[⚠️] Módulos Bitcoin não encontrados. Execute install_and_test.py primeiro.")


class BlockchainVisualizer:
    """Visualizador gráfico de blockchain."""
    
    def __init__(self, blockchain: BitcoinBlockchain):
        self.blockchain = blockchain
        self.fig = None
        self.ax = None
    
    def visualize_chain(self, save_path: str = "blockchain_visual.png"):
        """Visualiza a blockchain completa."""
        num_blocks = len(self.blockchain.chain)
        
        fig, ax = plt.subplots(figsize=(16, 10))
        ax.set_xlim(-0.5, num_blocks + 0.5)
        ax.set_ylim(-1, 6)
        ax.axis('off')
        
        # Título
        fig.suptitle('🔗 GALAXY BITCOIN BLOCKCHAIN', 
                     fontsize=20, fontweight='bold', y=0.98)
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        
        for i, block in enumerate(self.blockchain.chain):
            color = colors[i % len(colors)]
            
            # Desenhar bloco
            box = FancyBboxPatch(
                (i, 2), 0.8, 2.5,
                boxstyle="round,pad=0.1",
                facecolor=color,
                edgecolor='black',
                linewidth=2,
                alpha=0.8
            )
            ax.add_patch(box)
            
            # Número do bloco
            ax.text(i + 0.4, 4.2, f'BLOCO #{block.index}',
                   ha='center', va='center', fontsize=11, fontweight='bold')
            
            # Hash
            hash_short = block.hash[:8] + "..." if block.hash else "Genesis"
            ax.text(i + 0.4, 3.8, f'Hash: {hash_short}',
                   ha='center', va='center', fontsize=8, family='monospace')
            
            # Nonce
            ax.text(i + 0.4, 3.4, f'Nonce: {block.nonce:,}',
                   ha='center', va='center', fontsize=8)
            
            # Transações
            tx_count = len(block.transactions)
            ax.text(i + 0.4, 3.0, f'TX: {tx_count}',
                   ha='center', va='center', fontsize=8)
            
            # Timestamp
            timestamp = time.strftime('%H:%M:%S', time.localtime(block.timestamp))
            ax.text(i + 0.4, 2.6, timestamp,
                   ha='center', va='center', fontsize=7, style='italic')
            
            # Seta para próximo bloco
            if i < num_blocks - 1:
                arrow = FancyArrowPatch(
                    (i + 0.8, 3.25), (i + 1, 3.25),
                    arrowstyle='->,head_width=0.4,head_length=0.2',
                    color='black',
                    linewidth=2,
                    zorder=10
                )
                ax.add_patch(arrow)
        
        # Legenda
        legend_y = 0.5
        ax.text(num_blocks / 2, legend_y, 
               f'Total: {num_blocks} blocos | Dificuldade: {self.blockchain.difficulty}',
               ha='center', va='center', fontsize=12,
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"[✅] Visualização salva em: {save_path}")
        
        return fig
    
    def visualize_transaction_flow(self, save_path: str = "transaction_flow.png"):
        """Visualiza fluxo de transações entre endereços."""
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Coletar todas as transações
        addresses = set()
        edges = []
        
        for block in self.blockchain.chain:
            for tx in block.transactions:
                addresses.add(tx.sender)
                addresses.add(tx.recipient)
                edges.append((tx.sender, tx.recipient, tx.amount))
        
        # Criar grafo
        G = nx.DiGraph()
        
        for sender, recipient, amount in edges:
            if G.has_edge(sender, recipient):
                G[sender][recipient]['weight'] += amount
            else:
                G.add_edge(sender, recipient, weight=amount)
        
        # Layout
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Desenhar nós
        node_colors = []
        for node in G.nodes():
            if node == "GENESIS" or node == "SYSTEM":
                node_colors.append('#FFD700')  # Dourado
            else:
                node_colors.append('#4ECDC4')  # Azul claro
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                              node_size=2000, alpha=0.9, ax=ax)
        
        # Desenhar arestas
        edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
        max_weight = max(edge_weights) if edge_weights else 1
        
        edge_colors = ['#FF6B6B' if w > max_weight/2 else '#FFA07A' 
                      for w in edge_weights]
        
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors,
                              width=[w/max_weight*5 for w in edge_weights],
                              alpha=0.6, arrows=True, arrowsize=20,
                              connectionstyle='arc3,rad=0.1', ax=ax)
        
        # Labels
        labels = {}
        for node in G.nodes():
            if node == "GENESIS" or node == "SYSTEM":
                labels[node] = node
            else:
                labels[node] = node[:8] + "..."
        
        nx.draw_networkx_labels(G, pos, labels, font_size=9,
                               font_weight='bold', ax=ax)
        
        # Edge labels (valores)
        edge_labels = {(u, v): f'{G[u][v]["weight"]:.1f} BTC' 
                      for u, v in G.edges()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels,
                                     font_size=7, ax=ax)
        
        ax.set_title('💸 FLUXO DE TRANSAÇÕES', fontsize=18, fontweight='bold', pad=20)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"[✅] Fluxo de transações salvo em: {save_path}")
        
        return fig
    
    def visualize_mining_stats(self, save_path: str = "mining_stats.png"):
        """Visualiza estatísticas de mineração."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        fig.suptitle('⛏️ ESTATÍSTICAS DE MINERAÇÃO', 
                    fontsize=18, fontweight='bold')
        
        blocks = self.blockchain.chain[1:]  # Excluir genesis
        
        if not blocks:
            return fig
        
        # 1. Nonces por bloco
        nonces = [b.nonce for b in blocks]
        block_nums = [b.index for b in blocks]
        
        ax1.bar(block_nums, nonces, color='#4ECDC4', alpha=0.7)
        ax1.set_xlabel('Bloco')
        ax1.set_ylabel('Nonce')
        ax1.set_title('Nonces por Bloco')
        ax1.grid(True, alpha=0.3)
        
        # 2. Transações por bloco
        tx_counts = [len(b.transactions) for b in blocks]
        
        ax2.plot(block_nums, tx_counts, marker='o', color='#FF6B6B',
                linewidth=2, markersize=8)
        ax2.fill_between(block_nums, tx_counts, alpha=0.3, color='#FF6B6B')
        ax2.set_xlabel('Bloco')
        ax2.set_ylabel('Transações')
        ax2.set_title('Transações por Bloco')
        ax2.grid(True, alpha=0.3)
        
        # 3. Distribuição de nonces
        ax3.hist(nonces, bins=20, color='#45B7D1', alpha=0.7, edgecolor='black')
        ax3.set_xlabel('Nonce')
        ax3.set_ylabel('Frequência')
        ax3.set_title('Distribuição de Nonces')
        ax3.grid(True, alpha=0.3)
        
        # 4. Hash leading zeros (dificuldade)
        leading_zeros = []
        for block in blocks:
            if block.hash:
                zeros = len(block.hash) - len(block.hash.lstrip('0'))
                leading_zeros.append(zeros)
        
        if leading_zeros:
            ax4.scatter(block_nums, leading_zeros, s=100, 
                       color='#FFA07A', alpha=0.7, edgecolors='black')
            ax4.axhline(y=self.blockchain.difficulty, color='red',
                       linestyle='--', label=f'Dificuldade: {self.blockchain.difficulty}')
            ax4.set_xlabel('Bloco')
            ax4.set_ylabel('Leading Zeros')
            ax4.set_title('Zeros Iniciais no Hash')
            ax4.legend()
            ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"[✅] Estatísticas de mineração salvas em: {save_path}")
        
        return fig


def create_demo_blockchain() -> BitcoinBlockchain:
    """Cria blockchain de demonstração."""
    print("[🔨] Criando blockchain de demonstração...")
    
    blockchain = BitcoinBlockchain(difficulty=3)
    
    # Carteiras
    wallets = {}
    for name in ["Alice", "Bob", "Charlie", "Diana"]:
        wallet = BitcoinWallet()
        wallet.create_new_wallet()
        wallets[name] = wallet
    
    # Bloco 1
    print("  [⛏️] Minerando bloco #1...")
    tx1 = Transaction(wallets["Alice"].address, wallets["Bob"].address, 25.0)
    tx2 = Transaction(wallets["Alice"].address, wallets["Charlie"].address, 15.0)
    blockchain.add_transaction(tx1)
    blockchain.add_transaction(tx2)
    blockchain.mine_pending_transactions(wallets["Alice"].address)
    
    # Bloco 2
    print("  [⛏️] Minerando bloco #2...")
    tx3 = Transaction(wallets["Bob"].address, wallets["Diana"].address, 10.0)
    tx4 = Transaction(wallets["Charlie"].address, wallets["Alice"].address, 5.0)
    tx5 = Transaction(wallets["Diana"].address, wallets["Bob"].address, 3.0)
    blockchain.add_transaction(tx3)
    blockchain.add_transaction(tx4)
    blockchain.add_transaction(tx5)
    blockchain.mine_pending_transactions(wallets["Bob"].address)
    
    # Bloco 3
    print("  [⛏️] Minerando bloco #3...")
    tx6 = Transaction(wallets["Alice"].address, wallets["Diana"].address, 20.0)
    tx7 = Transaction(wallets["Bob"].address, wallets["Charlie"].address, 8.0)
    blockchain.add_transaction(tx6)
    blockchain.add_transaction(tx7)
    blockchain.mine_pending_transactions(wallets["Charlie"].address)
    
    print("[✅] Blockchain de demonstração criada!\n")
    
    return blockchain


def main():
    """Função principal."""
    print("╔" + "="*78 + "╗")
    print("║" + " GALAXY BITCOIN SYSTEM - VISUALIZAÇÕES ".center(78) + "║")
    print("╚" + "="*78 + "╝\n")
    
    # Criar blockchain
    blockchain = create_demo_blockchain()
    
    # Validar
    print("[🔍] Validando blockchain...")
    if blockchain.is_chain_valid():
        print("[✅] Blockchain válida!\n")
    else:
        print("[❌] Blockchain inválida!\n")
        return
    
    # Criar visualizador
    visualizer = BlockchainVisualizer(blockchain)
    
    # Gerar visualizações
    print("[🎨] Gerando visualizações...")
    print("  [1/3] Cadeia de blocos...")
    visualizer.visualize_chain()
    
    print("  [2/3] Fluxo de transações...")
    visualizer.visualize_transaction_flow()
    
    print("  [3/3] Estatísticas de mineração...")
    visualizer.visualize_mining_stats()
    
    print("\n[🎉] Todas as visualizações foram geradas!")
    print("\nArquivos criados:")
    print("  - blockchain_visual.png")
    print("  - transaction_flow.png")
    print("  - mining_stats.png")
    
    # Mostrar gráficos
    print("\n[📊] Abrindo visualizações...")
    plt.show()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[🛑] Visualização cancelada")
    except Exception as e:
        print(f"\n[❌] Erro: {e}")
        import traceback
        traceback.print_exc()
