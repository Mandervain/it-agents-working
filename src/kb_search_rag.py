from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

KB_ROOT = Path("knowledge_base")

_vectorizer: TfidfVectorizer | None = None
_matrix = None
_articles: list[str] = []


def _build_index() -> None:
    global _vectorizer, _matrix, _articles
    kb_files = sorted(KB_ROOT.glob("*.md"))
    _articles = [f.read_text() for f in kb_files]
    _vectorizer = TfidfVectorizer(stop_words="english")
    _matrix = _vectorizer.fit_transform(_articles)


def find_kb_article_rag(query: str, threshold: float = 0.05) -> str | None:
    if _vectorizer is None:
        _build_index()

    if not _articles:
        return None

    query_vec = _vectorizer.transform([query])
    scores = cosine_similarity(query_vec, _matrix).flatten()
    best_idx = int(np.argmax(scores))

    if scores[best_idx] < threshold:
        return None

    return _articles[best_idx]
