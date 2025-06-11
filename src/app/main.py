from fastapi import FastAPI
from .api import router as api_router
from .web import router as web_router  # Импортируем веб-интерфейс

app = FastAPI()

app.include_router(api_router, prefix="/chat")
app.include_router(web_router)