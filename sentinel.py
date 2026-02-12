import logging
import os
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

# --- CONFIGURAÇÃO E CONSTANTES ---

@dataclass(frozen=True)
class SentinelConfig:
    """Configurações imutáveis para o Sentinela Digital."""
    log_path: Path = Path("/var/log/auth.log") if os.name != "nt" else Path("simulated_auth.log")
    alert_path: Path = Path("sentinel_alerts.txt")
    patterns: List[str] = field(default_factory=lambda: [
        r"Failed password",
        r"PROJECT_OMEGA",
        r"UNAUTHORIZED_ACCESS"
    ])
    poll_interval_seconds: float = 1.0

# Configuração do LOG padrão do Python (Standard Library)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("sentinel_internal.log")
    ]
)
logger = logging.getLogger("Sentinel")

# --- MÓDULOS MODULARES (S.O.L.I.D.) ---

class LogTailer:
    """Responsável por monitorar e ler o final de arquivos de log."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Garante a existência do alvo para evitar FileNotFoundError."""
        if not self.file_path.exists():
            logger.warning(f"Alvo {self.file_path} não encontrado. Criando arquivo simulado.")
            self.file_path.touch()

    def follow(self):
        """Gerador que retorna novas linhas conforme aparecem no log."""
        try:
            with open(self.file_path, "r", encoding="utf-8", errors="ignore") as f:
                # Mover o cursor para o final (não processar dados históricos)
                f.seek(0, os.SEEK_END)
                
                while True:
                    line = f.readline()
                    if not line:
                        yield None
                        continue
                    yield line.strip()
        except Exception as e:
            logger.error(f"Erro ao acessar {self.file_path}: {e}")
            raise

class AnomalyDetector:
    """Responsável pela lógica de detecção de padrões (Business Logic)."""
    
    def __init__(self, patterns: List[str]):
        self.regex = re.compile("|".join(patterns))

    def check(self, line: str) -> bool:
        """Verifica se uma linha contém algum dos padrões monitorados."""
        return bool(self.regex.search(line))

class AlertManager:
    """Responsável pelo output e notificações do sentinela."""
    
    def __init__(self, alert_path: Path):
        self.alert_path = alert_path

    def notify(self, event: str) -> None:
        """Registra e notifica uma anomalia detectada."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        alert_msg = f"[!] SEGURANÇA: {timestamp} | EVENTO: {event}\n"
        
        logger.critical(f"ANOMALIA DETECTADA: {event}")
        
        try:
            with open(self.alert_path, "a", encoding="utf-8") as f:
                f.write(alert_msg)
        except IOError as e:
            logger.error(f"Falha ao escrever no arquivo de alertas: {e}")

# --- ORQUESTRADOR CENTRAL ---

class SentinelDaemon:
    """Orquestrador que gerencia o ciclo de vida do Sentinela."""
    
    def __init__(self, config: Optional[SentinelConfig] = None):
        self.config = config or SentinelConfig()
        self.tailer = LogTailer(self.config.log_path)
        self.detector = AnomalyDetector(self.config.patterns)
        self.alerter = AlertManager(self.config.alert_path)

    def run(self) -> None:
        """Loop principal de execução do Daemon."""
        logger.info(f"Sentinela Digital (v2) Ativo. Monitorando: {self.config.log_path}")
        
        try:
            for line in self.tailer.follow():
                if line:
                    if self.detector.check(line):
                        self.alerter.notify(line)
                else:
                    time.sleep(self.config.poll_interval_seconds)
        except KeyboardInterrupt:
            logger.info("Sentinela interrompido manualmente pelo Operador.")
        except Exception as e:
            logger.critical(f"Falha fatal no orquestrador: {e}")
            raise

if __name__ == "__main__":
    daemon = SentinelDaemon()
    daemon.run()
