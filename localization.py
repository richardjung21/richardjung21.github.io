"""Korean copy and presentation; shared research metadata stays in content.json."""
import re
from html import escape
from html.parser import HTMLParser


def korean_content(data):
    """Apply Korean field overrides, matching collection items by stable IDs.

    Dates, statuses, bylines, images and newly added items inherit shared data.
    Korean copy is independent of the wording of its English counterpart.
    """
    korean = data['translations']['ko']

    def merge(value, overrides):
        if isinstance(value, dict):
            return {key: merge(item, overrides[key]) if key in overrides else item
                    for key, item in value.items() if key != 'translations'}
        if isinstance(value, list) and isinstance(overrides, dict):
            return [merge(item, overrides.get(item.get('id'), {}))
                    if isinstance(item, dict) else item for item in value]
        return overrides

    return merge(data, korean), korean['ui']


class KoreanHTML(HTMLParser):
    """Translate generated UI text and accessible labels, never URLs or CSS hooks."""
    def __init__(self, ui):
        super().__init__(convert_charrefs=True)
        self.ui = ui
        self.output = []

    def text(self, value):
        # Keep the language names on the switch recognizable in either version.
        if value in self.ui:
            return self.ui[value]
        value = value.replace('Research portfolio', '연구 포트폴리오')
        value = value.replace('Enlarge figure: ', '그림 확대: ')
        for pattern, replacement in (
            (r'^(\d+) months$', r'\1개월'),
            (r'^([\d.]+)% less$', r'\1% 감소'),
            (r'^([+\d.]+) pp$', r'\1%p'),
            (r'(\d+) published papers?', r'게재 논문 \1편'),
            (r'(\d+) accepted papers?', r'게재 승인 논문 \1편'),
            (r'(\d+) papers? under review', r'심사 중인 논문 \1편'),
            (r'(\d+) papers? in progress', r'진행 중인 논문 \1편'),
            (r'(\d+) published', r'게재 완료 \1편'),
            (r'(\d+) accepted', r'게재 승인 \1편'),
            (r'(\d+) under review', r'심사 중 \1편'),
            (r'(\d+) in progress', r'진행 중 \1편'),
            (r'^(\d+) papers?$', r'\1편'),
            (r'Author (\d+) of (\d+)', r'저자 \2명 중 \1번째'),
        ):
            value = re.sub(pattern, replacement, value)
        # Join the English builder's publication summary naturally in Korean.
        value = re.sub(r'(편) and (?=(?:게재|심사|진행))', r'\1 및 ', value)
        months = ('January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December')
        for number, month in enumerate(months, 1):
            value = re.sub(rf'^{month} (\d+), (\d{{4}})$', rf'\2년 {number}월 \1일', value)
            value = re.sub(rf'^{month} (\d{{4}})$', rf'\1년 {number}월', value)
        return value

    def start(self, tag, attrs, closed=False):
        localized = []
        for key, value in attrs:
            if value is not None and key in ('aria-label', 'alt', 'content', 'data-alt'):
                value = self.text(value)
            localized.append(' '+key+(f'="{escape(value, quote=True)}"' if value is not None else ''))
        self.output.append('<'+tag+''.join(localized)+(' />' if closed else '>'))

    def handle_starttag(self, tag, attrs):
        self.start(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        self.start(tag, attrs, True)

    def handle_endtag(self, tag):
        self.output.append('</'+tag+'>')

    def handle_data(self, data):
        self.output.append(escape(self.text(data), quote=False))

    def handle_comment(self, data):
        self.output.append('<!--'+data+'-->')

    def handle_decl(self, decl):
        self.output.append('<!'+decl+'>')


def korean_html(html, ui):
    parser = KoreanHTML(ui)
    parser.feed(html)
    parser.close()
    return ''.join(parser.output)
