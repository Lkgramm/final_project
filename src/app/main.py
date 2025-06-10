from fastapi import FastAPI
from app.api import router

app = FastAPI(title="Friends-bot")

app.include_router(router)