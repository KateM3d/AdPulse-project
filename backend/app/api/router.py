from fastapi import APIRouter

from app.api.routes.ads import router as ads_router
from app.api.routes.campaigns import router as campaigns_router
from app.api.routes.health import router as health_router
from app.api.routes.insights import router as insights_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(campaigns_router, tags=["Campaign"])
api_router.include_router(ads_router, tags=["Ads"])
api_router.include_router(insights_router, tags=["Insights"])
