from __future__ import annotations

from typing import Iterable, Sequence

from .lexicon import Lexicon
from .models import ReasoningResult
from .phonology import normalize_phonemes, phonological_similarity
from .reasoner import PhonemicReasoner, ReasonerWeights


class PhonemicReasoningEngine:
    def __init__(
        self,
        lexicon: Lexicon,
        *,
        weights: ReasonerWeights | None = None,
        minimum_similarity: float = 0.45,
    ) -> None:
        self.lexicon = lexicon
        self.reasoner = PhonemicReasoner(
            lexicon,
            weights=weights,
            minimum_similarity=minimum_similarity,
        )

    def reason(
        self,
        observed_phonemes: Sequence[str],
        *,
        context: Iterable[str] = (),
    ) -> ReasoningResult:
        observed = normalize_phonemes(observed_phonemes)
        context_tuple = tuple(context)
        return ReasoningResult(
            observed_phonemes=observed,
            context=context_tuple,
            hypotheses=self.reasoner.rank(observed, context_tuple),
        )

    def segment(
        self,
        phoneme_stream: Sequence[str],
        *,
        max_word_phones: int = 8,
        unknown_penalty: float = 1.25,
    ) -> tuple[str, ...]:
        phones = normalize_phonemes(phoneme_stream)
        n = len(phones)
        best_cost = [float("inf")] * (n + 1)
        best_path: list[tuple[str, ...] | None] = [None] * (n + 1)
        best_cost[0] = 0.0
        best_path[0] = ()
        entries = tuple(self.lexicon)

        for start in range(n):
            if best_path[start] is None:
                continue

            matched = False
            upper = min(n, start + max_word_phones)
            for end in range(start + 1, upper + 1):
                span = phones[start:end]
                for entry in entries:
                    similarity = phonological_similarity(span, entry.phonemes)
                    if similarity < 0.70:
                        continue
                    matched = True
                    candidate_cost = best_cost[start] + (1.0 - similarity)
                    if candidate_cost < best_cost[end]:
                        best_cost[end] = candidate_cost
                        best_path[end] = best_path[start] + (entry.word,)

            if not matched and start + 1 <= n:
                candidate_cost = best_cost[start] + unknown_penalty
                if candidate_cost < best_cost[start + 1]:
                    best_cost[start + 1] = candidate_cost
                    best_path[start + 1] = best_path[start] + (f"<{phones[start]}>",)

        return best_path[n] or tuple(f"<{phone}>" for phone in phones)
