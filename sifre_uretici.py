# -*- coding: utf-8 -*-
"""
ŞİFRE ÜRETİCİ - Şifre Dedektifleri projesi, 1. program

Bu program GERÇEK kimsenin şifresini kullanmaz.
"veri" klasöründeki kelime listelerinden YAPAY şifreler üretir
ve bunları "ciktilar/sifreler.csv" dosyasına yazar.

Çalıştırmak için:  python sifre_uretici.py
"""

import csv
import random
from pathlib import Path

# ---------------------------------------------------------------
# AYARLAR (bunları değiştirerek deney yapabilirsiniz)
# ---------------------------------------------------------------
HER_KALIPTAN_KAC_SIFRE = 50   # Her kalıp türünden en fazla kaç şifre üretilsin?
TOHUM = 2204                  # Aynı tohum = her çalıştırmada aynı şifreler (tekrarlanabilirlik)
TEST_ORANI = 0.5              # Şifrelerin yüzde kaçı test setine ayrılsın? (0.5 = yarısı)

KLASOR = Path(__file__).parent
VERI = KLASOR / "veri"
CIKTI = KLASOR / "ciktilar" / "sifreler.csv"

# ---------------------------------------------------------------
# KLAVYE SATIRLARI (yalnızca harfler, soldan sağa)
# ---------------------------------------------------------------
F_KLAVYE = ["fgğıodrnhpqw", "uieaütkmlyşx", "jövcçzsb"]
Q_KLAVYE = ["qwertyuıopğü", "asdfghjklşi", "zxcvbnmöç"]

# Türkçe harfleri İngilizce karşılığına çeviren tablo
TURKCE_HARF = str.maketrans("çğıöşü", "cgiosu")


# ---------------------------------------------------------------
# YARDIMCI FONKSİYONLAR
# ---------------------------------------------------------------
def liste_oku(dosya_adi):
    """Bir kelime dosyasını okur. Boş satırları ve # ile başlayanları atlar."""
    satirlar = []
    with open(VERI / dosya_adi, encoding="utf-8") as dosya:
        for satir in dosya:
            satir = satir.strip()
            if satir and not satir.startswith("#"):
                satirlar.append(satir)
    return satirlar


def ciftli_liste_oku(dosya_adi):
    """'şehir;plaka' gibi iki parçalı satırları okur."""
    ciftler = []
    for satir in liste_oku(dosya_adi):
        sol, sag = satir.split(";")
        ciftler.append((sol, sag))
    return ciftler


def turkce_harf_var_mi(kelime):
    """Kelimede ç, ğ, ı, ö, ş, ü harflerinden biri var mı?"""
    return kelime != kelime.translate(TURKCE_HARF)


# ---------------------------------------------------------------
# KALIPLAR: Her fonksiyon bir kalıptan tek bir şifre üretir
# ---------------------------------------------------------------
def kelime_yil_turkce(kelime, yil):
    return kelime + str(yil)                          # ayşe2012


def kelime_yil_ascii(kelime, yil):
    return kelime.translate(TURKCE_HARF) + str(yil)   # ayse2012


def sehir_plaka(sehirler):
    sehir, plaka = random.choice(sehirler)
    return sehir + plaka                              # trabzon61


def klavye_dizisi(satirlar):
    satir = random.choice(satirlar)
    uzunluk = random.randint(6, min(9, len(satir)))
    baslangic = random.randint(0, len(satir) - uzunluk)
    return satir[baslangic:baslangic + uzunluk]       # fgğıodr


def rastgele():
    harfler = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(random.choice(harfler) for _ in range(10))   # k3x9qa0zmt


def cumle_sifre(kelimeler):
    return "-".join(random.sample(kelimeler, 3))      # kalem-deniz-bulut


# ---------------------------------------------------------------
# ANA PROGRAM
# ---------------------------------------------------------------
def benzersiz_uret(uretici, adet, deneme_siniri=2000):
    """Bir üretici fonksiyonu tekrar tekrar çağırıp birbirinden farklı şifreler toplar."""
    sifreler = []
    for _ in range(deneme_siniri):
        if len(sifreler) == adet:
            break
        sifre = uretici()
        if sifre not in sifreler:
            sifreler.append(sifre)
    return sifreler


def main():
    random.seed(TOHUM)
    n = HER_KALIPTAN_KAC_SIFRE

    isimler = liste_oku("isimler.txt")
    kelimeler = liste_oku("kelimeler.txt")
    sehirler = ciftli_liste_oku("sehirler.txt")
    takimlar = ciftli_liste_oku("takimlar.txt")

    # Türkçe karakterli ve karaktersiz şifreleri EŞLEŞTİRİYORUZ:
    # "ayşe2012" ile "ayse2012" aynı temelden üretilir, tek fark harflerdir.
    turkce_kelimeler = [k for k in isimler + [s for s, _ in sehirler] if turkce_harf_var_mi(k)]
    temeller = benzersiz_uret(lambda: (random.choice(turkce_kelimeler), random.randint(1950, 2020)), n)

    # Takım + kuruluş yılı (her iki yazımla).
    # Önce TAKIMLAR karıştırılır; "beşiktaş1903" ile "besiktas1903" yan yana kalır,
    # böylece aşağıda ikisi hep aynı sete düşer.
    random.shuffle(takimlar)
    takim_sifreleri = []
    for takim, yil in takimlar:
        takim_sifreleri.append(takim + yil)
        if turkce_harf_var_mi(takim):
            takim_sifreleri.append(takim.translate(TURKCE_HARF) + yil)

    kaliplar = {
        "kelime_yil_turkce": [kelime_yil_turkce(k, y) for k, y in temeller],
        "kelime_yil_ascii":  [kelime_yil_ascii(k, y) for k, y in temeller],
        "takim_kurulus":     takim_sifreleri[:n],
        "sehir_plaka":       benzersiz_uret(lambda: sehir_plaka(sehirler), n),
        "f_klavye":          benzersiz_uret(lambda: klavye_dizisi(F_KLAVYE), n),
        "q_klavye":          benzersiz_uret(lambda: klavye_dizisi(Q_KLAVYE), n),
        "rastgele":          benzersiz_uret(rastgele, n),
        "cumle_sifre":       benzersiz_uret(lambda: cumle_sifre(kelimeler), n),
    }

    # Her kalıbı geliştirme ve test setine böl.
    # Şifreler zaten rastgele sırada üretildi; burada tekrar KARIŞTIRILMAZ.
    # Böylece "ayşe2012" ile "ayse2012" hep aynı sete düşer.
    satirlar = []
    for kalip, sifreler in kaliplar.items():
        test_sayisi = round(len(sifreler) * TEST_ORANI)
        # Takımlarda bir çift (beşiktaş1903 / besiktas1903) sınırda ikiye bölünmesin:
        # sınır tam çiftin ortasına denk gelirse sınırı bir kaydır.
        if 0 < test_sayisi < len(sifreler):
            onceki, sonraki = sifreler[test_sayisi - 1], sifreler[test_sayisi]
            if onceki != sonraki and onceki.translate(TURKCE_HARF) == sonraki:
                test_sayisi += 1
        for i, sifre in enumerate(sifreler):
            set_adi = "test" if i < test_sayisi else "gelistirme"
            satirlar.append([sifre, kalip, set_adi])

    CIKTI.parent.mkdir(exist_ok=True)
    # "utf-8-sig": Excel Türkçe harfleri doğru göstersin diye
    with open(CIKTI, "w", newline="", encoding="utf-8-sig") as dosya:
        yazici = csv.writer(dosya)
        yazici.writerow(["no", "sifre", "kalip", "set"])
        for no, satir in enumerate(satirlar, start=1):
            yazici.writerow([no] + satir)

    # Özet
    print("Şifreler üretildi ->", CIKTI)
    for kalip, sifreler in kaliplar.items():
        print(f"  {kalip:<18} {len(sifreler):>4} şifre   örnek: {sifreler[0]}")
    print("  TOPLAM", len(satirlar))


if __name__ == "__main__":
    main()
