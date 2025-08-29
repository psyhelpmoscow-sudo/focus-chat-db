from typing import List, Dict
import requests
from .config import OPENAI_API_KEY, OPENAI_BASE_URL

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

def call_openai(model: str, messages: List[Dict[str, str]]) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY не задан")
    if OpenAI is not None:
        client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
        try:
            chat = client.chat.completions.create(
                model=model,
                messages=messages
            )
            return (chat.choices[0].message.content or "").strip()
        except Exception:
            pass
    url = (OPENAI_BASE_URL or "https://api.openai.com/v1").rstrip("/") + "/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": messages}
    r = requests.post(url, headers=headers, json=payload, timeout=120)
    r.raise_for_status()
    obj = r.json()
    return (obj["choices"][0]["message"]["content"] or "").strip()
