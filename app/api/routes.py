from fastapi import APIRouter
from app.modules.health.routes import router as health_router
from app.modules.users.routes import router as user_router
from app.modules.auth.routes import router as auth_router
from app.modules.water_meters.action_payments.routes import router as action_payments_router
from app.modules.members.routes import router as member_router

router = APIRouter()

router.include_router(health_router, prefix="/health", tags=["health"])
router.include_router(user_router, prefix="/users", tags=["user"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(action_payments_router, prefix="/action-payments", tags=["action_payments"])
router.include_router(member_router, prefix="/members", tags=["member"])
