#!/bin/bash
# scripts/gh-sync.sh — create GitHub Issues + Labels from backlog
# Prerequisite: gh auth login

set -e

REPO="akhmfz/papan-instrumen"

gh auth status &>/dev/null || {
    echo "❌ Not authenticated. Run: gh auth login"
    echo "   Then re-run: bash scripts/gh-sync.sh"
    exit 1
}

# ── Labels ──
echo "🏷  Creating labels..."
gh label create "P1-critical" --color "d73a4a" --repo "$REPO" 2>/dev/null || true
gh label create "P2-high" --color "f29513" --repo "$REPO" 2>/dev/null || true
gh label create "P3-medium" --color "0e8a16" --repo "$REPO" 2>/dev/null || true
gh label create "P4-low" --color "5319e7" --repo "$REPO" 2>/dev/null || true
gh label create "scoring" --color "006b75" --repo "$REPO" 2>/dev/null || true
gh label create "dashboard" --color "d4c5f9" --repo "$REPO" 2>/dev/null || true
gh label create "sector" --color "bfdadc" --repo "$REPO" 2>/dev/null || true
gh label create "performance" --color "fbca04" --repo "$REPO" 2>/dev/null || true
gh label create "docs" --color "c5def5" --repo "$REPO" 2>/dev/null || true
gh label create "test" --color "ededed" --repo "$REPO" 2>/dev/null || true
gh label create "phase-a" --color "1d76db" --repo "$REPO" 2>/dev/null || true
gh label create "phase-b" --color "ffa500" --repo "$REPO" 2>/dev/null || true
gh label create "phase-c" --color "32cd32" --repo "$REPO" 2>/dev/null || true
echo ""

# ── Issues ──
echo "📋 Creating issues..."

create_issue() {
    local title="$1"
    local body="$2"
    local labels="$3"
    local milestone="$4"

    echo "  → $title"
    gh issue create \
        --title "$title" \
        --body "$body" \
        --label "$labels" \
        --repo "$REPO" \
        ${milestone:+--milestone "$milestone"} \
        --assignee "@me" \
        &>/dev/null
}

# Phase A — Beta Readiness
create_issue "A1: Validasi klasifikasi seluruh sektor IDX (Consumer/Industri/Healthcare)" \
"Pisahkan Consumer, Industri, Healthcare sebagai kelas sektor terpisah dari Non-Finansial Umum.

**Scope:**
- Deteksi otomatis via syminfo + ticker watchlist
- Override manual di dropdown Sektor
- Bobot scoring per dimensi (saat ini ketiganya masih default)

**Ref:** BL-003, BL-007" \
"phase-a,sector,P2-high"

create_issue "A2: Batubara vs CPO sebagai kelas sektor terpisah" \
"Pisahkan Siklikal menjadi dua sub-kategori: Batubara dan CPO/Plantation.

**Scope:**
- Deteksi otomatis via ticker watchlist + industry field
- Threshold scoring berbeda (Batubara lebih volatile dari CPO)
- Override manual di dropdown Sektor

**Ref:** BL-011" \
"phase-a,sector,P3-medium"

create_issue "A3: Scoring audit via PineTS — semua dimensi" \
"Tambahkan unit test PineTS untuk setiap dimensi scoring.

**Target:**
- [ ] Value scoring test (10 rasio, 6 sektor)
- [ ] Quality scoring test (9 rasio, 6 sektor)
- [ ] Growth scoring test (3 rasio + modifier)
- [ ] Health scoring test (11 rasio, sektor thresholds)
- [ ] Income scoring test (4 rasio)
- [ ] Momentum scoring test (5 komponen)
- [ ] Indonesia Factor test (3 komponen)
- [ ] OverallScore test (6/7 factor)

**Target files:** tests/scoring/*.mjs" \
"phase-a,scoring,test,P2-high"

create_issue "A4: Benchmark performa 90-row table" \
"Ukur dan optimasi load time via Script Stopwatch di TradingView.

**Target:**
- [ ] Install Script Stopwatch di chart
- [ ] Ukur end-to-end load time (target < 2s)
- [ ] Profiling: identifikasi bottleneck (render, scoring, request)
- [ ] Optimasi jika > 2s: cache, lazy eval, conditional render

**Ref:**
- Script Stopwatch: https://www.tradingview.com/script/rRmrkRDr/
- PineTS benchmark: tests/transpile.sh" \
"phase-a,performance,P2-high"

create_issue "A5: User documentation (ID) — panduan pengguna" \
"Buat dokumentasi non-teknis untuk pengguna akhir.

**Target:**
- [ ] README.id.md — Quick start visual (screenshot + arrow annotations)
- [ ] Cara interpretasi skor per dimensi
- [ ] Penjelasan Faktor Indonesia (kapan ON/OFF)
- [ ] Cara override sektor manual
- [ ] Risiko Likuiditas: cara baca
- [ ] FAQ: data tidak tersedia, skor tidak berubah, dll." \
"phase-a,docs,P3-medium"

create_issue "A6: Refactor Dashboard Layout (compact mode preparation)" \
"Persiapan untuk compact mode: refactor render logic jadi lebih parameterized.

**Scope:**
- Pisahkan left/right column render menjadi fungsi terpisah
- Parameterized row rendering (bisa pilih compact vs full)
- Bersihkan duplikasi di render section

**Ref:** BL-001" \
"phase-a,dashboard,P2-high"

# Phase B — Feature Complete
create_issue "B1: Compact mode dashboard (45-row condensed view)" \
"Mode tampilan ringkas untuk layar kecil / mobile.

**Target:**
- [ ] Single-column layout toggle
- [ ] Sembunyikan detail, tampilkan hanya score card + ringkasan
- [ ] Auto-detect compact mode jika ukuran font = Kecil Sekali
- [ ] Backward compatible (default = full)" \
"phase-b,dashboard,P3-medium"

create_issue "B2: EN/ID language toggle (i18n)" \
"Internationalization — English labels sebagai alternatif.

**Target:**
- [ ] Label dictionary (ID default, EN toggle)
- [ ] Semua label: dimensi, rasio, grade, sektor, keterangan
- [ ] Input toggle: 'Bahasa: Indonesia | English'" \
"phase-b,dashboard,P3-medium"

create_issue "B3: Sector benchmark — perbandingan vs rata-rata sektor" \
"Tampilkan di dashboard: skor emiten vs rata-rata sektor.

**Data source:**
- Tidak butuh request tambahan — hitung dari data emiten yang sudah ada
- Atau: buat separate screener indicator yang menghitung rata-rata 40 ticker

**Scope (minimal):**
- Tampilkan label 'di atas rata-rata sektor' / 'di bawah rata-rata'" \
"phase-b,scoring,sector,P3-medium"

create_issue "B4: Save/load preset scoring config" \
"Fitur simpan/buka preset konfigurasi bobot scoring.

**Target:**
- [ ] Preset bawaan: Default (equal), Value-biased, Growth-biased, Conservative
- [ ] Simpan/load via TradingView Settings (input.string dengan JSON encoded?)
- [ ] Atau: dokumentasi cara simpan setting via TradingView Chart Layout" \
"phase-b,scoring,P4-low"

create_issue "B5: Multi-ticker screener mode" \
"Scan multiple ticker dalam satu chart untuk quick comparison.

**Scope (investigate dulu):**
- Pine Script limit: 40 request.security() max
- Pendekatan: pisah indicator terpisah untuk screener
- Atau: composite ticker trick (120 ticker Screener ref)

**Ref:** https://www.tradingview.com/script/0h0gKNcy-120x-ticker-screener-composite-tickers/" \
"phase-b,scoring,sector,P4-low"

# Phase C — Stable
create_issue "C1: Full documentation — user guide + methodology paper" \
"Dokumentasi lengkap untuk v1.0.

**Target:**
- [ ] User Guide (ID + EN)
- [ ] Methodology Paper (cara hitung skor, referensi akademik)
- [ ] API Reference (Pine Script functions)
- [ ] Installation Guide
- [ ] Comparison vs dashboard luar negeri" \
"phase-c,docs,P3-medium"

create_issue "C2: Webhook alert — fundamental signal notification" \
"Kirim alert saat skor fundamental berubah signifikan.

**Target:**
- [ ] Alert condition: OverallScore crossing threshold (e.g., > 70, < 40)
- [ ] Webhook payload: JSON dengan semua skor
- [ ] Discord/Telegram integration (via webhook services)

**Ref:**
- https://github.com/fabston/TradingView-Webhook-Bot
- https://traderspost.io/" \
"phase-c,scoring,P3-medium"

create_issue "C3: Public launch — TradingView Public Library" \
"Checklist publikasi ke TradingView Public Scripts.

**Target:**
- [ ] Kode comply dengan TradingView House Rules
- [ ] Deskripsi publik: eng + ind, screenshot, disclaimer
- [ ] Publish via akun akhmfz
- [ ] Share ke KSPM community
- [ ] Collect feedback 100+ users" \
"phase-c,docs,P2-high"

create_issue "C4: Community contribution guidelines" \
"Buka kontribusi publik: CONTRIBUTING.md + CODEOWNERS.

**Target:**
- [ ] CONTRIBUTING.md: cara submit PR, coding standard, testing
- [ ] CODEOWNERS: review assignment
- [ ] Pull Request template
- [ ] CLA atau DCO jika diperlukan" \
"phase-c,docs,P4-low"

echo ""
echo "✅ $(gh issue list --repo "$REPO" --limit 50 2>/dev/null | wc -l) issues created"
