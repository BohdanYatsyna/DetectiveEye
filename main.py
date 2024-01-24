from fastapi import FastAPI

from user_app.router import user_router
from results_app.router import results_router


app = FastAPI()


app.include_router(user_router)
app.include_router(results_router)
