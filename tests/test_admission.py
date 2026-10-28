import base64
import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

SRC = Path(__file__).resolve().parents[1] / "scripts" / "admission.py"
spec = importlib.util.spec_from_file_location("admission", SRC)
admission = importlib.util.module_from_spec(spec)
spec.loader.exec_module(admission)


class FormTests(unittest.TestCase):
    def setUp(self):
        self.user = {"login": "creator-alpha", "id": 1234}
        self.form = {
            "name": "Projeto Aurora", "slug": "aurora",
            "story": "Uma história detalhada sobre um projeto independente que resolve problemas reais e tem visão de futuro. Este texto tem tamanho suficiente.",
            "audience": "Criadores independentes e pequenas empresas de tecnologia.",
            "repo": "https://github.com/creator-alpha/aurora",
            "contact": "contato@aurora.com", "externals": "Nenhum",
            "declarations": "- [x] Aceito\n- [X] Autorizo\n- [x] Confirmo",
        }

    def test_valid_form(self):
        self.assertEqual(admission.validate_form(self.form, self.user), [])

    def test_bad_slug_and_owner(self):
        data = dict(self.form, slug="admin", repo="https://github.com/other/repo")
        self.assertEqual(len(admission.validate_form(data, self.user)), 2)

    def test_strict_repo_urls(self):
        for url in ("https://evil.com/o/r", "https://github.com/o/r/tree/main",
                    "https://github.com/o/r?tab=readme", "https://github.com@evil.com/o/r",
                    "http://github.com/o/r"):
            self.assertIsNone(admission.get_gh_repo_url(url))

    def test_parse_form(self):
        body = "\n".join("### " + label + "\n\n" + self.form[k]
                         for k, label in admission.FIELDS.items())
        self.assertEqual(admission.parse_form(body), self.form)

    def test_unchecked_declarations(self):
        data = dict(self.form, declarations="- [x] Sim\n- [ ] Não\n- [x] Sim")
        self.assertTrue(any("declarações" in msg for msg in admission.validate_form(data, self.user)))


class ScannerTests(unittest.TestCase):
    def test_remote_scripts_are_flagged(self):
        result = admission.scan_file("index.html", '<script src="https://cdn.example.com/a.js"></script>')
        self.assertTrue(any(f["severity"] == "high" for f in result))

    def test_external_google_fonts_link_is_flagged(self):
        html = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans">'
        results = admission.scan_file("index.html", html)
        self.assertTrue(any("recurso externo" in f["message"] for f in results))

    def test_external_media_is_flagged(self):
        html = '<img src="https://cdn.example.org/banner.png" alt="Banner">'
        results = admission.scan_file("index.html", html)
        self.assertTrue(any("Mídia" in f["message"] for f in results))

    def test_css_import_is_flagged(self):
        css = '@import url("https://fonts.googleapis.com/css2?family=DM+Sans");'
        results = admission.scan_file("style.css", css)
        self.assertTrue(any("Importação CSS" in f["message"] for f in results))

    def test_storage_is_flagged(self):
        result = admission.scan_file("app.js", "localStorage.setItem('x','y')")
        self.assertTrue(any("origem" in f["message"] for f in result))

    def test_basic_html(self):
        self.assertEqual(admission.scan_file("index.html", "<h1>Olá</h1>"), [])

    def test_snapshot_fixes_commit_sha(self):
        html = b"<html><h1>Projeto</h1></html>"
        replies = [
            {"visibility": "public", "default_branch": "main", "archived": False},
            {"sha": "a" * 40, "commit": {"tree": {"sha": "b" * 40}}},
            {"tree": [{"path": "index.html", "type": "blob", "size": len(html), "sha": "c" * 40}]},
            {"content": base64.b64encode(html).decode(), "encoding": "base64"},
        ]
        with patch.object(admission, "api_path", side_effect=replies) as mock:
            result = admission.repo_snapshot("creator-alpha", "aurora")
        self.assertEqual(result["commit_sha"], "a" * 40)
        self.assertEqual(result["files"], 1)
        self.assertEqual(mock.call_count, 4)
        self.assertEqual(result["findings"], [])


if __name__ == "__main__":
    unittest.main()
