from fastapi import FastAPI
from app.api import router
from app.core.config import settings
from app.core.logging import configure_logging

configure_logging()
app = FastAPI(title=settings.project_name, version="1.0.0")
app.include_router(router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}
