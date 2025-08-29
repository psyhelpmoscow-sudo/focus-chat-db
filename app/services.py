from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from .models import Conversation, Message
from .config import PROVIDER_DEFAULT, OPENAI_MODEL, YANDEX_MODEL, MAX_HISTORY
from .llm_openai import call_openai
from .llm_yandex import call_yandex
import os, logging

log = logging.getLogger(__name__)

def load_system_prompt() -> str:
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "system_prompt.txt")
    try:
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read().strip()
            return txt or "Вы — внимательный собеседник."
    except FileNotFoundError:
        return "Вы — внимательный собеседник."

class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.system_prompt = load_system_prompt()

    def ensure_conversation(self, conversation_id: Optional[int], provider: str, model: str):
        if conversation_id:
            conv = self.db.get(Conversation, conversation_id)
            if conv:
                return conv
        conv = Conversation(provider=(provider or PROVIDER_DEFAULT),
                            model=(model or (OPENAI_MODEL if provider=='openai' else YANDEX_MODEL)))
        self.db.add(conv)
        self.db.commit()
        self.db.refresh(conv)
        return conv

    def _history_core(self, conv) -> List[Dict[str, str]]:
        limit = max(1, MAX_HISTORY - 1)
        msgs = (self.db.query(Message)
                .filter(Message.conversation_id == conv.id)
                .order_by(Message.id.desc())
                .limit(limit)
                .all())
        msgs = list(reversed(msgs))
        return [{"role": m.role, "content": m.content} for m in msgs]

    def build_messages(self, conv) -> List[Dict[str, str]]:
        core = self._history_core(conv)
        messages = [{"role": "system", "content": self.system_prompt}] + core

        seen_system = False
        deduped = []
        for m in messages:
            if m["role"] == "system":
                if seen_system:
                    continue
                seen_system = True
            deduped.append(m)
        return deduped

    def add_user_message(self, conv, text: str):
        self.db.add(Message(conversation_id=conv.id, role="user", content=text))
        self.db.commit()

    def add_assistant_message(self, conv, text: str):
        self.db.add(Message(conversation_id=conv.id, role="assistant", content=text))
        self.db.commit()

    def reply(self, conv) -> str:
        messages = self.build_messages(conv)
        try:
            log.debug("LLM messages head: %s", messages[:2])
        except Exception:
            pass

        provider = (conv.provider or PROVIDER_DEFAULT).lower().strip()
        model = conv.model or (OPENAI_MODEL if provider == "openai" else YANDEX_MODEL)

        if provider == "openai":
            return call_openai(model, messages)
        elif provider == "yandex":
            return call_yandex(model, messages)
        else:
            raise RuntimeError(f"Неизвестный провайдер: {provider}")
