from .sentiment_analyzer import SentimentAnalyzer
from .router import TicketRouter

class ChatEngine:
    def __init__(self):
        self._sent = SentimentAnalyzer()
        self._router = TicketRouter()

    def analyze(self, text: str):
        return self._sent.analyze(text)

    def categorize(self, text: str):
        return self._router.route(text)

    def auto_reply(self, text: str, role: str = "agent"):
        sentiment = self._sent.analyze(text)
        category = self._router.route(text)
        if sentiment["label"] == "negative":
            base = "We are sorry to hear that. "
        elif sentiment["label"] == "positive":
            base = "Thanks for the update! "
        else:
            base = "Thanks for reaching out. "
        if role == "agent":
            template = base + f"Our {category} team will review and respond shortly."
        else:
            template = base + f"A support agent will get back to you about {category} issues."
        return {"reply": template, "category": category, "sentiment": sentiment}

    def summarize(self, messages: list):
        text = " ".join([m.get("message", "") for m in messages])
        words = {}
        for w in (text or "").lower().split():
            words[w] = words.get(w, 0) + 1
        sorted_words = sorted(words.items(), key=lambda x: x[1], reverse=True)
        keywords = [w for w, _ in sorted_words[:5]]
        return "Summary: " + ", ".join(keywords)
