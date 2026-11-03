# Seasonal GitHub profile themes

The new banner is shown directly above the Corsica card. Existing daily quote and snake workflows are unchanged.

## Calendar (Europe/Paris)
- Christmas: December 15–January 6
- Halloween: October 20–31
- Easter: seven days before through seven days after Easter Sunday (computus)
- Winter: December–February; spring: March–May; summer: June–August; autumn: September–November

Holiday windows override seasons. All SVG artwork is original procedural vector decoration, not raster sprites. SVGs are static; the existing snake remains animated separately.

## Test
`python3 scripts/seasonal.py --all` generates all eight preview SVGs and the current banner. `python3 scripts/seasonal.py --date 2026-12-25` previews Christmas as current. Rerun without flags to restore the present date.

## Deploy
Copy all files into the `angeBiancamaria` profile repository. Commit and push, then run Actions → Seasonal profile theme → Run workflow. The workflow runs daily at 04:10 UTC, but only commits when the SVG content changes. GitHub Actions may start late. Ensure Actions workflow has read/write contents permission. The daily quote workflow may update README concurrently; this workflow only stages the banner SVG.

## Notes
GitHub README SVG images cannot run JavaScript; a daily regenerated SVG is reliable and cache-friendly. GitHub may cache the displayed image for a while after a change. GitHub does not support theming the entire README with custom CSS, so this release themes the banner while preserving the rest of the profile.
