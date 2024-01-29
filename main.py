from fastapi import FastAPI

from settings import settings
from video_analysis.results.router import results_router
from users.router import user_router


app = FastAPI(title=settings.PROJECT_NAME)


app.include_router(user_router)
app.include_router(results_router, tags=["results"])
