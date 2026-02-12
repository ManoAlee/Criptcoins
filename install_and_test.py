#!/usr/bin/env python3
"""
GALAXY BITCOIN SYSTEM - Script de Instalação e Teste
Verifica dependências e executa testes básicos
"""

import sys
import subprocess
import importlib

def print_header(text):
    """Imprime cabeçalho formatado."""
    print("\n" + "="*80)
    print(text.center(80))
    print("="*80 + "\n")

def check_python_version():
    """Verifica versão do Python."""
    print("🐍 Verificando versão do Python...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"[❌] Python {version.major}.{version.minor} detectado")
        print("[!] Python 3.7+ é necessário")
        return False
    
    print(f"[✅] Python {version.major}.{version.minor}.{version.micro} OK")
    return True

def check_dependencies():
    """Verifica e instala dependências."""
    print("\n📦 Verificando dependências...")
    
    dependencies = {
        'numpy': 'numpy',
        'matplotlib': 'matplotlib',
        'scipy': 'scipy',
        'ecdsa': 'ecdsa',
        'base58': 'base58'
    }
    
    missing = []
    
    for module_name, pip_name in dependencies.items():
        try:
            importlib.import_module(module_name)
            print(f"[✅] {module_name:15} instalado")
        except ImportError:
            print(f"[❌] {module_name:15} NÃO instalado")
            missing.append(pip_name)
    
    if missing:
        print(f"\n[!] {len(missing)} dependência(s) faltando: {', '.join(missing)}")
        print("\nDeseja instalar automaticamente? (s/n): ", end='')
        
        choice = input().lower()
        if choice == 's':
            install_dependencies(missing)
            return True
        else:
            print("\n[!] Instale manualmente com: pip install " + " ".join(missing))
            return False
    
    print("\n[✅] Todas as dependências instaladas!")
    return True

def install_dependencies(packages):
    """Instala dependências via pip."""
    print("\n⚙️  Instalando dependências...")
    
    for package in packages:
        print(f"\n📥 Instalando {package}...")
        try:
            subprocess.check_call([
                sys.executable, 
                "-m", 
                "pip", 
                "install", 
                package,
                "--quiet"
            ])
            print(f"[✅] {package} instalado com sucesso")
        except subprocess.CalledProcessError:
            print(f"[❌] Erro ao instalar {package}")
            return False
    
    print("\n[✅] Todas as dependências instaladas!")
    return True

def test_bitcoin_blockchain():
    """Testa módulo de blockchain."""
    print("\n🔗 Testando Bitcoin Blockchain...")
    
    try:
        from bitcoin_blockchain import BitcoinBlockchain, Transaction
        
        # Criar blockchain de teste
        blockchain = BitcoinBlockchain(difficulty=2)
        
        # Criar transação
        tx = Transaction("Alice", "Bob", 10.0)
        blockchain.add_transaction(tx)
        
        # Minerar bloco
        blockchain.mine_pending_transactions("Miner")
        
        # Validar
        if blockchain.is_chain_valid():
            print("[✅] Blockchain: PASSOU")
            return True
        else:
            print("[❌] Blockchain: FALHOU")
            return False
            
    except Exception as e:
        print(f"[❌] Erro: {e}")
        return False

def test_bitcoin_crypto():
    """Testa módulo de criptografia."""
    print("\n🔐 Testando Bitcoin Crypto...")
    
    try:
        from bitcoin_crypto import BitcoinCrypto, BitcoinWallet
        
        crypto = BitcoinCrypto()
        
        # Criar carteira
        wallet = BitcoinWallet()
        wallet.create_new_wallet()
        
        # Testar assinatura
        message = "Test message"
        signature = wallet.sign_transaction(message)
        
        is_valid = crypto.verify_signature(
            message, 
            signature, 
            wallet.public_key
        )
        
        if is_valid:
            print("[✅] Crypto: PASSOU")
            return True
        else:
            print("[❌] Crypto: FALHOU")
            return False
            
    except Exception as e:
        print(f"[❌] Erro: {e}")
        return False

def test_p2p_network():
    """Testa módulo P2P."""
    print("\n🌐 Testando P2P Network...")
    
    try:
        from bitcoin_p2p_network import P2PNode
        
        # Criar nó
        node = P2PNode(port=9000)
        node.start_server()
        
        if node.is_running:
            print("[✅] P2P Network: PASSOU")
            node.stop()
            return True
        else:
            print("[❌] P2P Network: FALHOU")
            return False
            
    except Exception as e:
        print(f"[❌] Erro: {e}")
        return False

def test_galaxy_system():
    """Testa sistema integrado."""
    print("\n🌌 Testando Galaxy Bitcoin System...")
    
    try:
        from galaxy_bitcoin_system import GalaxyBitcoinSystem
        
        # Criar sistema
        system = GalaxyBitcoinSystem(difficulty=2)
        
        # Criar carteiras
        system.create_user_wallet("Alice")
        system.create_user_wallet("Bob")
        
        # Criar transação
        tx = system.create_validated_transaction("Alice", "Bob", 10.0)
        
        if tx:
            system.blockchain.add_transaction(tx)
            
            # Minerar
            system.mine_block_with_ai("Alice")
            
            # Validar
            if system.validate_blockchain_integrity():
                print("[✅] Galaxy System: PASSOU")
                return True
        
        print("[❌] Galaxy System: FALHOU")
        return False
            
    except Exception as e:
        print(f"[❌] Erro: {e}")
        return False

def run_all_tests():
    """Executa todos os testes."""
    print_header("🧪 EXECUTANDO TESTES")
    
    tests = [
        ("Blockchain", test_bitcoin_blockchain),
        ("Crypto", test_bitcoin_crypto),
        ("P2P Network", test_p2p_network),
        ("Galaxy System", test_galaxy_system)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n[❌] Erro no teste {test_name}: {e}")
            results[test_name] = False
    
    # Resumo
    print("\n" + "="*80)
    print("📊 RESUMO DOS TESTES".center(80))
    print("="*80)
    
    for test_name, passed in results.items():
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"  {test_name:20} {status}")
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    
    print("\n" + "-"*80)
    print(f"  Total: {passed}/{total} testes passaram ({passed/total*100:.0f}%)")
    print("="*80 + "\n")
    
    return all(results.values())

def main():
    """Função principal."""
    print_header("🌌 GALAXY BITCOIN SYSTEM - INSTALAÇÃO E TESTE")
    
    # Verificar Python
    if not check_python_version():
        return False
    
    # Verificar dependências
    if not check_dependencies():
        return False
    
    # Executar testes
    print("\n" + "-"*80)
    print("Deseja executar os testes? (s/n): ", end='')
    
    choice = input().lower()
    if choice == 's':
        success = run_all_tests()
        
        if success:
            print("\n[🎉] INSTALAÇÃO E TESTES CONCLUÍDOS COM SUCESSO!")
            print("\nPara executar o sistema completo:")
            print("  python galaxy_bitcoin_system.py")
        else:
            print("\n[⚠️] Alguns testes falharam. Verifique os logs acima.")
        
        return success
    else:
        print("\n[✅] Dependências verificadas. Sistema pronto!")
        return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n[🛑] Instalação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n[❌] Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
