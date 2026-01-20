from fastapi import FastAPI
from pydantic import BaseModel

from . import models
from .database import engine
from .middleware import LogProcessTimeMiddleware
from .routers import auth, orders

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.title = "Orders API - Lab 8"
app.version = "1.0.0"

app.include_router(auth.router)
app.include_router(orders.router)

app.add_middleware(LogProcessTimeMiddleware)


# Esquema Pydantic (Lo que recibimos del cliente)
class Item(BaseModel):
    nombre: str
    precio: float
    cantidad: int


@app.get("/")
def home():
    return {"mensaje": "Bienvenido al Sistema de Órdenes"}
