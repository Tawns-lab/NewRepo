import unittest

from phonemic_reasoning_engine import Lexicon, PhonemicReasoningEngine


class SegmentationTests(unittest.TestCase):
    def test_basic_segmentation(self):
        lexicon = Lexicon.from_entries(
            [
                ("night", ["N", "AY", "T"], {"dark"}, 0.8),
                ("bat", ["B", "AE", "T"], {"animal"}, 0.7),
            ]
        )
        engine = PhonemicReasoningEngine(lexicon)
        self.assertEqual(
            engine.segment(["N", "AY", "T", "B", "AE", "T"]),
            ("night", "bat"),
        )


if __name__ == "__main__":
    unittest.main()
