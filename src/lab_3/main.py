import random
import time
from functools import wraps
from typing import Iterable


# Decorador con Backoff
def retry_with_backoff(max_intentos: int, base_retraso: int = 1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retraso = base_retraso
            for intento in range(max_intentos):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if intento == max_intentos - 1:
                        raise e
                    print(f"Falló '{func.__name__}'. ")
                    print(f"Reintento {intento + 1}/{max_intentos} en {retraso}s...")
                    time.sleep(retraso)
                    retraso *= 2

        return wrapper

    return decorator


# Context Manager
class Temporizador:
    def __enter__(self):
        self.inicio = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fin = time.perf_counter()
        print("Tiempo total de ejecución:")
        print(f" {self.fin - self.inicio:.4f} segundos")


# Generador de lotes
def generador_lotes(datos: Iterable, tamano_lote: int):
    lote = []
    for item in datos:
        lote.append(item)
        if len(lote) == tamano_lote:
            yield lote
            lote = []
    if lote:
        yield lote


@retry_with_backoff(max_intentos=3)
def consulta_api_ia(id_doc: int):
    # Simula una llamada a una API de IA que a veces falla

    if random.random() < 0.3:  # 70% de probabilidad de fallo
        raise ConnectionError("Servicio de IA ocupado")
    return f"Resumen del doc {id_doc}"


if __name__ == "__main__":
    documentos = list(range(1, 13))  # X documentos para procesar

    print("Iniciando procesamiento de documentos...")
    with Temporizador():
        for lote in generador_lotes(documentos, 3):  # De 3 en 3
            print(f"\nProcesando lote: {lote}")
            for doc_id in lote:
                try:
                    resultado = consulta_api_ia(doc_id)
                    print(f"{resultado}")
                except Exception:
                    print(f"Documento {doc_id} falló tras todos los reintentos.")
