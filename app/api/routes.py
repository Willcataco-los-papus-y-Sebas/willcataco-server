from fastapi import APIRouter
from app.modules.health.routes import router as health_router
from app.modules.users.routes import router as user_router

router = APIRouter()

router.include_router(health_router, prefix="/health", tags=["health"])
router.include_router(user_router, prefix="/users", tags=["user"])