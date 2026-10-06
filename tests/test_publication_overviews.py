import copy
import json
import unittest

from build import ROOT, author_position, render, publication_groups
from test_build import Page


class PublicationOverviewTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))
        self.overview_count = sum(bool(p.get('overview')) for p in self.data['publications'])

    def test_author_groups_preserve_every_paper_and_date_order(self):
        page = Page(render(self.data))
        groups = page.css('pub-group')
        self.assertEqual([x['text'] for x in page.css('pub-group-title')],
                         ['First-author papers', 'Second-author papers'])
        for venue in ('ICISPC 2026', 'ICCRD 2026', 'ITC-CSCC 2025', 'Upcoming'):
            self.assertIn(venue, groups[0]['text'])
        self.assertIn('Sensors 2024', groups[1]['text'])
        self.assertIn('ECML PKDD 2026', groups[1]['text'])
        self.assertNotIn('Author 3 of 6', groups[1]['text'])
        self.assertLess(groups[1]['text'].index('ECML'), groups[1]['text'].index('Sensors'))
        self.assertEqual(len(page.css('pub-card')), len(self.data['publications']))
        self.assertLess(groups[0]['text'].index('ICISPC'), groups[0]['text'].index('ICCRD'))
        self.assertLess(groups[0]['text'].index('ICCRD'), groups[0]['text'].index('ITC-CSCC'))

    def test_author_order_is_derived_and_spacing_variants_match(self):
        paper = copy.deepcopy(self.data['publications'][0])
        paper['authors'] = ['Coauthor', 'Seungho Jung']
        self.assertEqual(author_position(paper, 'Seung Ho Jung'), 2)
        grouped = Page(publication_groups([paper], 'Seung Ho Jung'))
        self.assertEqual(grouped.css('pub-group-title')[0]['text'], 'Second-author papers')
        self.assertEqual(grouped.css('pub-author-self')[0]['text'], 'Seungho Jung')
        paper['authors'] = ['Unrelated Author']
        with self.assertRaisesRegex(ValueError, 'matching publication author'):
            publication_groups([paper], 'Seung Ho Jung')

    def test_all_supplied_papers_have_summaries_and_local_figures_without_pdf_links(self):
        page = Page(render(self.data))
        self.assertEqual(len(page.css('paper-overview')), self.overview_count)
        self.assertEqual(len(page.css('paper-figure-details')), self.overview_count)
        self.assertEqual(len(page.css('paper-results')), self.overview_count)
        publications = Page(publication_groups(self.data['publications'], self.data['profile']['publication_name']))
        self.assertFalse(any('.pdf' in x['attrs'].get('href', '').lower() for x in publications.elements))
        self.assertNotIn('assets/papers/', render(self.data))
        for paper in self.data['publications']:
            overview = paper.get('overview')
            if overview:
                self.assertTrue((ROOT / overview['source']['file']).is_file())
                self.assertTrue((ROOT / overview['figure']['src']).is_file())
                self.assertTrue(overview['figure']['alt'])
                self.assertEqual(len(overview['method']), 3)
        for paper in self.data['publications']:
            if not paper.get('overview'):
                card = next(c for c in page.css('pub-card') if paper['title'] in c['text'])
                self.assertNotIn('At a glance', card['text'])

    def test_summary_edits_are_escaped_and_optional(self):
        paper = self.data['publications'][0]
        paper['overview']['takeaway'] = '<script> & editable summary'
        page = Page(render(self.data))
        self.assertTrue(any(x['text'] == '<script> & editable summary' for x in page.css('paper-takeaway')))
        self.assertEqual(len([x for x in page.elements if x['tag'] == 'script']), 3)
        del paper['overview']
        self.assertEqual(len(Page(render(self.data)).css('paper-overview')), self.overview_count - 1)

    def test_figure_sources_reject_executable_urls(self):
        self.data['publications'][0]['overview']['figure']['src'] = 'javascript:alert(1)'
        with self.assertRaisesRegex(ValueError, 'Unsupported link scheme'):
            render(self.data)

    def test_confirmed_author_position_overrides_byline_order(self):
        paper = next(p for p in self.data['publications'] if p['venue'] == 'ECML PKDD 2026')
        self.assertEqual(author_position(paper, 'Seung Ho Jung'), 2)
        del paper['author_position']
        self.assertEqual(author_position(paper, 'Seung Ho Jung'), 3)
        for invalid in (0, -1, 7, True, '2'):
            paper['author_position'] = invalid
            with self.assertRaisesRegex(ValueError, 'Invalid author_position'):
                author_position(paper, 'Seung Ho Jung')

    def test_replacement_image_and_full_resolution_links(self):
        self.assertEqual((ROOT/'assets/research/quadtree.png').read_bytes(),
                         (ROOT/'assets/papers/Qualitative_Comparison.png').read_bytes())
        page = Page(render(self.data))
        self.assertEqual(len(page.css('paper-full-image')), self.overview_count)
        for paper in self.data['publications']:
            figure = paper.get('overview', {}).get('figure')
            if not figure:
                continue
            import struct
            size = struct.unpack('>II', (ROOT/figure['src']).read_bytes()[16:24])
            self.assertEqual(size, (figure['width'], figure['height']))

    def test_figures_open_individually_instead_of_a_shared_gallery(self):
        page = Page(render(self.data))
        triggers = page.css('paper-image-trigger')
        groups = [item['attrs']['data-lightbox'] for item in triggers]
        self.assertEqual(len(groups), self.overview_count)
        self.assertEqual(len(set(groups)), self.overview_count)
        self.assertTrue(all('data-lightbox' not in item['attrs'] for item in page.css('paper-full-image')))

    def test_summary_and_figure_share_one_closed_disclosure(self):
        page = Page(render(self.data))
        disclosures = page.css('paper-figure-details')
        self.assertEqual(len(disclosures), self.overview_count)
        self.assertEqual(len([x for x in disclosures if x['tag'] == 'details']), self.overview_count)
        for disclosure in disclosures:
            self.assertEqual(disclosure['tag'], 'details')
            self.assertNotIn('open', disclosure['attrs'])
            self.assertIn('At a glance & figure', disclosure['text'])
            self.assertIn('Enlarge figure', disclosure['text'])
        for paper in self.data['publications']:
            if 'overview' in paper:
                self.assertTrue(any(paper['overview']['takeaway'] in d['text'] for d in disclosures))
