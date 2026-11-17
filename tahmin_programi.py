# -*- coding: utf-8 -*-
"""
TAHMİN PROGRAMI - Şifre Dedektifleri projesi, 2. program

Bu program bir saldırganın şifreleri hangi SIRAYLA tahmin edeceğini taklit eder.
Saldırgan tahminlerini tek tek sayar; bir şifre kaçıncı tahminde bulunursa
o sayı, şifrenin DENEME SAYISI'dır.

Bu program NE YAPMAZ? (etik kurallar)
  - İnternete bağlanmaz, hiçbir siteye, hesaba veya sisteme giriş denemez.
  - Gerçek kişilerin şifrelerini kullanmaz; yalnızca sifre_uretici.py'nin
    ürettiği YAPAY şifreleri okur.
  - Gizli (şifrelenmiş) olarak saklanan şifreleri çözmeye çalışmaz.
    Sadece kendi tahminlerini yazılarla karşılaştırır; bir simülasyondur.
  - Şifrelerin kalıp türüne ('kalip' sütunu) bakmaz.

ÖNEMLİ: Bu program GitHub'da v2.0-tahmin olarak DONDURULMUŞTUR.
Güç ölçerimiz yazılırken bu programın ayarları değiştirilmez.

Çalıştırmak için önce şifreleri üretin, sonra:  python tahmin_programi.py
"""

import csv
from itertools import permutations
from pathlib import Path

# ---------------------------------------------------------------
# AYARLAR (araştırmanın kararları — v2.0-tahmin ile donduruldu)
# ---------------------------------------------------------------
DENEME_SINIRI = 10_000_000   # Saldırgan en fazla kaç tahmin dener? Daha fazlası = "sınırın üstünde"
YIL_BASI, YIL_SONU = 1900, 2030
KLAVYE_EN_KISA = 4           # Klavye dizileri en az kaç tuş uzunluğunda denensin?

# KURAL: Saldırgan önce EN AZ tahmin gerektiren grubu dener.
# (Sıra elle seçilmez; program grupların büyüklüğüne bakarak kendisi belirler.)

KLASOR = Path(__file__).parent
SOZLUK = KLASOR / "veri" / "saldirgan"     # Saldırganın kendi, daha büyük sözlüğü
GIRDI = KLASOR / "ciktilar" / "sifreler.csv"
CIKTI_GELISTIRME = KLASOR / "ciktilar" / "deneme_sayilari_gelistirme.csv"
CIKTI_TEST = KLASOR / "ciktilar" / "deneme_sayilari_test.csv"

# Klavye satırları (sifre_uretici.py ile aynı)
F_KLAVYE = ["fgğıodrnhpqw", "uieaütkmlyşx", "jövcçzsb"]
Q_KLAVYE = ["qwertyuıopğü", "asdfghjklşi", "zxcvbnmöç"]

TURKCE_HARF = str.maketrans("çğıöşü", "cgiosu")


# ---------------------------------------------------------------
# SALDIRGANIN SÖZLÜĞÜ (veri/saldirgan klasörü)
# ---------------------------------------------------------------
def liste_oku(dosya_adi):
    kelimeler = []
    with open(SOZLUK / dosya_adi, encoding="utf-8") as dosya:
        for satir in dosya:
            satir = satir.strip()
            if satir and not satir.startswith("#"):
                kelimeler.append(satir)
    return kelimeler


def iki_yazimla(kelimeler):
    """Her kelimeyi hem Türkçe karakterli hem karaktersiz yazar (tekrarları atar)."""
    sonuc = []
    for kelime in kelimeler:
        for yazim in (kelime, kelime.translate(TURKCE_HARF)):
            if yazim not in sonuc:
                sonuc.append(yazim)
    return sonuc


SIK_KELIMELER = liste_oku("kelimeler.txt")
TUM_KELIMELER = iki_yazimla(
    liste_oku("isimler.txt") + liste_oku("sehirler.txt")
    + liste_oku("takimlar.txt") + SIK_KELIMELER
)


# ---------------------------------------------------------------
# TAHMİN GRUPLARI: Her fonksiyon tahminleri SIRAYLA tek tek verir
# ---------------------------------------------------------------
def klavye():
    for satir in Q_KLAVYE + F_KLAVYE:
        for uzunluk in range(KLAVYE_EN_KISA, len(satir) + 1):
            for baslangic in range(len(satir) - uzunluk + 1):
                yield satir[baslangic:baslangic + uzunluk]


def tek_kelime():
    for kelime in TUM_KELIMELER:
        yield kelime


def kelime_iki_hane():
    for kelime in TUM_KELIMELER:
        for sayi in range(100):
            yield kelime + f"{sayi:02d}"      # 00, 01, ... 99


def kelime_yil():
    for kelime in TUM_KELIMELER:
        for yil in range(YIL_BASI, YIL_SONU + 1):
            yield kelime + str(yil)


def uc_kelime():
    for uclu in permutations(SIK_KELIMELER, 3):
        cumle = "-".join(uclu)
        yield cumle
        if cumle.translate(TURKCE_HARF) != cumle:
            yield cumle.translate(TURKCE_HARF)


GRUPLAR = {
    "klavye": klavye,
    "tek_kelime": tek_kelime,
    "kelime_iki_hane": kelime_iki_hane,
    "kelime_yil": kelime_yil,
    "uc_kelime": uc_kelime,
}


def grup_buyuklukleri():
    """Her gruptaki tahmin sayısını sayar."""
    return {ad: sum(1 for _ in uretici()) for ad, uretici in GRUPLAR.items()}


def tahmin_et(aranan_sifreler, sira):
    """Tahminleri sırayla dener. Her şifrenin kaçıncı tahminde bulunduğunu döndürür."""
    bulunanlar = {}                 # {şifre: (deneme_sayısı, grup)}
    deneme = 0
    for grup_adi in sira:
        for tahmin in GRUPLAR[grup_adi]():
            deneme += 1
            if deneme > DENEME_SINIRI:
                return bulunanlar, deneme - 1
            if tahmin in aranan_sifreler and tahmin not in bulunanlar:
                bulunanlar[tahmin] = (deneme, grup_adi)
    return bulunanlar, deneme


# ---------------------------------------------------------------
# ANA PROGRAM
# ---------------------------------------------------------------
def nokta(sayi):
    return f"{sayi:,}".replace(",", ".")


def main():
    buyuklukler = grup_buyuklukleri()
    sira = sorted(buyuklukler, key=buyuklukler.get)   # küçükten büyüğe
    print("Tahmin sırası (en küçük grup önce):")
    for ad in sira:
        print(f"  {ad:<16} {nokta(buyuklukler[ad]):>12} tahmin")

    # Program yalnızca 'sifre' ve 'set' sütunlarını kullanır.
    with open(GIRDI, encoding="utf-8-sig") as dosya:
        sifreler = list(csv.DictReader(dosya))

    bulunanlar, toplam_deneme = tahmin_et({s["sifre"] for s in sifreler}, sira)
    print(f"\nToplam yapılan tahmin: {nokta(toplam_deneme)} (sınır: {nokta(DENEME_SINIRI)})")

    sonuclar = {"gelistirme": [], "test": []}
    for satir in sifreler:
        if satir["sifre"] in bulunanlar:
            deneme, grup = bulunanlar[satir["sifre"]]
            bulundu = "evet"
        else:
            deneme, grup, bulundu = "", "", "hayir"   # sınırın üstünde
        sonuclar[satir["set"]].append(
            [satir["no"], satir["sifre"], satir["kalip"], satir["set"], bulundu, deneme, grup]
        )

    for set_adi, dosya_yolu in (("gelistirme", CIKTI_GELISTIRME), ("test", CIKTI_TEST)):
        with open(dosya_yolu, "w", newline="", encoding="utf-8-sig") as dosya:
            yazici = csv.writer(dosya)
            yazici.writerow(["no", "sifre", "kalip", "set", "bulundu", "deneme_sayisi", "tahmin_grubu"])
            yazici.writerows(sonuclar[set_adi])

    # Özet: YALNIZCA geliştirme seti gösterilir. Test seti sona saklanır!
    print("\nGeliştirme seti özeti (test seti sona saklanıyor):")
    print(f"  {'kalıp':<18} {'bulunan':>8}")
    kaliplar = {}
    for satir in sonuclar["gelistirme"]:
        toplam, bulunan = kaliplar.get(satir[2], (0, 0))
        kaliplar[satir[2]] = (toplam + 1, bulunan + (satir[4] == "evet"))
    for kalip, (toplam, bulunan) in kaliplar.items():
        print(f"  {kalip:<18} {bulunan:>3} / {toplam}")
    print("\nSonuçlar ->", CIKTI_GELISTIRME.name, "ve", CIKTI_TEST.name)


if __name__ == "__main__":
    main()
