from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.init_db import init_db

setup_logging()

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajusta esto en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


##@app.on_event("startup")
##def on_startup() -> None:
    # Solo para probar la conexión rápido. Luego usa Alembic y quita esto.
    ##init_db()


@app.get("/health")
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}