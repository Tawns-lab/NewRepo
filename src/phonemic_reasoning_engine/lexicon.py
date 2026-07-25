from __future__ import annotations

from collections import defaultdict
from typing import Iterable, Iterator, Sequence

from .models import LexicalEntry
from .phonology import normalize_phonemes


class Lexicon:
    def __init__(self, entries: Iterable[LexicalEntry]) -> None:
        self._entries = tuple(entries)
        self._by_phonemes: dict[tuple[str, ...], list[LexicalEntry]] = defaultdict(list)
        for entry in self._entries:
            self._by_phonemes[entry.phonemes].append(entry)

    @classmethod
    def from_entries(
        cls,
        entries: Iterable[tuple[str, Sequence[str], set[str] | frozenset[str], float]],
    ) -> "Lexicon":
        built = []
        for word, phonemes, semantic_tags, prior in entries:
            built.append(
                LexicalEntry(
                    word=word,
                    phonemes=normalize_phonemes(phonemes),
                    semantic_tags=frozenset(tag.lower() for tag in semantic_tags),
                    prior=prior,
                )
            )
        return cls(built)

    def __iter__(self) -> Iterator[LexicalEntry]:
        return iter(self._entries)

    def __len__(self) -> int:
        return len(self._entries)

    def exact(self, phonemes: Sequence[str]) -> tuple[LexicalEntry, ...]:
        key = normalize_phonemes(phonemes)
        return tuple(self._by_phonemes.get(key, ()))
