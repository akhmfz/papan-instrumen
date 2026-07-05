# Panduan Pengguna — Papan Instrumen

> Dashboard Fundamental Saham Indonesia di TradingView

---

## Apa itu Papan Instrumen?

Papan Instrumen adalah **dashboard analisis fundamental** untuk saham Bursa Efek Indonesia (IDX). Dijalankan langsung di chart TradingView — tidak perlu buka aplikasi lain.

Dashboard ini **bukan**:
- ❌ Rekomendasi beli / jual
- ❌ Sinyal trading otomatis
- ❌ Alat prediksi harga

Dashboard ini **adalah**:
- ✅ Alat bantu evaluasi fundamental cepat
- ✅ Skor yang mudah dipahami (0-100)
- ✅ Analisis yang disesuaikan per sektor bisnis
- ✅ Transparan: semua metodologi terbuka

---

## Cara Install

1. Buka [TradingView](https://tradingview.com) → **Pine Editor** (tab bawah)
2. Buka [src/PapanInstrumen.pine](https://github.com/akhmfz/papan-instrumen/blob/main/src/PapanInstrumen.pine)
3. Copy seluruh kode → Paste ke Pine Editor
4. Klik **"Add to Chart"**

Atau: import langsung via Pine Editor:
```
https://github.com/akhmfz/papan-instrumen/blob/main/src/PapanInstrumen.pine
```

**Syarat:** Timeframe **Daily** (D / 1D) — IDX hanya menyediakan data fundamental di Daily.

---

## 7 Dimensi Scoring

Setiap dimensi menghasilkan skor **0-100**:

| # | Dimensi | Arti | Skor Tinggi Artinya |
|---|---------|------|---------------------|
| 1 | **Value** | Apakah harga murah dibanding fundamental? | Murah / Undervalued |
| 2 | **Quality** | Apakah bisnisnya menguntungkan? | Profitabilitas tinggi |
| 3 | **Growth** | Apakah pendapatan & laba tumbuh? | Pertumbuhan kuat |
| 4 | **Health** | Apakah keuangannya sehat? | Tidak banyak utang berbahaya |
| 5 | **Income** | Apakah memberi dividen? | Dividen menarik |
| 6 | **Momentum** | Bagaimana pergerakan harga? | Trend positif |
| 7 | **Indonesia** | Bagaimana posisi di pasar IDX? | Likuid + stabil |

### Skor Keseluruhan

Skor 0-100 gabungan dari dimensi yang aktif:

| Skor | Grade | Arti |
|------|-------|------|
| 85-100 | SANGAT BAIK | Fundamental kuat di semua aspek |
| 70-85 | BAIK | Secara umum sehat |
| 55-70 | CUKUP | Ada kekuatan, ada kelemahan |
| 40-55 | LEMAH | Perlu perhatian lebih |
| < 40 | RISIKO TINGGI | Banyak indikator fundamental lemah |

> ⚠️ **Peringatan:** Skor tinggi ≠ jaminan untung. Selalu lakukan riset mandiri.

---

## Cara Membaca Dashboard

### Layout

Dashboard dibagi dua kolom:
- **Kiri:** Ringkasan, Skor, Valuasi, Dividen
- **Kanan:** Kualitas, Pertumbuhan, Kesehatan, Momentum, Indonesia, Risiko

### Arti Warna

| Warna | Arti |
|-------|------|
| 🟢 Hijau | Baik (skor ≥ 80) |
| 🟣 Ungu | Sedang-ke-baik (60-79) |
| 🟡 Emas | Cukup (40-59) |
| 🔴 Merah | Risiko (< 40) |

### Indikator Kelengkapan (n/x)

Contoh: `(7/9)` di samping Quality berarti **7 dari 9 rasio** memiliki data.

Semakin rendah n/x, semakin kurang akurat skor. Data fundamental IDX tidak selalu lengkap untuk semua emiten.

---

## Pengaturan Penting

### 1. Deteksi Sektor

**Paling penting.** Dashboard menyesuaikan cara menilai berdasarkan jenis bisnis:

| Setting | Rekomendasi untuk |
|---------|-------------------|
| **Otomatis** | Umum (deteksi otomatis) |
| Bank / Asuransi / Sekuritas | Saham finansial |
| Konsumer (Makanan/Minuman) | ICBP, UNVR, MYOR, INDF, dll |
| Industri (Manufaktur) | ASII, SMGR, WTON, dll |
| Kesehatan (Farmasi) | KLBF, SIDO, HEAL, dll |
| Batubara | ADRO, PTBA, ITMG, dll |
| CPO & Perkebunan | AALI, LSIP, SIMP, dll |
| Properti / Infrastruktur | CTRA, BSDE, JSMR, TLKM, dll |
| Teknologi | GOTO, BUKA, EMTK, dll |
| Transportasi | ASSA, BIRD, GIAA, dll |
| Siklikal (Komoditas/Energi) | MEDC, PGAS, ANTM, dll |

**Override manual jika auto-detect salah!**

### 2. Faktor Indonesia

Toggle **"Aktifkan Faktor Indonesia"** — default OFF (backward compatible).

Saat ON: menambahkan dimensi ke-7 yang menilai:
- **Likuiditas** (volume, kapitalisasi pasar)
- **Stabilitas** (beta vs IHSG, volatilitas)
- **Dukungan Makro** (stabilitas IDR)

Skor Indonesia cenderung lebih rendah untuk saham gorengan, lebih tinggi untuk saham blue chip likuid.

### 3. Bobot Kustom

Di **"Bobot Skor Keseluruhan"** → centang "Gunakan Bobot Kustom" lalu atur bobot per dimensi.

**Contoh preset:**
- **Value-biased:** Value 2.0, lainnya 1.0 → lebih menekankan valuasi
- **Growth-biased:** Growth 2.0, lainnya 1.0 → lebih menekankan pertumbuhan
- **Conservative:** Health 1.5, Quality 1.5, lainnya 1.0 → lebih aman

### 4. Tema Warna

5 pilihan: Gelap (default), Terang, Bursa Hijau, Biru Nusantara, Emas Premium.

### 5. Tampilan

Toggle ON/OFF per dimensi scoring untuk menyembunyikan/menampilkan.
Ukuran teks: Kecil Sekali (mobile-friendly), Kecil, Normal.

---

## Modul Risiko Likuiditas

Terpisah dari skor fundamental — **tidak dicampur ke skor utama.**

Menilai risiko saham:
- **Market cap** kecil
- **Nilai transaksi harian** rendah
- **Volatilitas** ekstrem
- **Frekuensi kena batas ARA/ARB**
- **Harga recehan** (< Rp 50)

Skor **semakin tinggi = semakin aman** dari risiko gorengan.

> ⚠️ Ini adalah proxy statistik harga & volume, **bukan** deteksi manipulasi terverifikasi.

---

## Tips

### Emiten Baru IPO
Data fundamental mungkin belum tersedia. Dashboard akan menampilkan: `⚠ DATA TIDAK TERSEDIA`.

### Sektor Salah Deteksi
Auto-detect tidak selalu akurat — override manual lewat Settings → Sektor.

### Skor Tidak Berubah
Data fundamental TradingView update per kuartal, bukan real-time. Skor berubah hanya setelah laporan keuangan baru terbit.

### Backward Compatibility
Faktor Indonesia default OFF — pengaturan lama tetap berfungsi.

---

## FAQ

**Q: Kenapa skor Bank berbeda dari Consumer?**
A: Dashboard sudah **sector-aware**. Bank dinilai dari ROE/PBV, Consumer dari margin + profitabilitas. Bobot dan threshold berbeda per sektor.

**Q: Kenapa skor Momentum rendah walau harga naik?**
A: Momentum menilai: RSI (tidak overbought), posisi vs 52W, relative strength vs IHSG, volatilitas, dan MA status — bukan hanya harga naik.

**Q: Apakah ini bisa dipakai untuk saham luar negeri?**
A: Dirancang khusus untuk IDX. Metodologi bisa berbeda untuk pasar lain.

**Q: Ada versi bahasa Inggris?**
A: Belum tersedia — masuk roadmap versi berikutnya.

---

## Disclaimer

Papan Instrumen adalah **alat bantu analisis, bukan nasihat keuangan/investasi.**

Seluruh keputusan investasi tetap menjadi tanggung jawab masing-masing pengguna. Kode bersifat open-source (MIT License) — tidak ada jaminan akurasi 100% karena data bergantung pada TradingView.

---

## Author

**Muhammad Akhmal** — AKHMFZ Analytics, Indonesia
- [TradingView: @akhmfz](https://www.tradingview.com/u/akhmfz/)
- [GitHub: akhmfz/papan-instrumen](https://github.com/akhmfz/papan-instrumen)
