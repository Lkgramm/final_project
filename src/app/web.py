from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .models import ChatSession, Message
from .db import SessionLocal
from sqlalchemy.future import select

router = APIRouter()
templates = Jinja2Templates(directory="templates")

async def get_db():
    async with SessionLocal() as session:
        yield session


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, db=Depends(get_db)):
    stmt = select(ChatSession).order_by(ChatSession.created_at.desc()).limit(10)
    result = await db.execute(stmt)
    sessions = result.scalars().all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "sessions": sessions
    })



@router.get("/history_ui/{session_id}", response_class=HTMLResponse)
async def history_ui(session_id: str, request: Request, db=Depends(get_db)):
    stmt = select(Message).where(Message.session_id == session_id).order_by(Message.timestamp)
    result = await db.execute(stmt)
    messages = result.scalars().all()
    return templates.TemplateResponse("history.html", {
        "request": request,
        "session_id": session_id,
        "messages": messages
    })
