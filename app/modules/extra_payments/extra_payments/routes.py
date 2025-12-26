from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from . import schemas, services

# Definimos el router con el tag para que aparezca agrupado en Swagger
router = APIRouter(prefix="/extra-payments", tags=["Extra Payments"])

@router.get("/", response_model=list[schemas.ExtraPaymentResponse])
async def read_extra_payments(db: AsyncSession = Depends(get_db)):
    """Obtiene la lista de todos los pagos extra (canastones, eventos, etc)."""
    return await services.get_all(db)

@router.post("/", response_model=schemas.ExtraPaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_extra_payment(
    extra_payment: schemas.ExtraPaymentCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Crea un nuevo concepto de pago extra."""
    return await services.create(db, extra_payment)