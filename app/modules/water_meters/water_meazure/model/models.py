from datetime import datetime
from sqlalchemy import ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class WaterMeter(Base):
    __tablename__ = "water_meters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    action_id: Mapped[int] = mapped_column(ForeignKey("actions.id"), index=True)
    water_reading: Mapped[float] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    action: Mapped["Action"] = relationship("app.modules.water_meazure=.actions.model.models.Action", back_populates="water_meters")
    meters: Mapped[list["Meter"]] = relationship("app.modules.water_meazure.meters.model.models.Meter", back_populates="water_meter")