from datetime import datetime
from sqlalchemy import ForeignKey, Numeric, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.modules.water_meters.water_meters.model.models import WaterMeter
from app.modules.water_meters.water_payments.model.models import WaterPayment

class Meter(Base):
    __tablename__ = "meters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    water_meter_id: Mapped[int] = mapped_column(ForeignKey("water_meters.id"), index=True)
    water_reading: Mapped[float] = mapped_column(Numeric(10, 2))
    past_water_reading: Mapped[float] = mapped_column(Numeric(10, 2))
    observation: Mapped[str | None] = mapped_column(String, nullable=True)
    photo_path: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    water_meter: Mapped["WaterMeter"] = relationship("WaterMeter", back_populates="meters")
    water_payment: Mapped["WaterPayment"] = relationship("WaterPayment", back_populates="meter", uselist=False)