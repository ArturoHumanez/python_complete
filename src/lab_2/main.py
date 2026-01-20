import json


def procesar_biblioteca(ruta_archivo: str):
    try:
        # Lectura de archivo
        with open(ruta_archivo, "r") as f:
            documentos = json.load(f)

        documentos_validos = []

        for doc in documentos:
            # Pattern Matching para validar la estructura del diccionario
            match doc:
                case {"id": int(idx), "contenido": str(texto)} if len(texto) > 0:
                    print(f"Documento {idx} válido para indexar.")
                    documentos_validos.append(doc)

                case {"id": int(idx), "contenido": ""}:
                    print(f"Documento {idx} omitido: Contenido vacío.")

                case _:
                    print(f"Error de formato en documento: {doc}")

        return documentos_validos

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta_archivo}'.")
    except json.JSONDecodeError:
        print("Error: El archivo no tiene un formato JSON válido.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


if __name__ == "__main__":
    resultado = procesar_biblioteca(r"src\lab_2\datos.json")
    print(f"\nTotal procesados con éxito: {len(resultado) if resultado else 0}")
