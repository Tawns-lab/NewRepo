from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Sequence

from .lexicon import Lexicon
from .models import CandidateScore, RankedHypothesis
from .phonology import normalize_phonemes, phonological_similarity


@dataclass(frozen=True, slots=True)
class ReasonerWeights:
    phonology: float = 0.65
    context: float = 0.25
    prior: float = 0.10

    def __post_init__(self) -> None:
        if self.phonology + self.context + self.prior <= 0:
            raise ValueError("weights must sum to a positive value")


class PhonemicReasoner:
    def __init__(
        self,
        lexicon: Lexicon,
        *,
        weights: ReasonerWeights | None = None,
        minimum_similarity: float = 0.45,
        max_candidates: int = 12,
    ) -> None:
        self.lexicon = lexicon
        self.weights = weights or ReasonerWeights()
        self.minimum_similarity = minimum_similarity
        self.max_candidates = max_candidates

    @staticmethod
    def _context_similarity(
        semantic_tags: frozenset[str],
        context: Iterable[str],
    ) -> float:
        context_set = {token.strip().lower() for token in context if token.strip()}
        if not semantic_tags or not context_set:
            return 0.0
        overlap = len(semantic_tags & context_set)
        union = len(semantic_tags | context_set)
        return overlap / union if union else 0.0

    def rank(
        self,
        observed_phonemes: Sequence[str],
        context: Iterable[str] = (),
    ) -> tuple[RankedHypothesis, ...]:
        observed = normalize_phonemes(observed_phonemes)
        context_tuple = tuple(context)
        scored = []

        for entry in self.lexicon:
            phon_score = phonological_similarity(observed, entry.phonemes)
            if phon_score < self.minimum_similarity:
                continue

            context_score = self._context_similarity(entry.semantic_tags, context_tuple)
            raw = (
                self.weights.phonology * phon_score
                + self.weights.context * context_score
                + self.weights.prior * entry.prior
            )
            scored.append(
                (
                    entry,
                    CandidateScore(
                        phonological_similarity=phon_score,
                        contextual_similarity=context_score,
                        lexical_prior=entry.prior,
                        raw_score=raw,
                    ),
                )
            )

        scored.sort(key=lambda item: item[1].raw_score, reverse=True)
        scored = scored[: self.max_candidates]
        if not scored:
            return ()

        temperature = 0.18
        logits = [score.raw_score / temperature for _, score in scored]
        max_logit = max(logits)
        exps = [math.exp(logit - max_logit) for logit in logits]
        denominator = sum(exps)

        return tuple(
            RankedHypothesis(
                word=entry.word,
                phonemes=entry.phonemes,
                confidence=value / denominator,
                score=score,
            )
            for (entry, score), value in zip(scored, exps)
        )
