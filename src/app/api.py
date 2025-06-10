from fastapi import APIRouter
from pydantic import BaseModel
from app.llm.gemma_client import generate_reply

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    response: str

@router.post("/chat", response_model=PromptResponse)
async def chat(request: PromptRequest):
    reply = await generate_reply(request.prompt)
    return {"response": reply}