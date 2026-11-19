"""Türkçe ve İngilizce harfler için büyük/küçük harf yardımcıları.

Python'un standart ``upper()``/``lower()`` fonksiyonları Türkçe'yi bilmez:
``"i".upper()`` → ``"I"`` (Türkçe'de ``"İ"`` olmalı) ve
``"I".lower()`` → ``"i"`` (Türkçe'de ``"ı"`` olmalı).

Her fonksiyon ``lang`` parametresi alır:

- ``lang="tr"`` (varsayılan): Türkçe kuralları uygulanır.
- ``lang="en"``: Standart İngilizce kuralları uygulanır (``I`` → ``i``).
"""

import re
import unicodedata

__all__ = [
    "tr_lower", "tr_upper", "tr_title", "tr_sort_key", "tr_fold", "tr_nfc", "tr_slug",
]

_LANGS = ("tr", "en")

# Türkçe alfabe sırası (29 harf)
_ORDER = "abcçdefgğhıijklmnoöprsştuüvyz"
_ORDER_INDEX = {c: i for i, c in enumerate(_ORDER)}

# Arama anahtarı için Türkçe harfleri ASCII karşılıklarına çevirir (kayıplı)
_FOLD_TABLE = str.maketrans("ıçğöşü", "icgosu")

# Slug için: kesme işaretleri kelimeyi bölmez, silinir
_APOSTROPHES = re.compile("['’ʼ`´]")
_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def _check_lang(lang):
    if lang not in _LANGS:
        raise ValueError(f"lang 'tr' veya 'en' olmalı, verilen: {lang!r}")


def tr_nfc(text):
    """Metni NFC biçimine getirir. Birleşik karakterler (örn. I + U+0307) düzelir."""
    return unicodedata.normalize("NFC", text)


def tr_lower(text, lang="tr"):
    """Küçük harfe çevirir.

    ``lang="tr"``: ``I`` → ``ı``, ``İ`` → ``i``.
    ``lang="en"``: standart küçük harf (``I`` → ``i``).
    """
    _check_lang(lang)
    text = tr_nfc(text)
    if lang == "en":
        return text.lower()
    return text.replace("İ", "i").replace("I", "ı").lower()


def tr_upper(text, lang="tr"):
    """Büyük harfe çevirir.

    ``lang="tr"``: ``i`` → ``İ``, ``ı`` → ``I``.
    ``lang="en"``: standart büyük harf (``i`` → ``I``).
    """
    _check_lang(lang)
    text = tr_nfc(text)
    if lang == "en":
        return text.upper()
    return text.replace("i", "İ").replace("ı", "I").upper()


def tr_title(text, lang="tr"):
    """Her kelimenin ilk harfini büyütür, geri kalanı küçültür.

    Yalnızca boşlukla ayrılmış kelimeleri işler.
    """
    _check_lang(lang)
    words = tr_nfc(text).split(" ")
    return " ".join(
        tr_upper(w[:1], lang) + tr_lower(w[1:], lang) for w in words
    )


def tr_sort_key(text, lang="tr"):
    """Sıralama anahtarı üretir. Kullanım: ``sorted(liste, key=tr_sort_key)``.

    ``lang="tr"``: Türkçe alfabe sırasına göre. Alfabede olmayan karakterler
    (rakam, boşluk, noktalama, yabancı harf) harflerden sonra gelir.
    ``lang="en"``: karakterleri küçük harfe çevirip kod noktasına göre sıralar.
    """
    _check_lang(lang)
    lowered = tr_lower(text, lang)
    if lang == "en":
        return tuple(ord(c) for c in lowered)
    return tuple(
        _ORDER_INDEX[c] if c in _ORDER_INDEX else len(_ORDER) + ord(c)
        for c in lowered
    )


def tr_fold(text, lang="tr"):
    """Arama için kayıplı anahtar.

    ``lang="tr"``: küçük harf + Türkçe harfler ASCII karşılığına (``ı``→``i``,
    ``ş``→``s`` vb.). ``tr_fold("Kılıç") == "kilic"``.
    ``lang="en"``: yalnızca küçük harf, ``tr_fold("IBM", lang="en") == "ibm"``.

    Bu değer saklanan veri olarak değil, yalnızca karşılaştırma/arama anahtarı
    olarak kullanılmalıdır.
    """
    _check_lang(lang)
    if lang == "en":
        return tr_lower(text, "en")
    return tr_lower(text, "tr").translate(_FOLD_TABLE)


def tr_slug(text, lang="tr", separator="-"):
    """URL için slug üretir.

    - Kesme işaretleri silinir, kelimeyi bölmez: ``"İstanbul'da"`` → ``"istanbulda"``.
    - ``lang="tr"``: Türkçe harfler aksansız karşılığına çevrilir (``ç``→``c``, ``ı``→``i``).
    - ``lang="en"``: aksanlar kaldırılır (``é``→``e``).
    - Harf ve rakam dışındaki her karakter dizisi ``separator`` ile değiştirilir.

    ``tr_slug("Çok güzel başlık! İstanbul'da") == "cok-guzel-baslik-istanbulda"``
    """
    _check_lang(lang)
    text = _APOSTROPHES.sub("", tr_nfc(text))
    if lang == "tr":
        base = tr_fold(text, "tr")
    else:
        base = tr_lower(text, "en")
    base = unicodedata.normalize("NFKD", base).encode("ascii", "ignore").decode("ascii")
    slug = _NON_ALNUM.sub(lambda _m: separator, base)
    return slug.strip(separator)
