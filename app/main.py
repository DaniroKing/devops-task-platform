from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Response, status

from app.schemas import (
    TaskCreate,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)


app = FastAPI(
    title="DevOps Task Platform",
    description="Учебное API для практики DevOps",
    version="0.2.0",
)


# Временное хранилище в оперативной памяти.
# После перезапуска приложения данные будут потеряны.
tasks: dict[int, TaskResponse] = {}
next_task_id = 1


def get_task_or_404(task_id: int) -> TaskResponse:
    """Возвращает задачу или прерывает запрос с ошибкой 404."""
    task = tasks.get(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@app.get("/")
def read_root() -> dict[str, str]:
    """Возвращает общую информацию о сервисе."""
    return {
        "message": "DevOps Task Platform API",
        "status": "running",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    """Проверяет, что приложение запущено и отвечает."""
    return {
        "status": "healthy",
    }


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks() -> list[TaskResponse]:
    """Возвращает список всех задач."""
    return list(tasks.values())


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int) -> TaskResponse:
    """Возвращает одну задачу по идентификатору."""
    return get_task_or_404(task_id)


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(task_data: TaskCreate) -> TaskResponse:
    """Создаёт новую задачу."""
    global next_task_id

    current_time = datetime.now(timezone.utc)

    task = TaskResponse(
        id=next_task_id,
        title=task_data.title,
        description=task_data.description,
        status=TaskStatus.TODO,
        created_at=current_time,
        updated_at=current_time,
    )

    tasks[task.id] = task
    next_task_id += 1

    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
) -> TaskResponse:
    """Частично обновляет существующую задачу."""
    stored_task = get_task_or_404(task_id)

    update_data = task_data.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.now(timezone.utc)

    updated_task = stored_task.model_copy(update=update_data)
    tasks[task_id] = updated_task

    return updated_task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(task_id: int) -> Response:
    """Удаляет задачу."""
    get_task_or_404(task_id)
    del tasks[task_id]

    return Response(status_code=status.HTTP_204_NO_CONTENT)
