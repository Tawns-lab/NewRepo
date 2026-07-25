from phonemic_reasoning_engine import Lexicon, PhonemicReasoningEngine

lexicon = Lexicon.from_entries(
    [
        ("write", ["R", "AY", "T"], {"pen", "text", "author"}, 0.85),
        ("right", ["R", "AY", "T"], {"correct", "direction", "side"}, 0.95),
    ]
)

engine = PhonemicReasoningEngine(lexicon)

for context in (["author", "text"], ["direction", "side"]):
    result = engine.reason(["R", "AY", "T"], context=context)
    print("context:", context)
    for item in result.hypotheses:
        print(item.word, round(item.confidence, 3))
    print()
