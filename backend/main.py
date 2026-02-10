from fastapi import FastAPI

from backend.app.api.routes import router
from backend.app.core.config import settings

app = FastAPI(title=settings.app_name, version='0.1.0')
app.include_router(router)
