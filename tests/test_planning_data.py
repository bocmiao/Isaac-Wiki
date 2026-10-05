import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'docs/.vitepress/theme/data'
class PlanningDataTests(unittest.TestCase):
    def test_synergies_match_every_source_row(self):
        section=(ROOT/'docs/strategy/items.md').read_text().split('## 常见组合\n')[1].split('\n## ')[0]
        rows=[[s.strip() for s in l.split('|')[1:-1]] for l in section.splitlines() if l.startswith('| ')][2:]
        combos=json.loads((DATA/'synergies.json').read_text())
        items={i['id'] for i in json.loads((DATA/'item-links.json').read_text())}
        self.assertEqual(len(rows),len(combos))
        for combo,row in zip(combos,rows):
            self.assertEqual([combo['title'],combo['individual'],combo['effect']],row)
            self.assertEqual(len(combo['items']),2)
            self.assertTrue(all(i in items for i in combo['items']))
    def test_route_steps_have_unique_ids_and_source(self):
        routes=json.loads((DATA/'routes.json').read_text())
        step_ids=[s['id'] for r in routes for s in r['steps']]
        self.assertEqual(len(step_ids),len(set(step_ids)))
        self.assertTrue(all(r['source']=='/guide/unlocks/endings' and r['steps'] for r in routes))
        by_id={r['id']:r for r in routes}
        self.assertEqual(by_id['mother']['requirements'],['hush3'])
        self.assertEqual(by_id['beast']['requirements'],['mother1'])
        self.assertIn('30 分钟',by_id['hush']['steps'][1]['text'])
        self.assertIn('2 个炸弹',by_id['mother']['steps'][2]['text'])
        self.assertIn('0-愚者',by_id['beast']['steps'][0]['text'])
