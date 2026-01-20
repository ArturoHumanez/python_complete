from fastapi.testclient import TestClient

from src.lab_8.main import app

client = TestClient(app)


def test_register_user(client):
    response = client.post(
        "/register",
        json={
            "username": "new_unique_user",
            "email": "unique@test.com",
            "password": "password123",
        },
    )
    # Si da 400, imprime la respuesta para ver el error real
    assert response.status_code == 200, f"Error: {response.json()}"


def test_login_user():
    response = client.post(
        "/login", data={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
