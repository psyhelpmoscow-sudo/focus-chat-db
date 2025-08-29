from __future__ import annotations
import os
from flask import Flask, request, jsonify, send_from_directory, session
from flask_session import Session

from dotenv import load_dotenv
load_dotenv()

from app.config import SESSION_SECRET, SESSION_DIR, PROVIDER_DEFAULT, OPENAI_MODEL, YANDEX_MODEL
from app.db import init_db, SessionLocal
from app.services import ChatService

app = Flask(__name__, static_folder="static", static_url_path="")
app.config["SECRET_KEY"] = SESSION_SECRET
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = SESSION_DIR
app.config["SESSION_COOKIE_NAME"] = "focus_session"
Session(app)

init_db()

@app.get("/")
def root():
    return app.send_static_file("index.html")

@app.get("/system-prompt.txt")
def get_prompt_file():
    return send_from_directory(".", "system_prompt.txt", mimetype="text/plain; charset=utf-8")

@app.post("/api/chat")
def api_chat():
    data = request.get_json(silent=True) or {}
    user_text = (data.get("prompt") or "").strip()
    provider = (data.get("provider") or PROVIDER_DEFAULT).strip().lower()
    model = (data.get("model") or (OPENAI_MODEL if provider == "openai" else YANDEX_MODEL)).strip()

    if not user_text:
        return jsonify({"error": "Пустой запрос."}), 400

    db = SessionLocal()
    try:
        svc = ChatService(db)
        conv_id = session.get("conversation_id")
        conv = svc.ensure_conversation(conv_id, provider, model)
        session["conversation_id"] = conv.id

        svc.add_user_message(conv, user_text)
        reply = svc.reply(conv)
        svc.add_assistant_message(conv, reply)

        return jsonify({"reply": reply, "provider": provider, "model": model, "conversation_id": conv.id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.post("/api/clear")
def api_clear():
    session.pop("conversation_id", None)
    return jsonify({"cleared": True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
