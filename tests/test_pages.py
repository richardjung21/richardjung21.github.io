import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import urlsplit

from build import ROOT, render_site
from test_build import Page


class PageTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT/'content.json').read_text(encoding='utf-8'))

    def test_cover_flows_into_all_sections_and_every_internal_link_resolves(self):
        pages = {name: Page(html) for name, html in render_site(self.data).items()}
        home = pages['index.html']
        self.assertEqual(len(home.css('hero-name')), 1)
        self.assertEqual(len(home.css('pub-card')), len(self.data['publications']))
        self.assertEqual(len(home.css('project-card')), len(self.data['projects']))
        section_ids = [x['attrs']['id'] for x in home.elements if x['tag'] == 'section']
        self.assertEqual(section_ids, ['hero', *[s['id'] for s in self.data['sections']]])
        for filename, page in pages.items():
            with self.subTest(page=filename):
                self.assertEqual(len([x for x in page.elements if x['tag'] == 'h1']), 1)
                self.assertEqual(len([x for x in page.elements if x['tag'] == 'main']), 1)
                for element in page.elements:
                    if element['tag'] not in ('a', 'img', 'script', 'link'):
                        continue
                    href = element['attrs'].get('href') or element['attrs'].get('src') or ''
                    url = urlsplit(href)
                    if url.scheme or url.netloc:
                        continue
                    target = pages.get(url.path or filename)
                    if url.path.endswith('.html'):
                        self.assertIsNotNone(target, href)
                    elif url.path:
                        self.assertTrue((ROOT/url.path).is_file(), href)
                    if url.fragment:
                        ids = {x['attrs'].get('id') for x in target.elements}
                        self.assertIn(url.fragment, ids)

    def test_old_page_urls_redirect_to_the_correct_section(self):
        for filename, html in render_site(self.data).items():
            page = Page(html)
            expected_url = self.data['profile']['site_url']
            canonical = next(x for x in page.elements if x['attrs'].get('rel') == 'canonical')
            self.assertEqual(canonical['attrs']['href'], expected_url)
            if filename != 'index.html':
                refresh = next(x for x in page.elements if x['attrs'].get('http-equiv') == 'refresh')
                destination = 'index.html#'+filename.removesuffix('.html')
                self.assertEqual(refresh['attrs']['content'], '0; url='+destination)
                self.assertTrue(any(x['attrs'].get('href') == destination for x in page.elements))

    def test_check_detects_stale_subpage_without_overwriting_it(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            shutil.copy2(ROOT/'build.py', root/'build.py')
            shutil.copy2(ROOT/'content.json', root/'content.json')
            shutil.copytree(ROOT/'templates', root/'templates')
            built = subprocess.run([sys.executable, '-B', str(root/'build.py')], capture_output=True, text=True)
            self.assertEqual(built.returncode, 0, built.stderr)
            (root/'contact.html').write_text('Stale page', encoding='utf-8')
            checked = subprocess.run([sys.executable, '-B', str(root/'build.py'), '--check'], capture_output=True, text=True)
            self.assertEqual(checked.returncode, 1)
            self.assertIn('contact.html', checked.stderr)
            self.assertEqual((root/'contact.html').read_text(encoding='utf-8'), 'Stale page')
