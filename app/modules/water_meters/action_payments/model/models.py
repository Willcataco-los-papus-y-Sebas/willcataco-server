from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, func, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.modules.water_meters.actions.model.models import Action

class ActionPayment(Base):
    __tablename__ = "action_payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    action_id: Mapped[int] = mapped_column(ForeignKey("actions.id"), index=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    action: Mapped["Action"] = relationship("Action", back_populates="payments")