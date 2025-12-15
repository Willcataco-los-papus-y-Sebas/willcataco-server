from fastapi import FastAPI

from app.core.config import config
from app.api import routes

app = FastAPI(title=config.app_name)

app.include_router(routes.router, prefix="/api")