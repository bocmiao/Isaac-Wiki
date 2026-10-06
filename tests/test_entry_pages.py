import json
from pathlib import Path
import runpy
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
GEN = runpy.run_path(str(ROOT / 'scripts/generate-entry-pages.py'))
IMPORT = runpy.run_path(str(ROOT / 'scripts/import-item-source.py'))


class EntryPages(unittest.TestCase):
    def test_paired_pills_use_challenge_rewards_not_placeholder_messages(self):
        for key, reward in [('p28',227),('p29',227),('p30',228),('p31',228)]:
            self.assertEqual([row['id'] for row in GEN['unlocks'](GEN['ITEMS'][key])], [reward])
        page=(ROOT/'docs/items/p31.md').read_text()
        self.assertIn('成就 228',page)
        self.assertNotIn('里雅各',page)
        self.assertNotIn('成就 541',page)
        self.assertIn('不计入普通道具收藏页',page)
    def test_reversed_cards_do_not_change_ordinary_unlocks(self):
        def unlock(key):
            return [row['id'] for row in GEN['unlocks'](GEN['ITEMS'][key])]
        self.assertEqual(unlock('k1'), [])
        self.assertEqual(unlock('k56'), [524])
        self.assertEqual(unlock('k57'), [525])
        self.assertEqual(unlock('k29'), [327])
        self.assertEqual(unlock('k32'), [89])
        self.assertEqual(unlock('k74'), [542])
        self.assertEqual(unlock('k75'), [542])
        self.assertEqual(unlock('k77'), [544])
        self.assertEqual(unlock('p9999'), [603])

    def test_same_name_special_forms_have_distinct_pages(self):
        for key in ['c59', 'c551', 'c656', 't39', 'k29']:
            self.assertTrue((ROOT / f'docs/items/{key}.md').exists())
        belial = (ROOT / 'docs/items/c59.md').read_text()
        self.assertIn('可搭配另一件主动', belial)
        self.assertNotIn('3 格常规充能', belial)
        golden = (ROOT / 'docs/items/p9999.md').read_text()
        self.assertNotIn('| 胶囊效果 ID | 9999 |', golden)
        self.assertIn('特殊胶囊颜色', golden)

    def test_every_source_record_has_complete_detail_page(self):
        for item in GEN['ITEMS'].values():
            page = (ROOT / f'docs/items/{item["key"]}.md').read_text()
            self.assertIn('## 效果与数值', page)
            self.assertIn('## 解锁与获取', page)
            self.assertIn('## 资料来源', page)
            self.assertNotIn('{{', page)
            self.assertNotIn('<道具不存在>', page)
            if item['kind'] == 'p' and item.get('horseRepPlus'):
                self.assertIn('## 巨型胶囊', page)
        for file, prefix in [('characters', ''), ('tainted', 'tainted-')]:
            original = (ROOT / f'data/entry-guides/{file}.md').read_text()
            for profile in GEN['sections'](original):
                page = (ROOT / f'docs/characters/{prefix}{profile["id"]}.md').read_text()
                for suffix in ['build', 'combat', 'route']:
                    self.assertIn('{#' + profile['id'] + '-' + suffix + '}', page)
                self.assertIn('## 获取方式', page)
                self.assertIn('## 开局速查', page)

    def test_empty_name_comment_does_not_consume_next_record(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'names.lua'
            source.write_text('[C_ID .. 13] = "", --\n[C_ID .. 14] = "道具", -- Test Item\n')
            self.assertEqual(list(IMPORT['load_names'](source)), ['c14'])

    def test_markup_keeps_links_and_rejects_unreviewed_data(self):
        text = GEN['render_effect']('{{Collectible118}}#伤害x1.5#example')
        self.assertIn('](/items/c118)', text)
        self.assertIn('伤害×1.5', text)
        self.assertIn('example', text)
        with self.assertRaises(ValueError):
            GEN['render_effect']('{{Unreviewed}}')
        with self.assertRaises(ValueError):
            GEN['render_effect']('伤害+{1}')

    def test_legacy_character_phase_links_keep_their_section(self):
        legacy = json.loads((ROOT / 'docs/.vitepress/theme/data/catalog/legacy-links.json').read_text())
        self.assertEqual(legacy['/strategy/characters#isaac-build'], '/characters/isaac#isaac-build')
        self.assertEqual(legacy['/strategy/tainted#lost-combat'], '/characters/tainted-lost#lost-combat')
        self.assertEqual(legacy['/strategy/rooms#dice'], '/rooms/dice')
        self.assertEqual(legacy['/strategy/floors#ascent'], '/floors/ascent')

    def test_alternate_floor_keeps_shared_unlock_and_entry_costs(self):
        for floor in ['downpour', 'dross', 'mines', 'ashpit', 'mausoleum', 'gehenna', 'corpse']:
            page = (ROOT / f'docs/floors/{floor}.md').read_text()
            self.assertIn('死寂累计击败 3 次', page)
            self.assertIn('1 钥匙', page)
            self.assertIn('2 炸弹', page)

    def test_warning_prefix_does_not_repeat_punctuation(self):
        self.assertEqual(GEN['render_effect']('{{Warning}} 一次只能激活1个头目'),'注意： 一次只能激活1个头目')
        self.assertNotIn('：：',GEN['render_effect']('{{Warning}}效果'))
        self.assertIn('神圣屏障',GEN['render_effect']('{{HolyMantle}}保护'))


if __name__ == '__main__':
    unittest.main()
