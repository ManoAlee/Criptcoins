#!/usr/bin/env python3
"""
🌌 Galaxy Bitcoin System - Smart Dependency Installer
Instala apenas as dependências que funcionam no seu sistema
"""
import subprocess
import sys

ESSENTIAL_PACKAGES = [
    'flask>=2.3.0',
    'flask-cors>=4.0.0',
    'flask-socketio>=5.3.0',
    'python-socketio>=5.9.0',
    'ecdsa>=0.18.0',
    'base58>=2.1.1',
    'requests>=2.31.0',
    'websocket-client>=1.6.0',
    'cryptography>=41.0.0',
    'pyjwt>=2.8.0',
    'opencv-python>=4.8.0',
    'pillow>=10.0.0',
    'numpy>=1.24.0',
    'scipy>=1.11.0',
    'scikit-learn>=1.3.0',
    'networkx>=3.1',
    'aiohttp>=3.8.0',
    'python-dotenv>=1.0.0',
    'colorama>=0.4.6',
    'tqdm>=4.66.0',
]

OPTIONAL_PACKAGES = {
    'audio': [
        'SpeechRecognition>=3.10.0',
        'pyttsx3>=2.90',
        'pyaudio>=0.2.13',
    ],
    'visualization': [
        'matplotlib>=3.7.0',
        'plotly>=5.17.0',
        'pandas>=2.0.0',
    ],
    'database': [
        'SQLAlchemy>=2.0.0',
    ],
    'testing': [
        'pytest>=7.4.0',
        'pytest-cov>=4.1.0',
        'black>=23.7.0',
        'flake8>=6.1.0',
    ],
}

def install_packages(packages, category=""):
    """Instala um conjunto de pacotes"""
    if not packages:
        return True
    
    category_str = f" ({category})" if category else ""
    print(f"\n📦 Instalando dependências{category_str}...\n")
    
    for package in packages:
        try:
            print(f"  ⏳ {package.split('>')[0]}...", end=" ", flush=True)
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-q', package],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                print("✅")
            else:
                print("⚠️ (pulado)")
                
        except subprocess.TimeoutExpired:
            print("⏱️ (timeout)")
        except Exception as e:
            print(f"❌ ({str(e)[:20]}...)")
    
    return True

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("🌌 Galaxy Bitcoin System - Smart Dependency Installer")
    print("="*70 + "\n")
    
    # Atualizar pip
    print("🔄 Atualizando pip...\n")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip', '-q'], 
                   capture_output=True)
    
    # Instalar essenciais
    install_packages(ESSENTIAL_PACKAGES, "Essenciais")
    
    # Perguntar sobre opcionais
    print("\n" + "="*70)
    print("📦 DEPENDÊNCIAS OPCIONAIS")
    print("="*70 + "\n")
    
    print("Deseja instalar pacotes opcionais?\n")
    print("1. 🎤 Audio & Speech Recognition (PyAudio - pode falhar)")
    print("2. 📊 Visualização Avançada (Matplotlib, Plotly)")
    print("3. 🧪 Testes & Qualidade (Pytest, Black)")
    print("4. 🗄️  Database (SQLAlchemy)")
    print("5. 🚫 Não instalar opcionais")
    print()
    
    choice = input("Escolha (1-5) ou pressione ENTER para pular: ").strip()
    
    if choice == '1':
        install_packages(OPTIONAL_PACKAGES['audio'], "Audio")
    elif choice == '2':
        install_packages(OPTIONAL_PACKAGES['visualization'], "Visualização")
    elif choice == '3':
        install_packages(OPTIONAL_PACKAGES['testing'], "Testes")
    elif choice == '4':
        install_packages(OPTIONAL_PACKAGES['database'], "Database")
    
    # Validar instalação
    print("\n" + "="*70)
    print("✅ VALIDANDO INSTALAÇÃO")
    print("="*70 + "\n")
    
    essential_ok = 0
    for package in ESSENTIAL_PACKAGES:
        pkg_name = package.split('>')[0].replace('-', '_')
        try:
            __import__(pkg_name)
            print(f"✅ {pkg_name}")
            essential_ok += 1
        except ImportError:
            print(f"❌ {pkg_name}")
    
    print()
    print("="*70)
    print(f"✅ {essential_ok}/{len(ESSENTIAL_PACKAGES)} pacotes essenciais instalados")
    print("="*70)
    
    if essential_ok == len(ESSENTIAL_PACKAGES):
        print("\n✅ Tudo pronto! Execute:")
        print("   python quick_start.py")
    else:
        print(f"\n⚠️  {len(ESSENTIAL_PACKAGES) - essential_ok} pacotes faltando")
        print("   Execute: pip install -r requirements.txt")
    
    print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Instalação cancelada")
        sys.exit(1)
