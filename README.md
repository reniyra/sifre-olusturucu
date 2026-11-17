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
| `veri/` | Şifre üreticinin kelime listeleri (isimler, şehirler + plaka, takımlar + kuruluş yılı, sık kelimeler) |
| `veri/saldirgan/` | Tahmin programının (saldırganın) kendi, daha büyük sözlüğü |
| `sifre_uretici.py` | 1. program: yapay şifreleri üretir |
| `ciktilar/sifreler.csv` | Üretilen şifreler, kalıp türleri ve set bilgisi |
| `tahmin_programi.py` | 2. program: her şifrenin kaçıncı tahminde bulunduğunu sayar |
| `ciktilar/deneme_sayilari_gelistirme.csv` | Geliştirme şifrelerinin deneme sayıları |
| `ciktilar/deneme_sayilari_test.csv` | Test şifrelerinin deneme sayıları (sona kadar açılmaz) |
| `sonuc_raporu.py` | Yardımcı program: sonuçları grafikli bir sayfaya çevirir |
| `ciktilar/rapor.html` | Geliştirme setinin grafikli raporu (tarayıcıda açılır) |
| `veri/rapor_metinleri.txt` | Rapor sayfasındaki yazılar, renk ve yazı tipi (öğrenciler yazar) |

Sonraki programlar (güç ölçer, karşılaştırma) bu klasöre eklenecek.

## Nasıl çalıştırılır?

Python 3 gerekir, ek paket gerekmez.

```
python sifre_uretici.py
python tahmin_programi.py
python sonuc_raporu.py
```

Son komut `ciktilar/rapor.html` sayfasını üretir; dosyayı çift tıklayarak tarayıcıda açabilirsiniz. Sayfadaki yazıları değiştirmek için `veri/rapor_metinleri.txt` dosyasını düzenleyin.

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

## Tahmin programı nasıl çalışır?

Program, bir saldırganın şifreleri hangi sırayla tahmin edeceğini taklit eder. Tahminlerini tek tek sayar; bir şifre kaçıncı tahminde bulunursa o sayı şifrenin **deneme sayısı**dır. Hiçbir tahminde bulunamayan şifreler "sınırın üstünde" sayılır.

Tahmin grupları: klavye dizileri, tek kelimeler, kelime + iki haneli sayı (00–99), kelime + yıl (1900–2030), üç kelimeli şifreler. Her kelime hem Türkçe karakterli hem karaktersiz denenir.

**Araştırmanın kararları (`v2.0-tahmin` ile donduruldu):**

- **Tahmin sırası:** Saldırgan önce en az tahmin gerektiren grubu dener. Sırayı program grupların büyüklüğüne bakarak kendisi belirler.
- **Saldırganın sözlüğü:** Tahmin programı, şifre üreticinin listelerini değil, `veri/saldirgan/` klasöründeki daha büyük listeleri kullanır. Gerçek bir saldırgan, şifre sahiplerinin kullandığından daha fazla kelime bilir. Saldırgan plaka kodlarını ve kuruluş yıllarını ayrıca bilmez; bunları sayı denemeleriyle bulur.
- **Deneme sınırı:** 10.000.000 tahmin.

**Tahmin programı ne yapmaz?**

- İnternete bağlanmaz; hiçbir siteye, hesaba veya sisteme giriş denemez.
- Gerçek şifre kullanmaz; yalnızca bu depodaki yapay şifreleri okur.
- Gizli (şifrelenmiş) olarak saklanan şifreleri çözmeye çalışmaz. Yalnızca kendi listesindeki yazılarla karşılaştırma yapan bir simülasyondur.
- Şifrelerin `kalip` sütununa bakmaz; bu sütun sonuç dosyasına yalnızca kopyalanır.

## Kaynaklar

Kelime listelerinin kaynakları buraya yazılacak.
