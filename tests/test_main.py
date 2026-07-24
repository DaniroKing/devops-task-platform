from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_read_root() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "DevOps Task Platform API",
        "status": "running",
    }


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
    }


def test_unknown_endpoint() -> None:
    response = client.get("/unknown")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Not Found",
    }
