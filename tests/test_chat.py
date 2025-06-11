import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from src.app.main import app
from src.app.db import init_db

@pytest.mark.asyncio
async def test_chat_response():
    await init_db()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/chat", json={"prompt": "Привет!", "character": "phoebe"})
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert isinstance(data["response"], str)
    assert len(data["response"]) > 0
