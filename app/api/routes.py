from fastapi import APIRouter
from app.modules.health.routes import router as health_router
from app.modules.users.routes import router as user_router
from app.modules.auth.routes import router as auth_router
from app.modules.members.routes import router as member_router
from app.modules.water_meters.water_payments.routes import router as water_payment_router
from app.modules.water_meters.meters.routes import router as meter_router

router = APIRouter()

router.include_router(health_router, prefix="/health", tags=["health"])
router.include_router(user_router, prefix="/users", tags=["user"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(member_router, prefix="/members", tags=["member"])
router.include_router(water_payment_router, prefix="/water-payments", tags=["water_payments"])
router.include_router(meter_router, prefix="/meters", tags=["meters"])
