import datetime as dt
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class SeasonalSyncTests(unittest.TestCase):
    def test_forced_theme_and_auto_preserve_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / 'repo'
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('__pycache__'))
            cache = root / 'stats/developer_cards_cache.json'
            before = cache.read_bytes()
            for theme in ('birthday', 'halloween', 'auto'):
                args = ['--date', '2026-11-14']
                if theme != 'auto': args += ['--theme', theme]
                subprocess.run([sys.executable, str(root/'scripts/seasonal.py'), *args], check=True, capture_output=True)
                subprocess.run([sys.executable, str(root/'scripts/developer_cards.py'), '--cached-only', '--date', '2026-11-14'], check=True, capture_output=True)
                meta = json.loads((root/'img/developer/data.json').read_text())
                self.assertEqual(meta['theme'], 'autumn' if theme == 'auto' else theme)
                self.assertEqual(cache.read_bytes(), before)
                self.assertGreater(meta['public_repos'], 0)
