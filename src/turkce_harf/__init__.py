"""Türkçe harfler için yardımcılar.

Python'un standart büyük/küçük harf dönüşümleri Türkçe'yi bilmez:
``"i".upper()`` → ``"I"`` (Türkçe'de ``"İ"`` olmalı) ve
``"I".lower()`` → ``"i"`` (Türkçe'de ``"ı"`` olmalı). Bu modül bu farkları kapatır.
"""

import unicodedata

__all__ = ["tr_lower", "tr_upper", "tr_title", "tr_sort_key", "tr_fold", "tr_nfc"]

# Türkçe alfabe sırası (29 harf)
_ORDER = "abcçdefgğhıijklmnoöprsştuüvyz"
_ORDER_INDEX = {c: i for i, c in enumerate(_ORDER)}

# Arama anahtarı için Türkçe harfleri ASCII karşılıklarına çevirir (kayıplı)
_FOLD_TABLE = str.maketrans("ıçğöşü", "icgosu")


def tr_nfc(text):
    """Metni NFC biçimine getirir. Birleşik karakterler (örn. I + U+0307) düzelir."""
    return unicodedata.normalize("NFC", text)


def tr_lower(text):
    """Türkçe kurallarıyla küçük harfe çevirir: ``I`` → ``ı``, ``İ`` → ``i``."""
    text = tr_nfc(text)
    return text.replace("İ", "i").replace("I", "ı").lower()


def tr_upper(text):
    """Türkçe kurallarıyla büyük harfe çevirir: ``i`` → ``İ``, ``ı`` → ``I``."""
    text = tr_nfc(text)
    return text.replace("i", "İ").replace("ı", "I").upper()


def tr_title(text):
    """Her kelimenin ilk harfini Türkçe kurallarıyla büyütür, geri kalanı küçültür.

    Yalnızca boşlukla ayrılmış kelimeleri işler; özel durumlar (ör. kesme işareti)
    için ayrıca bakılmaz.
    """
    words = tr_nfc(text).split(" ")
    return " ".join(tr_upper(w[:1]) + tr_lower(w[1:]) for w in words)


def tr_sort_key(text):
    """Türkçe alfabe sırasına göre sıralama anahtarı üretir.

    Kullanım: ``sorted(liste, key=tr_sort_key)``.
    Alfabede olmayan karakterler (rakam, boşluk, noktalama, yabancı harf) harflerden
    sonra, kod noktasına göre sıralanır.
    """
    return tuple(
        _ORDER_INDEX[c] if c in _ORDER_INDEX else len(_ORDER) + ord(c)
        for c in tr_lower(text)
    )


def tr_fold(text):
    """Arama için kayıplı anahtar: küçük harf + Türkçe harfler ASCII karşılığına.

    ``tr_fold("Kılıç") == "kilic"``. Bu değer saklanan veri olarak değil, yalnızca
    karşılaştırma/arama anahtarı olarak kullanılmalıdır, çünkü ``ı``/``i`` ve
    ``ş``/``s`` gibi ayrımlar kaybolur.
    """
    return tr_lower(text).translate(_FOLD_TABLE)
