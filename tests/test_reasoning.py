import unittest

from phonemic_reasoning_engine import Lexicon, PhonemicReasoningEngine


def make_engine():
    lexicon = Lexicon.from_entries(
        [
            ("night", ["N", "AY", "T"], {"dark", "sleep", "evening"}, 0.9),
            ("knight", ["N", "AY", "T"], {"armor", "castle", "medieval"}, 0.6),
            ("bat", ["B", "AE", "T"], {"baseball", "animal"}, 0.7),
            ("pat", ["P", "AE", "T"], {"touch", "name"}, 0.5),
        ]
    )
    return PhonemicReasoningEngine(lexicon)


class ReasoningTests(unittest.TestCase):
    def test_context_disambiguates_homophone(self):
        result = make_engine().reason(["N", "AY", "T"], context=["castle", "armor"])
        self.assertEqual(result.hypotheses[0].word, "knight")

    def test_prior_breaks_uncontextualized_homophone_tie(self):
        result = make_engine().reason(["N", "AY", "T"])
        self.assertEqual(result.hypotheses[0].word, "night")

    def test_near_phoneme_match_is_retained(self):
        result = make_engine().reason(["P", "AE", "T"])
        words = [candidate.word for candidate in result.hypotheses]
        self.assertIn("pat", words)
        self.assertIn("bat", words)


if __name__ == "__main__":
    unittest.main()
