# ROADMAP.md — Audit Gabungan: Papan Instrumen + Papan Gerak

> **UPDATE (revisi kedua, dicek ulang):** Anda mengirim ulang `papan-instrumen-main.zip` dan
> `papan-gerak-main.zip` yang sudah direvisi. Hasil re-check ada di **§8 di paling bawah file
> ini** — ringkasnya: **16 dari 17 temuan sudah diperbaiki dengan benar**, termasuk bug kritis
> `adxStrong` yang tadinya membuat file strategy gagal compile. Detail per-item ada di §8,
> termasuk 1 temuan baru kecil dari proses revisi ini sendiri. Bagian §1–§7 di bawah adalah
> laporan audit ASLI (kondisi sebelum revisi) — dipertahankan apa adanya sebagai jejak/referensi.

> Dibuat oleh audit eksternal (code review + testing statis) atas kedua repo:
> `papan-instrumen-main.zip` (v0.3.0-beta, Build 010) dan `papan-gerak-main_2.zip` (v0.2.1-alpha).
> Metodologi: baca penuh seluruh `src/modules/*.pine`, `src/strategies/*.pine`, rebuild via `build.sh` dan
> di-diff terhadap file `.pine` yang di-commit (hasil: **identik**, jadi build pipeline terpercaya),
> lalu ditelusuri manual baris-per-baris untuk logic error, dead code, dan inkonsistensi lintas-modul.
> Tidak bisa menjalankan `npm run test:all` di sandbox ini (tidak ada akses jaringan untuk `npm install pinets`),
> jadi semua temuan di bawah adalah hasil **code reading + reasoning manual**, bukan hasil run test otomatis.
> Silakan pakai file ini sebagai working checklist — centang tiap item setelah diverifikasi & di-fix di TradingView.

---

## 0. Ringkasan Eksekutif

Kedua proyek ini jauh di atas rata-rata script Pine Script publik dari segi kedisiplinan proses —
`CATATAN.md`, test suite, CI, changelog, dan "Golden Rule" sudah ada dan dipakai konsisten. Bug-bug
lama (P0-1 s/d P0-5, BG-1 s/d BG-19) sudah diperbaiki dengan baik dan didokumentasikan.

Namun, audit ini menemukan **7 bug baru di Papan Instrumen** dan **10 bug baru di Papan Gerak**
(termasuk **1 bug yang membuat `PapanGerakStrategy.pine` gagal compile** dan **1 bug visual yang
langsung terlihat di screenshot yang Anda kirim**). Beberapa di antaranya "tersembunyi" dalam arti:
kodenya terlihat benar sekilas, komentarnya bahkan mengklaim sudah benar, tapi hasil akhirnya diam-diam
salah (dead code, variable yang dihitung tapi tak pernah dipakai, cross-symbol mismatch).

Tidak ditemukan bug yang membuat Papan Instrumen gagal compile. Papan Gerak (indikator utama) juga
aman; masalah compile HANYA ada di file strategy pendampingnya.

---

## 1. BUG — PAPAN INSTRUMEN

### PI-1 · 🔴 KRITIS (VISIBLE) — Semua 44 input tidak punya `display = display.data_window`

| | |
|---|---|
| **Lokasi** | `src/modules/01-base.pine`, seluruh 44 pemanggilan `input.*()` |
| **Dampak** | **Ini persis penyebab teks acak-acakan di bawah candle pada screenshot Anda**: `PnInstrum COMPOSITE FQ Kanan Atas Kecil Sekali Profesional Gelap Indonesia Otomatis Custom 1 1 1 1 1 1 1 24 20 1,000 10,000 500 20,000 50 -1 -1 -1 300`. Itu adalah **status line** chart yang menampilkan seluruh nilai input karena tidak ada satu pun yang di-set `display = display.data_window`. |
| **Kenapa lolos** | Papan Gerak (`CATATAN.md` BG-9) sudah pernah mengalami persis bug ini dan sudah diperbaiki — tapi perbaikannya tidak pernah "diwariskan" balik ke Papan Instrumen, padahal keduanya satu penulis/pola yang sama. |
| **Cek cepat** | `grep -c "input\." 01-base.pine` → 44. `grep -c "input\." 01-base.pine \| grep -v display` → **44** (100% tidak ada `display=`). |
| **Fix** | Tambahkan `display = display.data_window` di akhir setiap `input.*()` yang murni parameter teknikal/tampilan (hampir semua). Sisakan **maksimal 2–3 input paling penting** (mis. `simbolInput`, `modeSektor`) dengan `display = display.data_window + display.status_line` bila memang ingin tetap terlihat ringkas di status line — itupun opsional. |
| **Contoh fix** | ```pine\n// SEBELUM\nposisiInput = input.string("Kanan Atas", "Posisi Tabel", options = [...], group = grupUtama)\n\n// SESUDAH\nposisiInput = input.string("Kanan Atas", "Posisi Tabel", options = [...], group = grupUtama, display = display.data_window)\n``` |
| **Effort** | 15–20 menit (cari-ganti terstruktur di 1 file, lalu `bash build.sh`). |

---

### PI-2 · 🟠 TINGGI (HIDDEN) — Bobot sector-aware "Faktor Indonesia" dihitung tapi tidak pernah dipakai

| | |
|---|---|
| **Lokasi** | `src/modules/04-scoring.pine` baris 577–600 |
| **Kode saat ini** | ```pine\nwIndonesia = 1.0\nif isSiklikalLike\n    wIndonesia := 1.3\nelse if isTechnologySektor\n    wIndonesia := 1.2\nelse if isBankSektor or isAsuransiSektor or isSekuritasSektor or isInfrastrukturSektor\n    wIndonesia := 0.8\nindonesiaScore = f_avg3(indoLiqScore, indoBetaScore, indoMacroScore)\n...\noverallScore = ... f_wavg7(..., indonesiaScore, ..., bobotIndonesia)  // ← wIndonesia TIDAK dipakai di sini!\n``` |
| **Dampak** | Header file (`01-base.pine` baris 8–12) secara eksplisit mengklaim: *"Bobot efektif 10-18% tergantung sektor"* untuk Faktor Indonesia. **Klaim ini salah** — variabel `wIndonesia` (0.8/1.2/1.3 tergantung sektor) dihitung, tapi baris `f_wavg7(...)` memakai `bobotIndonesia` (input slider user, default 1.0) secara langsung, bukan `bobotIndonesia * wIndonesia`. Artinya **semua sektor mendapat bobot Faktor Indonesia yang identik**, tidak peduli sektornya bank, siklikal, atau teknologi — fitur diferensiasi sektornya adalah dead code. |
| **Fix** | ```pine\n// Kalikan slider user dengan multiplier sektor sebelum dipakai:\neffectiveBobotIndonesia = bobotIndonesia * wIndonesia\noverallScore = tampilIndonesia ?\n     (pakaiBobotTertimbang ?\n          f_wavg7(valueScore, qualityScore, growthScore, healthScore, momentumScore, incomeScore, indonesiaScore,\n               bobotValue, bobotQuality, bobotGrowth, bobotHealth, bobotMomentum, bobotIncome, effectiveBobotIndonesia) :\n          ...)\n``` |
| **Catatan** | Karena `tampilIndonesia` default **OFF**, dampak bug ini ke pengguna umum kecil — tapi begitu seseorang mengaktifkan "Faktor Indonesia" (fitur yang dipromosikan sebagai unggulan build 006), mereka mendapat perilaku yang berbeda dari yang didokumentasikan. |
| **Effort** | 5 menit fix + re-run test overall score. |

---

### PI-3 · 🟠 TINGGI (HIDDEN, cross-symbol) — Beta vs IDX memakai `close` chart, bukan `dClose` simbol yang dipilih

| | |
|---|---|
| **Lokasi** | `src/modules/02-data.pine` baris 76–78 |
| **Kode saat ini** | ```pine\nfloat stockDailyRet = close / nz(close[1]) - 1     // ← "close" chart aktif, BUKAN sym!\nfloat benchDailyRet = benchClose / nz(benchClose[1]) - 1\nfloat betaVal = ta.correlation(stockDailyRet, benchDailyRet, 252) * ta.stdev(stockDailyRet, 252) / ta.stdev(benchDailyRet, 252)\n``` |
| **Kenapa bug** | Semua data lain di script ini (rasio, growth, dll.) diambil lewat `request.security(sym, "D", ...)` sehingga konsisten memakai simbol yang dipilih di input **"Simbol Saham"** (`sym`), walau chart aktif menampilkan simbol lain. Tapi `stockDailyRet` di sini memakai variabel bar `close` **langsung** (tanpa `request.security`), yang berarti ia selalu mengacu ke **simbol & timeframe chart yang sedang dibuka user**, bukan ke `sym`. |
| **Dampak konkret** | 1) Kalau user mengisi input "Simbol Saham" untuk melihat fundamental **BBCA** sementara chart yang terbuka adalah **BBRI** → kolom "Beta vs IDX" dan skor "Indonesia — Stabilitas" (`indoBetaScore`) yang tampil sebenarnya adalah **beta BBRI**, bukan BBCA. 2) Kalau chart dibuka di timeframe selain Daily (mis. 4H/Weekly), `close/close[1]-1` bukan return harian, tapi dikorelasikan dengan `benchDailyRet` yang genuinely harian → hasil beta secara statistik tidak berarti (mismatch frekuensi). |
| **Fix** | Pakai `dClose` (sudah tersedia, sudah benar via `request.security(sym,"D",...)`) untuk basis perhitungan return saham: ```pine\nfloat stockDailyRet = dClose / nz(dClose[1]) - 1\n``` Atau, lebih rapi: hitung beta di dalam `getMarketData()`/`request.security(sym,"D",...)` sekalian, supaya satu sumber kebenaran. |
| **Effort** | 10 menit fix, tapi **butuh verifikasi manual** (bandingkan beta sebelum/sesudah pada simbol yang sama vs simbol override) sebelum rilis. |

---

### PI-4 · 🟡 RENDAH — Komentar vs implementasi "IDR 3M Trend" tidak sinkron

| | |
|---|---|
| **Lokasi** | `04-scoring.pine` baris 572–574 |
| **Kode** | ```pine\nindoIdrTrend = na(idrTrend3M) ? na :\n     isSiklikalLike ? f_scoreHigher(idrTrend3M, -5, 15) :\n     f_scoreLower(idrTrend3M, -5, 5)   // komentar: "lain: IDR stabil = netral"\n``` |
| **Masalah** | Komentar bilang "IDR stabil = netral" (menyiratkan skor tertinggi ada di sekitar 0%, U-shape/`f_scoreMid`), tapi `f_scoreLower(v, good=-5, bad=5)` sebenarnya linear: skor tertinggi (100) justru di **-5%** (IDR menguat tajam), bukan di 0%. Jadi bukan "stabil = netral", tapi "menguat = terbaik". |
| **Fix** | Pilih salah satu yang benar-benar dimaksud: (a) kalau memang mau reward penguatan IDR, ubah komentar; atau (b) kalau memang mau "stabil = terbaik", ganti ke sesuatu seperti `f_scoreMid(math.abs(idrTrend3M), 0, 0, 8)`-style (skor tinggi saat `idrTrend3M` dekat 0, turun ke dua arah). |
| **Effort** | 5–10 menit, dampak kecil (dimensi opsional, default OFF). |

---

### PI-5 · 🟡 RENDAH (UX) — Kartu skor tetap tampil walau status "NO DATA" sudah aktif

| | |
|---|---|
| **Lokasi** | `04-scoring.pine` baris 635–658 |
| **Masalah** | `noData` hanya menyembunyikan header "SKOR KESELURUHAN" (`if not noData: l := f_section(...)`), tapi baris-baris `f_scoreCardN` (Quality/Value/Growth/Health/Income/Momentum) di bawahnya **tetap dieksekusi tanpa syarat** — sehingga saat emiten benar-benar tidak ada data sama sekali, tabel tetap menampilkan 5 baris peringatan "DATA TIDAK TERSEDIA" **diikuti** 6 kartu skor kosong (`—`) yang membingungkan pemula ("kok ada skor kalau katanya tidak ada data?"). |
| **Fix** | Bungkus blok scoreCard juga dengan `if not noData`, atau tampilkan pesan tunggal yang lebih jelas tanpa mem-render kartu kosong sama sekali. |
| **Effort** | 10 menit. |

---

### PI-6 · 🔵 INFO (risiko ke depan) — Budget request mendekati limit 40 panggilan dinamis Pine v6

| | |
|---|---|
| **Temuan** | Terhitung **35 pemanggilan** `request.security`/`request.financial` unik (32 field fundamental + 3 `request.security` lain: market data, benchmark, USDIDR) dari batas keras **40 dynamic request per eksekusi** di Pine Script v6. Itu artinya **87,5% dari budget sudah terpakai**. |
| **Risiko** | Penambahan field fundamental baru (mis. permintaan pengguna untuk EV/FCF, atau data sektor tambahan) berisiko **langsung menabrak limit compile** tanpa peringatan dini. |
| **Saran** | Sebelum menambah field baru, buat script kecil terpisah yang menghitung total pemanggilan otomatis (`grep -c` seperti yang dipakai di audit ini) dan jadikan bagian dari `scripts/lint.sh` sebagai *hard gate* CI (gagalkan build kalau > 36–37 panggilan), bukan cuma catatan di komentar. |

---

### PI-7 · ⚪ COSMETIC — `max_labels_count = 50` di header `indicator()` tapi tak ada `label.*()` dipakai

| | |
|---|---|
| **Lokasi** | `01-base.pine`, parameter `indicator()` |
| **Dampak** | Tidak ada dampak fungsional (harmless), tapi menyesatkan pembaca kode baru yang mengira ada elemen `label` di suatu tempat. |
| **Fix** | Hapus parameter tersebut kalau memang tidak ada rencana pakai `label.*()`. |

---

## 2. BUG — PAPAN GERAK

> Penomoran melanjutkan `BG-1..19` yang sudah ada di `CATATAN.md` Papan Gerak, supaya tetap satu sistem pelacakan.

### BG-20 · 🔴 KRITIS (COMPILE-BREAKING) — `adxStrong` dipakai tapi tidak pernah dideklarasikan

| | |
|---|---|
| **Lokasi** | `src/strategies/PapanGerakStrategy.pine` baris 72 |
| **Kode** | ```pine\n[adxUp, adxDn, adxValue] = ta.dmi(adxLength, adxLength)\n...\nadxScore = adxStrong ? (adxUp > adxDn ? 80 : 20) : 50   // ← "adxStrong" TIDAK PERNAH dideklarasikan di file ini\n``` |
| **Dampak** | **File `PapanGerakStrategy.pine`, seperti yang ada di zip, tidak akan lolos compile di TradingView** — akan muncul error "undeclared identifier 'adxStrong'". Di indikator utama (`02-data.pine`), variabel ini didefinisikan dengan `adxStrong = adxValue >= adxThreshold`, tapi baris itu tidak pernah disalin ke file strategy. |
| **Fix** | Tambahkan sebelum baris 72: ```pine\nadxStrong = adxValue >= adxThreshold\n``` |
| **Cara mencegah** | File strategy adalah salinan manual sebagian logika indikator (bukan hasil `build.sh`) — ini pola berisiko tinggi untuk *logic drift*. Lihat rekomendasi proses di §5. |
| **Effort** | 2 menit — tapi **wajib** di-compile-test ulang di Pine Editor sebelum publish, karena ini satu-satunya bug yang benar-benar memblokir pemakaian. |

---

### BG-21 · 🟠 SEDANG (VISIBLE, salah warna) — Return negatif ditampilkan warna HIJAU, bukan merah

| | |
|---|---|
| **Lokasi** | `src/strategies/PapanGerakStrategy.pine` baris 144 |
| **Kode** | ```pine\nnetStr = str.tostring(math.round(netPct * 10) / 10) + "%"\ntable.cell(tbl, 0, 4, "Return: " + netStr, text_size = size.small,\n text_color = netPct >= 0 ? color.rgb(38, 166, 154) : color.rgb(83, 239, 80))\n``` |
| **Kenapa bug** | `color.rgb(83, 239, 80)` — R=83, **G=239** (dominan hijau) — dipakai justru untuk kasus **rugi** (`netPct < 0`). Ini kebalikan dari konvensi universal industri trading (hijau = untung, merah = rugi — lihat referensi §4). Polanya jelas: digit `239` dan `83` **tertukar posisi** dari warna "bear" yang benar dipakai di seluruh script lain, yaitu `color.rgb(239, 83, 80)` (R=239 dominan → merah). Ini murni salah ketik/transposisi digit yang lolos karena tidak ada regression test visual. |
| **Fix** | ```pine\ntext_color = netPct >= 0 ? color.rgb(38, 166, 154) : color.rgb(239, 83, 80)\n``` |
| **Dampak** | Kalau strategy backtest merugi, tabel ringkasan **tetap terlihat "hijau/aman"** — berpotensi membuat trader kurang waspada terhadap performa strategy yang sebenarnya negatif. |
| **Effort** | 1 menit fix, tapi high-value untuk ditemukan karena bisa menyesatkan evaluasi backtest. |

---

### BG-22 · 🟠 SEDANG (HIDDEN, inkonsistensi) — Filter MTF pakai EMA 200/50/20 hardcode, bukan input user

| | |
|---|---|
| **Lokasi** | `src/modules/02-data.pine` baris 152–159 |
| **Kode** | ```pine\nmtfTrendScore = if enableMtfFilter\n    request.security(syminfo.tickerid, mtfTimeframe,\n        (close > ta.ema(close, 200) ? 50 : 0) +\n        (close > ta.ema(close, 50) ? 30 : 0) +\n        (close > ta.ema(close, 20) ? 20 : 0),\n        barmerge.gaps_off, barmerge.lookahead_off)\n``` |
| **Kenapa bug** | Dashboard utama memakai `emaFastPeriod`/`emaMidPeriod`/`emaSlowPeriod` (default 20/50/200, **bisa diubah user** di grup "Trend"). Tapi filter MTF ini selalu memakai angka **200/50/20 tetap**, tidak peduli apakah user sudah mengganti setting EMA-nya. Kalau user mengubah EMA Slow ke 100 misalnya (untuk saham dengan histori data pendek), definisi "tren" di dashboard utama dan definisi "tren" di filter MTF **jadi tidak sinkron secara diam-diam** — user tidak akan tahu ini kecuali membaca source code. |
| **Fix** | ```pine\nmtfTrendScore = if enableMtfFilter\n    request.security(syminfo.tickerid, mtfTimeframe,\n        (close > ta.ema(close, emaSlowPeriod) ? 50 : 0) +\n        (close > ta.ema(close, emaMidPeriod) ? 30 : 0) +\n        (close > ta.ema(close, emaFastPeriod) ? 20 : 0),\n        barmerge.gaps_off, barmerge.lookahead_off)\n``` |
| **Effort** | 5 menit. |

---

### BG-23 · 🟠 SEDANG (DESIGN DRIFT) — `PapanGerakStrategy.pine` punya rumus scoring berbeda dari indikator asli

| | |
|---|---|
| **Lokasi** | `src/strategies/PapanGerakStrategy.pine`, seluruh §3 "Simplified Scoring" vs `03-scoring.pine` |
| **Perbedaan konkret** | 1) Strategy: `overallScore = (trendScore*3 + momentumScore*3 + volScore*2) / 8` — **dimensi Volatilitas hilang total** dari overall score. Indikator asli: 4 dimensi (Tren/Momentum/Volatilitas/Volume) dengan bobot **yang bisa diatur user** (default 30/30/20/20). 2) Strategy tidak menerapkan `minSignalBars` (jarak minimal antar sinyal) maupun `signalFilterMode` (filter Chop) yang ada di indikator asli — sehingga entry di strategy bisa jauh lebih sering/lebih longgar daripada sinyal yang benar-benar akan muncul di indikator/alert. |
| **Dampak** | Angka **Win Rate / Profit Factor / Return** yang ditampilkan tabel strategy tester **tidak merepresentasikan** perilaku sinyal Papan Gerak yang sesungguhnya. Trader yang percaya diri karena "backtest menunjukkan win rate 55%" bisa kaget saat sinyal live (dari indikator asli, lewat alert) berperilaku berbeda karena rumusnya memang tidak sama. |
| **Fix** | Idealnya `PapanGerakStrategy.pine` **meng-import logic yang sama** (via 1 file scoring bersama yang di-`build.sh`-kan ke kedua output), bukan menyalin ulang secara manual dan disederhanakan. Kalau simplifikasi memang disengaja untuk alasan performa/budget compile, **wajib** ditulis eksplisit di komentar file + README: *"Strategy ini adalah APPROXIMASI, bukan replikasi 1:1 sinyal indikator — jangan jadikan angka win rate di sini sebagai janji performa sinyal live."* |
| **Effort** | Sedang–besar tergantung pendekatan (refactor build pipeline vs. cukup tambah disclaimer eksplisit). |

---

### BG-24 · 🟡 SEDANG (RISIKO TRADING, bukan bug compile) — Sinyal & alert tidak digerbang oleh `barstate.isconfirmed`

| | |
|---|---|
| **Lokasi** | `03-scoring.pine` §12 (Entry Trigger Engine), `04-ui.pine` §3 (Alerts) |
| **Penjelasan teknis** | Semua kondisi `entryTriggered`, `pullbackTrigger`, `breakoutTrigger`, serta seluruh `alert()` (RSI OB/OS, Volume Spike, Trend Extreme, dll.) dievaluasi **setiap bar berjalan**, termasuk bar yang **belum close** (real-time/intrabar). Menurut referensi resmi Pine Script maupun komunitas ([TradingView Pine Docs — Profiling](https://www.tradingview.com/pine-script-docs/writing/profiling-and-optimization/); Pineify — *"request.security() runs on every tick, no matter what... even inside an if statement"*), ini perilaku normal Pine Script, tapi konsekuensinya: **sinyal & alert bisa berubah-ubah / "repaint" selama bar berjalan**, dan alert bisa terkirim berdasarkan harga yang belum final sebelum candle benar-benar tutup. |
| **Dampak** | Trader pemula yang menerima alert lalu langsung entry manual di menit itu juga berisiko entry berdasarkan kondisi yang **berbalik lagi sebelum candle Daily selesai**. Ini bukan "bug" dalam arti salah logika, tapi **risiko trading nyata yang tidak didokumentasikan** di README/docs saat ini. |
| **Saran fix / mitigasi** | Tambahkan opsi input, mis. `confirmOnCloseOnly = input.bool(true, "Hanya Sinyal di Bar Close")`, lalu bungkus trigger dengan `and (not confirmOnCloseOnly or barstate.isconfirmed)`. Minimal: tambahkan catatan eksplisit di `docs/PANDUAN-TRADING.md` bahwa nilai di tabel & alert bisa berubah sebelum candle close, terutama di timeframe Daily saat market masih berjalan. |
| **Effort** | 30–60 menit untuk opsi konfirmasi bar-close + testing. |

---

### BG-25 · 🟡 RENDAH (DEAD CODE) — Ada 2 rumus "Smart Money Score" berbeda, satu di antaranya tak terpakai

| | |
|---|---|
| **Lokasi** | `smScore` di `02-data.pine` baris 137–147 vs `f_smartMoneyScore()` / `smartMoneyScore` di `03-scoring.pine` baris 172–199 |
| **Masalah** | `02-data.pine` mendefinisikan `smScore` (basis 50, +25/+15/+10 aditif). Tapi yang benar-benar dipakai di tabel & overall score adalah `smartMoneyScore` dari `f_smartMoneyScore()` (skema rata-rata berbobot 90/50, 80/50, dst.) di file lain. `smScore` **tidak pernah dipanggil di mana pun** — dead code yang jalan tiap bar tanpa hasil. |
| **Risiko ke depan** | Kalau suatu saat developer lain (atau AI assistant) diminta "perbaiki skor Smart Money" dan tidak sadar ada 2 salinan, mereka bisa mengedit `smScore` yang tidak berpengaruh sama sekali ke tampilan — perbaikan terasa "tidak ngefek" padahal sebenarnya mengedit kode yang salah. |
| **Fix** | Hapus `smScore` dari `02-data.pine`, atau beri komentar besar `// DEPRECATED — unused, real logic ada di f_smartMoneyScore() di 03-scoring.pine`. |
| **Effort** | 5 menit. |

---

### BG-26 · 🟡 RENDAH (UX edge case) — Position sizing hilang total (bukan tampil "min. 1 lot") saat hasil floor = 0

| | |
|---|---|
| **Lokasi** | `03-scoring.pine` baris 610–619 |
| **Kode** | ```pine\nsuggestedLots = showPositionSizing and not na(riskAmount) and riskAmount > 0 ? math.floor((riskRp / riskAmount) / 100) : na\n...\nsuggestedLotStr = if hasRisk and showPositionSizing and not na(suggestedLots) and suggestedLots > 0\n    "  |  " + lotLabel + ": " + str.tostring(math.max(1, suggestedLots)) + ...\nelse\n    ""\n``` |
| **Masalah** | Kalau modal/risiko per-trade terlalu kecil dibanding harga saham (mis. saham mahal atau ATR lebar), `suggestedLots` membulatkan ke bawah jadi **0**, dan karena syarat `suggestedLots > 0` gagal, **seluruh info Lot & Rupiah risiko hilang tanpa pesan apa pun** — padahal ada `math.max(1, suggestedLots)` di dalam string yang sebenarnya dirancang untuk kasus ini, tapi tidak pernah tereksekusi karena sudah diblokir duluan oleh syarat `> 0`. Pemula bisa mengira fitur "Position Sizing" tidak aktif/rusak. |
| **Fix** | Ganti syarat jadi `not na(suggestedLots)` saja (tanpa `> 0`), biarkan `math.max(1, suggestedLots)` yang menangani pembulatan minimum, dan tambahkan catatan "(min. 1 lot)" bila hasil asli 0. |
| **Effort** | 5 menit. |

---

### BG-27 · ⚪ COSMETIC — Tabel dideklarasikan 3 kolom, hanya 2 kolom yang pernah diisi

| | |
|---|---|
| **Lokasi** | `04-ui.pine` baris 65: `table.new(tablePos, 3, rowCount, ...)` |
| **Masalah** | Tidak ada satupun `table.cell(tblFull, 2, ...)` di seluruh file — kolom index 2 selalu kosong. Tidak fatal, tapi berpotensi menyisakan jalur kosong/space ekstra di sisi kanan tabel tanpa alasan fungsional. |
| **Fix** | Ganti ke `table.new(tablePos, 2, rowCount, ...)` kecuali memang ada rencana pakai kolom ke-3 (mis. sparkline mini atau ikon) di masa depan — kalau begitu, beri komentar `// kolom 2 reserved untuk fitur X`. |

---

### BG-28 · ⚪ COSMETIC — `max_lines_count` / `max_labels_count` di header, tapi `line.*()`/`label.*()` tak pernah dipakai

| | |
|---|---|
| **Lokasi** | `01-base.pine`, parameter `indicator()` |
| **Fix** | Hapus kalau memang tidak direncanakan dipakai — sama seperti PI-7 di Papan Instrumen. |

---

### BG-29 · ⚪ SANGAT MINOR — `chopRanging` (`>= 62`) vs filter sinyal "Only Ranging" (`> 62`) beda operator

| | |
|---|---|
| **Lokasi** | `02-data.pine` baris 83 (`chopRanging = chopValue >= 62`) vs `03-scoring.pine` baris 448 (`chopValue > 62`) |
| **Dampak** | Nyaris tidak berdampak (butuh `chopValue` persis `62.000...0` yang secara floating-point sangat jarang terjadi), tapi untuk konsistensi kode sebaiknya disamakan operatornya. |

---

## 3. OBSERVASI KOMBINASI (bukan bug, tapi penting untuk pemakaian bersama)

Karena Anda menjalankan keduanya sekaligus (seperti di screenshot), ada beberapa hal yang **secara
teknis benar di masing-masing indikator**, tapi berpotensi disalahpahami saat dilihat berdampingan:

1. **Skala 0–100 di kedua indikator TIDAK berarti sama.**
   Papan Instrumen: 5 tingkat (SANGAT BAIK ≥85 / BAIK ≥70 / CUKUP ≥55 / LEMAH ≥40 / RISIKO TINGGI <40) —
   ini menilai **kualitas fundamental** (valuasi, kesehatan keuangan, dst.).
   Papan Gerak: 3 tingkat (Bullish ≥70 / Netral 40–70 / Bearish <40) — ini menilai **arah momentum teknikal**.
   Angka "70" di kedua dashboard **bukan hal yang sama** — 70 di Papan Instrumen = "kualitas bisnis baik",
   70 di Papan Gerak = "harga sedang bullish". Bisa 70/70 (ideal), tapi bisa juga 85 Fundamental + 25 Teknikal
   (bisnis bagus, harga sedang jelek) — keduanya valid, bukan kontradiksi.

2. **"Volatilitas" tinggi di Papan Gerak ≠ "bullish".**
   Dimensi Volatilitas menilai *kualitas pergerakan* (trending & tidak choppy), bukan arah. Saham yang
   sedang **turun tajam dengan tren rapi** (low choppiness, ATR moderat) bisa mendapat skor Volatilitas
   tinggi meski harga sedang jatuh. Field ini sering disalahartikan pemula sebagai "sinyal beli".

3. **Papan Instrumen sadar-sektor penuh (15 kelas), Papan Gerak nol sadar-sektor.**
   Threshold teknikal (ADX 25, RSI 30/70, ATR 1–3%, dll.) di Papan Gerak sama persis untuk saham bank
   dan saham tambang batubara, padahal karakteristik volatilitasnya sangat berbeda. Ini sudah masuk
   backlog resmi Papan Gerak sendiri (`P1-1: Sektor-aware volatility calibration`) — belum dikerjakan.

4. **Biaya request ganda.** Kedua script menjalankan `request.security`/`request.financial` masing-masing
   secara independen (tidak saling berbagi), jadi kalau nanti Anda menambah indikator ke-3 yang juga berat
   data, perhatikan potensi lambat render karena TradingView menghitung limit per-script, bukan per-chart —
   jadi ini bukan masalah langsung, tapi baik untuk diketahui.

---

## 4. SARAN UI/UX (dengan referensi)

Screenshot Anda menunjukkan tabel Papan Instrumen sangat padat (font "Kecil Sekali", ~26 baris di 2 kolom
sekaligus) — realistis untuk power-user, cukup berat untuk pemula. Prinsip desain dashboard yang relevan:

- **Progressive disclosure** — tampilkan ringkasan dulu, detail atas permintaan. Riset Nielsen Norman Group
  menyebut pola ini bisa memangkas *cognitive load* hingga ~55% dibanding menampilkan semua sekaligus
  ([thedan.design, 2026](https://thedan.design/insights/dashboard-design-principles-best-practices-to-enhance-your-data-analysis/)).
  Papan Instrumen sudah punya `tampilCompact` — **saran**: jadikan mode ini **default ON** untuk pengguna baru
  (mis. deteksi lewat *first load* atau highlight di tooltip), baru pengguna lanjutan mematikannya sendiri.
- **Konsistensi warna hijau=untung/merah=rugi bersifat universal di industri finansial** — jangan
  didekorasi/dibalik meski untuk alasan estetika ([Lollypop Design, 2026](https://lollypop.design/blog/2026/june/trading-app-design/)).
  Ini relevan langsung ke BG-21 di atas — bug warna itu bukan cuma bug logika, tapi juga pelanggaran
  konvensi UX yang oleh riset disebut *"breaks user trust immediately"*.
  Saran tambahan: jangan hanya mengandalkan warna — tambahkan simbol (▲/▼ sudah ada, bagus) supaya tetap
  terbaca oleh ~8% pengguna pria dengan buta warna merah-hijau ([UXPilot, 2026](https://uxpilot.ai/blogs/dashboard-design-principles)).
- **Visual hierarchy F-pattern** — mata pengguna secara alami membaca kiri-atas dulu. Skor keseluruhan &
  narasi 1-baris Papan Gerak sudah ditempatkan di baris atas — bagus, pertahankan pola ini juga saat mode
  Detailed Papan Instrumen diringkas.
- **Saat digabung**, pertimbangkan menyamakan urutan baca: taruh **skor ringkasan** (overall score) kedua
  indikator sejajar secara visual (mis. sama-sama pojok kanan-atas di pane masing-masing seperti sekarang —
  ini sudah benar di screenshot Anda), lalu detail di bawahnya.
- **Legend/keterangan warna** sudah ada di Papan Gerak baris terakhir tabel ("🔴 <40 Bearish | 🟡 40–70
  Netral | 🟢 >70 Bullish") — pola bagus, sebaiknya direplikasi juga di Papan Instrumen (saat ini legend/grade
  hanya implisit dari warna teks, belum ada baris keterangan eksplisit).

---

## 5. SARAN OPTIMASI PERFORMA (dengan referensi)

1. **Cache `math.log(length)` / konstanta per-bar yang tidak berubah** — meski Pine sudah cukup pintar
   meng-inline banyak hal, LuxAlgo merekomendasikan eksplisit memakai `var`/`varip` untuk nilai yang jarang
   berubah agar tidak dihitung ulang tiap bar ([LuxAlgo, 2025 — *"5 Causes of Slow Pine Scripts"*](https://www.luxalgo.com/blog/5-causes-of-slow-pine-scripts-on-tradingview/)).
   `f_choppiness()` di Papan Gerak dipanggil ulang tiap bar dengan `math.log(length)` yang konstan
   selama input tidak berubah — bisa di-precompute sekali di luar fungsi sebagai `var float logLen = math.log(chopLength)`.
2. **Pertahankan pemakaian fungsi bawaan (`ta.highest`, `ta.lowest`, `ta.atr`, dll.) alih-alih loop manual**
   — kedua script sudah melakukan ini dengan baik (tidak ditemukan loop `for` yang menghitung ulang high/low
   manual, kecuali circular buffer histori sinyal Papan Gerak yang memang butuh array — itu wajar).
3. **Gunakan Pine Profiler resmi** (`More → Profiler mode` di Pine Editor) sebelum optimasi lebih lanjut,
   supaya tahu baris mana yang benar-benar mahal, bukan menebak
   ([TradingView Docs — Profiling and Optimization](https://www.tradingview.com/pine-script-docs/writing/profiling-and-optimization/)).
   Ini sangat relevan untuk `04-scoring.pine` Papan Instrumen (~90 baris tabel, banyak `f_wavgArr` dengan
   array literal baru tiap bar) — kandidat kuat untuk profiling sebelum menambah fitur baru.
4. **Awasi limit 40 dynamic request** (lihat PI-6) — dokumentasi resmi migrasi v6 menegaskan batas ini keras
   dan tidak dioptimasi otomatis oleh compiler
   ([TradingView — Migration Guide to v6](https://www.tradingview.com/pine-script-docs/migration-guides/to-pine-version-6/)).
5. **`request.security()` selalu berjalan tiap tick terlepas dari kondisi `if`** — sudah didokumentasikan
   sebagai gotcha umum ([Pineify, 2025](https://pineify.app/resources/blog/tradingview-request-security-complete-guide-to-multi-timeframe-data-analysis)).
   Papan Instrumen sudah benar membungkus render (bukan fetch data) di dalam `if barstate.islast` — tapi
   perhitungan fundamental sendiri (bagian atas modul) tetap jalan tiap bar sebagaimana mestinya karena
   memang dibutuhkan `request.security`/`request.financial` di top-level. Tidak perlu diubah, hanya
   dikonfirmasi bahwa ini sudah pola yang benar.

---

## 6. PENCEGAHAN — Tambahan untuk `CATATAN.md` / "Golden Rule"

Proses yang sudah berjalan (CATATAN.md, CI, test suite) sudah bagus. Tambahan konkret berdasarkan
pola bug yang ditemukan di audit ini:

1. **"No Orphan Weight" checklist** — setiap kali menambah variabel bobot/multiplier baru (pola `wXxx`),
   WAJIB `grep -n "wXxx"` di seluruh file scoring **sebelum** commit, pastikan dipakai minimal di 1 tempat
   selain deklarasinya sendiri. (Ini akan langsung menangkap PI-2 / BG-25 sebelum sampai produksi.)
2. **"Single Source for cross-symbol data"** — setiap kali menulis variabel baru yang melibatkan `close`,
   `open`, `high`, `low`, `volume` di scope global (bukan dalam `request.security(sym, ...)`), tanyakan
   eksplisit: *"apakah ini harus ikut simbol `sym` yang dipilih user, atau memang sengaja ikut chart aktif?"*
   Kalau jawabannya "harus ikut sym", **wajib** dibungkus lewat `request.security(sym, ...)`, jangan
   memakai variabel bar polos. (Ini akan menangkap PI-3.)
3. **Strategy file WAJIB ikut proses `build.sh`, bukan disalin manual** — root cause BG-20/BG-21/BG-23
   semuanya berasal dari `PapanGerakStrategy.pine` yang menyalin ulang logika secara manual dan tidak
   ter-cover CI/lint yang sama dengan `src/modules/`. Rekomendasi jangka menengah: refactor supaya
   `03-scoring.pine` bisa di-`import` atau strategy generation ditambahkan ke `build.sh` sebagai target
   ke-2, supaya drift semacam ini otomatis kedeteksi tiap `npm run ci`.
4. **Visual/warna regression checklist** — untuk setiap `color.rgb(r,g,b)` baru yang berpasangan
   bull/bear, tambahkan baris di `scripts/lint.sh` yang membandingkan pasangan tersebut memang berbeda
   dominan-channel (R dominan utk bear, G dominan utk bull) — akan langsung menangkap tipo transposisi
   digit seperti BG-21.
5. **`display = display.data_window` sebagai default wajib** — tambahkan ke `scripts/lint.sh` Papan
   Instrumen: setiap `input.*()` baru yang TIDAK punya `display=` di baris yang sama harus men-trigger
   warning lint (persis pola yang sudah dipakai Papan Gerak, cukup di-porting).
6. **Tambahkan "Compatibility Test" lintas simbol untuk fitur override simbol** — karena Papan Instrumen
   punya fitur "Simbol Saham" berbeda dari chart aktif, tambahkan 1 skenario test manual di release
   checklist: *"buka chart symbol A, isi Simbol Saham dengan symbol B, screenshot semua field harus
   konsisten mengacu ke B"*. Ini akan menangkap bug seperti PI-3 di masa depan.

---

## 7. ROADMAP PENGEMBANGAN — Saran Prioritas

### Jangka Pendek (1 sprint, prioritas P0/P1 — perbaikan bug di atas)
- [ ] PI-1 — tambah `display=` ke 44 input (Papan Instrumen)
- [ ] BG-20 — fix `adxStrong` undefined (Papan Gerak Strategy) — **wajib sebelum publish ulang**
- [ ] BG-21 — fix warna return negatif
- [ ] PI-2 — aktifkan `wIndonesia` di perhitungan bobot
- [ ] PI-3 — betulkan sumber data Beta vs IDX
- [ ] BG-22 — MTF filter pakai input EMA user, bukan hardcode

### Jangka Menengah (1–2 bulan)
- [ ] BG-24 — opsi "hanya sinyal saat bar close" + update docs risiko repaint
- [ ] BG-23 — selaraskan `PapanGerakStrategy.pine` dengan scoring engine asli, atau beri disclaimer eksplisit
- [ ] P1-1 (backlog lama Papan Gerak) — kalibrasi volatilitas sadar-sektor, supaya konsisten dengan
      pendekatan 15-sektor Papan Instrumen — ini akan sekaligus **menyatukan filosofi kedua indikator**
- [ ] Tambahkan mode "Ringkas untuk Pemula" eksplisit yang menyembunyikan >70% baris detail di kedua
      indikator sekaligus (progressive disclosure, lihat §4)
- [ ] Uji ulang seluruh test suite (`npm run test:all`) dengan lingkungan yang punya akses `npm install
      pinets` — audit ini tidak bisa menjalankannya karena sandbox tanpa akses jaringan; sebelum bug-bug
      di atas dianggap "selesai", jalankan dulu 96+90 test yang sudah ada + tambahkan test baru untuk
      PI-2/PI-3/BG-20/BG-21/BG-22.

### Jangka Panjang (backlog existing + tambahan dari audit ini)
- [ ] Multi-timeframe alignment score (sudah di backlog Papan Gerak: `P1-2`)
- [ ] Divergence detection RSI/MACD otomatis (sudah di backlog: `P2-2`)
- [ ] CAR/NPL/LDR otomatis untuk bank (masih manual input — `P3-1` lama Papan Instrumen), begitu TradingView
      menyediakan field-nya lewat `request.financial`
- [ ] Framework backtest terpadu (satu sumber logic untuk indikator + strategy, lih. §6 poin 3) supaya
      BG-23-class bug tidak berulang di fitur berikutnya
- [ ] Pertimbangkan **unifikasi skala skor** lintas kedua indikator (§3 poin 1) — bukan mengubah salah satu,
      cukup tambahkan badge/label eksplisit "Skor Fundamental" vs "Skor Teknikal" di kedua tabel supaya
      user baru tidak keliru membandingkan angka yang beda makna secara langsung.

---

## Lampiran — Ringkasan Tabel Semua Temuan

| ID | Proyek | Severity | Judul Singkat | File |
|----|--------|----------|---------------|------|
| PI-1 | Papan Instrumen | 🔴 Kritis (visible) | 44 input tanpa `display=` → legend penuh | 01-base.pine |
| PI-2 | Papan Instrumen | 🟠 Tinggi (hidden) | `wIndonesia` dihitung, tak dipakai | 04-scoring.pine |
| PI-3 | Papan Instrumen | 🟠 Tinggi (hidden) | Beta pakai `close` chart, bukan `dClose` sym | 02-data.pine |
| PI-4 | Papan Instrumen | 🟡 Rendah | Komentar vs implementasi IDR Trend tak sinkron | 04-scoring.pine |
| PI-5 | Papan Instrumen | 🟡 Rendah (UX) | Score card tetap render saat NO DATA | 04-scoring.pine |
| PI-6 | Papan Instrumen | 🔵 Info | 35/40 request budget terpakai | 02-data.pine |
| PI-7 | Papan Instrumen | ⚪ Cosmetic | `max_labels_count` tak terpakai | 01-base.pine |
| BG-20 | Papan Gerak | 🔴 Kritis (compile) | `adxStrong` undefined di Strategy | PapanGerakStrategy.pine |
| BG-21 | Papan Gerak | 🟠 Sedang (visible) | Return negatif warna hijau | PapanGerakStrategy.pine |
| BG-22 | Papan Gerak | 🟠 Sedang (hidden) | MTF EMA hardcode, bukan input user | 02-data.pine |
| BG-23 | Papan Gerak | 🟠 Sedang (drift) | Strategy scoring beda dari indikator asli | PapanGerakStrategy.pine |
| BG-24 | Papan Gerak | 🟡 Sedang (risiko) | Sinyal/alert tanpa gerbang bar-close | 03-scoring.pine, 04-ui.pine |
| BG-25 | Papan Gerak | 🟡 Rendah (dead code) | `smScore` dihitung, tak terpakai | 02-data.pine |
| BG-26 | Papan Gerak | 🟡 Rendah (UX) | Position sizing hilang total saat 0 lot | 03-scoring.pine |
| BG-27 | Papan Gerak | ⚪ Cosmetic | Kolom ke-3 tabel selalu kosong | 04-ui.pine |
| BG-28 | Papan Gerak | ⚪ Cosmetic | `max_lines/labels_count` tak terpakai | 01-base.pine |
| BG-29 | Papan Gerak | ⚪ Sangat minor | `>=62` vs `>62` beda operator | 02-data.pine, 03-scoring.pine |

**Total: 17 temuan baru** (2 kritis, 6 tinggi/sedang dengan dampak nyata, sisanya rendah/cosmetic/info).
Tidak ada temuan yang mengindikasikan manipulasi data atau kebocoran informasi — seluruhnya murni bug
logika/konfigurasi/UX khas pengembangan indikator kompleks.

---

## 8. RE-CHECK — Verifikasi Revisi Kedua

Metodologi verifikasi: `diff -rq` rekursif seluruh repo lama vs baru → `diff -u` per file yang
berubah → baca manual tiap potongan kode yang diubah → `bash build.sh` ulang di kedua proyek →
`diff` hasil build terhadap file `.pine` yang di-ship di zip baru (hasil: **identik**, build
pipeline tetap terpercaya). Tidak bisa menjalankan `npm run test:all` (masih tanpa akses jaringan
di sandbox ini) — verifikasi di bawah murni pembacaan kode, **bukan** hasil run test otomatis.

### Status per Temuan

| ID | Status | Bukti |
|----|--------|-------|
| PI-1 | ✅ **FIXED** | Ke-44 `input.*()` di `01-base.pine` sekarang punya `display = display.data_window` (diverifikasi dengan parser Python, termasuk yang multi-baris — 0 sisa). |
| PI-2 | ✅ **FIXED** | `effectiveBobotIndonesia = bobotIndonesia * wIndonesia` ditambahkan, dan dipakai di `f_wavg7(...)` menggantikan `bobotIndonesia` mentah. |
| PI-3 | ✅ **FIXED** | `stockDailyRet` sekarang `dClose / nz(dClose[1]) - 1` (ikut simbol `sym` via `request.security`), bukan `close` chart aktif lagi. |
| PI-4 | ✅ **FIXED** | Komentar diubah jadi `"lain: IDR menguat = skor tinggi (f_scoreLower, good=-5)"` — sekarang deskripsi cocok dengan perilaku kode (bukan lagi klaim "stabil = netral" yang salah). |
| PI-5 | ✅ **FIXED** | 6 baris `f_scoreCardN(...)` sekarang di-indent ke dalam blok `if not noData`, tidak lagi render tanpa syarat. |
| PI-6 | 🟡 **SEBAGIAN** | `scripts/lint.sh` sekarang mencetak `⚠️ WARNING` otomatis saat request ≥36/40 — ini soft-warning, bukan hard-gate CI seperti saran awal saya (`err` yang menggagalkan build), tapi sudah jauh lebih baik daripada tanpa peringatan sama sekali. Budget masih di angka yang sama (35 request) karena tidak ada field baru ditambah. |
| PI-7 | ✅ **FIXED** | `max_labels_count = 50` dihapus dari `indicator()`. |
| BG-20 | ✅ **FIXED** | `adxStrong = adxValue >= adxThreshold` ditambahkan sebelum dipakai — **file strategy sekarang seharusnya bisa compile.** Ini yang paling penting karena satu-satunya bug yang benar-benar blocking. |
| BG-21 | ✅ **FIXED** | Warna return negatif diperbaiki jadi `color.rgb(239, 83, 80)` (merah), sudah konsisten dengan `bearColor` di tempat lain. |
| BG-22 | ✅ **FIXED** | `mtfTrendScore` sekarang memakai `emaSlowPeriod`/`emaMidPeriod`/`emaFastPeriod` (input user), bukan `200/50/20` hardcode. |
| BG-23 | ✅ **DIATASI (dokumentasi)** | Disclaimer eksplisit 8 baris ditambahkan di header `PapanGerakStrategy.pine` menjelaskan strategy adalah APROKSIMASI, bukan replika 1:1 — sesuai opsi mitigasi yang saya sarankan. (Rumus scoring-nya sendiri masih disederhanakan/berbeda — itu memang pilihan desain yang sekarang sudah jujur didokumentasikan, bukan lagi "silent gap".) |
| BG-24 | ✅ **FIXED (lebih baik dari saran)** | Input baru `confirmOnBarClose` (default **ON**) ditambahkan, dan **ketujuh** `alert()` (bukan cuma alert entry) sekarang digerbang dengan `and (not confirmOnBarClose or barstate.isconfirmed)`. `docs/PANDUAN-TRADING.md` juga dapat tambahan poin disclaimer risiko repaint. Lihat catatan nuansa di bawah. |
| BG-25 | 🟡 **SEBAGIAN** | `smScore` di `02-data.pine` diberi komentar `// DEPRECATED — unused...` — sudah didokumentasikan supaya tidak membingungkan, tapi variabelnya **belum dihapus**, masih dihitung tiap bar tanpa efek. Cukup untuk mencegah kebingungan developer selanjutnya, tapi masih ada baris kode mati secara teknis. |
| BG-26 | ✅ **FIXED** | Syarat `suggestedLots > 0` dihapus dari kondisi tampil; sekarang saat `suggestedLots < 1`, teks `" (min. 1 lot)"` ditambahkan otomatis alih-alih menghilang total. |
| BG-27 | ✅ **FIXED** | `table.new(tablePos, 3, ...)` → `table.new(tablePos, 2, ...)`. Diverifikasi tidak ada lagi rujukan ke kolom index 2 di file. |
| BG-28 | ✅ **FIXED** | `max_labels_count`/`max_lines_count` dihapus dari `indicator()`. |
| BG-29 | ✅ **FIXED** | Operator filter "Only Ranging" diubah dari `chopValue > 62` menjadi `chopValue >= 62`, sekarang konsisten dengan `chopRanging` di `02-data.pine`. |

**Ringkasan: 15 FIXED penuh, 2 diatasi sebagian (PI-6, BG-25) — keduanya memang saya tandai
sebagai info/rendah sejak awal, bukan bug fungsional, jadi status "sebagian" ini masih sangat
baik.** Tidak ditemukan regresi (fitur yang tadinya benar jadi rusak akibat revisi).

### Catatan Nuansa — BG-24 (perlu diketahui, bukan bug baru)

`confirmOnBarClose` hanya menggerbang pemanggilan `alert()` di `04-ui.pine`. Variabel status
internal (`entryTriggered`, `lastSignalBar`, `signalEntryPrice`, dan buffer histori sinyal
`btEntryBars` di `03-scoring.pine`) **tidak** ikut digerbang — itu tetap update real-time setiap
bar seperti dashboard pada umumnya (memang wajar untuk tabel yang harus tetap "hidup" mengikuti
harga berjalan). Konsekuensinya: kalau ada sinyal yang sempat muncul intrabar lalu berbalik
sebelum candle tutup, sinyal itu **tidak akan mengirim alert** (sudah benar, terlindungi), tapi
**tetap tercatat** di statistik "Histori Sinyal (kumulatif)" dan bisa sempat menampilkan "Level
Referensi" di tabel sesaat sebelum hilang lagi. Ini bukan regresi — cakupan fix memang secara
wajar dibatasi ke alert (yang paling berisiko, karena bisa memicu eksekusi order otomatis via
webhook), bukan ke tampilan visual. Kalau ingin win-rate histori 100% konsisten dengan apa yang
sungguh-sungguh dikirim sebagai alert, `if entryTriggered` di §12/§13 `03-scoring.pine` juga bisa
ditambah gerbang `and (not confirmOnBarClose or barstate.isconfirmed)` yang sama — opsional,
prioritas rendah, silakan tambahkan ke backlog kalau dirasa perlu.

### Temuan Baru Kecil dari Proses Revisi Ini

| ID | Severity | Lokasi | Temuan |
|----|----------|--------|--------|
| BG-30 | ⚪ Sangat minor (dokumentasi) | `papan-gerak-main/docs/TV_PUBLISH_DESC.md` | Heading `## Judul` sekarang muncul **dua kali berturut-turut** (baris kosong di antaranya) — sepertinya artefak saat menyisipkan blok changelog baru "v0.2.1-alpha Update" di atas konten lama. Tidak berpengaruh ke script `.pine` sama sekali (murni file dokumentasi publikasi TradingView), tapi sebaiknya salah satu `## Judul` dihapus supaya deskripsi publikasi rapi. |

### Yang Masih Perlu Dilakukan Sebelum Publish Ulang

1. **Compile-test manual di Pine Editor** untuk kedua indikator + strategy — terutama
   `PapanGerakStrategy.pine` (fix `adxStrong`) — audit ini membaca kode dengan teliti tapi tidak
   punya akses compiler Pine Script sungguhan di sandbox ini, jadi verifikasi akhir tetap perlu
   dilakukan langsung di TradingView.
2. **Update `CATATAN.md`, `CHANGELOG.md` (Papan Gerak), dan bump versi di `package.json`** —
   dicek: **belum ada satupun yang diperbarui** untuk mencatat ke-15 fix di atas. Ini bertentangan
   dengan "Golden Rule" & "No Silent Changes" yang sudah Anda tulis sendiri di kedua `CATATAN.md`.
   Rekomendasi: tulis 1 baris changelog per fix (ID bug + fix singkat) sebelum tag rilis
   berikutnya, plus bump `0.3.0-beta` → mis. `0.3.1-beta` (Papan Instrumen) dan `0.2.0-alpha` →
   `0.2.1-alpha` (Papan Gerak, meski `docs/TV_PUBLISH_DESC.md` sudah menyebut versi ini duluan —
   sinkronkan `package.json` supaya tidak berbeda dari yang diklaim di deskripsi publikasi).
3. **Jalankan ulang test suite** (`npm run test:all`, butuh `npm install` dengan akses jaringan)
   di lingkungan yang punya akses internet — bug PI-2/PI-3/BG-20/BG-21/BG-22 semuanya cukup
   fundamental untuk pantas mendapat regression test baru, bukan cuma dianggap selesai dari
   pembacaan kode saja.
4. (Opsional, prioritas rendah) Hapus baris `smScore` yang sudah ditandai deprecated (BG-25) dan
   rapikan duplikasi `## Judul` (BG-30) saat sempat.
