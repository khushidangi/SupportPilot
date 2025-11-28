import time
from typing import List, Dict

class Ticket:
    def __init__(self, ticket_id: str, user_id: str, subject: str, category: str = "General", sentiment: dict = None, status: str = "open", assigned_agent: str = None, created_at: float = None):
        self._id = ticket_id
        self._user_id = user_id
        self._subject = subject
        self._category = category
        self._sentiment = sentiment or {"score": 0, "label": "neutral"}
        self._status = status
        self._assigned_agent = assigned_agent
        self._messages: List[Dict] = []
        self._created_at = created_at or time.time()

    @property
    def id(self):
        return self._id

    @property
    def user_id(self):
        return self._user_id

    @property
    def subject(self):
        return self._subject

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, val):
        self._category = val

    @property
    def sentiment(self):
        return self._sentiment

    @sentiment.setter
    def sentiment(self, val):
        self._sentiment = val

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, val):
        self._status = val

    @property
    def assigned_agent(self):
        return self._assigned_agent

    @assigned_agent.setter
    def assigned_agent(self, val):
        self._assigned_agent = val

    def add_message(self, sender: str, message: str, timestamp: float = None):
        ts = timestamp or time.time()
        self._messages.append({"sender": sender, "message": message, "timestamp": ts})

    def messages(self):
        return list(self._messages)

    def to_dict(self):
        return {
            "id": self._id,
            "user_id": self._user_id,
            "subject": self._subject,
            "category": self._category,
            "sentiment": self._sentiment,
            "status": self._status,
            "assigned_agent": self._assigned_agent,
            "created_at": self._created_at,
            "messages": self._messages,
        }
