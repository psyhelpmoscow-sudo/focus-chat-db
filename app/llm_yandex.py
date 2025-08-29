from typing import List, Dict
import requests
from .config import YANDEX_API_KEY, YA_FOLDER_ID

def call_yandex(model: str, messages: List[Dict[str, str]]) -> str:
    if not YANDEX_API_KEY:
        raise RuntimeError("YANDEX_API_KEY не задан")
    if not YA_FOLDER_ID:
        raise RuntimeError("YA_FOLDER_ID не задан")

    ya_msgs = []
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        ya_msgs.append({"role": role, "text": content})

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {"Authorization": f"Api-Key {YANDEX_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "modelUri": f"gpt://{YA_FOLDER_ID}/{model}",
        "completionOptions": {"stream": False, "temperature": 0.6, "maxTokens": "1000"},
        "messages": ya_msgs,
    }
    r = requests.post(url, headers=headers, json=payload, timeout=120)
    r.raise_for_status()
    obj = r.json()
    return obj["result"]["alternatives"][0]["message"]["text"].strip()
