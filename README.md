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
```

## Fonksiyonlar

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
