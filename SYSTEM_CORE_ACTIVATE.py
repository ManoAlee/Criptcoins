import subprocess
import time
import os
import sys
from TOTAL_STATION_ROOT import TotalStationRoot

def kill_port_owner(port):
    """Detecta e encerra processos que ocupam a porta especificada (Windows)."""
    try:
        if os.name == 'nt':
            output = subprocess.check_output(f"netstat -ano | findstr :{port}", shell=True).decode()
            for line in output.strip().split('\n'):
                if 'LISTENING' in line:
                    pid = line.strip().split()[-1]
                    print(f"[🛡️] Liberando porta {port} (Kill PID {pid})...")
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True, capture_output=True)
    except Exception:
        pass # Porta provavelmente livre ou erro de permissão

def activate_everything():
    print("="*80)
    print(" [SISTEMA OMNI-ARCHITECT] INICIANDO ATIVAÇÃO TOTAL ".center(80))
    print("="*80)
    
    # 0. Port Management (Safeguard)
    kill_port_owner(8000)

    # 1. Boot Subsystems (Logic Only)
    station = TotalStationRoot()
    station.boot_all_subsystems()
    
    # 2. Launch Telemetry Bridge (Background)
    print("\n[SYSTEM] Lancando Telemetry Bridge (FastAPI)...")
    try:
        # Usar -m uvicorn para garantir que o uvicorn esteja no path
        server_cmd = [sys.executable, "telemetry_server.py"]
        subprocess.Popen(server_cmd)
        print("[SUCCESS] Telemetry Server inicializado em background na porta 8000.")
    except Exception as e:
        print(f"[ERROR] Erro ao lancar Telemetry Server: {e}")

    time.sleep(2)

    # 3. Launch Dashboard (Background)
    print("\n[SYSTEM] Lancando Dashboard Neural (Vite)...")
    dashboard_dir = os.path.join(os.getcwd(), "dashboard")
    try:
        # Usar shell=True para comandos npm no Windows
        subprocess.Popen(["npm", "run", "dev"], cwd=dashboard_dir, shell=True)
        print("[SUCCESS] Dashboard inicializado em background.")
    except Exception as e:
        print(f"[ERROR] Erro ao lancar Dashboard: {e}")

    time.sleep(3) # Esperar o dashboard respirar

    # 4. Launch OMNI-VISION HUD (Foreground)
    print("\n[SYSTEM] Lancando OMNI-VISION HUD (Zero-Lag Kernel)...")
    hud_path = "topological_validator_gui.py"
    
    try:
        # O HUD assume o controle da janela principal e da câmera
        subprocess.run([sys.executable, hud_path])
    except KeyboardInterrupt:
        print("\n[🛑] Operação encerrada pelo Operador.")
    except Exception as e:
        print(f"[❌] Erro ao lançar HUD: {e}")

    print("\n" + "="*80)
    print(" [SISTEMA OMNI-ARCHITECT] CICLO DE ATIVAÇÃO CONCLUÍDO ".center(80))
    print("="*80)
    print("\n💡 DICA: Acesse o Dashboard em http://localhost:5173 para controle God-Mode.")

if __name__ == "__main__":
    activate_everything()
