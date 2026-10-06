import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'docs/.vitepress/theme/data'

class CompletionRewards(unittest.TestCase):
    def setUp(self):
        self.rows=json.loads((DATA/'completion-rewards.json').read_text())
        self.by_id={r['id']:r for r in self.rows}

    def reward(self, character, kind):
        return next(r for r in self.by_id[character]['rewards'] if r['kind']==kind)

    def test_all_characters_and_pinned_conditions(self):
        source={r['id']:r for r in json.loads((ROOT/'data/achievement-source.json').read_text())}
        catalog=json.loads((DATA/'catalog/characters.json').read_text())
        self.assertEqual([r['id'] for r in self.rows],[r['id'] for r in catalog])
        self.assertEqual(len(self.rows),34)
        self.assertEqual([len(r['rewards']) for r in self.rows],[14]*17+[7]*17)
        ids=[r['id'] for c in self.rows for r in c['rewards']]
        self.assertEqual(len(ids),len(set(ids)))
        for character in self.rows:
            page=(ROOT/f"docs/characters/{character['id']}.md").read_text()
            self.assertIn('{#completion-rewards}',page)
            for reward in character['rewards']:
                self.assertEqual(reward['condition'],source[reward['id']]['condition'])
                if reward['id'] not in [77,156,172,173]:
                    self.assertTrue(reward['condition'].endswith('as '+character['en']))
                self.assertIn(f"成就 #{reward['id']}",page)
                self.assertIn(f"id=\"reward-{reward['kind']}\"",page)
                for item in reward['items']:
                    self.assertTrue((ROOT/('docs'+item['link']+'.md')).is_file())

    def test_combinations_difficulties_and_current_version_branches(self):
        for row in self.rows[17:]:
            main=self.reward(row['id'],'main-four')
            self.assertEqual(set(main['marks']),{'isaac','bluebaby','satan','lamb'})
            self.assertEqual(self.reward(row['id'],'timed-pair')['marks'],['bossrush','hush'])
            self.assertEqual(self.reward(row['id'],'greedier')['minimum'],2)
            self.assertNotIn('heart',[r['kind'] for r in row['rewards']])
        self.assertEqual(self.reward('azazel','heart')['id'],173)
        self.assertEqual(self.reward('lazarus','heart')['id'],172)
        self.assertEqual(len(self.reward('lost','all-hard')['marks']),12)
        self.assertEqual(self.reward('lost','all-hard')['minimum'],2)
        self.assertEqual(self.reward('lost','all-hard')['id'],156)
        self.assertEqual(self.reward('judas','bluebaby')['id'],77)

    def test_starting_upgrades_and_non_collectible_rewards(self):
        self.assertEqual(self.reward('keeper','isaac')['id'],236)
        key=self.reward('keeper','satan')['items'][0]['link']
        self.assertEqual(key,'/items/t83')
        items=json.loads((ROOT/'data/item-source.json').read_text())['entries']
        self.assertEqual(next(i['en'] for i in items if '/items/'+i['key']==key),'Store Key')
        self.assertEqual(self.reward('keeper','hush')['id'],191)
        self.assertIn('第三个硬币心',self.reward('keeper','hush')['notes'])
        self.assertEqual(self.reward('bluebaby','isaac')['id'],29)
        self.assertIn('表以撒',self.reward('bluebaby','isaac')['notes'])
        self.assertEqual(self.by_id['tainted-jacob']['name'],'里雅各')
        self.assertTrue(self.by_id['tainted-jacob']['en'])
        self.assertEqual({i['link'] for i in self.reward('tainted-jacob','greedier')['items']},{'/items/k74','/items/k75'})
