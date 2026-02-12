#!/usr/bin/env python3
"""
🌌 Galaxy Bitcoin System - Quick Start
Inicia o sistema profissional rapidamente com todas as verificações
"""
import os
import sys
import subprocess
import time
import webbrowser
import threading

def print_banner():
    """Banner bonito do sistema"""
    print("\n" + "="*70)
    print("🌌 GALAXY BITCOIN SYSTEM - Quick Start Launcher")
    print("   Professional Bitcoin Trading Platform with AI & Biometric Security")
    print("="*70 + "\n")

def check_python_version():
    """Verifica versão do Python"""
    print("🐍 Verificando Python...")
    version = sys.version_info
    
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro}\n")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor} muito antigo!")
        print("     Requer Python 3.8 ou superior\n")
        return False

def check_dependencies():
    """Verifica dependências essenciais"""
    print("📦 Verificando dependências...\n")
    
    required = {
        'flask': ('Flask', True),
        'cv2': ('OpenCV', True),
        'numpy': ('NumPy', True),
        'ecdsa': ('ECDSA', True),
        'base58': ('Base58', True),
        'requests': ('Requests', False),
        'cryptography': ('Cryptography', True),
    }
    
    missing = []
    optional_missing = []
    
    for module, (name, is_required) in required.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            if is_required:
                print(f"  ❌ {name}")
                missing.append(module)
            else:
                print(f"  ⚠️  {name} (opcional)")
                optional_missing.append(module)
    
    print()
    
    if missing:
        print("⚠️  Dependências essenciais faltando!\n")
        print("Instale com:")
        print(f"  pip install {' '.join(missing)}\n")
        print("Ou execute:")
        print("  pip install -r requirements.txt\n")
        
        response = input("Deseja instalar automaticamente? (s/n): ")
        if response.lower() == 's':
            print("\n🔧 Instalando dependências...\n")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                             check=True)
                print("\n✅ Dependências instaladas!\n")
                return True
            except subprocess.CalledProcessError:
                print("\n❌ Erro na instalação! Instale manualmente.\n")
                return False
        return False
    
    if optional_missing:
        print("💡 Algumas dependências opcionais estão faltando.")
        print("   O sistema funcionará, mas com funcionalidade reduzida.\n")
    
    return True

def check_camera():
    """Verifica se há câmera disponível"""
    print("🎥 Verificando câmera...")
    
    try:
        import cv2
        cam = cv2.VideoCapture(0)
        
        if cam.isOpened():
            ret, _ = cam.read()
            cam.release()
            
            if ret:
                print("  ✅ Câmera detectada e funcionando\n")
                return True
            else:
                print("  ⚠️  Câmera detectada mas sem frames\n")
                return False
        else:
            print("  ⚠️  Nenhuma câmera detectada (sistema funcionará sem câmera)\n")
            return False
    except:
        print("  ⚠️  Erro ao verificar câmera\n")
        return False

def check_files():
    """Verifica arquivos essenciais"""
    print("📁 Verificando arquivos...")
    
    essential_files = [
        'simple_app.py',
        'bitcoin_blockchain.py',
        'bitcoin_crypto.py',
        'bitcoin_api.py',
        'config.py',
        'requirements.txt'
    ]
    
    missing = []
    
    for file in essential_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")
            missing.append(file)
    
    print()
    
    if missing:
        print(f"❌ Arquivos essenciais faltando: {', '.join(missing)}\n")
        return False
    
    return True

def run_validation():
    """Executa validação completa"""
    print("🧪 Executando validação completa...\n")
    
    try:
        result = subprocess.run([sys.executable, "validate_system.py"], 
                              capture_output=False, 
                              text=True, 
                              timeout=60)
        
        return result.returncode == 0
    except FileNotFoundError:
        print("⚠️  Script de validação não encontrado, pulando...\n")
        return True
    except subprocess.TimeoutExpired:
        print("⚠️  Validação demorou muito, continuando...\n")
        return True
    except Exception as e:
        print(f"⚠️  Erro na validação: {e}\n")
        return True

def start_server():
    """Inicia o servidor Flask"""
    print("="*70)
    print("🚀 Iniciando Galaxy Bitcoin System...")
    print("="*70 + "\n")
    
    print("📡 Configurações:")
    print("   • Servidor: http://localhost:5000")
    print("   • WebSocket: Ativo")
    print("   • Bitcoin API: Integrado")
    print("   • Blockchain: Ativo")
    print("   • Biometria: Disponível")
    print()
    
    print("💡 Recursos:")
    print("   ✅ Reconhecimento facial em tempo real")
    print("   ✅ Trading Bitcoin com dados reais")
    print("   ✅ Blockchain com Proof of Work")
    print("   ✅ Dashboard profissional")
    print("   ✅ APIs REST e WebSocket")
    print("   ✅ Sistema de carteiras")
    print()
    
    print("🔧 Comandos:")
    print("   • Ctrl+C: Parar servidor")
    print("   • http://localhost:5000: Abrir dashboard")
    print()
    
    print("="*70)
    print("🌐 Abrindo navegador em 3 segundos...")
    print("="*70 + "\n")
    
    # Aguardar e abrir navegador
    def open_browser():
        time.sleep(3)
        try:
            webbrowser.open('http://localhost:5000')
            print("✅ Navegador aberto!\n")
        except:
            print("⚠️  Não foi possível abrir navegador automaticamente")
            print("   Abra manualmente: http://localhost:5000\n")
    
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Iniciar servidor
    try:
        subprocess.run([sys.executable, "simple_app.py"])
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("👋 Servidor parado. Até logo!")
        print("="*70 + "\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}\n")
        sys.exit(1)

def show_menu():
    """Mostra menu de opções"""
    print("="*70)
    print("OPÇÕES")
    print("="*70)
    print()
    print("1. 🚀 Iniciar sistema (recomendado)")
    print("2. 🧪 Executar validação completa")
    print("3. 📋 Ver documentação")
    print("4. 🔧 Instalar/Atualizar dependências")
    print("5. 🌐 Configurar Git")
    print("6. ❌ Sair")
    print()
    
    choice = input("Escolha uma opção (1-6): ").strip()
    return choice

def main():
    """Função principal"""
    print_banner()
    
    # Verificações básicas
    if not check_python_version():
        print("❌ Versão do Python incompatível!\n")
        input("Pressione ENTER para sair...")
        sys.exit(1)
    
    if not check_files():
        print("❌ Arquivos essenciais faltando!\n")
        input("Pressione ENTER para sair...")
        sys.exit(1)
    
    # Menu interativo
    while True:
        choice = show_menu()
        
        if choice == '1':
            # Verificar dependências e iniciar
            if not check_dependencies():
                print("\n❌ Por favor, instale as dependências primeiro.\n")
                continue
            
            check_camera()
            
            print("✅ Sistema pronto para iniciar!\n")
            time.sleep(1)
            
            start_server()
            break
        
        elif choice == '2':
            # Validação completa
            run_validation()
            input("\nPressione ENTER para continuar...")
        
        elif choice == '3':
            # Documentação
            print("\n📋 Abrindo README.md...\n")
            if os.path.exists('README.md'):
                if sys.platform == 'win32':
                    os.system('notepad README.md')
                else:
                    os.system('less README.md')
            else:
                print("❌ README.md não encontrado\n")
            input("Pressione ENTER para continuar...")
        
        elif choice == '4':
            # Instalar dependências
            print("\n🔧 Instalando dependências...\n")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                             check=True)
                print("\n✅ Dependências instaladas!\n")
            except subprocess.CalledProcessError:
                print("\n❌ Erro na instalação!\n")
            input("Pressione ENTER para continuar...")
        
        elif choice == '5':
            # Git setup
            print("\n🌐 Configurando Git...\n")
            if sys.platform == 'win32':
                if os.path.exists('setup_git.bat'):
                    os.system('setup_git.bat')
                else:
                    print("❌ setup_git.bat não encontrado\n")
            else:
                if os.path.exists('setup_git.sh'):
                    os.system('bash setup_git.sh')
                else:
                    print("❌ setup_git.sh não encontrado\n")
            input("\nPressione ENTER para continuar...")
        
        elif choice == '6':
            # Sair
            print("\n👋 Até logo!\n")
            sys.exit(0)
        
        else:
            print("\n❌ Opção inválida! Tente novamente.\n")
            time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido. Até logo!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}\n")
        input("Pressione ENTER para sair...")
        sys.exit(1)
