import subprocess
import re
import time

class HardwareResonance:
    """
    [HARDWARE RESONANCE BRIDGE]
    Captura dados REAIS da placa de rede para alimentar a visão eletromagnética.
    """
    
    def __init__(self):
        self.last_data = {
            "ssid": "UNKNOWN",
            "band": 2.4,
            "signal": 0,
            "rssi": -100
        }

    def capture_wlan_telemetry(self):
        """Executa netsh e extrai métricas reais."""
        try:
            output = subprocess.check_output("netsh wlan show interfaces", shell=True).decode('cp1252')
            
            # Parsers Regex
            rssi_match = re.search(r"Rssi\s+:\s+(-\d+)", output)
            band_match = re.search(r"Banda\s+:\s+(\d+)", output) # Procura '5' ou '2.4'
            ssid_match = re.search(r"SSID\s+:\s+(.+)", output)
            signal_match = re.search(r"Sinal\s+:\s+(\d+)%", output)
            
            if rssi_match: self.last_data["rssi"] = int(rssi_match.group(1))
            if ssid_match: self.last_data["ssid"] = ssid_match.group(1).strip()
            if signal_match: self.last_data["signal"] = int(signal_match.group(1))
            
            if band_match:
                b = band_match.group(1)
                self.last_data["band"] = 5.0 if "5" in b else 2.4
                
            return self.last_data
        except Exception as e:
            print(f"[!] Hardware Bridge Error: {e}")
            return self.last_data

if __name__ == "__main__":
    bridge = HardwareResonance()
    while True:
        data = bridge.capture_wlan_telemetry()
        print(f"\r[RSSI: {data['rssi']} dBm] [SSID: {data['ssid']}] [BAND: {data['band']} GHz]   ", end="")
        time.sleep(1)
