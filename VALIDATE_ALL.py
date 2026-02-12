import sys
import os
import cv2
import numpy as np
import requests
import time
import subprocess
from topological_kernel import TopologicalKernel
from TOTAL_STATION_ROOT import TotalStationRoot

def validate_system():
    print("="*80)
    print(" [VALIDATION_ORCHESTRATOR] INICIANDO AUDITORIA FINAL ".center(80))
    print("="*80)
    
    results = {}

    # 1. Kernel Validation
    print("\n[SYSTEM] Validando Kernel Topologico...")
    try:
        tk = TopologicalKernel()
        dummy = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
        sig = tk.extract_signature(dummy)
        if len(sig) > 0 and not np.all(sig == 0):
            print("[SUCCESS] Signature Engine: OK")
            results["kernel"] = True
        else:
            print("[ERROR] Signature Engine: FALHA (Zero Output)")
            results["kernel"] = False
    except Exception as e:
        print(f"[ERROR] Kernel Error: {e}")
        results["kernel"] = False

    # 2. Hardware Vision Validation
    print("\n[SYSTEM] Validando Hardware de Visao (OpenCV)...")
    try:
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        ret, frame = cam.read()
        if ret:
            print("[SUCCESS] Camera Access: OK (Capture Success)")
            results["vision"] = True
        else:
            print("[WARNING] Camera Access: AVISO (Captura falhou, verifique se outra app usa a camera)")
            results["vision"] = False
        cam.release()
    except Exception as e:
        print(f"[ERROR] Vision Error: {e}")
        results["vision"] = False

    # 3. Telemetry Bridge Validation
    print("\n[SYSTEM] Validando Telemetry Bridge (FastAPI)...")
    try:
        # Tentar iniciar em uma porta temporária para teste ou checar se a 8000 está viva
        # Assumiremos que o usuário rodará o SYSTEM_CORE_ACTIVATE, aqui apenas checamos a infra
        import fastapi
        import uvicorn
        print("[SUCCESS] FastAPI/Uvicorn Dependencies: OK")
        results["bridge"] = True
    except ImportError:
        print("[ERROR] Bridge Dependencies: FALHA (pip install fastapi uvicorn)")
        results["bridge"] = False

    # 4. Neural Dashboard Validation
    print("\n[SYSTEM] Validando Dashboard Neural (React/Vite)...")
    dashboard_path = os.path.join(os.getcwd(), "dashboard", "src", "App.jsx")
    if os.path.exists(dashboard_path):
        print(f"[SUCCESS] Dashboard Source: OK ({os.path.basename(dashboard_path)})")
        results["dashboard"] = True
    else:
        print("[ERROR] Dashboard Source: NAO ENCONTRADO")
        results["dashboard"] = False

    # 5. Root Station Validation
    print("\n[SYSTEM] Validando TotalStationRoot...")
    try:
        station = TotalStationRoot()
        if station.status != "TOTAL_SYNC":
            station.boot_all_subsystems()
        
        if station.status == "TOTAL_SYNC":
            print("[✅] Station Boot: OK")
            results["station"] = True
        else:
            print(f"[❌] Station Status: {station.status} (FAILED)")
            results["station"] = False
    except Exception as e:
        print(f"[❌] Station Error: {e}")
        results["station"] = False

    print("\n" + "="*80)
    print(" [RELATÓRIO DE CONVERGÊNCIA] ".center(80))
    print("="*80)
    for k, v in results.items():
        status = "PASSED" if v else "FAILED"
        print(f"{k.upper():<20} | {status}")
    
    if all(results.values()):
        print("\n[🌟] SISTEMA PRONTO PARA SINGULARIDADE TOTAL [🌟]")
    else:
        print("\n[⚠️] SISTEMA REQUER ATENÇÃO EM ALGUNS MÓDULOS.")
    print("="*80)

if __name__ == "__main__":
    validate_system()
