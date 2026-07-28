from typing import Any

from fastapi.testclient import TestClient


def create_test_task(client: TestClient) -> dict[str, Any]:
    """Создаёт задачу для последующих тестов."""
    response = client.post(
        "/tasks",
        json={
            "title": "Изучить FastAPI",
            "description": "Реализовать CRUD API",
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_task(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "Изучить FastAPI",
            "description": "Реализовать CRUD API",
        },
    )

    assert response.status_code == 201

    task = response.json()

    assert task["id"] == 1
    assert task["title"] == "Изучить FastAPI"
    assert task["description"] == "Реализовать CRUD API"
    assert task["status"] == "todo"
    assert "created_at" in task
    assert "updated_at" in task


def test_get_tasks(client: TestClient) -> None:
    created_task = create_test_task(client)

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == [created_task]


def test_get_task_by_id(client: TestClient) -> None:
    created_task = create_test_task(client)

    response = client.get("/tasks/1")

    assert response.status_code == 200
    assert response.json() == created_task


def test_update_task(client: TestClient) -> None:
    create_test_task(client)

    response = client.patch(
        "/tasks/1",
        json={
            "status": "done",
        },
    )

    assert response.status_code == 200

    updated_task = response.json()

    assert updated_task["title"] == "Изучить FastAPI"
    assert updated_task["description"] == "Реализовать CRUD API"
    assert updated_task["status"] == "done"


def test_delete_task(client: TestClient) -> None:
    create_test_task(client)

    delete_response = client.delete("/tasks/1")

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get("/tasks/1")

    assert get_response.status_code == 404
    assert get_response.json() == {
        "detail": "Task not found",
    }


def test_get_missing_task(client: TestClient) -> None:
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found",
    }


def test_reject_empty_title(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "",
        },
    )

    assert response.status_code == 422
