from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "TestPassword123",
        },
    )

    assert response.status_code in [201, 409]


def test_login_invalid_password():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401