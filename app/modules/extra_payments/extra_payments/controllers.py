from fastapi import HTTPException

from app.core.database import SessionDep
from app.core.response_schema import IResponse

from app.modules.extra_payments.extra_payments.services import ExtraPaymentService
from app.modules.extra_payments.extra_payments.schemas import (
    ExtraPaymentCreate,
    ExtraPaymentUpdate,
)

class ExtraPaymentController:

    @staticmethod
    async def read_all(session: SessionDep):
        payments = await ExtraPaymentService.get_all(session)
        response = IResponse(
            detail="Extra payments found",
            status_code=200,
            data=payments
        )
        return response

    @staticmethod
    async def read_by_id(session: SessionDep, payment_id: int):
        payment = await ExtraPaymentService.get_by_id(session, payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Extra payment not found")

        response = IResponse(
            detail="Extra payment found",
            status_code=200,
            data=payment
        )
        return response

    @staticmethod
    async def create(session: SessionDep, data: ExtraPaymentCreate):
        payment = await ExtraPaymentService.create(session, data)
        response = IResponse(
            detail="Extra payment created",
            status_code=201,
            data=payment
        )
        return response

    @staticmethod
    async def update(
        session: SessionDep,
        payment_id: int,
        data: ExtraPaymentUpdate
    ):
        payment = await ExtraPaymentService.get_by_id(session, payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Extra payment not found")

        updated_payment = await ExtraPaymentService.update(
            session,
            payment_id,
            data
        )

        response = IResponse(
            detail="Extra payment updated",
            status_code=200,
            data=updated_payment
        )
        return response

    @staticmethod
    async def delete(session: SessionDep, payment_id: int):
        payment = await ExtraPaymentService.get_by_id(session, payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Extra payment not found")

        await ExtraPaymentService.delete_logical(session, payment_id)

        response = IResponse(
            detail="Extra payment deleted",
            status_code=200
        )
        return response
