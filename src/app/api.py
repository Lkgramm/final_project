from fastapi import APIRouter
from pydantic import BaseModel
from app.llm.gemma_client import generate_reply, DEFAULT_CHARACTER


router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str
    character: str = DEFAULT_CHARACTER  # Новое поле

class PromptResponse(BaseModel):
    response: str

@router.post("/chat", response_model=PromptResponse)
async def chat(request: PromptRequest):
    reply = await generate_reply(request.prompt, character=request.character)
    return {"response": reply}