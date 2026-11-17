# -*- coding: utf-8 -*-
"""
SONUÇ RAPORU - Şifre Dedektifleri projesi, yardımcı program

Tahmin programının sonuçlarını (CSV) okur ve tarayıcıda açılabilen
bir sayfa üretir: ciktilar/rapor.html

Sayfadaki bütün yazılar, renk ve yazı tipi veri/rapor_metinleri.txt
dosyasından gelir. Metinleri değiştirmek için kod yazmanız gerekmez.

Bu program araştırmanın bir parçası değildir; yalnızca sonuçları gösterir.
ÖNEMLİ: Rapor YALNIZCA geliştirme setini gösterir. Test seti sona saklanır.

Çalıştırmak için:  python sonuc_raporu.py
"""

import csv
import html
import math
import statistics
from pathlib import Path

KLASOR = Path(__file__).parent
GIRDI = KLASOR / "ciktilar" / "deneme_sayilari_gelistirme.csv"
METINLER = KLASOR / "veri" / "rapor_metinleri.txt"
CIKTI = KLASOR / "ciktilar" / "rapor.html"
DENEME_SINIRI = 10_000_000   # tahmin_programi.py ile aynı

KALIP_ADLARI = {
    "q_klavye": "Q klavye dizisi",
    "f_klavye": "F klavye dizisi",
    "sehir_plaka": "Şehir + plaka",
    "kelime_yil_turkce": "Kelime + yıl (Türkçe harfli)",
    "kelime_yil_ascii": "Kelime + yıl (Türkçe harfsiz)",
    "takim_kurulus": "Takım + kuruluş yılı",
    "cumle_sifre": "Üç kelime",
    "rastgele": "Rastgele",
}


def nokta(sayi):
    return f"{sayi:,}".replace(",", ".")


def metinleri_oku():
    """[BAŞLIK] gibi bölümleri ve altlarındaki yazıları okur."""
    metinler, bolum = {}, None
    with open(METINLER, encoding="utf-8") as dosya:
        for satir in dosya:
            satir = satir.rstrip("\n")
            if satir.startswith("#"):
                continue
            if satir.startswith("[") and satir.strip().endswith("]"):
                bolum = satir.strip()[1:-1]
                metinler[bolum] = []
            elif bolum is not None:
                metinler[bolum].append(satir)
    return {ad: "\n".join(satirlar).strip() for ad, satirlar in metinler.items()}


def paragraf(yazi):
    """Boş satırla ayrılan yazıları ayrı paragraflar yapar."""
    return "\n".join(f"<p>{html.escape(p.strip())}</p>" for p in yazi.split("\n\n") if p.strip())


def verileri_oku():
    with open(GIRDI, encoding="utf-8-sig") as dosya:
        satirlar = list(csv.DictReader(dosya))
    kaliplar = {}
    for s in satirlar:
        k = kaliplar.setdefault(s["kalip"], {"toplam": 0, "sayilar": []})
        k["toplam"] += 1
        if s["bulundu"] == "evet":
            k["sayilar"].append(int(s["deneme_sayisi"]))
    for k in kaliplar.values():
        k["sayilar"].sort()
        k["ortanca"] = int(statistics.median(k["sayilar"])) if k["sayilar"] else None
    sirali = sorted(kaliplar.items(),
                    key=lambda kv: kv[1]["ortanca"] if kv[1]["ortanca"] is not None else float("inf"))
    return sirali, len(satirlar)


def grafik(kaliplar, renk):
    """Logaritmik eksenli grafik: her kalıp için en az–en çok çizgisi ve ortanca noktası."""
    sol, sag, ust, satir_h = 220, 860, 50, 40
    yukseklik = ust + satir_h * len(kaliplar) + 50
    ust_us = math.log10(DENEME_SINIRI)
    x = lambda d: sol + (math.log10(max(d, 1)) / ust_us) * (sag - sol)

    p = [f'<svg viewBox="0 0 900 {yukseklik}" role="img" aria-label="Kalıplara göre deneme sayıları">']
    for us in range(0, int(ust_us) + 1):
        xx = x(10 ** us)
        p.append(f'<line x1="{xx:.1f}" y1="{ust - 8}" x2="{xx:.1f}" y2="{yukseklik - 45}" stroke="#ddd"/>')
        p.append(f'<text x="{xx:.1f}" y="{ust - 15}" font-size="12" text-anchor="middle" fill="#555">{nokta(10 ** us)}</text>')
    p.append(f'<text x="{(sol + sag) / 2}" y="{yukseklik - 15}" font-size="13" text-anchor="middle" fill="#333">Deneme sayısı (logaritmik eksen)</text>')

    for i, (kalip, k) in enumerate(kaliplar):
        y = ust + 20 + i * satir_h
        p.append(f'<text x="{sol - 12}" y="{y + 4}" font-size="13" text-anchor="end" fill="#222">{html.escape(KALIP_ADLARI.get(kalip, kalip))}</text>')
        if k["ortanca"] is None:
            p.append(f'<text x="{sag}" y="{y + 4}" font-size="12" text-anchor="end" fill="#222">bulunamadı (sınırın üstünde) →</text>')
        else:
            p.append(f'<line x1="{x(k["sayilar"][0]):.1f}" y1="{y}" x2="{x(k["sayilar"][-1]):.1f}" y2="{y}" stroke="#999" stroke-width="2"/>')
            p.append(f'<circle cx="{x(k["ortanca"]):.1f}" cy="{y}" r="5" fill="{html.escape(renk)}"/>')
    p.append("</svg>")
    return "\n".join(p)


def tablo(kaliplar):
    satirlar = []
    for kalip, k in kaliplar:
        sayilar = k["sayilar"]
        hucre = lambda d: nokta(d) if d is not None else "—"
        satirlar.append(
            f"<tr><td>{html.escape(KALIP_ADLARI.get(kalip, kalip))}</td>"
            f"<td>{len(sayilar)} / {k['toplam']}</td>"
            f"<td>{hucre(sayilar[0] if sayilar else None)}</td>"
            f"<td>{hucre(k['ortanca'])}</td>"
            f"<td>{hucre(sayilar[-1] if sayilar else None)}</td></tr>"
        )
    return "\n".join(satirlar)


def main():
    m = metinleri_oku()
    renk = m.get("RENK", "navy") or "navy"
    yazi_tipi = m.get("YAZI TİPİ", "Arial") or "Arial"
    kaliplar, toplam = verileri_oku()

    sayfa = f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(m.get("BAŞLIK", ""))}</title>
<style>
 body {{ font-family: "{html.escape(yazi_tipi)}", sans-serif; max-width: 900px; margin: 30px auto; padding: 0 16px; color: #111; line-height: 1.5; }}
 h1, h2 {{ color: {html.escape(renk)}; }}
 svg {{ width: 100%; height: auto; }}
 .baslik {{ font-weight: bold; margin-top: 4px; }}
 table {{ border-collapse: collapse; width: 100%; }}
 th, td {{ border: 1px solid #999; padding: 6px 8px; text-align: left; }}
 td:not(:first-child), th:not(:first-child) {{ text-align: right; }}
</style></head><body>
<h1>{html.escape(m.get("BAŞLIK", ""))}</h1>
<p>{html.escape(m.get("ALT BAŞLIK", ""))}</p>
{paragraf(m.get("GİRİŞ", ""))}

<p class="baslik">Şekil 1. Kalıplara göre deneme sayıları (geliştirme seti, {toplam} şifre)</p>
{grafik(kaliplar, renk)}
{paragraf(m.get("ŞEKİL AÇIKLAMASI", ""))}

<p class="baslik">Tablo 1. Kalıplara göre bulunan şifre sayısı ve deneme sayıları</p>
<table><tr><th>Kalıp</th><th>Bulunan</th><th>En az</th><th>Ortanca</th><th>En çok</th></tr>
{tablo(kaliplar)}
</table>
{paragraf(m.get("TABLO AÇIKLAMASI", ""))}

<h2>Yorum</h2>
{paragraf(m.get("YORUM", ""))}
</body></html>"""
    CIKTI.write_text(sayfa, encoding="utf-8")
    print("Rapor hazır ->", CIKTI)


if __name__ == "__main__":
    main()
