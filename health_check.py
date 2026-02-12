#!/usr/bin/env python3
"""
GALAXY BITCOIN SYSTEM - Health Check
Verifica integridade e status de todos os componentes
"""

import os
import sys
import importlib
from typing import Dict, Tuple

def print_header(text: str):
    """Imprime cabeçalho."""
    print("\n" + "="*80)
    print(text.center(80))
    print("="*80 + "\n")

def check_python_version() -> Tuple[bool, str]:
    """Verifica versão do Python."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    return False, f"Python {version.major}.{version.minor} (requer 3.7+)"

def check_dependencies() -> Dict[str, bool]:
    """Verifica todas as dependências."""
    deps = {
        'numpy': False,
        'matplotlib': False,
        'scipy': False,
        'ecdsa': False,
        'base58': False,
        'networkx': False
    }
    
    for dep in deps:
        try:
            importlib.import_module(dep)
            deps[dep] = True
        except ImportError:
            deps[dep] = False
    
    return deps

def check_files() -> Dict[str, bool]:
    """Verifica existência dos arquivos principais."""
    files = {
        # Bitcoin Core
        'bitcoin_blockchain.py': False,
        'bitcoin_crypto.py': False,
        'bitcoin_p2p_network.py': False,
        'galaxy_bitcoin_system.py': False,
        
        # Neural/Matrix
        'genesis.py': False,
        'matrix_kernel.py': False,
        'universal_validator.py': False,
        
        # Launchers
        'launch.py': False,
        'quick_demo.py': False,
        'install_and_test.py': False,
        'api_examples.py': False,
        'visualize_blockchain.py': False,
        
        # Documentação
        'README.md': False,
        'BITCOIN_README.md': False,
        'QUICKSTART.md': False,
        'requirements.txt': False
    }
    
    for filename in files:
        files[filename] = os.path.exists(filename)
    
    return files

def test_imports() -> Dict[str, bool]:
    """Testa imports dos módulos principais."""
    modules = {
        'bitcoin_blockchain': False,
        'bitcoin_crypto': False,
        'bitcoin_p2p_network': False,
        'galaxy_bitcoin_system': False,
        'genesis': False,
        'universal_validator': False
    }
    
    for module_name in modules:
        try:
            importlib.import_module(module_name)
            modules[module_name] = True
        except Exception:
            modules[module_name] = False
    
    return modules

def calculate_health_score(results: Dict[str, Dict]) -> float:
    """Calcula score de saúde do sistema."""
    total_checks = 0
    passed_checks = 0
    
    for category, checks in results.items():
        if isinstance(checks, dict):
            for check, status in checks.items():
                total_checks += 1
                if status:
                    passed_checks += 1
        elif checks:  # boolean
            total_checks += 1
            passed_checks += 1
    
    return (passed_checks / total_checks * 100) if total_checks > 0 else 0

def print_results(results: Dict):
    """Imprime resultados detalhados."""
    
    # Python Version
    print("🐍 PYTHON VERSION")
    print("─" * 80)
    python_ok, python_version = results['python_version']
    status = "✅" if python_ok else "❌"
    print(f"{status} {python_version}")
    
    # Dependencies
    print("\n📦 DEPENDÊNCIAS")
    print("─" * 80)
    for dep, installed in results['dependencies'].items():
        status = "✅" if installed else "❌"
        print(f"{status} {dep:15} {'Instalado' if installed else 'NÃO instalado'}")
    
    # Files
    print("\n📄 ARQUIVOS DO SISTEMA")
    print("─" * 80)
    
    categories = {
        'Bitcoin Core': [
            'bitcoin_blockchain.py',
            'bitcoin_crypto.py',
            'bitcoin_p2p_network.py',
            'galaxy_bitcoin_system.py'
        ],
        'Neural/Matrix': [
            'genesis.py',
            'matrix_kernel.py',
            'universal_validator.py'
        ],
        'Launchers': [
            'launch.py',
            'quick_demo.py',
            'install_and_test.py',
            'api_examples.py',
            'visualize_blockchain.py'
        ],
        'Documentação': [
            'README.md',
            'BITCOIN_README.md',
            'QUICKSTART.md',
            'requirements.txt'
        ]
    }
    
    for category, files in categories.items():
        print(f"\n{category}:")
        for file in files:
            exists = results['files'].get(file, False)
            status = "✅" if exists else "❌"
            print(f"  {status} {file}")
    
    # Module Imports
    print("\n🔌 IMPORTS DE MÓDULOS")
    print("─" * 80)
    for module, importable in results['imports'].items():
        status = "✅" if importable else "❌"
        print(f"{status} {module:30} {'OK' if importable else 'FALHOU'}")

def generate_recommendations(results: Dict) -> list:
    """Gera recomendações baseadas nos resultados."""
    recommendations = []
    
    # Check Python version
    python_ok, _ = results['python_version']
    if not python_ok:
        recommendations.append("⚠️  Atualize o Python para versão 3.7 ou superior")
    
    # Check dependencies
    missing_deps = [dep for dep, installed in results['dependencies'].items() 
                   if not installed]
    if missing_deps:
        recommendations.append(
            f"📦 Instale dependências faltando: pip install {' '.join(missing_deps)}"
        )
    
    # Check files
    missing_files = [file for file, exists in results['files'].items() 
                    if not exists]
    if missing_files:
        recommendations.append(
            f"📄 {len(missing_files)} arquivo(s) faltando - verifique instalação"
        )
    
    # Check imports
    failed_imports = [mod for mod, ok in results['imports'].items() if not ok]
    if failed_imports:
        recommendations.append(
            f"🔌 {len(failed_imports)} módulo(s) com erro de import - verifique código"
        )
    
    return recommendations

def main():
    """Função principal."""
    print("\n" + "🏥"*40)
    print("GALAXY BITCOIN SYSTEM - HEALTH CHECK".center(80))
    print("🏥"*40)
    
    print_header("🔍 EXECUTANDO VERIFICAÇÕES")
    
    # Coletar resultados
    print("Verificando Python version...", end=' ')
    python_result = check_python_version()
    print("✓")
    
    print("Verificando dependências...", end=' ')
    deps_result = check_dependencies()
    print("✓")
    
    print("Verificando arquivos...", end=' ')
    files_result = check_files()
    print("✓")
    
    print("Testando imports...", end=' ')
    imports_result = test_imports()
    print("✓")
    
    results = {
        'python_version': python_result,
        'dependencies': deps_result,
        'files': files_result,
        'imports': imports_result
    }
    
    # Calcular score
    health_score = calculate_health_score(results)
    
    # Imprimir resultados
    print_header("📊 RESULTADOS")
    print_results(results)
    
    # Score de saúde
    print("\n" + "="*80)
    print("🎯 HEALTH SCORE".center(80))
    print("="*80)
    
    if health_score >= 90:
        emoji = "🟢"
        status = "EXCELENTE"
    elif health_score >= 70:
        emoji = "🟡"
        status = "BOM"
    elif health_score >= 50:
        emoji = "🟠"
        status = "ATENÇÃO"
    else:
        emoji = "🔴"
        status = "CRÍTICO"
    
    print(f"\n{emoji} {health_score:.1f}% - {status}")
    
    # Recomendações
    recommendations = generate_recommendations(results)
    
    if recommendations:
        print("\n" + "="*80)
        print("💡 RECOMENDAÇÕES".center(80))
        print("="*80 + "\n")
        for rec in recommendations:
            print(f"  {rec}")
    else:
        print("\n✅ Sistema em perfeito estado! Nenhuma ação necessária.")
    
    # Próximos passos
    print("\n" + "="*80)
    print("🚀 PRÓXIMOS PASSOS".center(80))
    print("="*80 + "\n")
    
    if health_score >= 90:
        print("  Sistema pronto! Execute:")
        print("    python launch.py          # Menu interativo")
        print("    python quick_demo.py      # Demo rápida")
        print("    python galaxy_bitcoin_system.py  # Sistema completo")
    elif health_score >= 70:
        print("  Sistema funcional com pequenos problemas.")
        print("  Corrija as recomendações acima e execute:")
        print("    python install_and_test.py")
    else:
        print("  Sistema necessita atenção.")
        print("  Execute primeiro:")
        print("    pip install -r requirements.txt")
        print("    python install_and_test.py")
    
    print("\n" + "="*80 + "\n")
    
    return health_score >= 70

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n[🛑] Verificação cancelada")
        sys.exit(1)
    except Exception as e:
        print(f"\n[❌] Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
