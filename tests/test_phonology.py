import unittest

from phonemic_reasoning_engine.phonology import (
    normalize_phonemes,
    phonological_similarity,
    weighted_edit_distance,
)


class PhonologyTests(unittest.TestCase):
    def test_normalization(self):
        self.assertEqual(normalize_phonemes([" n ", "ay", "T"]), ("N", "AY", "T"))

    def test_identical_sequence_has_zero_distance(self):
        phones = ("N", "AY", "T")
        self.assertEqual(weighted_edit_distance(phones, phones), 0.0)
        self.assertEqual(phonological_similarity(phones, phones), 1.0)

    def test_confusable_substitution_is_cheaper_than_unrelated_substitution(self):
        close = weighted_edit_distance(("P", "AE", "T"), ("B", "AE", "T"))
        far = weighted_edit_distance(("P", "AE", "T"), ("K", "AE", "T"))
        self.assertLess(close, far)


if __name__ == "__main__":
    unittest.main()
