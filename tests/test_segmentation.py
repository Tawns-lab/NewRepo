from phonemic_reasoning_engine import Lexicon, PhonemicReasoningEngine


def test_basic_segmentation():
    lexicon = Lexicon.from_entries(
        [
            ("night", ["N", "AY", "T"], {"dark"}, 0.8),
            ("bat", ["B", "AE", "T"], {"animal"}, 0.7),
        ]
    )
    engine = PhonemicReasoningEngine(lexicon)
    assert engine.segment(["N", "AY", "T", "B", "AE", "T"]) == ("night", "bat")
