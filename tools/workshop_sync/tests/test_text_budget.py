import unittest
from text_budget import byte_size,merge_repair

class BudgetTests(unittest.TestCase):
    def test_utf8_and_crlf(self):
        self.assertEqual(byte_size('한\n가'),8)
        self.assertEqual(byte_size('한\r\n가'),8)

    def test_only_requested_language_and_original_passage_can_change(self):
        patches=[dict(language='english',old_text='a',new_text='b'),dict(language='russian',old_text='c',new_text='long')]
        repaired=[dict(language='russian',old_text='c',new_text='short')]
        result=merge_repair(patches,repaired,{'russian'})
        self.assertEqual(result[0],patches[0]);self.assertEqual(patches[1]['new_text'],'long')
        repaired[0]['old_text']='unrelated'
        with self.assertRaises(ValueError):merge_repair(patches,repaired,{'russian'})

    def test_missing_or_extra_patch_is_rejected(self):
        patch=dict(language='russian',old_text='a',new_text='b')
        for repaired in ([],[patch,patch]):
            with self.assertRaises(ValueError):merge_repair([patch],repaired,{'russian'})
