import asyncio
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient

uri = "mongodb://localhost:27017"
client = AsyncIOMotorClient(uri)
db = client.online_shop
coleccion = db.users_actions


async def transacciones_mongo():
    print("Iniciando Laboratorio de MongoDB...")

    # --- CREATE ---
    nuevo_documento = {
        "usuario": "Arturo_HD",
        "accion": "Consulta de saldo",
        "fecha": datetime.utcnow(),
        "metadatos": {"ip": "192.168.1.1", "dispositivo": "Android"},
    }
    resultado = await coleccion.insert_one(nuevo_documento)
    print(f"Documento insertado con ID: {resultado.inserted_id}")

    # --- READ ---
    documento = await coleccion.find_one({"usuario": "Arturo_HD"})
    print(f"Registro encontrado: {documento['accion']} el {documento['fecha']}")

    # --- UPDATE ---
    await coleccion.update_one(
        {"usuario": "Arturo_HD"}, {"$set": {"accion": "Consulta de saldo - COMPLETADA"}}
    )
    print("Documento actualizado")

    # --- DELETE ---
    # await coleccion.delete_one({"usuario": "Arturo_HD"})


if __name__ == "__main__":
    try:
        asyncio.run(transacciones_mongo())
    except Exception as e:
        print(f"Error: {e}")
