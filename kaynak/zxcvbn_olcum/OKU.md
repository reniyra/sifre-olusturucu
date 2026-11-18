# zxcvbn_olcum.html nasıl üretildi?

`zxcvbn_olcum.html` tek dosyadır; zxcvbn-ts paketleri içine gömülüdür, internete bağlanmaz.
Bu klasör, o dosyanın kaynağıdır. Öğrencilerin bu klasörde bir şey yapması gerekmez.

- `olcum.js`: ölçerin kurulumu (ortak paket + Türkçe paket) ve ölçüm kodu
- `sayfa.html`: sayfanın görünümü
- `package.json`, `package-lock.json`: kullanılan paket sürümleri

Yeniden üretmek için (Node.js gerekir):

```
npm ci
npx esbuild olcum.js --bundle --minify --format=iife --global-name=Olcum --target=es2017 --define:__SURUMLER__='{"@zxcvbn-ts/core":"4.3.0","@zxcvbn-ts/language-common":"4.2.0","@zxcvbn-ts/language-tr":"4.1.2"}' --outfile=olcum.bundle.js
```

Sonra `sayfa.html` içindeki `__BUNDLE__` yazısının yerine `olcum.bundle.js` dosyasının içeriği konur.
