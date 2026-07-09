from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate


def get_category(db: Session, category_id: int) -> Category | None:
    return db.query(Category).filter(Category.id == category_id).first()


def get_categories(db: Session) -> list[Category]:
    return db.query(Category).order_by(Category.name).all()


def create_category(db: Session, category_in: CategoryCreate) -> Category:
    db_category = Category(name=category_in.name, icon=category_in.icon)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category