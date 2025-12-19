import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

import app.core.mapping_database
from app.api import routes
from app.core.config import config
from app.core.database import engine

logger = logging.getLogger("uvicorn.info")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            logger.info(f"Database connection successful: {config.db_name}")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
    yield

app = FastAPI(title=config.app_name, lifespan=lifespan)

app.include_router(routes.router, prefix="/api")