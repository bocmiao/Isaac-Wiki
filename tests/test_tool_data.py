import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'docs/.vitepress/theme/data'
class ToolDataTests(unittest.TestCase):
 def test_all_challenge_rules_match_the_article(self):
  original=[]
  for line in (ROOT/'docs/strategy/challenges.md').read_text().splitlines():
   cells=[x.strip()for x in line.strip('|').split('|')]
   if len(cells)==7 and cells[0].isdigit():original.append(cells)
  data=json.loads((DATA/'challenges.json').read_text())
  self.assertEqual([c['id']for c in data],list(range(1,46)))
  for item,cells in zip(data,original):
   self.assertEqual(item['name'],cells[1].split('<br>')[0])
   for key,i in [('character',2),('target',3),('rules',4),('reward',5),('unlock',6)]:
    self.assertEqual(item[key],re.sub('<[^>]+>',' ',cells[i]).strip())
 def test_normal_donations_match_achievement_source(self):
  data=json.loads((DATA/'normal-donations.json').read_text())
  source=json.loads((ROOT/'data/achievement-source.json').read_text())
  expected=[]
  for a in source:
   m=re.fullmatch(r'Donate (\d+) [Cc]oins to the Donation Machine',a['condition'])
   if m:expected.append(dict(coins=int(m[1]),id=a['id'],name=a['name']))
  self.assertEqual(data,sorted(expected,key=lambda x:x['coins']))
 def test_known_collectible_ids_and_no_duplicates(self):
  data=json.loads((DATA/'item-links.json').read_text());by_id={i['id']:i for i in data}
  self.assertEqual(len(data),len(by_id));self.assertEqual(len(data),720)
  for n,name in [(1,'The Sad Onion'),(105,'The D6'),(118,'Brimstone'),(723,'Spindown Dice')]:
   self.assertEqual(by_id[n]['en'],name)
  self.assertTrue(all(i['id']>0 and i['name'] and i['en'] and i['enum'].startswith('COLLECTIBLE_')for i in data))
if __name__=='__main__':unittest.main()
