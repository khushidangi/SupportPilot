class User:
    def __init__(self, user_id: str, name: str, email: str):
        self._id = user_id
        self._name = name
        self._email = email

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    def get_report(self):
        return {"type": "user", "id": self._id, "name": self._name}

    def reply_style(self):
        return "default"
