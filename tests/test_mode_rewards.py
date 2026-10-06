import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class ModeRewards(unittest.TestCase):
    def setUp(self):
        self.rows=json.loads((ROOT/'docs/.vitepress/theme/data/mode-rewards.json').read_text())
        self.by_id={row['id']:row for row in self.rows}

    def test_character_specific_rewards_match_pinned_boss_conditions(self):
        source={row['id']:row for row in json.loads((ROOT/'data/achievement-source.json').read_text())}
        self.assertEqual(len(self.rows),34)
        self.assertEqual(sum(r['greed'] is not None for r in self.rows),17)
        self.assertEqual(sum(r['greedier'] is not None for r in self.rows),34)
        for row in self.rows:
            for mode,boss in [('greed','Ultra Greed'),('greedier','Ultra Greedier')]:
                reward=row[mode]
                if reward:
                    self.assertEqual(source[reward['id']]['condition'],f"Defeat {boss} as {row['en']}")
                    for item in reward['items']:
                        self.assertTrue((ROOT/('docs'+item['link']+'.md')).is_file())

    def test_reversed_cards_and_shared_reward_do_not_include_unrelated_pills(self):
        jacob=self.by_id['tainted-jacob']['greedier']
        self.assertEqual(jacob['id'],542)
        self.assertEqual({x['link'] for x in jacob['items']},{'/items/k74','/items/k75'})
        self.assertEqual([x['link'] for x in self.by_id['tainted-isaac']['greedier']['items']],['/items/k73'])
        for row in self.rows[17:]:
            self.assertIsNone(row['greed'])
            self.assertTrue(all('?' in item['en'] for item in row['greedier']['items']))

    def test_formerly_missing_characters_and_character_reward(self):
        for character,ident in [('apollyon',316),('forgotten',399),('bethany',422),('jacob',434)]:
            self.assertEqual(self.by_id[character]['greed']['id'],ident)
        self.assertEqual(self.by_id['azazel']['greed']['items'][0]['link'],'/characters/lilith')
