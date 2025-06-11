from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from .llm.gemma_client import generate_reply, DEFAULT_CHARACTER
from .models import ChatSession, Message
from .db import SessionLocal
from sqlalchemy.future import select
import uuid

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str
    character: str = DEFAULT_CHARACTER
    session_id: str | None = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest, db=Depends(get_db)):
    if not payload.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    session_id = payload.session_id or str(uuid.uuid4())

    # 1. Load or create session
    stmt = select(ChatSession).where(ChatSession.id == session_id)
    result = await db.execute(stmt)
    session = result.scalars().first()
    if not session:
        session = ChatSession(id=session_id, character=payload.character)
        db.add(session)

    # 2. Add user message
    user_msg = Message(session_id=session_id, role="user", content=payload.prompt)
    db.add(user_msg)

    # 3. Generate reply
    reply = await generate_reply(prompt=payload.prompt, character=payload.character)

    # 4. Add bot message
    bot_msg = Message(session_id=session_id, role="bot", content=reply)
    db.add(bot_msg)

    await db.commit()

    return ChatResponse(response=reply, session_id=session_id)


@router.get("/history/{session_id}")
async def get_history(session_id: str, db=Depends(get_db)):
    stmt = select(Message).where(Message.session_id == session_id).order_by(Message.timestamp)
    result = await db.execute(stmt)
    messages = result.scalars().all()
    return [
        {"role": m.role, "content": m.content, "timestamp": m.timestamp.isoformat()} for m in messages
    ]