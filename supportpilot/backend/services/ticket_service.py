from ..models.ticket import Ticket
from .supabase_client import get_client
import time

class TicketService:
    def __init__(self):
        self._db = get_client()

    def create_ticket(self, ticket: Ticket):
        payload = {
            "id": ticket.id,
            "user_id": ticket.user_id,
            "category": ticket.category,
            "sentiment": ticket.sentiment,
            "status": ticket.status,
            "assigned_agent": ticket.assigned_agent,
            "subject": ticket.subject,
            "created_at": ticket._created_at,
        }
        resp = self._db.table("tickets").insert(payload).execute()
        for m in ticket._messages:
            self._db.table("messages").insert({"ticket_id": ticket.id, "sender": m["sender"], "message": m["message"], "timestamp": m["timestamp"]}).execute()
        return resp

    def get_tickets_for_user(self, user_id: str):
        resp = self._db.table("tickets").select("*").eq("user_id", user_id).execute()
        return resp

    def get_all_tickets(self):
        resp = self._db.table("tickets").select("*").execute()
        return resp

    def add_message(self, ticket_id: str, sender: str, message: str):
        ts = time.time()
        resp = self._db.table("messages").insert({"ticket_id": ticket_id, "sender": sender, "message": message, "timestamp": ts}).execute()
        return resp

    def assign_agent(self, ticket_id: str, agent_id: str):
        resp = self._db.table("tickets").update({"assigned_agent": agent_id}).eq("id", ticket_id).execute()
        return resp

    def get_messages(self, ticket_id: str):
        resp = self._db.table("messages").select("*").eq("ticket_id", ticket_id).order("timestamp", desc=False).execute()
        return resp
