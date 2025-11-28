from .user import User

class SupportAgent(User):
    def __init__(self, user_id: str, name: str, email: str, level: str = "tier1"):
        super().__init__(user_id, name, email)
        self._level = level

    @property
    def level(self):
        return self._level

    def get_report(self):
        return {"type": "agent", "id": self.id, "name": self.name, "level": self._level}

    def reply_style(self):
        return "formal"
