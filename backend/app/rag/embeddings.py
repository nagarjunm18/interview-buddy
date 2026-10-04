import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class EmbeddingService:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )
        self.fitted = False

    def fit(self, texts: list[str]):
        self.vectorizer.fit(texts)
        self.fitted = True

    def embed(self, texts: list[str]):
        if not self.fitted:
            self.fit(texts)

        vectors = self.vectorizer.transform(texts).toarray()

        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1

        return vectors / norms