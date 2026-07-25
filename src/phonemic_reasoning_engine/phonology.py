from __future__ import annotations

from typing import Iterable, Sequence, Tuple

PhonemeSequence = Tuple[str, ...]


DEFAULT_CONFUSABLES: dict[frozenset[str], float] = {
    frozenset(("P", "B")): 0.35,
    frozenset(("T", "D")): 0.35,
    frozenset(("K", "G")): 0.35,
    frozenset(("F", "V")): 0.35,
    frozenset(("S", "Z")): 0.35,
    frozenset(("SH", "ZH")): 0.35,
    frozenset(("CH", "JH")): 0.40,
    frozenset(("M", "N")): 0.55,
    frozenset(("IH", "IY")): 0.45,
    frozenset(("EH", "AE")): 0.45,
}


def normalize_phonemes(phonemes: Iterable[str]) -> PhonemeSequence:
    normalized = tuple(p.strip().upper() for p in phonemes if p and p.strip())
    if not normalized:
        raise ValueError("phoneme sequence must contain at least one phoneme")
    return normalized


def substitution_cost(
    left: str,
    right: str,
    confusables: dict[frozenset[str], float] | None = None,
) -> float:
    if left == right:
        return 0.0
    table = confusables or DEFAULT_CONFUSABLES
    return table.get(frozenset((left, right)), 1.0)


def weighted_edit_distance(
    observed: Sequence[str],
    candidate: Sequence[str],
    *,
    insertion_cost: float = 1.0,
    deletion_cost: float = 1.0,
    confusables: dict[frozenset[str], float] | None = None,
) -> float:
    """Weighted Levenshtein distance over phoneme tokens."""
    a = tuple(observed)
    b = tuple(candidate)
    previous = [j * insertion_cost for j in range(len(b) + 1)]

    for i, left in enumerate(a, start=1):
        current = [i * deletion_cost]
        for j, right in enumerate(b, start=1):
            current.append(
                min(
                    previous[j] + deletion_cost,
                    current[j - 1] + insertion_cost,
                    previous[j - 1] + substitution_cost(left, right, confusables),
                )
            )
        previous = current

    return previous[-1]


def phonological_similarity(
    observed: Sequence[str],
    candidate: Sequence[str],
    *,
    confusables: dict[frozenset[str], float] | None = None,
) -> float:
    max_len = max(len(observed), len(candidate))
    if max_len == 0:
        return 1.0
    distance = weighted_edit_distance(observed, candidate, confusables=confusables)
    return max(0.0, 1.0 - (distance / max_len))
