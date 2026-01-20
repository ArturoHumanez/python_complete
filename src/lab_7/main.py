from database import SessionLocal, engine
from models import Base, Order, OrderItem, User

# Crear las tablas en base
Base.metadata.create_all(bind=engine)


def ejecutar_laboratorio():
    db = SessionLocal()

    # CREATE USER
    usuario = User(username="Arturo_HD", email="arturo@achity.com")
    db.add(usuario)
    db.commit()  # Guarda los cambios
    db.refresh(usuario)  # Actualiza el objeto con el ID generado por la BD

    # CREATE ORDER
    nueva_orden = Order(user_id=usuario.id)
    item = OrderItem(product_name="Juegósfera", price=500.0, order=nueva_orden)

    db.add(nueva_orden)
    db.add(item)
    db.commit()

    # --- READ ---
    usuario = db.query(User).filter(User.username == "Arturo_HD").first()
    print(f"Usuario: {usuario.username} tiene {len(usuario.orders)} órdenes.")

    db.close()


if __name__ == "__main__":
    ejecutar_laboratorio()
