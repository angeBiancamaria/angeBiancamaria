# Developer cards — v9.0

The profile README and existing workflows are preserved. The dedicated workflow updates the seven SVG cards and keeps the last valid GitHub API snapshot in `stats/developer_cards_cache.json`.

## Commands

```powershell
python scripts/developer_cards.py --self-test
python -m unittest discover -s tests -v
python scripts/developer_cards.py --offline
```

Offline mode does **not** overwrite existing cards. For a deliberate preview on a test branch:

```powershell
python scripts/developer_cards.py --offline --allow-preview-overwrite --theme autumn --force-variant cheapy
```

## Real GitHub contribution calendar

The GraphQL calendar needs an authenticated token. The default `github.token` may be insufficient for reading a user's contribution calendar. If the workflow logs `GraphQL contribution calendar` errors, create a **classic personal access token** with the minimum necessary `read:user` scope (and `repo` only if you explicitly need private contributions), then save it as the repository Actions secret `GH_STATS_TOKEN`. Never commit tokens. Run the `Developer Cards v9.0 (safe)` workflow manually and inspect the logs. If GraphQL remains unavailable, other cards can still update, and the previous valid calendar is reused if present.

## Safety

- Do not commit generated offline placeholders to `main`.
- Work on a branch, run the tests, inspect the SVGs, then merge.
- `GH_STATS_TOKEN` is optional and used only to read stats; GitHub Actions uses its built-in token to commit.
- Special variants are deterministic for the date: 8% Cheapy, 2% strike Cheapy, and Sleepy on weekends otherwise.
- The current seasonal illustrations are provisional; keep the approved Cheapy as the joke variant until the normal costumes are replaced with original illustrated assets.
