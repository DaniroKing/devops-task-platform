from fastapi import FastAPI

app = FastAPI(
    title="DevOps Task Platform",
    description="Учебное API для практики DevOps",
    version="0.1.0",
)


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
