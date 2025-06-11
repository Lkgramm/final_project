from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db import init_db
from .api import router as api_router
from .web import router as web_router
from dotenv import load_dotenv
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
app.include_router(web_router)
