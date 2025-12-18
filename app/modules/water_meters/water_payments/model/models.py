from datetime import datetime
from sqlalchemy import ForeignKey, Numeric, DateTime, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.modules.members.model.models import Member
from app.core.enums import PaymentStatus
from app.modules.water_meters.meters.model.models import Meter

class WaterPayment(Base):
    __tablename__ = "water_payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    meter_id: Mapped[int] = mapped_column(ForeignKey("meters.id"), unique=True, index=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), index=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.UNPAID)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    meter: Mapped["Meter"] = relationship("Meter", back_populates="water_payment")
    member: Mapped["Member"] = relationship("Member", back_populates="water_payments")