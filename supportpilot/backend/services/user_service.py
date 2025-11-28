from ..models.user import User
from .supabase_client import get_client
import time

class UserService:
    def __init__(self):
        self._db = get_client()

    def create_user(self, user_id: str, name: str, email: str, type_: str = "customer"):
        payload = {"id": user_id, "name": name, "email": email, "type": type_}
        resp = self._db.table("users").insert(payload).execute()
        return resp

    def get_user(self, user_id: str):
        resp = self._db.table("users").select("*").eq("id", user_id).execute()
        data = resp.data if hasattr(resp, "data") else resp
        if data and len(data) > 0:
            d = data[0]
            return User(d.get("id"), d.get("name"), d.get("email"))
        return None
