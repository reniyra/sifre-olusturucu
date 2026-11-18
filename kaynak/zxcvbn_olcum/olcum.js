// zxcvbn_olcum.html sayfasının hesap kısmı.
// zxcvbn-ts'yi ortak paket + Türkçe paketle kurar, şifreleri puanlar.
import { ZxcvbnFactory } from '@zxcvbn-ts/core'
import * as ortak from '@zxcvbn-ts/language-common'
import * as turkce from '@zxcvbn-ts/language-tr'

const sozlukler = { ...ortak.dictionary, ...turkce.dictionary }

const olcer = new ZxcvbnFactory({
  dictionary: sozlukler,
  graphs: ortak.adjacencyGraphs,
  translations: turkce.translations,
})

export const AYARLAR = {
  surumler: __SURUMLER__,
  sozlukler: Object.keys(sozlukler),
  klavyeler: Object.keys(ortak.adjacencyGraphs),
}

const PARCA_ADLARI = {
  dictionary: 'sözlükte bulunan kelime',
  spatial: 'klavye dizisi',
  repeat: 'tekrar eden karakterler',
  sequence: 'sıralı karakterler (abc, 123)',
  regex: 'yakın bir yıl',
  date: 'tarih',
  bruteforce: 'tahmin edilemeyen parça',
  separator: 'ayırıcı işaret',
}

export function olc(sifre) {
  const s = olcer.check(sifre)
  return {
    puan: s.score,
    tahmin: Math.round(s.guesses),
    parcalar: s.sequence.map((p) => ({
      parca: p.token,
      tur: PARCA_ADLARI[p.pattern] || p.pattern,
      ayrinti: p.pattern === 'dictionary' ? p.dictionaryName
        : p.pattern === 'spatial' ? p.graph : '',
    })),
    uyari: s.feedback.warning || '',
  }
}

// sifreler.csv dosyasını okur (no,sifre,kalip,set).
export function csvOku(metin) {
  const satirlar = metin.replace(/^﻿/, '').split(/\r?\n/).filter((x) => x.trim() !== '')
  const baslik = satirlar[0].split(',')
  const beklenen = ['no', 'sifre', 'kalip', 'set']
  if (beklenen.some((b, i) => baslik[i] !== b)) {
    throw new Error('Bu dosya sifreler.csv değil. İlk satır "no,sifre,kalip,set" olmalı.')
  }
  return satirlar.slice(1).map((s) => {
    const [no, sifre, kalip, set] = s.split(',')
    return { no, sifre, kalip, set }
  })
}

// Yalnızca geliştirme setini ölçer. Test seti büyük teste kadar ölçülmez.
export function gelistirmeyiOlc(kayitlar) {
  return kayitlar
    .filter((k) => k.set === 'gelistirme')
    .map((k) => {
      const s = olcer.check(k.sifre)
      return { ...k, zxcvbn_puan: s.score, zxcvbn_tahmin: Math.round(s.guesses) }
    })
}

export function csvYaz(sonuclar) {
  const satirlar = ['no,sifre,kalip,set,zxcvbn_puan,zxcvbn_tahmin']
  for (const s of sonuclar) {
    satirlar.push([s.no, s.sifre, s.kalip, s.set, s.zxcvbn_puan, s.zxcvbn_tahmin].join(','))
  }
  return '﻿' + satirlar.join('\n') + '\n'
}
