import os

# --- Переключатели и настройки (читаются из окружения) ---
PROVIDER_DEFAULT = os.getenv("PROVIDER_DEFAULT", "openai").strip().lower()

# OpenAI
OPENAI_API_KEY   = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_BASE_URL  = (os.getenv("OPENAI_BASE_URL", "") or "").strip() or None
OPENAI_MODEL     = os.getenv("OPENAI_MODEL", "gpt-5").strip()

# Yandex
YANDEX_API_KEY   = os.getenv("YANDEX_API_KEY", "").strip()
YA_FOLDER_ID     = os.getenv("YA_FOLDER_ID", "").strip()
YANDEX_MODEL     = os.getenv("YANDEX_MODEL", "yandexgpt-lite").strip()

# Flask/session
SESSION_SECRET   = os.getenv("SESSION_SECRET", "change-me-please")
SESSION_DIR      = os.getenv("SESSION_DIR", "./.flask_session")

# DB
DATABASE_URL     = os.getenv("DATABASE_URL", "sqlite:///db.sqlite")  # для Render лучше Postgres
MAX_HISTORY      = int(os.getenv("MAX_HISTORY", "15"))  # сколько последних сообщений включать в запрос к LLM
