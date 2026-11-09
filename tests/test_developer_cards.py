"""Offline regression tests; never contact GitHub or alter committed SVGs."""
import datetime as dt
import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import shutil
import unittest
import xml.etree.ElementTree as ET

ROOT=pathlib.Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'scripts'/'developer_cards.py'

class CardTests(unittest.TestCase):
 def test_offline_does_not_overwrite_cards(self):
  with tempfile.TemporaryDirectory() as td:
   root=pathlib.Path(td)
   shutil.copytree(ROOT/'scripts',root/'scripts')
   (root/'img'/'developer').mkdir(parents=True)
   sentinel=root/'img'/'developer'/'streak.svg'
   sentinel.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
   subprocess.run([sys.executable,str(root/'scripts'/'developer_cards.py'),'--offline','--theme','halloween'],check=True,capture_output=True,text=True)
   self.assertEqual(sentinel.read_text(),'<svg xmlns="http://www.w3.org/2000/svg"/>')
 def test_all_seasonal_svg_previews(self):
  with tempfile.TemporaryDirectory() as td:
   root=pathlib.Path(td)
   shutil.copytree(ROOT/'scripts',root/'scripts')
   target=root/'img'/'developer'
   target.mkdir(parents=True)
   # These assets are deliberately optional in the generator.
   for theme in ('winter','spring','summer','autumn','halloween','christmas','easter','birthday'):
    subprocess.run([sys.executable,str(root/'scripts'/'developer_cards.py'),'--offline','--allow-preview-overwrite','--theme',theme],check=True,capture_output=True,text=True)
    for name in ('streak','pulse','languages','rpg','timeline','achievements','automation'):
     ET.parse(target/(name+'.svg'))
 def test_streak_logic(self):
  sys.path.insert(0,str(ROOT/'scripts'))
  import developer_cards as cards
  self.assertEqual(cards.streak_stats({'2026-11-04':2,'2026-11-05':1},dt.date(2026,11,6)),(2,2,3))

if __name__=='__main__':unittest.main()
