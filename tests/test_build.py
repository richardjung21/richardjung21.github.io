import copy
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build import ROOT, render_site


def render(data):
    return render_site(data)['index.html']


class Page(HTMLParser):
    """Check balanced markup while recording content and attributes."""
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.stack = []
        self.feed(html)
        assert not self.stack, self.stack

    def handle_starttag(self, tag, attrs):
        item = {'tag': tag, 'attrs': dict(attrs), 'text': ''}
        self.elements.append(item)
        if tag not in ('meta', 'link', 'img', 'br', 'hr', 'input'):
            self.stack.append(item)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        assert self.stack.pop()['tag'] == tag, tag

    def handle_data(self, text):
        for item in self.stack:
            item['text'] += text

    def css(self, name):
        return [x for x in self.elements if name in x['attrs'].get('class', '').split()]


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT/'content.json').read_text(encoding='utf-8'))

    def test_gpa_updates_both_locations(self):
        self.data['education'][0].update(gpa='4.37', gpa_max='4.7')
        page = Page(render(self.data))
        self.assertEqual(page.css('hero-stat-num')[1]['text'], '4.37')
        self.assertEqual(page.css('hero-stat-label')[1]['text'], 'GPA / 4.7')
        self.assertIn('GPA 4.37/4.7', page.css('edu-detail')[0]['text'])

    def test_publication_status_updates_all_summaries(self):
        next(p for p in self.data['publications'] if p['venue'] == 'ECML PKDD 2026')['status'] = 'Accepted'
        self.data['publications'][-1]['status'] = 'Published'
        page = Page(render(self.data))
        self.assertEqual(page.css('hero-stat-num')[0]['text'], '4')
        self.assertIn('4 published papers and 2 accepted papers', page.css('about-bio')[1]['text'])
        meta = next(x for x in page.elements if x['attrs'].get('property') == 'og:description')
        self.assertIn('4 published papers', meta['attrs']['content'])
        self.assertEqual(len(page.css('pub-card-upcoming')), 0)

    def test_add_remove_and_optional_dates(self):
        item = copy.deepcopy(self.data['publications'][0])
        item.pop('date')
        self.data['publications'] = [item]
        self.data['projects'] = []
        page = Page(render(self.data))
        self.assertEqual(len(page.css('pub-card')), 1)
        self.assertEqual(len(page.css('pub-date')), 0)
        self.assertEqual(len(page.css('project-card')), 0)
        self.assertIn('With 1 published paper,', page.css('about-bio')[1]['text'])
        self.data['publications'] = []
        page = Page(render(self.data))
        self.assertEqual(page.css('hero-stat-num')[0]['text'], '0')

    def test_shared_name_photo_and_email_and_text_escaping(self):
        name = 'A & B <Researcher>'
        self.data['profile'].update(name=name, photo='assets/new.jpg')
        self.data['contact']['links'][0]['value'] = 'new@example.com'
        self.data['projects'][0]['title'] = '<script>alert("test")</script>'
        page = Page(render(self.data))
        self.assertEqual(page.css('hero-name')[0]['text'], name)
        self.assertIn(name, page.css('about-bio')[0]['text'])
        photos = [x for x in page.elements if x['tag'] == 'img' and x['attrs'].get('src') == 'assets/new.jpg']
        self.assertTrue(photos)
        self.assertTrue(all(x['attrs']['src'] == 'assets/new.jpg' and x['attrs']['alt'] == name for x in photos))
        self.assertEqual(page.css('contact-link')[0]['attrs']['href'], 'mailto:new@example.com')
        self.assertEqual(page.css('contact-link-value')[0]['text'], 'new@example.com')
        self.assertEqual(len([x for x in page.elements if x['tag']=='script']), 3)

    def test_navigation_and_animation_hooks(self):
        page = Page(render(self.data))
        ids = {x['attrs']['id'] for x in page.elements if 'id' in x['attrs']}
        for item in page.elements:
            href = item['attrs'].get('href', '')
            if href.startswith('#'):
                self.assertIn(href[1:], ids)
        for css in ('pub-card', 'project-card', 'timeline-item'):
            self.assertTrue(all('reveal-item' in x['attrs']['class'] for x in page.css(css)))
        self.assertEqual(len(page.css('reveal-section')), 6)

    def test_invalid_status_and_featured_degree_fail(self):
        self.data['publications'][0]['status'] = 'Typo'
        with self.assertRaisesRegex(ValueError, 'publication status'):
            render(self.data)
        self.data['publications'] = []
        self.data['profile']['featured_education'] = 'missing'
        with self.assertRaisesRegex(ValueError, 'featured_education'):
            render(self.data)

    def test_research_statuses_and_editable_topics(self):
        next(p for p in self.data['publications'] if p['venue'] == 'ECML PKDD 2026')['status'] = 'Accepted'
        self.data['hero']['research_interests'] = ['New research topic']
        self.data['profile']['photo_caption'] = 'Updated caption'
        page = Page(render(self.data))
        self.assertEqual(page.css('research-topic')[0]['text'], 'New research topic')
        self.assertIn('3 published · 2 accepted · 1 in progress', page.css('publication-summary')[0]['text'])
        self.assertEqual(len(page.css('accepted')), 2)
        self.assertIn('Updated caption', page.css('hero-visual')[0]['text'])

    def test_accessible_landmarks_and_navigation_order(self):
        for filename, html in {'index.html': render(self.data)}.items():
            with self.subTest(page=filename):
                page = Page(html)
                ids = [x['attrs']['id'] for x in page.elements if 'id' in x['attrs']]
                self.assertEqual(len(ids), len(set(ids)))
                for element in page.elements:
                    for reference in element['attrs'].get('aria-labelledby', '').split():
                        self.assertIn(reference, ids)
                self.assertEqual([x['attrs']['data-section'] for x in page.css('nav-link')],
                                 ['hero', *[x['id'] for x in self.data['sections']]])
                active = [x for x in page.css('nav-link') if x['attrs'].get('aria-current') == 'location']
                self.assertEqual(len(active), 1)
                self.assertEqual(active[0]['attrs']['href'], '#hero')
                self.assertNotIn('hidden', page.css('nav-drawer')[0]['attrs'])

    def test_hero_github_uses_shared_contact_value(self):
        contact = next(x for x in self.data['contact']['links'] if x['label'] == 'GitHub')
        contact['value'] = 'updated-account'
        page = Page(render(self.data))
        github = [x for x in page.elements if x['tag'] == 'a' and x['attrs'].get('href') == 'https://github.com/updated-account']
        self.assertEqual(len(github), 2)

    def test_optional_resource_links_and_project_details(self):
        project = self.data['projects'][0]
        project['links'] = [{'label': 'Code & docs', 'url': 'https://example.com/code?a=1&b=2'}]
        project['details'] = [{'label': 'Implementation', 'text': '<script> is plain text'}]
        self.data['publications'][0]['links'] = [{'label': 'Paper', 'url': 'assets/paper.pdf'}]
        page = Page(render(self.data))
        self.assertEqual(len(page.css('resource-link')), 2)
        self.assertEqual({x['text'] for x in page.css('resource-link')}, {'Code & docs', 'Paper'})
        self.assertIn('<script> is plain text', page.css('project-details')[0]['text'])
        project.pop('links')
        project.pop('details')
        page = Page(render(self.data))
        self.assertEqual(len(page.css('resource-link')), 1)

    def test_resource_links_reject_executable_urls(self):
        self.data['publications'][0]['links'] = [{'label': 'Paper', 'url': 'javascript:alert(1)'}]
        with self.assertRaisesRegex(ValueError, 'Unsupported link scheme'):
            render(self.data)

    def test_shared_academic_profile(self):
        self.data['education'][0]['degree'] = 'Updated degree'
        self.data['hero']['research_interests'] = [{'title': 'Model adaptation', 'description': 'Models for medical images.'}]
        page = Page(render(self.data))
        self.assertIn('Updated degree', page.css('hero-education')[0]['text'])
        self.assertIn('Updated degree', page.css('edu-degree')[0]['text'])
        self.assertEqual(page.css('research-area-description')[0]['text'], 'Models for medical images.')
        self.assertTrue(all(x['text'] == 'Seung Ho Jung' for x in page.css('pub-author-self')))

    def test_rendered_publication_order_survives_json_reordering(self):
        original = copy.deepcopy(self.data)
        before = Page(render(self.data))
        self.data['publications'].reverse()
        after = Page(render(self.data))
        self.assertEqual([x['text'] for x in before.css('pub-title')],
                         [x['text'] for x in after.css('pub-title')])
        self.assertEqual(before.css('publication-summary'), after.css('publication-summary'))
        self.assertEqual(self.data['publications'], list(reversed(original['publications'])))


if __name__ == '__main__':
    unittest.main()
