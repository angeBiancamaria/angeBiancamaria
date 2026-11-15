from collections import Counter
import datetime as dt
import pathlib, sys, tempfile, unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'scripts'))
import developer_cards as c

class VisualLayoutTests(unittest.TestCase):
 def test_streak_divider_and_mascot(self):
  with tempfile.TemporaryDirectory() as td:
   root=pathlib.Path(td)
   with patch.object(c,'OUT',root), patch.object(c,'mascot_image',return_value='<image x="621" y="48" width="194" height="132"/>'):
    c.generate('spring',dt.date(2026,11,15),[],[],Counter(),[],[],variant='sleepy')
   svg=ET.parse(root/'streak.svg').getroot()
   ns={'s':'http://www.w3.org/2000/svg'}
   self.assertEqual(svg.find('s:path',ns).get('d'),'M22 55 H608')
   self.assertEqual(svg.find('s:rect',ns).get('fill'),'#0d1117')
   self.assertEqual(svg.find('s:image',ns).get('height'),'132')
