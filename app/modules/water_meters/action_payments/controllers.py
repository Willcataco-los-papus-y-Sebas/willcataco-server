from fastapi import HTTPException
from app.core.database import SessionDep
from app.core.response_schema import IResponse
from app.modules.water_meters.action_payments.model.schemas import ActionPaymentCreate, ActionPaymentPatch
from app.modules.water_meters.action_payments.services import ActionPaymentService

class ActionPaymentController:
    @staticmethod
    async def create_payment(session: SessionDep, payment_info: ActionPaymentCreate):
        try:
            payment = await ActionPaymentService.create_payment(session, payment_info)
            return IResponse(detail="Payment created", status_code=201, data=payment)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def read_payment(id: int, session: SessionDep):
        payment = await ActionPaymentService.get_payment_by_id(session, id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return IResponse(detail="Payment found", status_code=200, data=payment)

    @staticmethod
    async def read_all_payments(session: SessionDep, skip: int = 0, limit: int = 100):
        payments = await ActionPaymentService.get_all_payments(session, skip, limit)
        return IResponse(detail="Payments list", status_code=200, data=payments)

    @staticmethod
    async def update_payment(id: int, session: SessionDep, payment_info: ActionPaymentPatch):
        payment = await ActionPaymentService.get_payment_by_id(session, id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        updated_payment = await ActionPaymentService.update_payment(session, id, payment_info)
        return IResponse(detail="Payment updated", status_code=200, data=updated_payment)

    @staticmethod
    async def delete_payment(id: int, session: SessionDep):
        payment = await ActionPaymentService.get_payment_by_id(session, id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
            
        await ActionPaymentService.delete_payment(session, id)
        return IResponse(detail="Payment deleted", status_code=200)
