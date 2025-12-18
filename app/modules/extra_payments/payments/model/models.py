from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.core.enums import PaymentStatus

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), index=True)
    extra_payment_id: Mapped[int] = mapped_column(ForeignKey("extra_payments.id"), index=True)
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.UNPAID)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    member: Mapped["Member"] = relationship("app.modules.members.model.models.Member", back_populates="payments")
    extra_payment: Mapped["ExtraPayment"] = relationship("app.modules.extra_payments.extra_payments.model.models.ExtraPayment", back_populates="payments")