"""Keep authored guides connected to the pinned facts they claim to use."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return json.loads((ROOT / 'data' / name).read_text())


class ReferenceSources(unittest.TestCase):
    def test_boss_source_coverage_and_distinct_records(self):
        guides = {row['id']: row for row in read('boss-guides.json')}
        source = read('boss-state-source.json')
        self.assertEqual(set(guides), set(source['bosses']))
        self.assertRegex(source['isaacDocsCommit'], r'^[a-f0-9]{40}$')
        for ident, row in guides.items():
            with self.subTest(boss=ident):
                facts = source['bosses'][ident]
                self.assertEqual(row['sourceFile'], facts['file'])
                self.assertTrue(row['attacks'])
                for attack in row['attacks']:
                    self.assertTrue(all(attack.get(key) for key in ['attack', 'tell', 'response']))
                self.assertTrue(facts['blocks'])
                for block in facts['blocks']:
                    self.assertGreater(block['startLine'], 0)
                    self.assertGreaterEqual(block['endLine'], block['startLine'])
                    self.assertTrue(block['attacks'])
        self.assertIn('lokii', guides['loki']['related'])
        self.assertIn('loki', guides['lokii']['related'])
        self.assertNotEqual(guides['loki']['summary'], guides['lokii']['summary'])
        self.assertEqual(guides['baby-plum']['achievement'], 410)

    def test_pickup_entity_variants_match_subtype_families(self):
        source = read('pickup-enum-source.json')
        enums = source['enums']
        variants = enums['PickupVariant']
        families = {
            'HeartSubType': {variants['PICKUP_HEART']},
            'CoinSubType': {variants['PICKUP_COIN']},
            'KeySubType': {variants['PICKUP_KEY']},
            'BombSubType': {variants['PICKUP_BOMB']},
            'BatterySubType': {variants['PICKUP_LIL_BATTERY']},
            'ChestSubType': {value for key, value in variants.items()
                             if key in {'PICKUP_CHEST', 'PICKUP_BOMBCHEST', 'PICKUP_SPIKEDCHEST',
                                        'PICKUP_MIMICCHEST', 'PICKUP_OLDCHEST', 'PICKUP_WOODENCHEST',
                                        'PICKUP_MEGACHEST', 'PICKUP_HAUNTEDCHEST', 'PICKUP_LOCKEDCHEST',
                                        'PICKUP_REDCHEST'}},
        }
        items = read('item-source.json')['entries']
        for row in read('pickup-guides.json'):
            with self.subTest(pickup=row['id']):
                self.assertTrue(row['steps'] and row['pitfall'])
                if 'entity' not in row:
                    self.assertEqual(row['id'], 'golden-trinket')
                    continue
                entity = row['entity']
                self.assertIn(entity['variant'], families[entity['source']])
                self.assertEqual(entity['subtype'], enums[entity['source']][entity['enum']])
                if entity['source'] == 'ChestSubType':
                    self.assertEqual(entity['enum'], 'CHEST_CLOSED')
                if row.get('pool'):
                    self.assertTrue(any(row['pool'] in item['poolsRepSnapshot'] for item in items))


if __name__ == '__main__':
    unittest.main()
