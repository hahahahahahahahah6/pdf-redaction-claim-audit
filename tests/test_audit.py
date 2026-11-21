import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pdf_redaction_claim_audit.__main__ import main

from pdf_redaction_claim_audit.audit import audit, evidence, paragraphs
from pdf_redaction_claim_audit.phrases import PDFREDACTION, NOPDFREDACTION, GENERIC_NAMES
EXPECTED_YES = ('add redaction to pdf', 'adds redaction to pdf', 'adding redaction to pdf', 'apply redaction to pdf', 'applies redaction to pdf', 'applying redaction to pdf', 'redact pdf', 'redacts pdf', 'redacting pdf', 'redact pdfs', 'redacts pdfs', 'redacting pdfs', 'pdf redaction', 'pdf redactions', 'redact pdf document', 'redacts pdf document', 'redacting pdf document', 'redact pdf file', 'redacts pdf file', 'redacting pdf file', 'redact sensitive information from pdf', 'redacts sensitive information from pdf', 'redacting sensitive information from pdf', 'remove sensitive information from pdf', 'removes sensitive information from pdf', 'removing sensitive information from pdf', 'black out text in pdf', 'blacks out text in pdf', 'blacking out text in pdf', 'redact text in pdf', 'redacts text in pdf', 'redacting text in pdf', 'redact text from pdf', 'redacts text from pdf', 'redacting text from pdf', 'remove text from pdf', 'removes text from pdf', 'removing text from pdf', 'redact confidential information from pdf', 'redacts confidential information from pdf', 'redacting confidential information from pdf', 'redact personal information from pdf', 'redacts personal information from pdf', 'redacting personal information from pdf', 'redact pdf page', 'redacts pdf page', 'redacting pdf page', 'redact pdf pages', 'redacts pdf pages', 'redacting pdf pages')
EXPECTED_NO = ('no pdf redaction', 'does not redact pdf', 'does not redact pdfs', 'does not redact pdf document', 'does not redact pdf file', 'does not redact sensitive information from pdf', 'does not remove sensitive information from pdf', 'does not black out text in pdf', 'does not redact text in pdf', 'does not redact text from pdf', 'does not remove text from pdf', 'does not redact confidential information from pdf', 'does not redact personal information from pdf', 'does not redact pdf page', 'does not redact pdf pages', 'does not add redaction to pdf', 'does not apply redaction to pdf', 'no pdf redactions', 'does not support pdf redaction', 'without pdf redaction', 'pdf redaction not supported', 'no pdf redaction support', 'pdf redaction not available', 'no redact pdf')
EXPECTED_GENERIC = ('redact_pdf', 'redact_pdfs', 'redact_pdf_document', 'redact_pdf_file', 'redact_pdf_page', 'redact_pdf_pages', 'apply_redaction', 'add_redaction', 'add_redactions', 'redact_text', 'redact_sensitive_information', 'remove_sensitive_information', 'black_out_text', 'redact_document', 'redact_file', 'redact_page', 'redact_pages', 'redact_pdf_text', 'apply_pdf_redaction', 'add_pdf_redaction', 'create_redaction', 'redact_pdf_content', 'redact_confidential_information', 'redact_personal_information')

class AuditTests(unittest.TestCase):
    def test_phrase_oracle(self):
        self.assertEqual(PDFREDACTION, EXPECTED_YES)
        self.assertEqual(NOPDFREDACTION, EXPECTED_NO)
        self.assertEqual(GENERIC_NAMES, EXPECTED_GENERIC)
        self.assertEqual((len(set(EXPECTED_YES)), len(set(EXPECTED_NO)), len(set(EXPECTED_GENERIC))), (50, 24, 24))

    def test_routes(self):
        cases = [
            'from fitz import open as op\nop()\np.add_redact_annot()',
            'from fitz import Document as D\nD()\np.add_redact_annot()',
            'import fitz\nd=fitz.open()\np=d[0]\np.add_redact_annot()',
            'import fitz\nfitz.Document()\np.add_redact_annot()',
            'import pymupdf\npymupdf.open()\np.add_redact_annot()',
            'import pymupdf\npymupdf.Document()\np.add_redact_annot()',
            'from pdf_redactor import redactor as r\nr()',
            'import pdf_redactor as r\nr.redactor()',
            'from lib import redact_pdf as f\nf()',
        ] + ['x.%s()' % name for name in EXPECTED_GENERIC]
        for case in cases:
            with self.subTest(case=case): self.assertTrue(evidence(case))

    def test_not_evidence(self):
        cases = ['import '+x for x in ('fitz','pymupdf','pdf_redactor','pdfrw','pypdf','PyPDF2','pikepdf','reportlab')]
        cases += ['import fitz\nfitz.open()', 'p.add_redact_annot()', 'p.apply_redactions()', 'p.scrub()', 'redactor()', 'from pdf_redactor import RedactorOptions\nRedactorOptions()', 'from reportlab.pdfgen import canvas\ncanvas.Canvas().save()', 'def redact_pdf(): pass\nx.redact_pdf()', 'from x import redact_pdf\nredact_pdf=1\nredact_pdf()', 'import fitz\nwith x as fitz: pass\nfitz.open()\np.add_redact_annot()', 'def x(:', '"pdf redaction"', 'x.redact_pdf']
        cases += ['import fitz\nfitz.open()\np.%s()' % method for method in ('apply_redactions','save','scrub','draw_rect','set_rotation','show_pdf_page','insert_text','insert_textbox')]
        cases += ['import pypdf\npypdf.PdfWriter().%s()' % method for method in ('append','merge','add_page','encrypt','update_page_form_field_values')]
        cases += ['import pypdf\npypdf.PdfReader().%s()' % method for method in ('rotate','merge_page','extract_text','get_fields')]
        cases += ['import subprocess\nsubprocess.run([%r])' % cmd for cmd in ('qpdf','pdftk','gs')]
        cases += ['client.%s()' % method for method in ('parse','begin_analyze_document','process_document','analyze_document','universal_ai','load_data','ocr','upload','sign_pdf','signature_request_send')]
        for case in cases:
            with self.subTest(case=case): self.assertFalse(evidence(case))

    def test_audit_and_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); doc=root/'README.md'; src=root/'app.py'
            doc.write_text('pdf redaction')
            self.assertEqual(audit(root)['findings'][0]['severity'],'HIGH')
            self.assertEqual(audit(root)['findings'][0]['rule'],'documented-pdf-redaction-claim-false')
            src.write_text('x.redact_pdf()')
            self.assertEqual(audit(root)['verdict'],'PASS')
            doc.write_text('no pdf redaction')
            result=audit(root); self.assertEqual(result['findings'][0]['rule'],'documented-no-pdf-redaction-claim-false')
            src.unlink(); self.assertEqual(audit(root)['verdict'],'PASS')
            doc.write_text('pdf redaction'); tests=root/'tests'; tests.mkdir(); (tests/'test_x.py').write_text('x.redact_pdf()')
            self.assertEqual(audit(root)['findings'][0]['severity'],'MEDIUM')
            self.assertEqual(audit(root, fail_on='medium')['verdict'],'FAIL')
            for args, code in [([],0),(['--fail-on','medium'],2)]:
                p=subprocess.run([sys.executable,'-m','pdf_redaction_claim_audit','audit',str(root),'--json']+args,capture_output=True,text=True)
                self.assertEqual(p.returncode,code); self.assertIn('message',json.loads(p.stdout)['findings'][0])
            doc.write_text('```\npdf redaction\n```'); self.assertEqual(audit(root)['findings'],[])
            doc.write_text('`pdf redaction`'); self.assertTrue(audit(root)['findings'])
            doc.write_text('nothing here'); self.assertEqual(audit(root)['findings'],[])
            self.assertEqual(subprocess.run([sys.executable,'-m','pdf_redaction_claim_audit','--version'],capture_output=True,text=True).stdout.strip(),'0.1.0')

    def test_scope_ignore_and_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'README.md').write_text('pdf redaction')
            (root/'a.py').write_text('import fitz\nfitz.open()')
            (root/'b.py').write_text('p.add_redact_annot()')
            self.assertEqual(audit(root)['verdict'],'FAIL')
            (root/'a.py').write_text('x.redact_pdf()')
            self.assertEqual(audit(root,ignore=['a.py'])['verdict'],'FAIL')
            (root/'a.py').rename(root/'target.txt'); (root/'a.py').symlink_to(root/'target.txt')
            self.assertEqual(audit(root)['verdict'],'FAIL')

    def test_console_main_and_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'README.md').write_text('pdf redaction')
            with redirect_stdout(StringIO()) as out:
                self.assertEqual(main(['audit', str(root), '--json']), 2)
            self.assertEqual(json.loads(out.getvalue())['verdict'], 'FAIL')
            with redirect_stdout(StringIO()) as out:
                with self.assertRaises(SystemExit) as caught:
                    main(['--version'])
            self.assertEqual(caught.exception.code, 0)
            self.assertEqual(out.getvalue().strip(), '0.1.0')

    def test_denial_normalization_and_exclusions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'README.md').write_text("Doesn't redact PDF.\n\n~~~\npdf redaction\n~~~")
            result = audit(root)
            self.assertEqual(result['claims'], [])
            self.assertEqual(result['denials'], ['README.md'])
            for directory in ('fixtures', 'docs', 'examples'):
                folder = root / directory
                folder.mkdir()
                (folder / 'source.py').write_text('x.redact_pdf()')
            self.assertEqual(audit(root)['production_evidence'], [])

    def test_readme_self_audit(self):
        self.assertEqual(audit(Path(__file__).resolve().parents[1])['findings'], [])

if __name__ == '__main__': unittest.main()
