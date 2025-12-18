from datetime import datetime
from sqlalchemy import ForeignKey, Numeric, DateTime, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.core.enums import ActionStatus
from app.modules.water_meters.action_payments.model.models import ActionPayment
from app.modules.water_meters.streets.model.models import Street
from app.modules.water_meters.water_meters.model.models import WaterMeter

class Action(Base):
    __tablename__ = "actions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), index=True)
    street_id: Mapped[int] = mapped_column(ForeignKey("streets.id"), index=True)
    total_price: Mapped[float] = mapped_column(Numeric(10, 2))
    status: Mapped[ActionStatus] = mapped_column(Enum(ActionStatus), default=ActionStatus.UNPAID)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    member: Mapped["Member"] = relationship("app.modules.members.model.models.Member", back_populates="actions")
    street: Mapped["Street"] = relationship("Street", back_populates="actions")
    payments: Mapped[list["ActionPayment"]] = relationship("ActionPayment", back_populates="action")
    water_meters: Mapped[list["WaterMeter"]] = relationship("WaterMeter", back_populates="action")