from sqlalchemy.orm import Session

from app.crud.crud_search_history import get_recent_searches
from app.models.favorite import Favorite
from app.models.place import Place, PlaceStatus


def get_home_recommendations(db: Session, user_id: int, limit: int = 10) -> list[Place]:
    favorites = db.query(Favorite).filter(Favorite.user_id == user_id).all()
    recent_searches = get_recent_searches(db, user_id, limit=20)

    category_weights: dict[int, float] = {}
    price_points: list[float] = []

    for fav in favorites:
        cat_id = fav.place.category_id
        category_weights[cat_id] = category_weights.get(cat_id, 0) + 3
        if fav.place.price is not None:
            price_points.append(fav.place.price)

    for search in recent_searches:
        if search.category_id:
            category_weights[search.category_id] = category_weights.get(search.category_id, 0) + 2
        if search.max_price is not None:
            price_points.append(search.max_price)

    if not category_weights:
        # Usuario nuevo sin historial -> fallback a recientes/destacados
        return (
            db.query(Place)
            .filter(Place.status == PlaceStatus.APPROVED)
            .order_by(Place.created_at.desc())
            .limit(limit)
            .all()
        )

    avg_price = sum(price_points) / len(price_points) if price_points else None
    favorite_ids = {fav.place_id for fav in favorites}

    candidates = (
        db.query(Place)
        .filter(Place.status == PlaceStatus.APPROVED)
        .filter(~Place.id.in_(favorite_ids) if favorite_ids else True)
        .all()
    )

    scored = []
    for place in candidates:
        score = category_weights.get(place.category_id, 0)
        if avg_price is not None and place.price is not None:
            price_diff = abs(place.price - avg_price)
            score += max(0, 2 - (price_diff / max(avg_price, 1)))
        scored.append((score, place))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = [place for score, place in scored[:limit] if score > 0]
    return top or candidates[:limit]