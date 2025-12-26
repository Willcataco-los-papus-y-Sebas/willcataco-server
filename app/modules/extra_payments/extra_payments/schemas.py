from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Lo que comparten todos los estados del objeto
class ExtraPaymentBase(BaseModel):
    name: str # Ej: "Canastón 2025"
    description: Optional[str] = None
    amount: float # Ej: 150.00
    is_active: bool = True

# Para crear un nuevo pago extra
class ExtraPaymentCreate(ExtraPaymentBase):
    pass

# Para actualizar un pago (todos los campos opcionales)
class ExtraPaymentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    is_active: Optional[bool] = None

# Lo que la API devuelve al Frontend
class ExtraPaymentResponse(ExtraPaymentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True) # Reemplaza orm_mode en Pydantic v2