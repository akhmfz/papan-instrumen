# METHODOLOGY.md
---
Document ID   : DOC-004
Document Name : METHODOLOGY
Version       : 1.0.0
Status        : Active
Owner         : Muhammad Akhmal
Architect     : ChatGPT
Last Updated  : 2026
Review Cycle  : Every Major Release
---
# Purpose
Dokumen ini mendefinisikan metodologi analisis fundamental yang digunakan pada proyek **Saham: Papan Instrumen By. Akhmfz**.
Seluruh proses penilaian perusahaan harus mengacu pada metodologi dalam dokumen ini.
Implementasi kode tidak boleh mengubah metodologi.
Apabila metodologi berubah, dokumen ini harus diperbarui terlebih dahulu sebelum implementasi dilakukan.
---
# Design Philosophy
Dashboard ini **bukan stock screener**.
Dashboard ini **bukan signal generator**.
Dashboard ini **bukan sistem rekomendasi beli atau jual**.
Dashboard ini merupakan alat bantu analisis fundamental yang menyajikan data, konteks, dan interpretasi agar pengguna dapat mengambil keputusan investasi secara mandiri.
---
# Core Principles
Seluruh metodologi mengikuti prinsip berikut.
## Indonesia First
Metodologi harus mempertimbangkan karakteristik Bursa Efek Indonesia (IDX).
Parameter yang relevan di pasar Amerika belum tentu relevan di Indonesia.
---
## Sector Aware
Tidak semua rasio berlaku sama pada seluruh sektor.
Contoh:
- DER penting untuk Consumer.
- DER kurang relevan pada Bank.
- PBV lebih relevan dibanding PER pada Bank.
Interpretasi harus mempertimbangkan karakteristik bisnis.
---
## Context Before Score
Skor tidak boleh diberikan tanpa konteks.
Contoh:
DER = 2.5
Tidak otomatis buruk.
Interpretasi harus mempertimbangkan:
- sektor
- model bisnis
- karakter industri
---
## Simplicity
Semua hasil harus mudah dipahami.
Hindari istilah teknis yang tidak diperlukan.
---
## Transparency
Seluruh metode penilaian harus terdokumentasi.
Tidak boleh ada "black box scoring".
---
# Analysis Framework
Dashboard dibangun menggunakan lima pilar utama.
---
## 1. Valuation
Menilai apakah harga pasar relatif murah, wajar, atau mahal.
Contoh rasio:
- PER
- PBV
- EV/EBITDA (Future)
- PEG (Future)
---
## 2. Profitability
Mengukur kemampuan perusahaan menghasilkan laba.
Contoh:
- ROE
- ROA
- Net Margin
- Operating Margin
---
## 3. Growth
Mengukur kemampuan perusahaan bertumbuh.
Contoh:
- Revenue Growth
- EPS Growth
- Net Income Growth
---
## 4. Financial Health
Mengukur kesehatan keuangan perusahaan.
Contoh:
- Current Ratio
- DER
- Interest Coverage (Future)
---
## 5. Shareholder Return
Mengukur manfaat yang diterima pemegang saham.
Contoh:
- Dividend Yield
- Dividend Payout Ratio
- Buyback (Future)
---
# Sector Methodology
Setiap sektor memiliki karakteristik yang berbeda.
Oleh karena itu, interpretasi indikator harus menyesuaikan sektor perusahaan.
Contoh:
Bank
Fokus:
- PBV
- ROE
- NPL (Future)
- CAR (Future)
DER tidak menjadi indikator utama.
---
Property
Fokus:
- DER
- Cash Flow
- Book Value
---
Technology
Fokus:
- Revenue Growth
- Gross Margin
- Cash Position
Profit belum tentu menjadi indikator utama.
---
Mining
Fokus:
- Cash Flow
- Dividend
- Commodity Cycle
---
Infrastructure
Fokus:
- Cash Flow
- Debt Structure
- Long-term Assets
---
# Scoring Philosophy
Dashboard menggunakan sistem skor untuk menyederhanakan interpretasi.
Namun skor bukan tujuan utama.
Skor hanyalah representasi visual dari kondisi fundamental.
Pengguna tetap dianjurkan memahami data di balik skor tersebut.
---
# Interpretation Philosophy
Setiap skor harus memiliki alasan.
Contoh:
★★★★★
↓
ROE tinggi.
PBV masih wajar
Pertumbuhan EPS stabil.
DER sesuai karakter sektor.
Interpretasi tidak boleh hanya berupa:
★★★★★
Bagus.
---
# Limitations
Dashboard memiliki beberapa keterbatasan.
- Bergantung pada data TradingView.
- Tidak seluruh metrik tersedia untuk semua emiten.
- Tidak menggantikan analisis laporan keuangan.
- Tidak memperhitungkan faktor makroekonomi secara langsung.
---
# Future Methodology
Versi mendatang dapat menambahkan metodologi baru.
Contoh:
- Quality Score
- Economic Moat
- ESG
- Ownership Analysis
- Capital Allocation
- Earnings Quality
Seluruh penambahan harus tetap mengikuti filosofi proyek.
---
# Closing Statement
Metodologi merupakan fondasi utama proyek.
Kode dapat berubah.
Tampilan dapat berubah.
Namun metodologi harus tetap konsisten, transparan, dan terdokumentasi.
