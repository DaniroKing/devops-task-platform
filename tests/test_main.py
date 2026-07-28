from fastapi.testclient import TestClient


def test_read_root(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "DevOps Task Platform API",
        "status": "running",
    }


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
    }


def test_unknown_endpoint(client: TestClient) -> None:
    response = client.get("/unknown")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Not Found",
    }
