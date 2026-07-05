# TESTING.md

---

Document ID   : DOC-013
Document Name : TESTING
Version       : 1.0.0
Status        : Active
Owner         : Muhammad Akhmal
Architect     : ChatGPT
Last Updated  : 2026-07
Review Cycle  : Every Build

---

# Purpose

Dokumen ini mendefinisikan standar pengujian untuk seluruh proyek.

Tujuannya memastikan setiap Build memiliki kualitas yang konsisten sebelum dirilis.

Seluruh fitur baru maupun perubahan kode wajib melewati proses pengujian sesuai standar yang ditetapkan.

---

# Testing Philosophy

Testing bukan bertujuan membuktikan bahwa kode benar.

Testing bertujuan mencari kemungkinan bahwa kode salah.

Semakin banyak skenario yang diuji, semakin tinggi tingkat kepercayaan terhadap Build.

---

# Testing Levels

## Level 1 — Compile Test

Objective

Memastikan Pine Script berhasil dikompilasi.

Checklist

☐ No compile error

☐ No syntax error

☐ No type error

☐ No warning penting

Status

Mandatory

---

## Level 2 — Functional Test

Objective

Memastikan seluruh fitur berjalan sesuai desain.

Checklist

☐ Dashboard tampil

☐ Seluruh skor muncul

☐ Label benar

☐ Warna benar

☐ Tooltip benar

☐ Tidak ada nilai aneh

Status

Mandatory

---

## Level 3 — Data Validation

Objective

Memastikan data fundamental yang digunakan sesuai.

Checklist

☐ request.financial() mengembalikan nilai valid

☐ Penanganan NA berjalan

☐ Tidak terjadi divide by zero

☐ Rasio sesuai perhitungan

Status

Mandatory

---

## Level 4 — Sector Validation

Objective

Memastikan klasifikasi sektor berjalan benar.

Checklist

☐ Bank

☐ Asuransi

☐ Sekuritas

☐ Property

☐ Infrastruktur

☐ Teknologi

☐ Consumer

☐ Mining

☐ Energy

☐ Healthcare

☐ Transportation

☐ Industrial

☐ Others

Status

Mandatory

---

## Level 5 — Regression Test

Objective

Memastikan perubahan baru tidak merusak fitur lama.

Checklist

☐ Dashboard tetap tampil

☐ Skor lama tidak berubah tanpa alasan

☐ Tidak ada perubahan warna

☐ Tidak ada layout rusak

☐ Tidak ada fitur hilang

Status

Mandatory

---

## Level 6 — Performance Test

Objective

Mengukur dampak perubahan terhadap performa.

Checklist

☐ Tidak ada request.financial() yang tidak perlu

☐ Tidak ada kalkulasi berulang

☐ Tidak ada variabel mati

☐ Render tetap ringan

Status

Mandatory

---

# Manual Test Matrix

Setiap Build minimal diuji pada emiten dari berbagai sektor IDX.

| Sector | Example | Build 001 | Build 002 | Build 003 | Build 004 | Build 005 | Build 006 |
|---------|---------|-----------|-----------|-----------|-----------|-----------|-----------|
| Bank | BBCA | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Insurance | AMAG | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Securities | TRIM | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Consumer | ICBP | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Mining | ADRO | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Energy | MEDC | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Property | CTRA | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Infrastructure | JSMR | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Technology | GOTO | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Healthcare | KLBF | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Transportation | ASSA | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Industrial | ASII | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

Catatan:
Daftar ticker dapat diperbarui sesuai perkembangan klasifikasi sektor.

---

# Bug Classification

## Critical

- Compile gagal
- Dashboard tidak muncul
- Error perhitungan utama

Harus diperbaiki sebelum release.

---

## Major

- Skor salah
- Sektor salah
- Layout rusak

Harus diperbaiki sebelum merge.

---

## Minor

- Tooltip
- Warna
- Alignment
- Typo

Boleh ditunda jika tidak memengaruhi fungsi utama.

---

# Build Acceptance Checklist

Sebelum Build selesai:

☐ Compile berhasil

☐ Functional Test lulus

☐ Data Validation lulus

☐ Sector Validation lulus

☐ Regression Test lulus

☐ Performance Test lulus

☐ CHANGELOG diperbarui

☐ CURRENT_SPRINT diperbarui

☐ Commit dibuat

☐ Product Owner menyetujui

---

# Future Testing

Versi berikutnya dapat menambahkan:

- Benchmark Test
- Automated Screenshot Comparison
- Performance Benchmark
- Historical Dataset Validation

Apabila Pine Script mendukung otomatisasi yang lebih baik, metode pengujian akan diperluas.

---

# Closing Statement

Testing merupakan bagian dari proses pengembangan, bukan tahap terakhir.

Kualitas produk dibangun sejak implementasi pertama, bukan diperiksa setelah selesai.
