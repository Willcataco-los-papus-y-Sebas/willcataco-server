from fastapi import HTTPException
from app.core.database import SessionDep
from app.core.response_schema import IResponse
from app.modules.water_meters.water_payments.model.schemas import WaterPaymentBase
from app.modules.water_meters.water_payments.services import WaterPaymentService

class WaterPaymentController:
    @staticmethod
    async def create_water_payment(session: SessionDep, payment_info: WaterPaymentBase):
        payment = await WaterPaymentService.create_water_payment(session, payment_info)
        response = IResponse(detail="Water payment created", status_code=201, data=payment)
        return response

    @staticmethod
    async def change_status(id: int, session: SessionDep):
        payment = await WaterPaymentService.get_water_payment_by_id(session, id)
        if not payment:
            raise HTTPException(status_code=404, detail="water payment not found")
        updated_payment = await WaterPaymentService.change_status(session, id)
        response = IResponse(detail="Water payment status updated", status_code=200, data=updated_payment)
        return response

    @staticmethod
    async def read_water_payment(id: int, session: SessionDep):
        payment = await WaterPaymentService.get_water_payment_by_id(session, id)
        if not payment:
            raise HTTPException(status_code=404, detail="water payment not found")
        response = IResponse(detail="Water payment retrieved", status_code=200, data=payment)
        return response

    @staticmethod
    async def delete_water_payment(id: int, session: SessionDep):
        payment = await WaterPaymentService.get_water_payment_by_id(session, id)
        if not payment:
            raise HTTPException(status_code=404, detail="water payment not found")
        await WaterPaymentService.delete_water_payment(session, id)
        response = IResponse(detail="Water payment deleted", status_code=200)
        return response