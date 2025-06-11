from fastapi import FastAPI
from .web import router as web_router
from .api import router as api_router
from .db import init_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(web_router)
app.include_router(api_router)
