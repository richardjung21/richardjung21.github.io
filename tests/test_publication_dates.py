import copy
import itertools
import unittest

from build import publication_date, sorted_publications


class PublicationDateTests(unittest.TestCase):
    def paper(self, title, value='', **extra):
        return {'title': title, 'date': value, 'venue': 'Conference',
                'authors': ['Author'], 'status': 'Published', **extra}

    def test_sorting_is_independent_of_input_order_and_featured_status(self):
        papers = [self.paper('Older featured', '2024-09-21', featured=True),
                  self.paper('Newest', '2026-07-12', status='Accepted'),
                  self.paper('Middle', 'May 12, 2026'),
                  self.paper('Upcoming', '', status='In Progress')]
        for permutation in itertools.permutations(papers):
            self.assertEqual([p['title'] for p in sorted_publications(permutation)],
                             ['Newest', 'Middle', 'Older featured', 'Upcoming'])
        original = copy.deepcopy(papers)
        sorted_publications(papers)
        self.assertEqual(papers, original)

    def test_partial_dates_and_ties(self):
        papers = [self.paper('Year only', '2026'), self.paper('Previous year', '2025-12-31'),
                  self.paper('Month only', '2026-05'), self.paper('Z title', '2026-05-01'),
                  self.paper('A title', '2026-05-01'), self.paper('Undated', 'TBA')]
        expected = ['A title', 'Z title', 'Month only', 'Year only', 'Previous year', 'Undated']
        self.assertEqual([p['title'] for p in sorted_publications(papers)], expected)
        self.assertEqual([p['title'] for p in sorted_publications(reversed(papers))], expected)

    def test_normalized_display_without_inventing_precision(self):
        cases = [('2026-07-12', (2026, 7, 12), 'July 12, 2026'),
                 ('July 12, 2026', (2026, 7, 12), 'July 12, 2026'),
                 ('2026-07', (2026, 7, 0), 'July 2026'),
                 ('2026', (2026, 0, 0), '2026'),
                 ('To be announced', (0, 0, 0), 'To be announced'),
                 ('', (0, 0, 0), '')]
        for value, calendar, label in cases:
            with self.subTest(value=value):
                self.assertEqual(publication_date(self.paper('Paper', value)), (calendar, label))
        paper = self.paper('No date')
        del paper['date']
        self.assertEqual(publication_date(paper), ((0, 0, 0), ''))

    def test_invalid_calendar_dates_fail_with_paper_title(self):
        for value in ('2026-02-29', '2026-13', '2026-00', '2026-01-00',
                      '2026-1-2', 'July 32, 2026', '07/12/2026', '0000', None):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'Broken paper'):
                publication_date(self.paper('Broken paper', value))
        self.assertEqual(publication_date(self.paper('Leap year', '2024-02-29'))[0], (2024, 2, 29))
