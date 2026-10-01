from fastapi import APIRouter
from app.api.routes import auth, buses, routes, locations

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(buses.router, prefix="/buses", tags=["buses"])
api_router.include_router(routes.router, prefix="/routes", tags=["routes"])
api_router.include_router(locations.router, prefix="/buses", tags=["locations"])
