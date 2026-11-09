import datetime as dt
import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'scripts'))
import developer_cards as c
class VariantTests(unittest.TestCase):
 def test_deterministic(self):
  for i in range(365):
   day=dt.date(2026,1,1)+dt.timedelta(days=i)
   self.assertEqual(c.choose_variant(day),c.choose_variant(day))
 def test_probability_rules(self):
  for i in range(365):
   day=dt.date(2026,1,1)+dt.timedelta(days=i)
   v=c.choose_variant(day)
   self.assertIn(v,c.VARIANTS)
   if day.weekday()<5:self.assertNotEqual(v,'sleepy')
 def test_force_variants(self):
  for v in c.VARIANTS:self.assertEqual(c.choose_variant(dt.date(2026,11,6),v),v)
 def test_assets(self):
  root=pathlib.Path(__file__).resolve().parents[1]/'img/developer/chaty'
  for v in ('cheapy','strike','sleepy'):self.assertTrue((root/(v+'.png')).is_file())
