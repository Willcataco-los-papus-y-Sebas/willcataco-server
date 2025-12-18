from datetime import datetime
from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.modules.users.model.models import User
from app.modules.extra_payments.payments.model.models import Payment
from app.modules.water_meters.actions.model.models import Action
from app.modules.water_meters.water_payments.model.models import WaterPayment

class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, index=True)    
    name: Mapped[str] = mapped_column(String, index=True)
    last_name: Mapped[str] = mapped_column(String, index=True)
    ci: Mapped[str] = mapped_column(String, unique=True, index=True)
    phone: Mapped[str] = mapped_column(String, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="member")
    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="member")
    actions: Mapped[list["Action"]] = relationship("Action", back_populates="member")
    water_payments: Mapped[list["WaterPayment"]] = relationship("WaterPayment", back_populates="member")
