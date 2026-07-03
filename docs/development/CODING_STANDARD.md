# CODING_STANDARD.md

---

Document ID   : DOC-012
Document Name : CODING_STANDARD
Version       : 1.0.0
Status        : Active
Owner         : Muhammad Akhmal
Architect     : ChatGPT
Last Updated  : 2026
Review Cycle  : Every Major Release

---

# Purpose

Dokumen ini mendefinisikan standar penulisan kode untuk seluruh proyek.

Tujuannya adalah menjaga konsistensi, keterbacaan, performa, dan kemudahan pemeliharaan kode Pine Script.

Seluruh kontributor wajib mengikuti standar ini.

---

# General Principles

Kode harus:

- Mudah dibaca.
- Mudah dipelihara.
- Konsisten.
- Modular.
- Efisien.

Kode bukan hanya ditulis untuk komputer.

Kode ditulis agar manusia dapat memahaminya.

---

# Pine Script Version

Standar menggunakan:

Pine Script Version 6

Seluruh implementasi harus kompatibel dengan versi tersebut.

---

# Naming Convention

## Variables

Gunakan camelCase.

Contoh:

```
currentRatio
dividendYield
sectorWeight
```

---

## Constants

Gunakan UPPER_SNAKE_CASE.

```
MAX_SCORE
DEFAULT_COLOR
```

---

## Functions

Gunakan camelCase dengan awalan kata kerja.

```
calculateScore()
getSector()
drawPanel()
```

---

## Boolean

Selalu diawali:

```
is
has
can
should
```

Contoh:

```
isBankSector
hasDividend
canRender
shouldUpdate
```

---

# File Structure

Urutan penulisan kode.

1. Header
2. Indicator Declaration
3. Inputs
4. Constants
5. Colors
6. Utility Functions
7. Financial Functions
8. Sector Functions
9. Score Calculation
10. Dashboard Rendering
11. Debug Section

---

# Comment Standard

Gunakan komentar hanya jika memberikan nilai tambah.

Hindari komentar seperti:

```
x = 5 // set x menjadi 5
```

Gunakan:

```
//
// Financial Health Calculation
//
```

atau

```
// Return ROE score using sector-specific thresholds.
```

---

# Function Rules

Setiap function harus:

- Memiliki satu tanggung jawab.
- Menghasilkan output yang konsisten.
- Tidak memiliki efek samping yang tidak diperlukan.

Hindari function yang terlalu panjang.

Target maksimum:

30–50 baris.

---

# Performance Guidelines

Prioritaskan efisiensi.

### Hindari

- Perhitungan berulang.
- request.financial() yang tidak diperlukan.
- Variabel sementara yang tidak dipakai.

### Gunakan

- Cache hasil perhitungan.
- Reuse variabel.
- Conditional calculation bila memungkinkan.

---

# Dashboard Rules

Dashboard harus:

- Konsisten.
- Ringkas.
- Mudah dibaca.
- Tidak menampilkan informasi berlebihan.

---

# Error Handling

Selalu pertimbangkan:

- na
- Divide by zero
- Missing financial data
- Empty string
- Invalid sector

---

# Refactoring Rules

Refactoring tidak boleh:

- Mengubah metodologi.
- Mengubah skor.
- Mengubah perilaku indikator.

Kecuali telah disetujui Product Owner.

---

# Documentation Rules

Perubahan kode yang signifikan wajib memperbarui:

- CHANGELOG.md
- CURRENT_SPRINT.md
- BACKLOG.md (jika diperlukan)

---

# Commit Standard

Setiap commit harus:

- Fokus pada satu perubahan logis.
- Memiliki pesan yang jelas.
- Dapat di-review secara independen.

Contoh:

```
feat(sector): add insurance classification
```

```
fix(valuation): restore financial fallback
```

```
docs(methodology): update valuation framework
```

---

# Code Review Checklist

Sebelum merge, pastikan:

☐ Tidak ada compile error.

☐ Tidak ada warning penting.

☐ Naming sesuai standar.

☐ Tidak ada kode mati (dead code).

☐ Tidak ada variabel tidak terpakai.

☐ Dokumentasi diperbarui.

☐ CHANGELOG diperbarui.

☐ Manual test dilakukan.

---

# Anti-Patterns

Hindari:

- Magic Number
- Hardcoded Text
- Duplicate Logic
- Nested if berlebihan
- Function terlalu panjang
- Silent Changes

---

# Definition of Good Code

Kode dianggap baik apabila:

- Benar.
- Jelas.
- Efisien.
- Dapat diuji.
- Mudah dipelihara.

---

# Closing Statement

Standar ini dibuat untuk menjaga kualitas proyek dalam jangka panjang.

Apabila terdapat konflik antara kecepatan implementasi dan kualitas kode, maka kualitas kode menjadi prioritas.
