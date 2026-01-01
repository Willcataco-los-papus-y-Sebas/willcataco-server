from fastapi import APIRouter
from app.modules.health.routes import router as health_router
from app.modules.users.routes import router as user_router
from app.modules.water_meters.water_measure.routes import router as water_meter_router
from app.modules.auth.routes import router as auth_router
from app.modules.water_meters.actions.routes import router as actions_router
from app.modules.auth.routes import router as auth_router
from app.modules.extra_payments.payments.routes import router as payments_router
from app.modules.water_meters.action_payments.routes import router as action_payments_router
from app.modules.members.routes import router as member_router
from app.modules.water_meters.streets.routes import router as street_router
from app.modules.extra_payments.extra_payments.routes import router as extra_payments_router


router = APIRouter()

router.include_router(health_router, prefix="/health", tags=["health"])
router.include_router(user_router, prefix="/users", tags=["user"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(actions_router, prefix="/actions", tags=["actions"])
router.include_router(water_meter_router, prefix="/water_measure", tags=["water_measure"])
router.include_router(payments_router, prefix="/payments", tags=["payments"])
router.include_router(water_meter_router, prefix="/water_measure", tags=["water_measure"])
router.include_router(action_payments_router, prefix="/action-payments", tags=["action_payments"])
router.include_router(member_router, prefix="/members", tags=["member"])
router.include_router(street_router, prefix="/street", tags=["street"]) 
router.include_router(extra_payments_router, prefix="/extra-payments", tags=["extra-payments"])
