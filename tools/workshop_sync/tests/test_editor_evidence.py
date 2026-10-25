import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from release import changed_design_evidence

class EditorEvidenceTests(unittest.TestCase):
    def test_changed_rationale_retained_without_unrelated_documents(self):
        path = 'design/changes/vestal.md'
        a = f'diff --git a/{path} b/{path}\n@@ -4 +4 @@\n-old\n+new human rationale\n'
        b = 'diff --git a/tools/x.py b/tools/x.py\n+internal\n'
        result = changed_design_evidence(a+b, [path,'tools/x.py'])
        self.assertEqual(result, {path:a})
        self.assertEqual(changed_design_evidence(a, []), {})

    def test_multiple_hunks_and_unicode_are_not_truncated(self):
        p = 'design/changes/vestal.md'
        d = f'diff --git a/{p} b/{p}\n@@ -1 +1 @@\n+의도\n@@ -99 +99 @@\n+회피와 방어 모두\n'
        self.assertEqual(changed_design_evidence(d,[p])[p],d)
