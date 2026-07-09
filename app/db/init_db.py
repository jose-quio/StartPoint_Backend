from app.db.base import Base
from app.db.session import engine


def init_db() -> None:
    """Crea las tablas directamente (solo para pruebas rápidas).
    En producción usa Alembic en vez de esto."""
    Base.metadata.create_all(bind=engine)