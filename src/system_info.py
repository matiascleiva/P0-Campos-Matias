"""Genera data/system_info.json con información básica del computador.

Uso:
    python src/system_info.py

La salida se guarda en data/system_info.json (relativo a la raíz del repo).
"""

import json
import platform
from pathlib import Path

import psutil

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = REPO_ROOT / "data" / "system_info.json"


def cpu_model() -> str:
    modelo = platform.processor()
    if not modelo:
        try:
            with open("/proc/cpuinfo", encoding="utf-8") as f:
                for linea in f:
                    if linea.startswith("model name"):
                        return linea.split(":", 1)[1].strip()
        except OSError:
            pass
    return modelo or "No disponible"


def collect_info() -> dict:
    return {
        "sistema_operativo": f"{platform.system()} {platform.release()}",
        "plataforma": platform.platform(),
        "arquitectura": platform.machine(),
        "version_python": platform.python_version(),
        "procesador": cpu_model(),
        "nucleos_fisicos": psutil.cpu_count(logical=False),
        "procesadores_logicos": psutil.cpu_count(logical=True),
        "ram_total_bytes": psutil.virtual_memory().total,
        "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
    }


def main() -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    info = collect_info()
    OUTPUT_FILE.write_text(json.dumps(info, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Información guardada en: {OUTPUT_FILE}")
    for clave, valor in info.items():
        print(f"  {clave}: {valor}")


if __name__ == "__main__":
    main()
