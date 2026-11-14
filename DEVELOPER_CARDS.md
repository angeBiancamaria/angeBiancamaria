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

The GraphQL calendar needs an authenticated token. The default `github.token` may be insufficient for reading a user's contribution calendar. If the workflow logs `GraphQL contribution calendar` errors, create a **classic personal access token** with the minimum necessary `read:user` scope (and `repo` only if you explicitly need private contributions), then save it as the repository Actions secret `GH_STATS_TOKEN`. Never commit tokens. Run the `Developer Cards` workflow manually and inspect the logs. If GraphQL remains unavailable, other cards can still update, and the previous valid calendar is reused if present.

## Safety

- Do not commit generated offline placeholders to `main`.
- Work on a branch, run the tests, inspect the SVGs, then merge.
- `GH_STATS_TOKEN` is optional and used only to read stats; GitHub Actions uses its built-in token to commit.
- Special variants are deterministic for the date: 8% Cheapy, 2% strike Cheapy, and Sleepy on weekends otherwise.
- Seasonal costumes and Sleepy use illustrated PNGs; Cheapy and strike retain their deliberately cheap assets.

## Seasonal synchronization

Run Seasonal profile theme with `preview_theme` set to a theme or `auto`. It updates README and all seven cards in one commit, using the last valid snapshot without API requests. Developer Cards reads the active theme from the README. If no valid snapshot exists, run Developer Cards first.

```powershell
python scripts/seasonal.py --theme halloween
python scripts/developer_cards.py --cached-only
```
