# Focus Chat (DB edition)

Веб-чат с ИИ (OpenAI/Yandex) + хранение истории в базе (SQLite/SQLAlchemy). Интерфейс и системный промпт — как в простом варианте; логика работы вынесена в слои и файл `app/config.py` для переключателей.

## Запуск локально

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # заполните ключи
python server.py
# открыть http://127.0.0.1:5000
```

## Deploy на Render (Web Service)

- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn server:app --bind 0.0.0.0:$PORT`
- Environment Variables: как в `.env.example` (на проде вместо SQLite лучше Postgres).
