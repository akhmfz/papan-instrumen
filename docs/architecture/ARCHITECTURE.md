# ARCHITECTURE.md
---
Document ID   : DOC-003
Document Name : ARCHITECTURE
Version       : 1.0.0
Status        : Active
Owner         : Muhammad Akhmal
Architect     : ChatGPT
Last Updated  : 2026
Review Cycle  : Every Major Release
---
# Purpose
Dokumen ini menjelaskan arsitektur teknis proyek **Saham: Papan Instrumen By. Akhmfz**.
Seluruh implementasi Pine Script harus mengikuti struktur yang dijelaskan pada dokumen ini agar kode tetap konsisten, mudah dipelihara, dan dapat dikembangkan dalam jangka panjang.
---
# Architecture Philosophy
Arsitektur proyek dibangun berdasarkan lima prinsip utama.
## 1. Modular
Setiap fitur harus memiliki tanggung jawab yang jelas.
Contoh:
Valuation hanya menghitung valuation.
Growth hanya menghitung growth.
Jangan mencampur logika antar modul.
---
## 2. Readability
Kode harus mudah dibaca.
Prioritas utama bukan membuat kode paling pendek.
Prioritas utama adalah kode yang dapat dipahami enam bulan kemudian.
---
## 3. Maintainability
Setiap perubahan harus dapat dilakukan tanpa memengaruhi modul lain.
Perubahan pada Valuation tidak boleh merusak Dashboard.
---
## 4. Performance
TradingView memiliki keterbatasan resource.
Karena itu:
- Hindari perhitungan berulang.
- Hindari request.financial() yang tidak diperlukan.
- Hindari pembuatan object yang tidak digunakan.
---
## 5. Scalability
Arsitektur harus memungkinkan penambahan fitur baru tanpa melakukan redesign besar.
---
# High Level Architecture
```
                    User
                      │
                      ▼
               TradingView Chart
                      │
                      ▼
              Data Collection Layer
                      │
                      ▼
              Sector Classification
                      │
                      ▼
             Fundamental Calculation
                      │
                      ▼
                Scoring Engine
                      │
                      ▼
               Dashboard Renderer
                      │
                      ▼
                   End User
```
---
# Layer Architecture
## Layer 1
### Configuration
Berisi seluruh input pengguna.
Contoh:
- Dashboard Position
- Color Theme
- Sector Override
- Display Mode
Layer ini tidak melakukan perhitungan.
---
## Layer 2
### Data Layer
Bertugas mengambil seluruh data fundamental.
Contoh:
- EPS
- Book Value
- Revenue
- Net Income
- ROE
- ROA
Seluruh request.financial() hanya boleh dilakukan pada layer ini.
---
## Layer 3
### Sector Engine
Bertugas menentukan karakteristik emiten.
Contoh:
- Bank
- Asuransi
- Sekuritas
- Consumer
- Mining
- Property
- Technology
Layer ini tidak menghitung skor.
---
## Layer 4
### Calculation Engine
Menghitung seluruh rasio.
Contoh:
- PBV
- PER
- ROE
- DER
- Dividend Yield
Layer ini hanya menghasilkan angka.
Tidak melakukan interpretasi.
---
## Layer 5
### Scoring Engine
Mengubah angka menjadi skor.
Contoh:
ROE
↓
95
PBV
↓
80
DER
↓
70
↓
Overall Score
---
## Layer 6
### Interpretation Engine
Memberikan konteks.
Contoh:
PBV tinggi
↓
Normal karena sektor Bank
atau
DER tinggi
↓
Wajar karena Infrastruktur
Layer ini merupakan pembeda utama proyek ini dibanding dashboard fundamental umum.
---
## Layer 7
### Dashboard Renderer
Menampilkan seluruh hasil.
Renderer tidak boleh melakukan perhitungan.
Renderer hanya menampilkan data.
---
# Source Code Structure
Urutan kode di Pine Script harus mengikuti struktur berikut.
```
Header
↓
Input
↓
Constant
↓
Financial Request
↓
Sector Engine
↓
Calculation Engine
↓
Scoring Engine
↓
Interpretation Engine
↓
Dashboard
↓
Alert (Future)
```
Urutan ini wajib dipertahankan.
---
# Module Dependency
```
Configuration
↓
Data Layer
↓
Sector Engine
↓
Calculation Engine
↓
Scoring Engine
↓
Interpretation Engine
↓
Dashboard
```
Tidak boleh ada dependency terbalik.
---
# Design Rules
1. Dashboard tidak boleh menghitung data.
2. Dashboard hanya membaca hasil.
3. Seluruh financial request dilakukan satu kali.
4. Hindari duplicate calculation.
5. Gunakan nama variabel yang eksplisit.
6. Gunakan komentar pada setiap section utama.
7. Hindari nested if yang berlebihan.
8. Pisahkan antara data, logika, dan tampilan.
---
# Future Architecture
Versi mendatang dapat menambahkan engine baru tanpa mengubah struktur utama.
Contoh:
- Risk Engine
- Momentum Engine
- Ownership Engine
- Macro Engine
- Composite Rating Engine
Seluruh engine baru harus ditempatkan sebelum Dashboard Renderer.
---
# Architecture Decision
Keputusan arsitektur harus mengikuti prinsip berikut.
- Stabilitas lebih penting daripada kompleksitas.
- Kinerja lebih penting daripada estetika kode.
- Konsistensi lebih penting daripada kreativitas.
- Metodologi lebih penting daripada implementasi.
---
# Closing Statement
Dokumen ini menjadi acuan utama seluruh implementasi teknis proyek.
Perubahan terhadap struktur arsitektur hanya boleh dilakukan apabila terdapat alasan teknis yang kuat dan telah didokumentasikan pada CHANGELOG.md.
