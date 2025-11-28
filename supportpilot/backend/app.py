from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from models.chat_engine import ChatEngine
from services.ticket_service import TicketService
from services.user_service import UserService
from models.faq_kb import FAQKnowledgeBase

load_dotenv()

app = Flask(__name__)
CORS(app)

_chat = ChatEngine()
_ticket_service = TicketService()
_user_service = UserService()
_faq = FAQKnowledgeBase()

@app.route("/create_ticket", methods=["POST"])
def create_ticket():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    subject = data.get("subject", "No Subject")
    message = data.get("message", "")
    from models.ticket import Ticket
    t = Ticket(data.get("id") or str(int(os.times().system)), user_id, subject)
    t.add_message(user_id, message)
    t.category = _chat.categorize(subject + " " + message)
    t.sentiment = _chat.analyze(message)
    resp = _ticket_service.create_ticket(t)
    return jsonify({"ok": True, "result": getattr(resp, 'data', resp)}), 201

@app.route("/get_tickets", methods=["GET"])
def get_tickets():
    user_id = request.args.get("user_id")
    if user_id:
        resp = _ticket_service.get_tickets_for_user(user_id)
    else:
        resp = _ticket_service.get_all_tickets()
    return jsonify({"ok": True, "tickets": getattr(resp, 'data', resp)}), 200

@app.route("/analyze_sentiment", methods=["POST"])
def analyze_sentiment():
    data = request.get_json() or {}
    text = data.get("text", "")
    out = _chat.analyze(text)
    return jsonify({"ok": True, "sentiment": out}), 200

@app.route("/auto_reply", methods=["POST"])
def auto_reply():
    data = request.get_json() or {}
    text = data.get("text", "")
    role = data.get("role", "agent")
    out = _chat.auto_reply(text, role=role)
    return jsonify({"ok": True, "reply": out}), 200

@app.route("/assign_agent", methods=["POST"])
def assign_agent():
    data = request.get_json() or {}
    ticket_id = data.get("ticket_id")
    agent_id = data.get("agent_id")
    resp = _ticket_service.assign_agent(ticket_id, agent_id)
    return jsonify({"ok": True, "result": getattr(resp, 'data', resp)}), 200

@app.route("/get_faq", methods=["GET"])
def get_faq():
    term = request.args.get("q", "")
    if term:
        out = _faq.search(term)
    else:
        out = _faq.list_entries()
    return jsonify({"ok": True, "faq": out}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
