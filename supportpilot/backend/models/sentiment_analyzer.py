class SentimentAnalyzer:
    def __init__(self):
        self._negative = ["angry", "worst", "terrible", "bad", "hate"]
        self._positive = ["great", "good", "thanks", "awesome", "love"]

    def analyze(self, text: str):
        t = (text or "").lower()
        score = 0
        for w in self._negative:
            if w in t:
                score -= 1
        for w in self._positive:
            if w in t:
                score += 1
        label = "neutral"
        if score < 0:
            label = "negative"
        elif score > 0:
            label = "positive"
        return {"score": score, "label": label}
