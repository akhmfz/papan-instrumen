# CATATAN PENGEMBANGAN — Lessons Learned

> Kumpulan bug, error, pelajaran, dan anti-pattern yang ditemukan selama pengembangan Papan Instrumen.
> Dibaca ulang sebelum mulai sprint baru. Diperbarui setiap kali nemu pelajaran baru.

---

## ⛔ Pine Script v6 — Jebakan & Anti-Pattern

### 1. Reserved Keywords
| Keyword | Kenapa Error | Solusi |
|---------|-------------|--------|
| `base` | Parameter `security()` legacy v4/v5 | Ganti jadi `col` atau `column` |
| `open`, `high`, `low`, `close`, `volume` | Built-in bar variables | Jangan dipakai sebagai nama parameter/variable |
| `hl2`, `hlc3`, `ohlc4` | Built-in price averages | Sama — jangan dipakai |

### 2. NO Local Functions Inside `if` Blocks
```
// ❌ ERROR (CE10156)
if barstate.islast
    f_renderLeft(col, row) => ...

// ❌ ERROR — type annotations di local function
    f_renderLeft(int col, int row) => ...

// ❌ ERROR — arrow syntax di local block
    f_renderLeft(col, row) => ...

// ✅ CORRECT — inline code only, no functions
    // render langsung, tidak pakai fungsi
```
**Pelajaran:** Pine Script v6 hanya support fungsi di **TOP LEVEL** (di luar `if`/`for`/`while`).

### 3. Type Annotations pada Parameter
| Context | Allowed? |
|---------|----------|
| Top-level function parameter | ✅ `f_foo(int x, float y) =>` |
| Local function parameter | ❌ Not allowed at all (local functions not allowed) |

### 4. Semicolons di `if` Blocks
```
// ❌ ERROR — PineTS parse gagal
if cond; stmt1; stmt2

// ✅ CORRECT
if cond
    stmt1
    stmt2
```

---

## 🐛 Bug yang Pernah Ada (Fase 0)

| ID | Bug | Lokasi | Dampak | Fix |
|----|-----|--------|--------|-----|
| **P0-1** | `netDebtEbitdaScore` pakai `f_scoreLower` | `04-scoring.pine:478` | EBITDA negatif + net debt positif → skor ~100 (padding) | Ganti ke `f_scoreLowerSafe` |
| **P0-2** | Consumer/Industri/Kesehatan cuma label | `02-data.pine`, `04-scoring.pine` | 3 sektor detected tapi 0 impact scoring | Tambah 12 blok bobot (4 dimensi × 3 sektor) |
| **P0-3** | Komentar `earningsQuality` mismatch | `04-scoring.pine:300` | Klaim OCF > NI, kode cek OCF sign only | Disclaimer di komentar |
| **P0-4** | `growthSpread` saat `revGrowth == 0` | `04-scoring.pine:309` | Modifier default 1.0 (no penalty) meski EPS turun | Guard + penalti 0.9 |
| **P0-5** | Sekuritas warning hilang di Quality | `04-scoring.pine:684` | Quality cuma cek Bank+Asuransi, Sekuritas lupa | Tambah `isSekuritasSektor` |
| **K1** | Multi-var float declarations | `PapanInstrumen.pine` | Compile error di TV | Split 7→16 baris |
| **K2** | Guard nilai negatif (Valuasi) | `04-scoring.pine` | Emiten rugi dapat skor 100 | `f_scoreLowerSafe` guard |
| **K3** | Skala `debtAssetScore` | `04-scoring.pine` | Threshold 80% skala 0-100 → desimal 0-0.8 | Fix ke `f_scoreLowerSafe(debtAsset, 0, 0.8)` |

---

## 🧪 Testing — Pelajaran

### PineTS Limitations
```
✅ BISA: Utility functions, scoring formulas, ta.*() functions
❌ GAK BISA: syminfo.tickerid, syminfo.sector, syminfo.industry
❌ GAK BISA: request.financial() (TradingView proprietary)
❌ GAK BISA: table.* (some PineTS versions)
```

### Test vs Production Gap
**Masalah:** Tests di `tests/scoring/*.mjs` menyalin konstanta bobot manual, bukan dari source 04-scoring.pine. Bug produksi seperti P0-1 dan P0-2 tidak mungkin tertangkap oleh test yang ada.

**Rencana perbaikan (P1-1):** Verifikasi test menggunakan kode yang sama dengan produksi, baik via import concatenation atau test snapshot.

### Test Count History
```
12 utility + 77 scoring = 89 → 96 (+7 regression: P0-1,P0-2,P0-4)
```

---

## 📋 Process — Pelajaran

### Rilis Harus Diverifikasi
Setiap tag rilis WAJIB:
- [ ] `git diff <previous_tag>..HEAD -- src/` dijalankan dan hasilnya ada di changelog
- [ ] README versi + build number sinkron SEBELUM tag dibuat
- [ ] Screenshot compile sukses dari Pine Editor dilampirkan
- [ ] Setiap klaim angka (jumlah test, sektor, field) dihitung ulang manual dari kode
- [ ] Infrastruktur yang disebut (CI, linter, script) benar-benar ada di commit yang ditag

### No Silent Changes
- Setiap perubahan: update CHANGELOG di DEVELOPMENT.md
- Jangan commit perubahan yang tidak direncanakan
- Diff sebelum commit: `git diff --cached`

### Commit Convention
```
feat(scope): deskripsi     — fitur baru
fix(scope): deskripsi      — bug fix
docs(scope): deskripsi     — dokumentasi
refactor(scope): deskripsi — perubahan struktur tanpa fitur baru
test(scope): deskripsi     — test
perf(scope): deskripsi     — optimasi
ci: deskripsi              — CI/CD
release: deskripsi         — rilis/tag
```

---

## 🔧 Dev Tools — Yang Sudah Terpasang

| Tool | Command | Fungsi |
|------|---------|--------|
| Build | `bash build.sh` | Concat modules → PapanInstrumen.pine |
| Lint | `bash scripts/lint.sh` | Cek reserved keywords, budget, syntax |
| Test | `npm run test:all` | 96 tests via PineTS |
| Transpile | `bash tests/transpile.sh` | Syntax check via PineTS |
| CI | `.github/workflows/build.yml` | lint → build → transpile → test |
| Issues | `bash scripts/gh-sync.sh` | Auto-create GitHub Issues |

---

## 📊 Engine Comparison — Yang Sudah Dipelajari

| Engine | Type | Use Case | Status |
|--------|------|----------|--------|
| **PineTS** (LuxAlgo) | JS/TS runtime | Unit test scoring functions | ✅ Active (96 tests) |
| **PineForge** | C++ backtest library | Strategy backtesting | 📚 Compiled (78/78 tests) |
| **PyneCore** | Python AST transform | Alt unit test framework | 📚 Installed (v6.5.4) |
| **everget/unit-test** | Pine Script framework | Test langsung di TV chart | 📚 Studied |
| **awesome-pinescript** | Directory | Reference resources | ✅ Referenced |

---

## 📁 File Structure — Yang Ada Sekarang

```
papan-instrumen/
├── src/
│   ├── modules/
│   │   ├── 01-base.pine      — Header, inputs, tema, utils (542 lines)
│   │   ├── 02-data.pine       — Market, financial, sector (261 lines)
│   │   ├── 03-ui.pine          — Table & cell rendering (83 lines)
│   │   └── 04-scoring.pine     — Scoring + render (891 lines)
│   └── PapanInstrumen.pine    — Built output (1820 lines)
├── tests/
│   ├── pinets-verify.mjs       — 12 utility tests
│   ├── transpile.sh            — PineTS syntax check
│   └── scoring/
│       ├── runner.mjs          — Shared test runner
│       ├── test-value.mjs      — 14 tests
│       ├── test-quality.mjs    — 15 tests
│       ├── test-growth.mjs     — 8 tests
│       ├── test-health.mjs     — 16 tests
│       ├── test-income.mjs     — 10 tests
│       ├── test-momentum.mjs   — 11 tests
│       ├── test-overall.mjs    — 3 tests
│       └── test-regression.mjs — 7 tests (P0-1, P0-2, P0-4)
├── scripts/
│   ├── lint.sh                 — Custom Pine Script linter
│   └── gh-sync.sh              — GitHub Issues auto-create
├── docs/
│   ├── README.id.md            — Panduan pengguna (ID)
│   ├── AI.md                   — AI collaboration context
│   ├── ARCHITECTURE.md         — Arsitektur, metodologi, roadmap
│   └── DEVELOPMENT.md          — Coding standard, testing, changelog
├── .github/
│   ├── workflows/build.yml     — CI/CD pipeline
│   └── ISSUE_TEMPLATE/         — Bug + feature templates
├── CATATAN.md                  — THIS FILE
├── CONTRIBUTING.md
├── README.md
├── build.sh
└── package.json
```

---

## ⏳ Yang Belum Selesai (Backlog Aktif)

| ID | Item | Prioritas |
|----|------|-----------|
| P1-1 | Test import dari source sungguhan | P2-high |
| P1-4 | Coverage matrix ke README | P3-medium |
| P2-2 | Profitability refinement (Sekuritas vs Bank) | P3-medium |
| P2-3 | Batubara vs CPO separation | P4-low |
| P2-4 | Sekuritas Quality review | P3-medium |
| P3-1 | CAR/NPL/LDR manual inputs for banks | P2-high |
| P3-2 | Graded `f_scorePositive` (bukan biner 0/100) | P3-medium |
| P4-1 | Release checklist di DEVELOPMENT.md | P3-medium |
| P4-2 | Known Limitations ke README | P3-medium |

---

> **Golden Rule:** Jangan tambah fitur baru di atas fondasi yang belum diverifikasi.
> Setiap rilis publik WAJIB lolos Release Gate.
> No Silent Changes — setiap commit tercatat di changelog.
