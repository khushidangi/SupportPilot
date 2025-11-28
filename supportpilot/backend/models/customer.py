from .user import User


class Customer(User):
    def __init__(self, user_id: str, name: str, email: str, loyalty_points: int = 0):
        super().__init__(user_id, name, email)
        self._loyalty_points = loyalty_points

    def add_points(self, pts: int):
        self._loyalty_points += pts

    def get_report(self):
        return {"type": "customer", "id": self.id, "points": self._loyalty_points}
