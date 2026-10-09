"""Meaning metadata must not swallow future senses of an existing headword."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('meaning_groups', ROOT / 'data/meaning_groups.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class MeaningGroupsTest(unittest.TestCase):
    def test_existing_equivalences_and_future_meaning(self):
        entries = json.loads((ROOT / 'data/dictionary.json').read_text())['entries']
        items = [{k: v for k, v in e.items() if k != 'meaningKey'} for e in entries if e['term'] == 'PT']
        items.append(dict(id='fixture', field='dev', term='PT', definition='자동 포함 검사용 별도 개념'))
        module.apply(items)
        self.assertEqual(items[0]['meaningKey'], items[1]['meaningKey'])
        self.assertNotEqual(items[0]['meaningKey'], items[2]['meaningKey'])

    def test_copy_and_explicit_same_concept(self):
        entries = [dict(id='a', definition='같은 뜻.'), dict(id='b', definition='같은 뜻 !')]
        module.apply(entries)
        self.assertEqual(entries[0]['meaningKey'], entries[1]['meaningKey'])
        entries.append(dict(id='c', definition='분야에 맞춰 다시 설명한 문장', meaningKey=entries[0]['meaningKey']))
        module.apply(entries)
        self.assertEqual(entries[0]['meaningKey'], entries[2]['meaningKey'])

    def test_rebuild_preserves_meanings_and_content(self):
        entries = json.loads((ROOT / 'data/dictionary.json').read_text())['entries']
        originals = json.loads(json.dumps(entries))
        for e in entries:
            del e['meaningKey']
        module.apply(entries)
        self.assertEqual(entries, originals)
        module.apply(entries)
        self.assertEqual(entries, originals)


if __name__ == '__main__':
    unittest.main()
