# scripts/ — DEPRECATED (Phase 2)

Tools in this directory have been moved to **[pine-semantic-platform](https://github.com/akhmfz/pine-semantic-platform) v2.0+**.

## Migration

Requirement: `pip install` from GitHub or local path.

```bash
# Install from GitHub (v2.0+)
pip install git+https://github.com/akhmfz/pine-semantic-platform.git@v2.0.0

# Or local development
pip install -e /path/to/pine-semantic-platform

# Now CLI commands are available globally:
pine-extract --project-dir /path/to/my-project
pine-query search "pattern" --format table
pine-context "explain scoring" --profile review
pine-validate --workspace /path/to/my-project
pine-inject-graph /path/to/repo1 /path/to/repo2
pine-validate-semantic --project /path/to/my-project
```

Or via Python module:

```bash
python -m scripts.extract_ast --project-dir .
python -m scripts.pine_query search "pattern"
```

## What moved

| Tool | New Location |
|------|-------------|
| CLI tools | `pip install pine-semantic-platform` → `pine-*` commands |
| Python package | `pine_query` (installed as part of platform) |
| Tests | `pine-semantic-platform/tests/` |
| Docs | `pine-semantic-platform/docs/` |
| Research | `pine-semantic-platform/tools/market-data/` + `tests/e2/` |

## Schedule

- **Phase 1** (completed): Deprecation notice. Files still here, still work.
- **Phase 2** (current): Use `pine-*` CLI from installed platform. Direct `python scripts/*.py` deprecated.
- **Phase 3** (future): Files removed. Use platform exclusively.

## Compatibility

| papan-instrumen | pine-semantic-platform |
|----------------|----------------------|
| v1.2+          | v2.0.x               |

See [pine-semantic-platform](https://github.com/akhmfz/pine-semantic-platform) for full documentation.
