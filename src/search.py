from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ADRSearch:
    def __init__(self, adrs):
        self.adrs = adrs
        corpus = [self._text(a) for a in adrs]
        self.vectorizer = TfidfVectorizer()
        self.matrix = self.vectorizer.fit_transform(corpus) if corpus else None

    def _text(self, adr):
        return f"{adr.title} {adr.context} {adr.decision} {adr.consequences}"

    def search(self, query, top_k=5):
        if self.matrix is None:
            return []
        q = self.vectorizer.transform([query])
        sims = cosine_similarity(q, self.matrix)[0]
        idx = sims.argsort()[::-1][:top_k]
        return [{"adr": self.adrs[i].__dict__, "score": float(sims[i])}
                for i in idx if sims[i] > 0]
