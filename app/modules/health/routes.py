from fastapi import APIRouter
from app.modules.health.controller import HealthController

router = APIRouter()

@router.get("/")
async def health_check():
    return await HealthController.get_health_status()
