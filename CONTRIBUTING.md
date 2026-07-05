# Contributing to Papan Instrumen

Terima kasih atas minatnya! Proyek ini open-source dan menerima kontribusi.

## Cara Berkontribusi

### 1. Laporkan Bug
Gunakan [Issue Template → Bug Report](https://github.com/akhmfz/papan-instrumen/issues/new?template=bug.yml).

### 2. Usulkan Fitur
Gunakan [Issue Template → Feature Request](https://github.com/akhmfz/papan-instrumen/issues/new?template=feature.yml).

### 3. Pull Request

1. Fork repo & clone
2. Buat branch: `git checkout -b feat/nama-fitur`
3. Edit modul di `src/modules/` (JANGAN edit `src/PapanInstrumen.pine` langsung)
4. Jalankan: `npm run build`
5. Test: `npm run test:all` & `npm run lint`
6. Commit dengan format: `feat(scope): deskripsi` atau `fix(scope): deskripsi`
7. Push & buka Pull Request

### Development Setup

```bash
git clone git@github.com:akhmfz/papan-instrumen.git
cd papan-instrumen
npm install        # install PineTS + deps
npm run build      # concat modules → built file
npm run lint       # lint check
npm run test:all   # 89 tests
npm run transpile  # syntax check via PineTS
```

### Struktur Source

```
src/modules/
├── 01-base.pine     — Header, inputs, tema, utilities
├── 02-data.pine     — Market engine, financial requests, sektor
├── 03-ui.pine       — Table & cell rendering
└── 04-scoring.pine  — Scoring engine + render
```

**Golden Rule:** Edit modul, lalu `build.sh` untuk generate `src/PapanInstrumen.pine`.

### Testing

89 automated tests via [PineTS](https://github.com/LuxAlgo/PineTS):

```bash
npm run test:all    # run semua test
```

Tambahkan test untuk fitur baru di `tests/scoring/`.

### Coding Standard

- Pine Script v6
- camelCase untuk variable/fungsi
- UPPER_SNAKE_CASE untuk konstanta
- `is`/`has` prefix untuk boolean
- Maksimal 50 baris per fungsi
- Setiap perubahan: update CHANGELOG di `docs/DEVELOPMENT.md`
- No silent changes

### Ngecek di TradingView

1. `npm run build`
2. Copy isi `src/PapanInstrumen.pine`
3. Paste ke TradingView Pine Editor → Add to Chart

### Keterbatasan

- `request.financial()` — data dari TradingView, tidak bisa di-test di PineTS
- Maksimal 40 `request.*()` calls — budget saat ini 35, sisa 5
- Hanya timeframe Daily (D/1D) — IDX EOD-only
