from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Tuple

PhonemeSequence = Tuple[str, ...]


@dataclass(frozen=True, slots=True)
class LexicalEntry:
    word: str
    phonemes: PhonemeSequence
    semantic_tags: FrozenSet[str] = field(default_factory=frozenset)
    prior: float = 0.5

    def __post_init__(self) -> None:
        if not self.word.strip():
            raise ValueError("word must be non-empty")
        if not self.phonemes:
            raise ValueError("phonemes must be non-empty")
        if not 0.0 <= self.prior <= 1.0:
            raise ValueError("prior must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class CandidateScore:
    phonological_similarity: float
    contextual_similarity: float
    lexical_prior: float
    raw_score: float


@dataclass(frozen=True, slots=True)
class RankedHypothesis:
    word: str
    phonemes: PhonemeSequence
    confidence: float
    score: CandidateScore


@dataclass(frozen=True, slots=True)
class ReasoningResult:
    observed_phonemes: PhonemeSequence
    context: Tuple[str, ...]
    hypotheses: Tuple[RankedHypothesis, ...]
