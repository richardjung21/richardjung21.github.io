"""Generate the static portfolio: python build.py (Python 3.9+, no packages)."""
import argparse
import json
import re
from datetime import date
from html import escape
from pathlib import Path
from string import Template
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parent
MONTHS = ('January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December')
MONTH_NUMBERS = {name.lower(): number for number, name in enumerate(MONTHS, 1)}
PAGE_FILES = {page: ('index.html' if page == 'home' else page+'.html')
              for page in ('home', 'publications', 'about', 'experience', 'projects', 'skills', 'contact')}


def page_link(href):
    """Normalize links to the continuous portfolio's section anchors."""
    for page, filename in PAGE_FILES.items():
        if href == filename:
            return '#hero' if page == 'home' else '#'+page
    return href


def publication_date(item):
    """Return chronological components and a consistently formatted label.

    Zero month/day represents unknown precision, not an invented calendar date.
    """
    value = item.get('date', '')
    if not isinstance(value, str):
        raise ValueError(f'Publication date must be a string for {item["title"]!r}')
    value = value.strip()
    if value.lower() in ('', 'to be announced', 'tba'):
        return (0, 0, 0), value
    iso = re.fullmatch(r'(\d{4})(?:-(\d{2})(?:-(\d{2}))?)?', value)
    try:
        if iso:
            year = int(iso[1])
            month = int(iso[2]) if iso[2] is not None else None
            day = int(iso[3]) if iso[3] is not None else None
        else:
            english = re.fullmatch(r'([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})', value)
            if not english or english[1].lower() not in MONTH_NUMBERS:
                raise ValueError('use YYYY-MM-DD, YYYY-MM, YYYY, or leave it empty')
            year, month, day = int(english[3]), MONTH_NUMBERS[english[1].lower()], int(english[2])
        date(year, month if month is not None else 1, day if day is not None else 1)
    except ValueError as error:
        raise ValueError(f'Invalid publication date {value!r} for {item["title"]!r}: {error}') from error
    label = str(year)
    if month is not None:
        label = f'{MONTHS[month-1]} {day}, {year}' if day is not None else f'{MONTHS[month-1]} {year}'
    return (year, month or 0, day or 0), label


def sorted_publications(papers):
    def key(item):
        calendar, _ = publication_date(item)
        return (*(-part for part in calendar), item['title'].casefold(),
                item['venue'].casefold(), tuple(item['authors']), item['status'])
    return sorted(papers, key=key)


def e(value):
    return escape(str(value), quote=True)


def tag(name, css, content, **attrs):
    attributes = {'class': css, **attrs}
    return f'<{name}' + ''.join(f' {k}="{e(v)}"' for k, v in attributes.items() if v) + f'>{content}</{name}>'


def span(css, value):
    return tag('span', css, e(value))


def safe_url(value):
    if urlsplit(value).scheme.lower() not in ('', 'https', 'http', 'mailto'):
        raise ValueError(f'Unsupported link scheme: {value!r}')
    return value


def resource_links(item):
    """Only show paper, repository, or demo links supplied in the content file."""
    links = item.get('links', [])
    if not links:
        return ''
    return tag('div', 'resource-links', ''.join(
        tag('a', 'resource-link', e(link['label']), href=safe_url(link['url']))
        for link in links))


def project_details(item):
    details = item.get('details', [])
    if not details:
        return ''
    return tag('dl', 'project-details', ''.join(
        tag('div', 'project-detail', tag('dt', '', e(detail['label']))+
            tag('dd', '', e(detail['text']))) for detail in details))


def research_interests(items):
    areas = []
    for item in items:
        title = item if isinstance(item, str) else item['title']
        description = '' if isinstance(item, str) else item.get('description', '')
        areas.append(tag('article', 'research-area', tag('h3', 'research-topic', e(title))+
            (tag('p', 'research-area-description', e(description)) if description else '')))
    return ''.join(areas)


def publication_card(item, author_name):
    _, date_label = publication_date(item)
    status = {'In Progress': 'upcoming', 'Accepted': 'accepted', 'Published': 'published'}[item['status']]
    authors = ', '.join(tag('strong', 'pub-author-self', e(name)) if name == author_name else e(name)
                        for name in item['authors'])
    return tag('article', 'pub-card reveal-item'+(' pub-card-upcoming' if status == 'upcoming' else '')+
        (' pub-card-featured' if item.get('featured') else ''),
        (span('pub-feature-label', 'Selected publication') if item.get('featured') else '')+
        tag('div', 'pub-venue-row', span('pub-venue', item['venue'])+
            (span('pub-date', date_label) if date_label else ''))+
        tag('h3', 'pub-title', e(item['title']))+tag('p', 'pub-authors', authors)+
        span('pub-badge '+status, item['status'])+resource_links(item))


def build_context(data):
    profile = data['profile']
    papers = sorted_publications(data['publications'])
    counts = {status: sum(p['status'] == status for p in papers)
              for status in ('Published', 'Accepted', 'In Progress')}
    for paper in papers:
        if paper['status'] not in counts:
            raise ValueError(f'Unknown publication status: {paper["status"]!r}')
    parts = []
    for status, count in counts.items():
        if count:
            noun = 'paper' if count == 1 else 'papers'
            parts.append(f'{count} {noun} in progress' if status == 'In Progress'
                         else f'{count} {status.lower()} {noun}')
    summary = (', '.join(parts[:-1]) + ' and ' + parts[-1]) if len(parts) > 1 else (parts[0] if parts else 'research underway')
    variables = {'name': profile['name'], 'published_count': counts['Published'],
                 'accepted_count': counts['Accepted'], 'in_progress_count': counts['In Progress'],
                 'publication_summary': summary}

    def copy(value):
        return e(value.format_map(variables))

    featured = next((x for x in data['education'] if x['id'] == profile['featured_education']), None)
    if featured is None:
        raise ValueError('profile.featured_education must match an education id')
    context = {key: e(profile[key]) for key in ('name', 'logo', 'photo', 'site_url')}
    context.update(description=copy(data['metadata']['description']),
                   social_description=copy(data['metadata']['social_description']),
                   social_image=e(urljoin(profile['site_url'], profile['photo'])),
                   eyebrow=copy(data['hero']['eyebrow']),
                   roles=' <em>&amp;</em> '.join(e(s) for s in data['hero']['roles']),
                   hero_bio=copy(data['hero']['bio']),
                   photo_caption=e(profile.get('photo_caption', '')),
                   education_summary=e(f'{featured["degree"]} · {featured["school"]}'),
                   research_topics=research_interests(data['hero'].get('research_interests', [])),
                   research_counts=e(' · '.join(f'{count} {status.lower()}' for status, count in counts.items() if count)),
                   contact_description=copy(data['contact']['description']))
    for section in data['sections']:
        for field in ('label', 'heading'):
            context[f'{section["id"]}_{field}'] = e(section[field])
    actions = []
    for action in data['hero']['actions']:
        if 'contact' in action:
            contact = next((x for x in data['contact']['links'] if x['label'] == action['contact']), None)
            if contact is None:
                raise ValueError(f'Unknown hero contact: {action["contact"]}')
            href = contact['url_prefix'] + contact['value']
        else:
            href = action['href']
        actions.append(tag('a', 'btn btn-'+action['style'], e(action['label']), href=safe_url(page_link(href))))
    context['hero_actions'] = '\n'.join(actions)
    stats = [(counts['Published'], 'Publications'), (featured['gpa'], 'GPA / '+featured['gpa_max']), (profile['years_dev'], 'Years Dev')]
    context['stats'] = tag('div', 'hero-stat-divider', '', **{'aria-hidden': 'true'}).join(
        tag('div', 'hero-stat', span('hero-stat-num', value)+span('hero-stat-label', label)) for value,label in stats)
    context['about_paragraphs'] = '\n'.join(tag('p', 'about-bio', copy(p)) for p in data['about']['paragraphs'])
    context['education'] = '\n'.join(tag('div', 'edu-item', span('edu-degree', x['degree'])+
        span('edu-detail', f'{x["school"]} · {x["period"]} · GPA {x["gpa"]}/{x["gpa_max"]}')) for x in data['education'])
    context['languages'] = '\n'.join(tag('span', 'lang-chip', e(x['name'])+' '+tag('em', '', e(x['level']))) for x in data['languages'])
    context['language_scores'] = '\n'.join(tag('div', 'lang-score-item', span('lang-score-label', x['name'])+
        tag('span', 'lang-score-value', e(x['value'])+(span('lang-score-max', '/'+x['max']) if x.get('max') else ''))) for x in data['language_scores'])
    context['skills'] = '\n'.join(tag('div', 'skill-category', tag('h3', 'skill-cat-label', e(x['category']))+
        tag('div', 'skill-tags', ''.join(span('skill-tag'+(' skill-tag-accent' if x.get('accent') else ''), item) for item in x['items']))) for x in data['skills'])
    context['experience'] = '\n'.join(tag('div', 'timeline-item reveal-item',
        tag('div', 'timeline-marker', '', **{'aria-hidden': 'true'})+
        tag('div', 'timeline-content', tag('div', 'timeline-header', tag('h3', 'timeline-role', e(x['role']))+
            (span('timeline-badge current', 'Current') if x.get('current') else ''))+
            tag('div', 'timeline-org-row', span('timeline-org', x['organization'])+span('timeline-period', x['period']))+
            tag('p', 'timeline-desc', e(x['description'])))) for x in data['experience'])
    context['publications'] = '\n'.join(publication_card(x, profile.get('publication_name', profile['name'])) for x in papers)
    context['projects'] = '\n'.join(tag('div', 'project-card reveal-item', tag('div', 'project-year', e(x['year']))+
        tag('h3', 'project-title', e(x['title']))+tag('p', 'project-desc', e(x['description']))+project_details(x)+
        tag('div', 'project-tags', ''.join(span('project-tag', item) for item in x['tags']))+resource_links(x)) for x in data['projects'])
    links = []
    for x in data['contact']['links']:
        url = safe_url(x['url_prefix']+x['value'])
        attrs = {'target': '_blank', 'rel': 'noopener'} if url.startswith(('https:', 'http:')) else {}
        links.append(tag('a', 'contact-link', tag('span', 'contact-icon', e(x['icon']), **{'aria-hidden': 'true'})+
            tag('div', 'contact-link-text', span('contact-link-label', x['label'])+span('contact-link-value', x['value'])), href=url, **attrs))
    context['contact_links'] = '\n'.join(links)
    context['footer'] = span('', f'© {data["footer"]["year"]} {profile["name"]}')+tag('span', 'footer-sep', '·', **{'aria-hidden': 'true'})+span('', data['footer']['credit'])
    return context


def render_page(data, context, page):
    sections = {s['id']: s for s in data['sections']}
    if page not in PAGE_FILES or (page != 'home' and page not in sections):
        raise ValueError(f'Unknown page: {page}')
    context = dict(context)
    if page != 'home':
        return Template((ROOT/'templates/redirect.html').read_text(encoding='utf-8')).substitute(
            title=e(sections[page]['label']), name=context['name'],
            destination=e('index.html#'+page), canonical=e(data['profile']['site_url']))
    label = 'Home' if page == 'home' else sections[page]['label']
    context['page_title'] = e(f'{data["profile"]["name"]} — Research portfolio')
    context['page_url'] = e(urljoin(data['profile']['site_url'], '' if page == 'home' else PAGE_FILES[page]))
    context['page_id'] = page
    navigation = [{'id': 'hero', 'label': 'Home'}, *data['sections']]
    context['navigation'] = '\n'.join(tag('a', 'nav-link'+(' active' if s['id'] == 'hero' else ''),
        e(s['label']), href='#'+s['id'], **{'data-section': s['id'],
            'aria-current': 'location' if s['id'] == 'hero' else ''}) for s in navigation)
    context['first_section_href'] = '#'+data['sections'][0]['id']
    context['page_content'] = '\n'.join(Template((ROOT/'templates'/f'{part}.html').read_text(encoding='utf-8')).substitute(context)
                                       for part in ['home', *sections])
    return Template((ROOT/'templates/page.html').read_text(encoding='utf-8')).substitute(context)


def render(data, page='home'):
    return render_page(data, build_context(data), page)


def render_site(data):
    ids = [s['id'] for s in data['sections']]
    if len(ids) != len(set(ids)) or set(ids) != set(PAGE_FILES)-{'home'}:
        raise ValueError('sections must contain each supported page id exactly once')
    context = build_context(data)
    return {PAGE_FILES[page]: render_page(data, context, page) for page in ['home', *ids]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if any generated page needs rebuilding')
    args = parser.parse_args()
    try:
        pages = render_site(json.loads((ROOT/'content.json').read_text(encoding='utf-8')))
        if args.check:
            stale = [name for name, html in pages.items() if not (ROOT/name).exists()
                     or (ROOT/name).read_text(encoding='utf-8') != html]
            if stale:
                parser.exit(1, 'Pages out of date: '+', '.join(stale)+'. Run python build.py\n')
            print(f'All {len(pages)} pages are up to date.')
        else:
            for name, html in pages.items():
                (ROOT/name).write_text(html, encoding='utf-8')
            print(f'Built {len(pages)} pages from content.json and templates/')
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(1, f'Build failed: {error}\n')


if __name__ == '__main__':
    main()
