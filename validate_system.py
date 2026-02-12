#!/usr/bin/env python3
"""
🌌 Galaxy Bitcoin System - Complete Validation & Testing
Validação completa do sistema antes de deploy
"""
import sys
import os
import time
import subprocess
from typing import Dict, List, Tuple

class SystemValidator:
    """Validador completo do sistema"""
    
    def __init__(self):
        self.results = []
        self.errors = []
        self.warnings = []
    
    def log(self, message: str, level: str = "INFO"):
        """Log com formatação"""
        symbols = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "ERROR": "❌",
            "WARNING": "⚠️",
            "TEST": "🧪"
        }
        symbol = symbols.get(level, "•")
        print(f"{symbol} {message}")
    
    def test_python_version(self) -> bool:
        """Testa versão do Python"""
        self.log("Testando versão do Python...", "TEST")
        version = sys.version_info
        
        if version.major >= 3 and version.minor >= 8:
            self.log(f"Python {version.major}.{version.minor}.{version.micro} OK", "SUCCESS")
            return True
        else:
            self.log(f"Python {version.major}.{version.minor} muito antigo! Requer 3.8+", "ERROR")
            self.errors.append("Python version < 3.8")
            return False
    
    def test_dependencies(self) -> bool:
        """Testa dependências"""
        self.log("Testando dependências...", "TEST")
        
        required_packages = {
            'flask': 'Flask',
            'cv2': 'OpenCV (opencv-python)',
            'numpy': 'NumPy',
            'ecdsa': 'ECDSA',
            'base58': 'Base58',
            'requests': 'Requests',
            'cryptography': 'Cryptography'
        }
        
        missing = []
        installed = []
        
        for module, name in required_packages.items():
            try:
                __import__(module)
                installed.append(name)
                self.log(f"  {name} OK", "SUCCESS")
            except ImportError:
                missing.append(name)
                self.log(f"  {name} FALTANDO", "ERROR")
        
        if missing:
            self.errors.append(f"Missing packages: {', '.join(missing)}")
            self.log(f"\nInstale com: pip install {' '.join(missing)}", "INFO")
            return False
        
        return True
    
    def test_files_structure(self) -> bool:
        """Testa estrutura de arquivos"""
        self.log("Testando estrutura de arquivos...", "TEST")
        
        required_files = [
            'simple_app.py',
            'bitcoin_blockchain.py',
            'bitcoin_crypto.py',
            'bitcoin_api.py',
            'face_recog.py',
            'biometric_key.py',
            'requirements.txt',
            'README.md',
            'config.py',
            'quick_start.py',
            '.gitignore'
        ]
        
        required_dirs = [
            'templates',
            'static' if os.path.exists('static') else None,
        ]
        required_dirs = [d for d in required_dirs if d]
        
        missing_files = []
        missing_dirs = []
        
        for file in required_files:
            if os.path.exists(file):
                self.log(f"  {file} OK", "SUCCESS")
            else:
                missing_files.append(file)
                self.log(f"  {file} FALTANDO", "ERROR")
        
        for dir in required_dirs:
            if os.path.isdir(dir):
                self.log(f"  {dir}/ OK", "SUCCESS")
            else:
                missing_dirs.append(dir)
                self.log(f"  {dir}/ FALTANDO", "WARNING")
        
        if missing_files:
            self.errors.append(f"Missing files: {', '.join(missing_files)}")
            return False
        
        if missing_dirs:
            self.warnings.append(f"Missing directories: {', '.join(missing_dirs)}")
        
        return True
    
    def test_imports(self) -> bool:
        """Testa imports dos módulos principais"""
        self.log("Testando imports dos módulos...", "TEST")
        
        modules_to_test = [
            'simple_app',
            'bitcoin_blockchain',
            'bitcoin_crypto',
            'bitcoin_api',
            'face_recog',
            'biometric_key',
            'config'
        ]
        
        failed = []
        
        for module in modules_to_test:
            try:
                __import__(module)
                self.log(f"  {module}.py importado OK", "SUCCESS")
            except Exception as e:
                failed.append(module)
                self.log(f"  {module}.py FALHOU: {str(e)[:50]}", "ERROR")
        
        if failed:
            self.errors.append(f"Failed imports: {', '.join(failed)}")
            return False
        
        return True
    
    def test_blockchain(self) -> bool:
        """Testa blockchain"""
        self.log("Testando blockchain...", "TEST")
        
        try:
            from bitcoin_blockchain import BitcoinBlockchain, Transaction
            
            # Criar blockchain
            blockchain = BitcoinBlockchain(difficulty=1)
            self.log("  Blockchain criado OK", "SUCCESS")
            
            # Criar transação
            tx = Transaction("Alice", "Bob", 10.0)
            blockchain.add_transaction(tx)
            self.log("  Transação criada OK", "SUCCESS")
            
            # Minerar bloco
            blockchain.mine_pending_transactions("Miner")
            self.log("  Bloco minerado OK", "SUCCESS")
            
            # Verificar saldo
            balance = blockchain.get_balance("Miner")
            if balance > 0:
                self.log(f"  Saldo do minerador: {balance} BTC", "SUCCESS")
                return True
            else:
                self.log("  Erro no saldo do minerador", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"  Erro no teste de blockchain: {e}", "ERROR")
            self.errors.append(f"Blockchain test failed: {e}")
            return False
    
    def test_bitcoin_api(self) -> bool:
        """Testa API Bitcoin"""
        self.log("Testando Bitcoin API...", "TEST")
        
        try:
            from bitcoin_api import BitcoinAPI
            
            api = BitcoinAPI()
            self.log("  API Bitcoin instanciada OK", "SUCCESS")
            
            # Tentar obter preço
            price = api.get_current_price()
            if price and price > 0:
                self.log(f"  Preço atual: ${price:,.2f} USD", "SUCCESS")
                return True
            else:
                self.log("  Não foi possível obter preço (API pode estar offline)", "WARNING")
                self.warnings.append("Bitcoin API price fetch failed")
                return True  # Não é erro crítico
                
        except Exception as e:
            self.log(f"  Erro no teste de API: {e}", "WARNING")
            self.warnings.append(f"Bitcoin API test warning: {e}")
            return True  # Não é erro crítico
    
    def test_camera(self) -> bool:
        """Testa câmera"""
        self.log("Testando câmera...", "TEST")
        
        try:
            import cv2
            
            # Tentar abrir câmera
            cam = cv2.VideoCapture(0)
            
            if cam.isOpened():
                ret, frame = cam.read()
                cam.release()
                
                if ret and frame is not None:
                    self.log("  Câmera funcionando OK", "SUCCESS")
                    return True
                else:
                    self.log("  Câmera aberta mas sem frames", "WARNING")
                    self.warnings.append("Camera opened but no frames")
                    return True  # Sistema pode funcionar sem câmera
            else:
                self.log("  Nenhuma câmera detectada (sistema funcionará sem câmera)", "WARNING")
                self.warnings.append("No camera detected")
                return True  # Sistema pode funcionar sem câmera
                
        except Exception as e:
            self.log(f"  Erro no teste de câmera: {e}", "WARNING")
            self.warnings.append(f"Camera test warning: {e}")
            return True  # Sistema pode funcionar sem câmera
    
    def test_server_start(self) -> bool:
        """Testa se o servidor pode iniciar"""
        self.log("Testando inicialização do servidor...", "TEST")
        
        try:
            # Não vamos realmente iniciar o servidor, apenas validar imports
            import simple_app
            
            if hasattr(simple_app, 'app'):
                self.log("  Flask app instanciado OK", "SUCCESS")
                return True
            else:
                self.log("  Flask app não encontrado", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"  Erro ao validar servidor: {e}", "ERROR")
            self.errors.append(f"Server validation failed: {e}")
            return False
    
    def test_git_setup(self) -> bool:
        """Verifica se Git está configurado"""
        self.log("Verificando Git...", "TEST")
        
        try:
            result = subprocess.run(['git', '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            if result.returncode == 0:
                self.log(f"  Git instalado: {result.stdout.strip()}", "SUCCESS")
                
                # Verificar se é um repositório Git
                if os.path.exists('.git'):
                    self.log("  Repositório Git inicializado OK", "SUCCESS")
                else:
                    self.log("  Repositório Git não inicializado (execute setup_git.bat)", "WARNING")
                    self.warnings.append("Git repository not initialized")
                
                return True
            else:
                self.log("  Git não instalado", "WARNING")
                self.warnings.append("Git not installed")
                return True  # Não é erro crítico
                
        except Exception as e:
            self.log("  Git não disponível (não é crítico)", "WARNING")
            self.warnings.append("Git not available")
            return True
    
    def run_all_tests(self) -> Tuple[bool, Dict]:
        """Executa todos os testes"""
        print("\n" + "="*70)
        print("🌌 GALAXY BITCOIN SYSTEM - VALIDATION SUITE")
        print("="*70 + "\n")
        
        tests = [
            ("Python Version", self.test_python_version),
            ("Dependencies", self.test_dependencies),
            ("File Structure", self.test_files_structure),
            ("Module Imports", self.test_imports),
            ("Blockchain", self.test_blockchain),
            ("Bitcoin API", self.test_bitcoin_api),
            ("Camera", self.test_camera),
            ("Server", self.test_server_start),
            ("Git", self.test_git_setup),
        ]
        
        passed = 0
        failed = 0
        
        for name, test_func in tests:
            print()
            try:
                if test_func():
                    passed += 1
                    self.results.append((name, "PASS"))
                else:
                    failed += 1
                    self.results.append((name, "FAIL"))
            except Exception as e:
                failed += 1
                self.results.append((name, "ERROR"))
                self.log(f"Erro inesperado: {e}", "ERROR")
        
        print("\n" + "="*70)
        print("RESULTADOS DA VALIDAÇÃO")
        print("="*70)
        
        for name, result in self.results:
            symbol = "✅" if result == "PASS" else "❌"
            print(f"{symbol} {name}: {result}")
        
        print("\n" + "="*70)
        print(f"✅ Passados: {passed}")
        print(f"❌ Falhados: {failed}")
        print(f"⚠️  Avisos: {len(self.warnings)}")
        print("="*70)
        
        if self.errors:
            print("\n❌ ERROS CRÍTICOS:")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print("\n⚠️  AVISOS (não críticos):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        print("\n" + "="*70)
        
        if failed == 0:
            print("✅ SISTEMA VALIDADO E PRONTO PARA USO!")
            print("="*70)
            print("\n💡 Para iniciar o sistema:")
            print("   python quick_start.py")
            print("\n💡 Para configurar Git:")
            print("   setup_git.bat  (Windows)")
            print("   ./setup_git.sh (Linux/Mac)")
            print()
            return True, {
                'passed': passed,
                'failed': failed,
                'warnings': len(self.warnings)
            }
        else:
            print("❌ SISTEMA COM ERROS - CORRIJA ANTES DE USAR")
            print("="*70)
            print()
            return False, {
                'passed': passed,
                'failed': failed,
                'warnings': len(self.warnings),
                'errors': self.errors
            }


if __name__ == '__main__':
    validator = SystemValidator()
    success, results = validator.run_all_tests()
    sys.exit(0 if success else 1)
