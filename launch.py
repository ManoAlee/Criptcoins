#!/usr/bin/env python3
"""
MASTER LAUNCHER - Galaxy Bitcoin System
Menu interativo para todos os módulos do sistema
"""

import sys
import os

def clear_screen():
    """Limpa a tela."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    """Imprime menu principal."""
    clear_screen()
    
    print("╔" + "="*78 + "╗")
    print("║" + " 🌌 GALAXY BITCOIN SYSTEM - MASTER LAUNCHER 🌌 ".center(78) + "║")
    print("╚" + "="*78 + "╝\n")
    
    print("📋 MENU PRINCIPAL:\n")
    
    print("  🚀 DEMOS E TESTES:")
    print("    [1] Quick Demo (5 min) - Demonstração rápida animada")
    print("    [2] Sistema Completo - Demo completa com blockchain real")
    print("    [3] Instalar e Testar - Verificar dependências e rodar testes\n")
    
    print("  🔗 MÓDULOS BITCOIN:")
    print("    [4] Blockchain - Demonstração de blockchain com PoW")
    print("    [5] Criptografia - Sistema de carteiras e ECDSA")
    print("    [6] Rede P2P - Rede descentralizada peer-to-peer\n")
    print("    [16] Biometria - Captura webcam e derivação de chave\n")
    
    print("  🎨 VISUALIZAÇÕES:")
    print("    [7] Visualizador - Gráficos da blockchain\n")
    
    print("  🧠 MÓDULOS ORIGINAIS:")
    print("    [8] Genesis - Rede neural evolutiva")
    print("    [9] Omni Bridge - Ponte neural (Bio-radar)")
    print("    [10] Matrix Kernel - Geometria diferencial")
    print("    [11] Universal Validator - Validação termodinâmica")
    print("    [12] Unified Field - Campo unificado de informação")
    print("    [13] Mandelbrot - Fractais e singularidades\n")
    
    print("  📚 DOCUMENTAÇÃO:")
    print("    [14] Documentação Bitcoin")
    print("    [15] README Principal\n")
    
    print("  [0] Sair\n")
    print("─" * 80)

def run_module(module_name):
    """Executa um módulo."""
    print(f"\n[🚀] Executando {module_name}...\n")
    print("─" * 80 + "\n")
    
    try:
        os.system(f"python {module_name}")
    except Exception as e:
        print(f"\n[❌] Erro ao executar: {e}")
    
    print("\n" + "─" * 80)
    input("\nPressione ENTER para voltar ao menu...")

def show_docs(filename):
    """Mostra documentação."""
    print(f"\n[📖] Abrindo {filename}...\n")
    
    try:
        if os.name == 'nt':  # Windows
            os.system(f"notepad {filename}")
        else:  # Linux/Mac
            os.system(f"less {filename}")
    except Exception as e:
        print(f"[❌] Erro: {e}")
        print("\n[ℹ️] Abra manualmente o arquivo:", filename)
    
    input("\nPressione ENTER para voltar ao menu...")

def main():
    """Função principal."""
    modules = {
        '1': 'quick_demo.py',
        '2': 'galaxy_bitcoin_system.py',
        '3': 'install_and_test.py',
        '4': 'bitcoin_blockchain.py',
        '5': 'bitcoin_crypto.py',
        '6': 'bitcoin_p2p_network.py',
        '7': 'visualize_blockchain.py',
        '8': 'genesis.py',
        '9': 'omni_bridge.py',
        '10': 'matrix_kernel.py',
        '11': 'universal_validator.py',
        '12': 'unified_field.py',
        '13': 'mandelbrot.py'
        ,
        '16': 'biometric_key.py'
    }
    
    while True:
        print_menu()
        
        choice = input("Escolha uma opção: ").strip()
        
        if choice == '0':
            print("\n[👋] Encerrando Galaxy Bitcoin System...")
            print("🌌 Até logo! 🌌\n")
            break
        
        elif choice in modules:
            run_module(modules[choice])
        
        elif choice == '14':
            show_docs('BITCOIN_README.md')
        
        elif choice == '15':
            show_docs('README.md')
        
        else:
            print("\n[⚠️] Opção inválida!")
            input("Pressione ENTER para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[🛑] Sistema interrompido pelo usuário")
        print("🌌 Até logo! 🌌\n")
    except Exception as e:
        print(f"\n[❌] Erro fatal: {e}")
        import traceback
        traceback.print_exc()
