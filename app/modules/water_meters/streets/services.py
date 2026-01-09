from sqlalchemy import select, func

from app.core.database import SessionDep
from app.modules.water_meters.streets.model.models import Street
from app.modules.water_meters.streets.model.schemas import (
    StreetBase,
    StreetResponse
)


class StreetServices():

    @staticmethod
    async def create_street(session: SessionDep, street_info: StreetBase):
        try:
            new_street = Street(
                name = street_info.name
            )
            session.add(new_street)
            await session.commit()
            await session.refresh(new_street)
            return StreetResponse.model_validate(new_street)
        except Exception:
            await session.rollback()
            raise
    

    @staticmethod
    async def patch_info_street(session: SessionDep, id: int, street_info: StreetBase):
        try:
            street = await session.execute(select(Street).where(Street.id == id))
            street_orm = street.scalars().one_or_none()
            if street_info.name is not None:
                street_orm.name = street_info.name
            await session.commit()
            await session.refresh(street_orm)
            return StreetResponse.model_validate(street_orm)
        except Exception:
            await session.rollback()
            raise
    

    @staticmethod
    async def delete_street(session: SessionDep, id: int):
        try:
            street = await session.execute(select(Street).where(Street.id == id))
            street_orm = street.scalars().one_or_none()
            street_orm.deleted_at = func.now()
            await session.commit()
        except Exception:
            await session.rollback()
            raise


    @staticmethod
    async def get_street_by_id(session: SessionDep, id: int):
        try:
            street = await session.execute(select(Street).where(Street.id == id))
            street_orm = street.scalars().one_or_none()
            return StreetResponse.model_validate(street_orm) if street_orm else None
        except Exception:
            await session.rollback()
            raise

    
    @staticmethod
    async def get_street_by_name(session: SessionDep, name: str):
        try:
            street = await session.execute(select(Street).where(Street.name == name))
            street_orm = street.scalars().one_or_none()
            return StreetResponse.model_validate(street_orm) if street_orm else None
        except Exception:
            await session.rollback()
            raise
    

    @staticmethod
    async def get_all_streets(session: SessionDep):
        try:
            streets = await session.execute(select(Street).where(Street.deleted_at.is_(None)).order_by(Street.id))
            streets_orm = streets.scalars().all()
            return [StreetResponse.model_validate(s) for s in streets_orm]
        except Exception:
            await session.rollback()
            raise