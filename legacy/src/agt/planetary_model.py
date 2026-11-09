from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from .memory import SQLiteMemoryStore


STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "into", "does",
    "not", "are", "was", "were", "uma", "com", "para", "que", "como",
    "das", "dos", "por", "não", "nao", "agora", "sobre", "entre",
}


@dataclass(frozen=True)
class LearningResult:
    observation_id: Optional[int]
    content_hash: str
    document_id: int
    term_count: int
    top_terms: List[str]


class PlanetarySymbolicModel:
    """
    Local trainable symbolic model.

    This is deliberately modest: it learns a weighted vocabulary from live
    observations and persists document vectors. It is not an LLM, but it is a
    real trained local model that can be inspected, reloaded and updated.
    """

    def __init__(self, memory: SQLiteMemoryStore) -> None:
        self.memory = memory

    def train_text(
        self,
        text: str,
        observation_id: Optional[int] = None,
    ) -> LearningResult:
        term_counts = _count_terms(text)
        content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        vector = _tf_vector(term_counts)

        self.memory.upsert_model_terms(term_counts)
        document_id = self.memory.add_model_document(
            observation_id=observation_id,
            content_hash=content_hash,
            term_vector=vector,
        )

        top_terms = [
            term
            for term, _count in sorted(
                term_counts.items(),
                key=lambda item: (-item[1], item[0]),
            )[:10]
        ]

        return LearningResult(
            observation_id=observation_id,
            content_hash=content_hash,
            document_id=document_id,
            term_count=sum(term_counts.values()),
            top_terms=top_terms,
        )

    def summarize(self, limit: int = 12) -> str:
        terms = self.memory.top_model_terms(limit)
        if not terms:
            return "Planetary symbolic model has no learned terms yet."

        rendered = ", ".join(
            f"{row['term']}({row['count']})"
            for row in terms
        )
        return f"Learned planetary terms: {rendered}"


def _count_terms(text: str) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for token in _tokens(text):
        if token in STOPWORDS or len(token) < 3:
            continue
        counts[token] = counts.get(token, 0) + 1
    return counts


def _tf_vector(counts: Dict[str, int]) -> Dict[str, float]:
    total = max(sum(counts.values()), 1)
    return {
        term: math.log1p(count) / math.log1p(total)
        for term, count in sorted(counts.items())
    }


def _tokens(text: str) -> Iterable[str]:
    token = []
    for char in text.lower():
        if char.isalnum():
            token.append(char)
        elif token:
            yield "".join(token)
            token = []
    if token:
        yield "".join(token)
