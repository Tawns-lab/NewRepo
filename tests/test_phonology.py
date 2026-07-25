from phonemic_reasoning_engine.phonology import (
    normalize_phonemes,
    phonological_similarity,
    weighted_edit_distance,
)


def test_normalization():
    assert normalize_phonemes([" n ", "ay", "T"]) == ("N", "AY", "T")


def test_identical_sequence_has_zero_distance():
    phones = ("N", "AY", "T")
    assert weighted_edit_distance(phones, phones) == 0.0
    assert phonological_similarity(phones, phones) == 1.0


def test_confusable_substitution_is_cheaper_than_unrelated_substitution():
    close = weighted_edit_distance(("P", "AE", "T"), ("B", "AE", "T"))
    far = weighted_edit_distance(("P", "AE", "T"), ("K", "AE", "T"))
    assert close < far
