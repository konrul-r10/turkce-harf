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


# --- lang="en" ---

def test_en_lower_maps_i_to_i():
    assert tr_lower("IBM", lang="en") == "ibm"
    assert tr_lower("ISTANBUL", lang="en") == "istanbul"


def test_en_upper_maps_i_to_i():
    assert tr_upper("istanbul", lang="en") == "ISTANBUL"


def test_en_title():
    assert tr_title("hello world", lang="en") == "Hello World"


def test_en_sort_is_plain_codepoint_order():
    assert sorted(["c", "a", "b"], key=lambda s: tr_sort_key(s, "en")) == ["a", "b", "c"]
    # İngilizce'de ı diye bir harf yok, sıralama standart
    assert tr_sort_key("i", "en") < tr_sort_key("j", "en")


def test_en_fold_only_lowercases():
    assert tr_fold("IBM", lang="en") == "ibm"
    assert tr_fold("Kılıç", lang="en") == "kılıç"


def test_default_lang_is_turkish():
    assert tr_lower("I") == tr_lower("I", lang="tr") == "ı"


@pytest.mark.parametrize("func", [tr_lower, tr_upper, tr_title, tr_sort_key, tr_fold])
def test_invalid_lang_raises(func):
    with pytest.raises(ValueError):
        func("abc", lang="de")


# --- tr_slug ---

from turkce_harf import tr_slug  # noqa: E402


@pytest.mark.parametrize(
    "given, expected",
    [
        ("Çok güzel başlık!", "cok-guzel-baslik"),
        ("İstanbul'da ılık", "istanbulda-ilik"),
        ("ŞİŞLİ  --  Çankaya", "sisli-cankaya"),
        ("Ğ Ü Ö Ş Ç", "g-u-o-s-c"),
        ("  Başta ve sonda  ", "basta-ve-sonda"),
        ("", ""),
        ("!!!", ""),
    ],
)
def test_tr_slug(given, expected):
    assert tr_slug(given) == expected


def test_tr_slug_apostrophe_does_not_split_word():
    assert tr_slug("Ankara'nın") == "ankaranin"


def test_tr_slug_en_strips_accents():
    assert tr_slug("Café Ünlü", lang="en") == "cafe-unlu"
    assert tr_slug("Hello, World!", lang="en") == "hello-world"


def test_tr_slug_custom_separator():
    assert tr_slug("Çok güzel", separator="_") == "cok_guzel"


def test_tr_slug_invalid_lang_raises():
    with pytest.raises(ValueError):
        tr_slug("abc", lang="de")
