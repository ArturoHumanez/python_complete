import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# 3. IMPORTA LOS MODELOS PARA QUE SE REGISTREN EN EL BASE QUE ACABAMOS DE TRAER
# 2. IMPORTA EL BASE Y EL GET_DB DESDE EL MISMO LUGAR QUE LA APP
from src.lab_8.database import Base, get_db

# 1. IMPORTA LA APP
from src.lab_8.main import app

# Configuración del motor de test
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # IMPORTANTE: Mantiene la DB viva en memoria
)
TestingSessionLocal = sessionmaker(bind=test_engine)


@pytest.fixture(scope="function")
def client():
    # Creamos las tablas usando el Base que YA TIENE registrados los modelos
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def user_token(client):
    client.post(
        "/register",
        json={
            "username": "test_tester",
            "email": "test@test.com",
            "password": "password123",
        },
    )

    login = client.post(
        "/login", data={"username": "test_tester", "password": "password123"}
    )
    return login.json()["access_token"]
