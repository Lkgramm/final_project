from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .models import ChatSession, Message
from .db import SessionLocal
from sqlalchemy.future import select
from pathlib import Path
from .llm.gemma_client import generate_reply
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("/", response_class=HTMLResponse)
async def chat_form(
    request: Request,
    prompt: str = Form(...),
    character: str = Form("phoebe"),
    db: AsyncSession = Depends(get_db)
):
    # создаём сессию и сохраняем user message
    session_id = str(uuid.uuid4())
    session = ChatSession(id=session_id, character=character)
    db.add(session)
    db.add(Message(session_id=session_id, role="user", content=prompt))

    # вызываем модель
    reply = await generate_reply(prompt, character=character)
    db.add(Message(session_id=session_id, role="bot", content=reply))

    await db.commit()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "prompt": prompt,
        "response": reply
    })

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
