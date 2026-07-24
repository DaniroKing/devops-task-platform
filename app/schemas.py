from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Допустимые состояния задачи."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskCreate(BaseModel):
    """Данные, необходимые для создания задачи."""

    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class TaskUpdate(BaseModel):
    """Поля, которые разрешено изменить."""

    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    status: TaskStatus | None = None


class TaskResponse(BaseModel):
    """Полное представление задачи в ответе API."""

    id: int
    title: str
    description: str | None
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
