# turkce-harf

Türkçe harfler için büyük/küçük harf dönüşümü, alfabe sıralaması ve arama anahtarı yardımcıları. Bağımlılığı yoktur.

Python'un standart `upper()`/`lower()` fonksiyonları Türkçe'yi bilmez: `"i".upper()` `"I"` döndürür, oysa Türkçe'de `"İ"` olmalıdır.

## Kurulum

```bash
pip install turkce-harf
```

## Kullanım

```python
from turkce_harf import tr_lower, tr_upper, tr_title, tr_sort_key, tr_fold

tr_upper("istanbul")        # 'İSTANBUL'
tr_lower("ISPARTA")         # 'ısparta'
tr_title("ılık su")         # 'Ilık Su'

sorted(["şapka", "sabun", "ırmak"], key=tr_sort_key)
# ['ırmak', 'sabun', 'şapka']

tr_fold("Kılıç")            # 'kilic'  (yalnızca arama için)

# İngilizce metin için lang="en" kullan
tr_lower("IBM", lang="en")       # 'ibm'
tr_upper("istanbul", lang="en")  # 'ISTANBUL'
```

Her fonksiyon `lang` parametresi alır: `"tr"` (varsayılan) Türkçe kurallarını, `"en"` standart İngilizce kurallarını uygular. Karışık ya da İngilizce metinde `lang="en"` kullanmak `I` harfinin `ı`'ya dönüşmesini önler.

## Fonksiyonlar

Tüm fonksiyonlar `lang="tr"` (varsayılan) ya da `lang="en"` alır.

- `tr_lower(text)`: Türkçe kurallarıyla küçük harf (`I` → `ı`, `İ` → `i`).
- `tr_upper(text)`: Türkçe kurallarıyla büyük harf (`i` → `İ`, `ı` → `I`).
- `tr_title(text)`: Her kelimenin ilk harfini büyütür, geri kalanı küçültür.
- `tr_sort_key(text)`: Türkçe alfabe sırasına göre sıralama anahtarı. Alfabe dışı karakterler sona gider.
- `tr_fold(text)`: Kayıplı arama anahtarı (`ı`→`i`, `ş`→`s`, `ç`→`c`, `ğ`→`g`, `ö`→`o`, `ü`→`u`). Saklanan veri için değil, yalnızca karşılaştırma için kullanın.
- `tr_nfc(text)`: Metni NFC biçimine getirir.

## Geliştirme

```bash
pip install -e ".[test]"
pytest
```

## Lisans

MIT

---

# turkce-harf (English)

Helpers for uppercasing, lowercasing, Turkish alphabet sorting, and search keys for Turkish letters. No dependencies.

Python's standard `upper()`/`lower()` do not know Turkish: `"i".upper()` returns `"I"`, but in Turkish it should be `"İ"`.

## Installation

```bash
pip install turkce-harf
```

## Usage

```python
from turkce_harf import tr_lower, tr_upper, tr_title, tr_sort_key, tr_fold

tr_upper("istanbul")        # 'İSTANBUL'
tr_lower("ISPARTA")         # 'ısparta'
tr_title("ılık su")         # 'Ilık Su'

sorted(["şapka", "sabun", "ırmak"], key=tr_sort_key)
# ['ırmak', 'sabun', 'şapka']

tr_fold("Kılıç")            # 'kilic'  (for search only)

# Use lang="en" for English text
tr_lower("IBM", lang="en")       # 'ibm'
tr_upper("istanbul", lang="en")  # 'ISTANBUL'
```

Every function accepts a `lang` parameter: `"tr"` (default) applies Turkish rules, and `"en"` applies standard English rules. Using `lang="en"` for mixed or English text prevents `I` from becoming `ı`.

## Functions

All functions accept `lang="tr"` (default) or `lang="en"`.

- `tr_lower(text)`: Lowercases with Turkish rules (`I` → `ı`, `İ` → `i`).
- `tr_upper(text)`: Uppercases with Turkish rules (`i` → `İ`, `ı` → `I`).
- `tr_title(text)`: Capitalizes the first letter of each word and lowercases the rest.
- `tr_sort_key(text)`: Sort key following the Turkish alphabet. Non-alphabet characters go last.
- `tr_fold(text)`: Lossy search key (`ı`→`i`, `ş`→`s`, `ç`→`c`, `ğ`→`g`, `ö`→`o`, `ü`→`u`). Use it only for comparison, not for stored data.
- `tr_nfc(text)`: Normalizes text to NFC form.

## Development

```bash
pip install -e ".[test]"
pytest
```

## License

MIT
