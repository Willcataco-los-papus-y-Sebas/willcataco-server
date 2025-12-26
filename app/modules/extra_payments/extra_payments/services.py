from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime
from typing import Sequence

from .model.models import ExtraPayment
from . import schemas

async def get_all(db: AsyncSession) -> Sequence[ExtraPayment]:
    """Obtiene todos los pagos extra (canastones, eventos) que no han sido borrados."""
    query = select(ExtraPayment).where(ExtraPayment.deleted_at == None)
    result = await db.execute(query)
    return result.scalars().all()

async def get_by_id(db: AsyncSession, extra_payment_id: int) -> ExtraPayment | None:
    """Busca un pago extra específico por su ID."""
    query = select(ExtraPayment).where(
        ExtraPayment.id == extra_payment_id, 
        ExtraPayment.deleted_at == None
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create(db: AsyncSession, data: schemas.ExtraPaymentCreate) -> ExtraPayment:
    """Crea un nuevo registro de pago extra (ej: Canastón de Navidad)."""
    new_extra_payment = ExtraPayment(**data.model_dump())
    db.add(new_extra_payment)
    await db.commit()
    await db.refresh(new_extra_payment)
    return new_extra_payment

async def delete_logical(db: AsyncSession, payment_id: int):
    """Realiza un borrado lógico marcando la fecha en deleted_at."""
    query = update(ExtraPayment).where(ExtraPayment.id == payment_id).values(
        deleted_at=datetime.now()
    )
    await db.execute(query)
    await db.commit()
    return {"message": "Registro eliminado con éxito"}