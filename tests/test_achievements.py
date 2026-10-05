"""Catalog completeness and checked-in guide consistency against the source snapshot."""
import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=json.loads((ROOT/'data/achievement-source.json').read_text())
CATALOG=json.loads((ROOT/'docs/.vitepress/theme/data/achievements.json').read_text())

class AchievementTests(unittest.TestCase):
 def test_ids_and_source_identity(self):
  self.assertEqual(sorted(x['id']for x in SOURCE),list(range(1,642)))
  self.assertEqual(sorted(x['id']for x in CATALOG),list(range(1,642)))
  original={x['id']:x for x in SOURCE}
  for item in CATALOG:
   self.assertEqual(item['name'],original[item['id']]['name'])
   self.assertTrue(re.search('[\u4e00-\u9fff]',item['conditionZh']))
   self.assertNotIn('待补',item['conditionZh'])
 def test_every_entry_has_a_unique_tutorial(self):
  pages=list((ROOT/'docs/achievements').glob('ids-*.md'))
  all_ids=[]
  for page in pages:all_ids.extend(map(int,re.findall(r'\{#achievement-(\d+)\}',page.read_text())))
  self.assertEqual(sorted(all_ids),list(range(1,642)))
  for item in CATALOG:
   text=(ROOT/f"docs/achievements/{item['page']}.md").read_text()
   section=text.split(f"{{#achievement-{item['id']}}}",1)[1].split('\n## ',1)[0]
   self.assertIn(item['conditionZh'],section)
   self.assertGreaterEqual(len(re.findall(r'^- ',section,re.M)),1)
 def test_reward_groups_and_challenge_distinctions(self):
  self.assertEqual(sum(x['group']=='挑战奖励'for x in CATALOG),45)
  self.assertEqual(sum(x['group']=='挑战开放'for x in CATALOG),34)
  self.assertEqual(sum(x['group']=='里角色合并奖励'for x in CATALOG),34)
  names=['以撒','抹大拉','该隐','犹大','小蓝人','夏娃','参孙','阿撒泻勒','拉撒路','伊甸','游魂','莉莉丝','店主','亚玻伦','遗骸','伯大尼','雅各']
  for first,last,step,tainted in [(474,490,1,False),(491,507,1,True),(548,580,2,True),(584,600,1,True),(601,617,1,True),(618,634,1,True)]:
   for number,name in zip(range(first,last+1,step),names):
    expected=('里'+name)if tainted else('雅各与以扫'if name=='雅各'else name)
    self.assertIn(f'用{expected}',CATALOG[number-1]['conditionZh'])
 def test_version_specific_gates(self):
  self.assertEqual(sum(x['id']<=637 for x in CATALOG),637)
  self.assertEqual([x['minimum']for x in CATALOG[637:]],['忏悔+']*4)
  self.assertIn('全程不死亡',CATALOG[403]['conditionZh'])
  self.assertIn('忏悔非加号',CATALOG[267]['conditionZh'])
  self.assertIn('新增四项',CATALOG[636]['conditionZh'])
  self.assertIn('极贪',CATALOG[635]['conditionZh'])

if __name__=='__main__':unittest.main()
