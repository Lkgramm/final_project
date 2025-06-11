from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .llm.gemma_client import generate_reply
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "response": None})

@router.post("/", response_class=HTMLResponse)
async def chat(request: Request, prompt: str = Form(...), character: str = Form("phoebe")):
    response = await generate_reply(prompt, character=character)
    return templates.TemplateResponse("index.html", {"request": request, "response": response, "prompt": prompt})
