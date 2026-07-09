from fastapi import APIRouter
from app.api.v1.endpoints import auth, places, categories, reviews, favorites, images, schedules, services, chatbot, recommendations
api_router = APIRouter()


api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(places.router, prefix="/places", tags=["places"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(favorites.router, prefix="/favorites", tags=["favorites"])
api_router.include_router(images.router, prefix="/images", tags=["images"])
api_router.include_router(schedules.router, prefix="/schedules", tags=["schedules"])
api_router.include_router(services.router, prefix="/services", tags=["services"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])