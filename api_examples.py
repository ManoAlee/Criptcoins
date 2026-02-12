#!/usr/bin/env python3
"""
GALAXY BITCOIN SYSTEM - Exemplos de API
Exemplos práticos de como usar cada componente
"""

# ============================================================================
# EXEMPLO 1: Blockchain Básico
# ============================================================================

def example_basic_blockchain():
    """Criar blockchain simples e adicionar transações."""
    from bitcoin_blockchain import BitcoinBlockchain, Transaction
    
    print("="*80)
    print("EXEMPLO 1: BLOCKCHAIN BÁSICO".center(80))
    print("="*80 + "\n")
    
    # Criar blockchain com dificuldade 3
    blockchain = BitcoinBlockchain(difficulty=3)
    
    # Adicionar transações
    tx1 = Transaction("Alice", "Bob", 50.0)
    tx2 = Transaction("Bob", "Charlie", 25.0)
    
    blockchain.add_transaction(tx1)
    blockchain.add_transaction(tx2)
    
    # Minerar bloco
    blockchain.mine_pending_transactions("Minerador1")
    
    # Consultar saldo
    print(f"Saldo de Minerador1: {blockchain.get_balance('Minerador1')} BTC")
    
    # Validar blockchain
    print(f"Blockchain válida? {blockchain.is_chain_valid()}")
    
    return blockchain


# ============================================================================
# EXEMPLO 2: Criar e Usar Carteira
# ============================================================================

def example_wallet():
    """Criar carteira e assinar transações."""
    from bitcoin_crypto import BitcoinWallet, BitcoinCrypto
    
    print("\n" + "="*80)
    print("EXEMPLO 2: CARTEIRAS E ASSINATURAS".center(80))
    print("="*80 + "\n")
    
    # Criar carteira
    wallet = BitcoinWallet()
    wallet.create_new_wallet()
    
    # Mostrar informações
    wallet.print_wallet_info(show_private=False)
    
    # Assinar mensagem
    message = "Transferir 10 BTC"
    signature = wallet.sign_transaction(message)
    
    print(f"Mensagem assinada: {signature[:64]}...")
    
    # Verificar assinatura
    crypto = BitcoinCrypto()
    is_valid = crypto.verify_signature(message, signature, wallet.public_key)
    
    print(f"Assinatura válida? {is_valid}")
    
    return wallet


# ============================================================================
# EXEMPLO 3: Rede P2P
# ============================================================================

def example_p2p_network():
    """Criar rede P2P com múltiplos nós."""
    from bitcoin_p2p_network import P2PNode
    import time
    
    print("\n" + "="*80)
    print("EXEMPLO 3: REDE P2P".center(80))
    print("="*80 + "\n")
    
    # Criar 3 nós
    nodes = []
    for i in range(3):
        node = P2PNode(port=9000 + i)
        node.start_server()
        nodes.append(node)
        time.sleep(0.5)
    
    # Conectar nós
    nodes[0].connect_to_peer('localhost', 9001)
    nodes[0].connect_to_peer('localhost', 9002)
    nodes[1].connect_to_peer('localhost', 9002)
    
    # Status da rede
    for i, node in enumerate(nodes):
        print(f"Nó {i+1}: {len(node.peers)} peers conectados")
    
    # Broadcast de transação
    test_tx = {'sender': 'Alice', 'recipient': 'Bob', 'amount': 10}
    nodes[0].broadcast_transaction(test_tx)
    
    time.sleep(1)
    
    # Parar nós
    for node in nodes:
        node.stop()
    
    return nodes


# ============================================================================
# EXEMPLO 4: Sistema Integrado Completo
# ============================================================================

def example_integrated_system():
    """Sistema completo com todas as funcionalidades."""
    from galaxy_bitcoin_system import GalaxyBitcoinSystem
    
    print("\n" + "="*80)
    print("EXEMPLO 4: SISTEMA INTEGRADO".center(80))
    print("="*80 + "\n")
    
    # Criar sistema
    system = GalaxyBitcoinSystem(difficulty=3)
    
    # Criar usuários
    system.create_user_wallet("Alice")
    system.create_user_wallet("Bob")
    system.create_user_wallet("Charlie")
    
    # Inicializar rede (opcional)
    # system.initialize_network(num_nodes=3)
    
    # Transação 1
    tx1 = system.create_validated_transaction("Alice", "Bob", 25.0)
    if tx1:
        system.blockchain.add_transaction(tx1)
    
    # Transação 2
    tx2 = system.create_validated_transaction("Alice", "Charlie", 15.0)
    if tx2:
        system.blockchain.add_transaction(tx2)
    
    # Minerar
    system.mine_block_with_ai("Bob")
    
    # Validar
    system.validate_blockchain_integrity()
    
    # Status
    system.print_system_status()
    
    return system


# ============================================================================
# EXEMPLO 5: Validação Personalizada
# ============================================================================

def example_custom_validation():
    """Usar validador universal."""
    from universal_validator import UniversalValidator
    from bitcoin_blockchain import BitcoinBlockchain
    
    print("\n" + "="*80)
    print("EXEMPLO 5: VALIDAÇÃO PERSONALIZADA".center(80))
    print("="*80 + "\n")
    
    # Criar validador
    validator = UniversalValidator()
    
    # Testar entropia
    data = "0000abc123def456"
    entropy = validator.shannon_entropy_check(data)
    print(f"Entropia calculada: {entropy:.4f} bits")
    
    # Turing test
    hypothesis = "Sistema blockchain mantém integridade"
    variables = [f"var_{i}" for i in range(10)]
    
    result = validator.turing_torture_test(hypothesis, variables)
    print(f"Turing test passou? {result}")
    
    return validator


# ============================================================================
# EXEMPLO 6: Integração com Neural Network
# ============================================================================

def example_neural_integration():
    """Usar rede neural com blockchain."""
    from genesis import NeuralNetwork
    import numpy as np
    
    print("\n" + "="*80)
    print("EXEMPLO 6: NEURAL NETWORK INTEGRATION".center(80))
    print("="*80 + "\n")
    
    # Criar rede neural
    nn = NeuralNetwork(input_nodes=10, hidden_nodes=20, output_nodes=5)
    
    # Simular análise de bloco
    block_features = np.random.rand(10)
    output = nn.feed_forward(block_features)
    
    # Usar output para otimizar mineração
    suggested_nonce = int(output[0] * 1000000)
    print(f"IA sugere nonce inicial: {suggested_nonce:,}")
    
    # Genoma da rede
    dna = nn.get_dna()
    print(f"Tamanho do genoma: {len(dna)} parâmetros")
    
    return nn


# ============================================================================
# EXEMPLO 7: Análise de Transações
# ============================================================================

def example_transaction_analysis():
    """Analisar transações na blockchain."""
    from bitcoin_blockchain import BitcoinBlockchain, Transaction
    
    print("\n" + "="*80)
    print("EXEMPLO 7: ANÁLISE DE TRANSAÇÕES".center(80))
    print("="*80 + "\n")
    
    # Criar blockchain
    blockchain = BitcoinBlockchain(difficulty=2)
    
    # Adicionar várias transações
    addresses = ["Alice", "Bob", "Charlie", "Diana"]
    
    for i in range(5):
        sender = addresses[i % len(addresses)]
        recipient = addresses[(i + 1) % len(addresses)]
        amount = 10.0 * (i + 1)
        
        tx = Transaction(sender, recipient, amount)
        blockchain.add_transaction(tx)
    
    blockchain.mine_pending_transactions("Minerador")
    
    # Análise
    print("Análise de Saldos:")
    for addr in addresses:
        balance = blockchain.get_balance(addr)
        print(f"  {addr:10} {balance:8.2f} BTC")
    
    # Estatísticas
    total_blocks = len(blockchain.chain)
    total_tx = sum(len(b.transactions) for b in blockchain.chain)
    
    print(f"\nEstatísticas:")
    print(f"  Total de blocos: {total_blocks}")
    print(f"  Total de transações: {total_tx}")
    print(f"  Média tx/bloco: {total_tx/total_blocks:.2f}")
    
    return blockchain


# ============================================================================
# EXEMPLO 8: Importar/Exportar Carteira
# ============================================================================

def example_wallet_import_export():
    """Importar e exportar carteiras."""
    from bitcoin_crypto import BitcoinWallet
    import json
    
    print("\n" + "="*80)
    print("EXEMPLO 8: IMPORT/EXPORT DE CARTEIRA".center(80))
    print("="*80 + "\n")
    
    # Criar carteira
    wallet1 = BitcoinWallet()
    wallet1.create_new_wallet()
    
    print("Carteira Original:")
    print(f"  Endereço: {wallet1.address}")
    
    # Exportar
    wallet_data = wallet1.export_wallet()
    
    # Salvar em arquivo (opcional)
    # with open('wallet.json', 'w') as f:
    #     json.dump(wallet_data, f, indent=2)
    
    # Importar em nova carteira
    wallet2 = BitcoinWallet()
    wallet2.import_from_private_key(wallet_data['private_key'])
    
    print("\nCarteira Importada:")
    print(f"  Endereço: {wallet2.address}")
    
    # Verificar se são iguais
    print(f"\nCarteiras idênticas? {wallet1.address == wallet2.address}")
    
    return wallet1, wallet2


# ============================================================================
# EXEMPLO 9: Merkle Tree Verification
# ============================================================================

def example_merkle_verification():
    """Verificar Merkle Root de transações."""
    from bitcoin_blockchain import Block, Transaction
    
    print("\n" + "="*80)
    print("EXEMPLO 9: MERKLE TREE VERIFICATION".center(80))
    print("="*80 + "\n")
    
    # Criar transações
    transactions = [
        Transaction("Alice", "Bob", 10.0),
        Transaction("Bob", "Charlie", 5.0),
        Transaction("Charlie", "Diana", 3.0),
        Transaction("Diana", "Alice", 2.0)
    ]
    
    # Criar bloco
    block = Block(
        index=1,
        transactions=transactions,
        previous_hash="0" * 64
    )
    
    # Calcular Merkle Root
    merkle_root = block.calculate_merkle_root()
    
    print(f"Merkle Root: {merkle_root}")
    print(f"Número de transações: {len(transactions)}")
    
    # Verificar integridade
    print(f"\nMerkle Root válido? {merkle_root == block.merkle_root}")
    
    return block


# ============================================================================
# EXEMPLO 10: Simulação de Halving
# ============================================================================

def example_halving_simulation():
    """Simular processo de halving do Bitcoin."""
    from bitcoin_blockchain import BitcoinBlockchain
    
    print("\n" + "="*80)
    print("EXEMPLO 10: SIMULAÇÃO DE HALVING".center(80))
    print("="*80 + "\n")
    
    blockchain = BitcoinBlockchain(difficulty=1)
    blockchain.halving_interval = 3  # Halving a cada 3 blocos (para demo)
    
    print("Recompensas de mineração:")
    print(f"  Bloco 0 (Genesis): {blockchain.mining_reward} BTC")
    
    # Minerar vários blocos
    for i in range(1, 10):
        blockchain.mine_pending_transactions(f"Miner{i}")
        reward = blockchain.get_mining_reward()
        print(f"  Bloco {i}: {reward} BTC")
    
    return blockchain


# ============================================================================
# MAIN - Executar todos os exemplos
# ============================================================================

def main():
    """Executar todos os exemplos."""
    print("\n" + "🌌"*40)
    print("GALAXY BITCOIN SYSTEM - EXEMPLOS DE API".center(80))
    print("🌌"*40 + "\n")
    
    print("Executando exemplos...\n")
    
    examples = [
        ("Blockchain Básico", example_basic_blockchain),
        ("Carteiras e Assinaturas", example_wallet),
        ("Rede P2P", example_p2p_network),
        ("Sistema Integrado", example_integrated_system),
        ("Validação Personalizada", example_custom_validation),
        ("Neural Network", example_neural_integration),
        ("Análise de Transações", example_transaction_analysis),
        ("Import/Export Carteira", example_wallet_import_export),
        ("Merkle Tree", example_merkle_verification),
        ("Halving Simulation", example_halving_simulation)
    ]
    
    results = {}
    
    for name, func in examples:
        try:
            print(f"\n{'='*80}")
            print(f"Executando: {name}")
            print('='*80)
            results[name] = func()
            print(f"\n[✅] {name} concluído!")
        except Exception as e:
            print(f"\n[❌] Erro em {name}: {e}")
            import traceback
            traceback.print_exc()
            results[name] = None
    
    # Resumo
    print("\n" + "="*80)
    print("RESUMO DOS EXEMPLOS".center(80))
    print("="*80 + "\n")
    
    for name, result in results.items():
        status = "✅" if result is not None else "❌"
        print(f"  {status} {name}")
    
    print("\n" + "🌌"*40 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[🛑] Exemplos interrompidos")
    except Exception as e:
        print(f"\n[❌] Erro: {e}")
        import traceback
        traceback.print_exc()
