import csv
import json
import logging
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Rutas con Pathlib
BASE_DIR = Path(__file__).resolve().parent.parent.parent
INPUT_PATH = BASE_DIR / "data" / "entrenamiento.csv"
OUTPUT_PATH = BASE_DIR / "data" / "knowledge_base.json"

LOGS_DIR = BASE_DIR / "logs" / "lab_6"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOGS_DIR / f"log_lab_6_{datetime.now().strftime('%Y-%m-%d')}.log"

# Configuración de Logs


def configurar_logs():
    format = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(format)

    logger = logging.getLogger("logger")
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    return logger


logger = configurar_logs()


def process_csv():
    logger.info("Procesando csv...")

    if not INPUT_PATH.exists():
        logger.error(f"No se encontró el archivo en: {INPUT_PATH}")
        return

    conocimiento_agente = []

    try:
        # Parseo CSV
        with open(INPUT_PATH, mode="r", encoding="utf-8") as archivo:
            archivo = csv.DictReader(archivo)
            for fila in archivo:
                # Datetime y zonas horarias
                fila["procesado_en"] = datetime.now(timezone.utc).isoformat()
                conocimiento_agente.append(fila)
                logger.debug(f"Procesado tema: {fila['tema']}")

        # Métricas simples para el loggin
        total_items = len(conocimiento_agente)
        logger.info(f"Se procesaron {total_items} registros exitosamente.")

        # Exportación a JSON (Serialización)
        with open(OUTPUT_PATH, mode="w", encoding="utf-8") as f_json:
            json.dump(conocimiento_agente, f_json, indent=4, ensure_ascii=False)

        logger.info(f"Base de conocimientos guardada en: {OUTPUT_PATH}")

    except Exception as e:
        logger.critical(f"Fallo catastrófico en la ingesta: {e}")


def execute_on_os(ruta_archivo: Path):
    logger.info("Ejecutando comandos con subprocess...")

    # Especificamos mostrar detalles de archivo
    comando = ["cmd", "/c", "dir", str(ruta_archivo)]
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)

        print("\n--- SALIDA DEL SISTEMA ---")
        print(resultado.stdout)
        print("--------------------------\n")

        logger.info("Tarea de verificación de sistema completada.")

    except subprocess.CalledProcessError as e:
        logger.error(f"Error al ejecutar comando de sistema: {e}")


if __name__ == "__main__":
    process_csv()
    execute_on_os(OUTPUT_PATH)
