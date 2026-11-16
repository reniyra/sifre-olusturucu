# Şifre Dedektifleri

TÜBİTAK 2204-B Ortaokul Öğrencileri Araştırma Projesi · Ana alan: Yazılım · Tematik alan: Siber Güvenlik

**Araştırma sorusu:** Türkçeye özgü şifre kalıplarını (Türkçe karaktersiz yazım, F klavye dizileri, takım veya şehir adı + yıl ya da plaka) tanıyan bir güç ölçer, yaygın kullanılan bir güç ölçere göre şifrelerin tahmin edilme zorluğunu daha doğru gösterir mi?

## Etik kurallar

- Bu depoda **gerçek kişilere ait hiçbir şifre yoktur.** Bütün şifreler kelime listelerinden yapay olarak üretilir.
- Sızdırılmış şifre listeleri kullanılmaz.
- Hiçbir gerçek siteye veya hesaba giriş denemesi yapılmaz.

## Klasörler

| Klasör / dosya | İçinde ne var? |
| --- | --- |
| `veri/` | Kelime listeleri (isimler, şehirler + plaka, takımlar + kuruluş yılı, sık kelimeler) |
| `sifre_uretici.py` | 1. program: yapay şifreleri üretir |
| `ciktilar/sifreler.csv` | Üretilen şifreler, kalıp türleri ve set bilgisi |

Sonraki programlar (tahmin programı, güç ölçer, karşılaştırma) bu klasöre eklenecek.

## Nasıl çalıştırılır?

Python 3 gerekir, ek paket gerekmez.

```
python sifre_uretici.py
```

Ayarlar dosyanın en üstündedir: her kalıptan kaç şifre üretileceği, tohum sayısı ve test oranı. Aynı tohumla her çalıştırmada aynı şifreler üretilir; bu, deneyin tekrarlanabilmesini sağlar.

## Üretilen kalıplar

| Kalıp | Örnek | Neden var? |
| --- | --- | --- |
| `kelime_yil_turkce` | ayşe2012 | Türkçe karakterli yazım |
| `kelime_yil_ascii` | ayse2012 | Aynı şifrenin Türkçe karaktersiz hâli (eşli) |
| `takim_kurulus` | fenerbahçe1907 | Takım + kuruluş yılı |
| `sehir_plaka` | trabzon61 | Şehir + plaka kodu |
| `f_klavye` | fgğıodr | F klavyede yan yana tuşlar |
| `q_klavye` | qwertyu | Q klavyede yan yana tuşlar (karşılaştırma için) |
| `rastgele` | k3x9qa0zmt | Güçlü şifre örneği (karşılaştırma için) |
| `cumle_sifre` | kalem-deniz-bulut | Uzun kelime şifresi |

## Geliştirme seti ve test seti

Her şifrenin `set` sütununda `gelistirme` ya da `test` yazar. Güç ölçerimizi yazarken yalnızca **geliştirme** şifrelerine bakarız. **Test** şifreleri en sondaki karşılaştırmaya kadar saklanır.

Kurallar:

- Bir şifrenin Türkçe karakterli ve karaktersiz hâli (`beşiktaş1903` / `besiktas1903`, `ayşe1958` / `ayse1958`) her zaman **aynı sete** düşer. Böylece test şifrelerinin bir benzeri geliştirme setine sızmaz.
- Klavye dizileri aynı klavye satırlarından üretildiği için iki setteki diziler birbirine benzeyebilir. Bu yüzden güç ölçerimiz klavye dizilerini **klavyenin tuş sırasına bakarak** tanımalıdır; geliştirme setindeki şifreleri ezberleyerek değil.

## Kaynaklar

Kelime listelerinin kaynakları buraya yazılacak.
