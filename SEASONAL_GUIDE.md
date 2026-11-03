# Seasonal profile skins v2

This version **does not add a second banner**. It preserves the original animated header, Corsica silhouette, goal targets, quotes, and contribution Snake.

The daily workflow updates:
- the existing capsule-render header accent and typing text color in README.md;
- `img/seasonal/corsica_current.svg` (derived from the original Corsica card);
- `img/seasonal/goals_current.svg` (derived from the original targets).

The Snake workflow now chooses its palette from the same calendar, each time it runs. Snake images are still published to the `output` branch.

## Theme calendar (Europe/Paris)
- Birthday: **January 9**, highest priority
- Christmas: December 15 through January 6
- Halloween: October 20–31
- Easter: 4 days before through 4 days after Easter Sunday (computed each year)
- Winter: December–February
- Spring: March–May
- Summer: June–August
- Autumn: September–November

## Install
Copy all files into the `angeBiancamaria` profile repository, keeping paths. Commit and push. In **Actions → Seasonal profile theme → Run workflow**, choose `auto` or a specific preview theme. If testing a forced theme, the next scheduled run restores the current calendar theme. Run **Generate contribution snake** to regenerate its colors too.

## Local tests
`python3 scripts/seasonal.py --date 2026-01-09 --print-theme` prints `birthday`.
`python3 scripts/seasonal.py --date 2026-11-03` applies autumn.
`python3 scripts/seasonal.py --theme halloween --preview-all` applies Halloween and generates standalone previews of the decorated Corsica card and goals.

The script regenerates themed copies from `img/corsica_card.svg` and `img/my_goals.svg`, leaving the originals untouched. The existing daily quote workflow is unchanged.

Note: GitHub caches SVGs; hard-refresh after Actions finishes. GitHub SVG rendering may limit some SVG animations. GitHub Actions scheduled jobs may run later than their cron time.
