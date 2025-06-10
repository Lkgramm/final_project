import httpx
import os

LM_ENDPOINT = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1/completions")
MODEL_NAME = os.getenv("LM_MODEL", "google/gemma-3-12b") 
async def generate_reply(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 200,
        "stream": False
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(LM_ENDPOINT, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()["choices"][0]["text"].strip()
        except Exception as e:
            return f"[Error from Gemma client: {e}]"
