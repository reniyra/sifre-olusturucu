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
| `zxcvbn_olcum.html` | 3. program: zxcvbn'i Türkçe paketle çalıştırır. Tarayıcıda açılır; tek şifre dener ya da geliştirme setini toplu ölçüp `zxcvbn_puanlari_gelistirme.csv` indirir |
| `kaynak/zxcvbn_olcum/` | `zxcvbn_olcum.html` sayfasının kaynak kodu |
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

zxcvbn puanları için `zxcvbn_olcum.html` dosyasını Chrome ya da Edge ile açın ve `ciktilar/sifreler.csv` dosyasını seçin. İnen `zxcvbn_puanlari_gelistirme.csv` dosyasını `ciktilar/` klasörüne taşıyın. (`kaynak/zxcvbn_olcum/sayfa.html` bu sayfanın kalıbıdır, tek başına çalışmaz.)

Şifre üreticinin ayarları `sifre_uretici.py` dosyasının en üstündedir: her kalıptan kaç şifre üretileceği, tohum sayısı ve test oranı. Aynı tohumla her çalıştırmada aynı şifreler üretilir; bu, deneyin tekrarlanabilmesini sağlar.

## Üretilen kalıplar

| Kalıp | Örnek | Neden var? |
| --- | --- | --- |
| `kelime_yil_turkce` | ayşe2012 | Türkçe karakterli yazım |
| `kelime_yil_ascii` | ayse2012 | Aynı şifrenin Türkçe karaktersiz hâli (eşli) |
| `takim_kurulus` | fenerbahçe1907 | Takım + kuruluş yılı |
| `sehir_plaka` | denizli20 | Şehir + plaka kodu |
| `f_klavye` | fgğıodrn | F klavyede yan yana tuşlar |
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

**Yarışma belgesi**

- TÜBİTAK (2026). *2204-B Ortaokul Öğrencileri Araştırma Projeleri Yarışması Proje Rehberi 2027.* https://tubitak.gov.tr/sites/default/files/2026-09/ortaokul_proje_rehberi_2027.pdf

**Karşılaştırılacak güç ölçer**

- zxcvbn-ts (sürümler: @zxcvbn-ts/core 4.3.0, @zxcvbn-ts/language-common 4.2.0, @zxcvbn-ts/language-tr 4.1.2): açık kaynaklı şifre güç ölçer ve dil paketleri (Türkçe paket dahil). https://zxcvbn-ts.github.io/zxcvbn/guide/languages/

**Veri listeleri**

| Dosya | Kaynağı |
| --- | --- |
| `veri/sehirler.txt`, `veri/saldirgan/sehirler.txt` | Türkiye'nin 81 ili ve plaka kodları (01 Adana – 81 Düzce) |
| `veri/takimlar.txt`, `veri/saldirgan/takimlar.txt` | Kulüplerin kuruluş yılları, danışman öğretmen tarafından kulüplerin resmî internet siteleri (ör. https://www.eyupspor.org.tr/kulup) ve Transfermarkt kulüp sayfaları üzerinden doğrulandı (erişim tarihi: 17.11.2026) |
| `veri/isimler.txt`, `veri/kelimeler.txt`, `veri/saldirgan/isimler.txt`, `veri/saldirgan/kelimeler.txt` | Proje ekibi tarafından örnek liste olarak hazırlandı (resmî bir istatistikten alınmadı) |

**Kulüplerin resmî internet siteleri** (erişim tarihi: 17.11.2026)

| Kulüp | Listedeki yıl | Resmî site |
| --- | --- | --- |
| Beşiktaş | 1903 | https://www.bjk.com.tr |
| Galatasaray | 1905 | https://www.galatasaray.org |
| Fenerbahçe | 1907 | https://www.fenerbahce.org |
| MKE Ankaragücü | 1910 | https://ankaragucu.org.tr/tarihce/ |
| Altay | 1914 | https://www.altay.org.tr |
| Eyüpspor | 1919 | https://www.eyupspor.org.tr/kulup |
| Kasımpaşa | 1921 | https://www.kasimpasa.com.tr |
| Konyaspor | 1922 | https://www.konyaspor.org.tr |
| Gençlerbirliği | 1923 | https://www.genclerbirligi.org.tr |
| Göztepe | 1925 | https://www.goztepe.org.tr/Kulup/Tarihce |
| Fatih Karagümrük | 1926 | https://www.karagumruk.com/kulup/tarihce/ |
| Adana Demirspor | 1940 | https://www.adanademirspor.org.tr |
| Alanyaspor | 1948 | https://www.alanyaspor.org.tr |
| Çaykur Rizespor | 1953 | https://www.caykurrizespor.org.tr |
| Bursaspor | 1963 | https://www.bursaspor.org.tr |
| Samsunspor | 1965 | https://www.samsunspor.com.tr/tarihce |
| Sakaryaspor | 1965 | https://sakaryaspor.org.tr |
| Eskişehirspor | 1965 | https://www.eskisehirspor.org.tr |
| Kayserispor | 1966 | https://kayserispor.org.tr |
| Antalyaspor | 1966 | https://www.antalyaspor.com.tr |
| Kocaelispor | 1966 | https://www.kocaelispor.com.tr |
| Denizlispor | 1966 | (eklenecek) |
| Trabzonspor | 1967 | https://www.trabzonspor.org.tr/tr/kulup/tarihce |
| Sivasspor | 1967 | https://www.sivasspor.org.tr/tarihce/ |
| Hatayspor | 1967 | https://www.hatayspor.org.tr |
| Gaziantep FK | 1988 | https://www.gaziantepfk.org/kulubumuz/kulup-tarihcesi |
| İstanbul Başakşehir | 1990 | (eklenecek) |

**Literatür**

Şifre güvenliği ve güç ölçerlerle ilgili kaynaklar öğrenciler tarafından eklenecek.

## Yapay zekâ kullanımı

Programların iskeleti ve bu belgenin ilk hâli bir yapay zekâ asistanı (Claude, Anthropic) yardımıyla hazırlanmıştır. Araştırma sorusu, yöntem kararları ve güç ölçerin kuralları proje ekibine aittir. Öğrenciler programların her bölümünü okuyup açıklayabilecek düzeyde incelemiştir.
