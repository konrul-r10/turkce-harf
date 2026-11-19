import unicodedata

import pytest

from turkce_harf import tr_fold, tr_lower, tr_nfc, tr_sort_key, tr_title, tr_upper


# --- tr_lower ---

@pytest.mark.parametrize(
    "given, expected",
    [
        ("ISPARTA", "ısparta"),
        ("İSTANBUL", "istanbul"),
        ("Iğdır", "ığdır"),
        ("ÇORUM", "çorum"),
        ("", ""),
        ("a", "a"),
        ("ı", "ı"),
    ],
)
def test_tr_lower(given, expected):
    assert tr_lower(given) == expected


def test_tr_lower_handles_decomposed_dotted_capital_i():
    # İ bazen I + birleşik nokta (U+0307) olarak gelir
    decomposed = "İstanbul"
    assert tr_lower(decomposed) == "istanbul"


# --- tr_upper ---

@pytest.mark.parametrize(
    "given, expected",
    [
        ("istanbul", "İSTANBUL"),
        ("ılık", "ILIK"),
        ("çorum", "ÇORUM"),
        ("şişli", "ŞİŞLİ"),
        ("", ""),
    ],
)
def test_tr_upper(given, expected):
    assert tr_upper(given) == expected


def test_tr_upper_and_lower_are_consistent_for_turkish_pairs():
    assert tr_lower(tr_upper("ılık")) == "ılık"
    assert tr_upper(tr_lower("İSTANBUL")) == "İSTANBUL"


# --- tr_title ---

@pytest.mark.parametrize(
    "given, expected",
    [
        ("istanbul", "İstanbul"),
        ("ılık su", "Ilık Su"),
        ("ANKARA ÇANKAYA", "Ankara Çankaya"),
        ("", ""),
    ],
)
def test_tr_title(given, expected):
    assert tr_title(given) == expected


# --- tr_sort_key ---

def test_sort_uses_turkish_alphabet_order():
    words = ["şapka", "sabun", "zil", "ırmak", "ilk", "çay", "ev"]
    expected = ["çay", "ev", "ırmak", "ilk", "sabun", "şapka", "zil"]
    assert sorted(words, key=tr_sort_key) == expected


def test_sort_dotless_i_comes_before_i():
    # Türkçe alfabesinde ı, i'den önce gelir
    assert tr_sort_key("ı") < tr_sort_key("i")


def test_sort_c_cedilla_after_c():
    assert tr_sort_key("c") < tr_sort_key("ç") < tr_sort_key("d")


def test_sort_handles_non_alphabet_characters():
    items = ["a1", "a", "ab", "A-", "42"]
    assert len(sorted(items, key=tr_sort_key)) == len(items)


# --- tr_fold ---

@pytest.mark.parametrize(
    "given, expected",
    [
        ("Kılıç", "kilic"),
        ("ŞİŞLİ", "sisli"),
        ("Göl", "gol"),
        ("Üsküdar", "uskudar"),
        ("", ""),
    ],
)
def test_tr_fold(given, expected):
    assert tr_fold(given) == expected


def test_tr_fold_matches_ascii_and_turkish_forms():
    assert tr_fold("İstanbul") == tr_fold("istanbul") == tr_fold("Istanbul")


# --- tr_nfc ---

def test_tr_nfc_composes_sequences():
    decomposed = unicodedata.normalize("NFD", "ş")
    assert tr_nfc(decomposed) == "ş"
