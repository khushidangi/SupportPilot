from .knowledge_base import KnowledgeBase

class FAQKnowledgeBase(KnowledgeBase):
    def __init__(self, entries=None):
        self._entries = entries or []

    def load(self, entries):
        self._entries = list(entries)

    def query(self, text: str):
        text_low = text.lower()
        for e in self._entries:
            if text_low in e.get("question", "").lower() or text_low in e.get("answer", "").lower():
                return e.get("answer")
        return None

    def list_entries(self):
        return list(self._entries)

    def search(self, term: str):
        term_low = term.lower()
        out = []
        for e in self._entries:
            if term_low in e.get("question", "").lower() or term_low in e.get("answer", "").lower():
                out.append(e)
        return out
