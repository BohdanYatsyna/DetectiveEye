from fastapi import FastAPI

from core.settings import settings
from results_app.router import results_router
from user_app.router import user_router


app = FastAPI(title=settings.PROJECT_NAME)


app.include_router(user_router)
app.include_router(results_router, tags=["results"])
