from __future__ import annotations

from .engine import PhonemicReasoningEngine
from .lexicon import Lexicon


def demo_lexicon() -> Lexicon:
    return Lexicon.from_entries(
        [
            ("night", ["N", "AY", "T"], {"dark", "sleep", "evening"}, 0.90),
            ("knight", ["N", "AY", "T"], {"armor", "castle", "medieval"}, 0.60),
            ("write", ["R", "AY", "T"], {"pen", "text", "author"}, 0.85),
            ("right", ["R", "AY", "T"], {"correct", "direction", "side"}, 0.95),
            ("bat", ["B", "AE", "T"], {"baseball", "animal", "cave"}, 0.70),
            ("pat", ["P", "AE", "T"], {"touch", "name"}, 0.50),
        ]
    )


def main() -> None:
    engine = PhonemicReasoningEngine(demo_lexicon())
    result = engine.reason(["N", "AY", "T"], context=["castle", "armor"])

    print("Observed:", " ".join(result.observed_phonemes))
    print("Context:", ", ".join(result.context))
    print()

    for hypothesis in result.hypotheses:
        score = hypothesis.score
        print(
            f"{hypothesis.word:10} "
            f"confidence={hypothesis.confidence:.3f} "
            f"phonology={score.phonological_similarity:.3f} "
            f"context={score.contextual_similarity:.3f} "
            f"prior={score.lexical_prior:.3f}"
        )


if __name__ == "__main__":
    main()
