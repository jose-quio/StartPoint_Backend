from app.db.base_class import Base  # noqa

# Importa aquí todos los modelos para que Alembic y Base.metadata los detecten
from app.models.user import User            # noqa
from app.models.category import Category    # noqa
from app.models.place import Place          # noqa
from app.models.review import Review        # noqa
from app.models.favorite import Favorite    # noqa
from app.models.image import PlaceImage     # noqa
from app.models.schedule import PlaceSchedule, Service, place_services  # noqa
from app.models.search_history import SearchHistory  # noqa