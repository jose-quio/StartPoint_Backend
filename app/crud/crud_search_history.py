from sqlalchemy.orm import Session

from app.models.search_history import SearchHistory


def log_search(
    db: Session,
    user_id: int,
    query_text: str | None = None,
    category_id: int | None = None,
    max_price: float | None = None,
) -> SearchHistory:
    entry = SearchHistory(
        user_id=user_id,
        query_text=query_text,
        category_id=category_id,
        max_price=max_price,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_recent_searches(db: Session, user_id: int, limit: int = 20) -> list[SearchHistory]:
    return (
        db.query(SearchHistory)
        .filter(SearchHistory.user_id == user_id)
        .order_by(SearchHistory.created_at.desc())
        .limit(limit)
        .all()
    )