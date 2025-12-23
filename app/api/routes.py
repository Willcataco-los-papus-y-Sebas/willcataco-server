from fastapi import APIRouter
from app.modules.health.routes import router as health_router
from app.modules.users.routes import router as user_router
<<<<<<< HEAD
from app.modules.auth.routes import router as auth_router
=======
from app.modules.members.routes import router as member_router
>>>>>>> 4ef0c5d (feat: add router for members)

router = APIRouter()

router.include_router(health_router, prefix="/health", tags=["health"])
router.include_router(user_router, prefix="/users", tags=["user"])
<<<<<<< HEAD
router.include_router(auth_router, prefix="/auth", tags=["auth"])
=======
router.include_router(member_router, prefix="/members", tags=["member"])
>>>>>>> 4ef0c5d (feat: add router for members)
