class TicketRouter:
    def __init__(self):
        self._rules = {
            "billing": ["refund", "payment", "charge"],
            "delivery": ["delay", "order", "shipped", "delivery"],
            "technical": ["issue", "broken", "error", "bug"],
        }

    def route(self, text: str):
        t = (text or "").lower()
        for cat, keywords in self._rules.items():
            for k in keywords:
                if k in t:
                    return cat.capitalize()
        return "General"
