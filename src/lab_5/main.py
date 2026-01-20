from dataclasses import dataclass
from typing import Annotated, Generic, Optional, Protocol, TypeVar, Union


# Protocol 🦆
class Procesador(Protocol):
    def procesar(self, contenido: str) -> str:
        ...


T = TypeVar("T")


@dataclass
class ContenedorIA(Generic[T]):
    dato: T
    metadatos: Optional[dict] = None  # Puede ser un dict o None


# Implementación
class ProcesadorTexto:
    def procesar(self, contenido: str) -> str:
        return contenido.upper()


class ProcesadorResumen:
    def procesar(self, contenido: str) -> str:
        return f"Resumen: {contenido[:10]}..."


def ejecutar_tarea(
    agente: Procesador, texto: Annotated[str, "Debe ser UTF-8"]
) -> Union[str, None]:
    if not texto:
        return None
    return agente.procesar(texto)


if __name__ == "__main__":
    p1 = ProcesadorTexto()
    p2 = ProcesadorResumen()

    res1 = ejecutar_tarea(p1, "hola mundo")
    res2 = ejecutar_tarea(p2, "este es un texto largo")

    print(res1, "|", res2)
