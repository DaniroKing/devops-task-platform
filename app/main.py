from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Task
from app.schemas import TaskCreate, TaskResponse, TaskUpdate


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """Создаёт отсутствующие таблицы при запуске приложения."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="DevOps Task Platform",
    description="Учебное API для практики DevOps",
    version="0.3.0",
    lifespan=lifespan,
)


DatabaseSession = Annotated[Session, Depends(get_db)]


def get_task_or_404(task_id: int, db: Session) -> Task:
    """Возвращает задачу или завершает запрос ошибкой 404."""
    task = db.get(Task, task_id)

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
def health_check(db: DatabaseSession) -> dict[str, str]:
    """Проверяет доступность приложения и базы данных."""
    db.execute(text("SELECT 1"))

    return {
        "status": "healthy",
    }


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: DatabaseSession) -> list[Task]:
    """Возвращает список всех задач."""
    statement = select(Task).order_by(Task.id)

    return list(db.scalars(statement).all())


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: DatabaseSession) -> Task:
    """Возвращает задачу по идентификатору."""
    return get_task_or_404(task_id, db)


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task_data: TaskCreate,
    db: DatabaseSession,
) -> Task:
    """Создаёт новую задачу."""
    task = Task(
        title=task_data.title,
        description=task_data.description,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: DatabaseSession,
) -> Task:
    """Частично обновляет существующую задачу."""
    task = get_task_or_404(task_id, db)
    update_data = task_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(task, field, value)

    task.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(task)

    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(task_id: int, db: DatabaseSession) -> Response:
    """Удаляет задачу."""
    task = get_task_or_404(task_id, db)

    db.delete(task)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
