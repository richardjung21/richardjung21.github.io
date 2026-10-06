import copy
import json
import unittest

from build import ROOT, render_site
from test_build import Page


class LocalizationTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))

    def test_language_links_metadata_and_research_are_consistent(self):
        pages = render_site(self.data)
        english, korean = Page(pages['index.html']), Page(pages['index.ko.html'])
        for page, locale, current in ((english, 'en', 'index.html'), (korean, 'ko', 'index.ko.html')):
            self.assertEqual(next(x for x in page.elements if x['tag'] == 'html')['attrs']['lang'], locale)
            switch = page.css('language-switch')
            self.assertEqual(len(switch), 1)
            links = page.css('language-link')
            self.assertEqual([x['attrs']['href'] for x in links], ['index.html', 'index.ko.html'])
            self.assertEqual(next(x for x in links if x['attrs']['aria-current'] == 'page')['attrs']['href'], current)
            alternates = [x for x in page.elements if x['attrs'].get('rel') == 'alternate']
            self.assertEqual({x['attrs']['hreflang'] for x in alternates}, {'en', 'ko'})
        for css in ('pub-authors', 'hero-stat-num'):
            self.assertEqual([x['text'] for x in english.css(css)], [x['text'] for x in korean.css(css)])
        for paper in self.data['publications']:
            if paper.get('overview'):
                self.assertIn(paper['title'], [x['text'] for x in korean.css('pub-title')])
        self.assertEqual(len(korean.css('paper-overview')), len(english.css('paper-overview')))
        self.assertEqual([x['attrs']['href'] for x in english.css('paper-image-trigger')],
                         [x['attrs']['href'] for x in korean.css('paper-image-trigger')])
        self.assertEqual(korean.css('hero-name')[0]['text'], '정승호')
        self.assertIn('심사 중 1편', korean.css('publication-summary')[0]['text'])
        self.assertTrue(any(x['text'] == '심사 중' for x in korean.css('pub-badge')))
        self.assertIn('2026년 8월 25일', [x['text'] for x in korean.css('pub-date')])
        for item in korean.css('paper-takeaway') + korean.css('timeline-desc') + korean.css('project-desc'):
            self.assertRegex(item['text'], '[가-힣]')

    def test_shared_status_edits_and_escaping_reach_korean_page(self):
        data = copy.deepcopy(self.data)
        next(p for p in data['publications'] if p['venue'] == 'WACV 2027')['status'] = 'Accepted'
        data['translations']['ko']['projects']['functional-desk']['description'] = '<script>alert("x")</script> & 새 내용'
        paper = next(p for p in data['publications'] if p['id'] == 'ma-bbdm')
        paper['overview']['results'][0]['value'] = '85.000%'
        page = Page(render_site(data)['index.ko.html'])
        self.assertIn('85.000%', page.css('paper-results')[0]['text'])
        self.assertIn('게재 승인 2편', page.css('publication-summary')[0]['text'])
        self.assertNotIn('심사 중', page.css('publication-summary')[0]['text'])
        self.assertEqual(page.css('project-desc')[0]['text'], '<script>alert("x")</script> & 새 내용')
        self.assertEqual(len([x for x in page.elements if x['tag'] == 'script']), 3)


    def test_korean_copy_is_editable_in_content_json_and_survives_reordering(self):
        data = copy.deepcopy(self.data)
        data['translations']['ko']['hero']['bio'] = '한국어 소개 수정'
        data['translations']['ko']['publications']['ma-bbdm']['overview']['takeaway'] = '한국어 논문 요약 수정'
        # Editing English prose must not discard the corresponding Korean copy.
        data['hero']['bio'] = 'Edited English introduction'
        data['publications'].reverse()
        pages = render_site(data)
        korean = Page(pages['index.ko.html'])
        self.assertEqual(korean.css('hero-bio')[0]['text'], '한국어 소개 수정')
        self.assertIn('한국어 논문 요약 수정', [x['text'] for x in korean.css('paper-takeaway')])
        self.assertEqual(Page(pages['index.html']).css('hero-bio')[0]['text'], 'Edited English introduction')
        data['publications'] = [p for p in data['publications'] if p['id'] != 'ma-bbdm']
        self.assertNotIn('한국어 논문 요약 수정', render_site(data)['index.ko.html'])


    def test_project_image_is_shared_but_caption_is_localized(self):
        pages = render_site(self.data)
        for filename in ('index.html', 'index.ko.html'):
            page = Page(pages[filename])
            disclosures = page.css('project-disclosure')
            self.assertEqual(len(disclosures), len(self.data['projects']))
            self.assertTrue(all('open' not in x['attrs'] for x in disclosures))
            trigger = page.css('project-image-trigger')[0]
            self.assertEqual(trigger['attrs']['href'], 'assets/projects/functional-desk.png')
            self.assertEqual(trigger['attrs']['data-lightbox'], 'project-functional-desk')
            self.assertEqual(len(page.css('project-full-image')), 1)
            if filename == 'index.ko.html':
                self.assertRegex(trigger['attrs']['data-alt'], '[가-힣]')
        import struct
        project = next(p for p in self.data['projects'] if p['id'] == 'functional-desk')
        figure = project['figure']
        self.assertEqual(struct.unpack('>II', (ROOT / figure['src']).read_bytes()[16:24]),
                         (figure['width'], figure['height']))
        project['figure']['src'] = 'javascript:alert(1)'
        with self.assertRaisesRegex(ValueError, 'Unsupported link scheme'):
            render_site(self.data)
