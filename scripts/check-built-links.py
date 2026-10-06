"""Check every rendered internal page/anchor after BASE=/Isaac-Wiki/ npm run build."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import sys

ROOT = Path(__file__).resolve().parents[1] / 'docs/.vitepress/dist'
BASE = sys.argv[1] if len(sys.argv) > 1 else '/Isaac-Wiki/'


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = set()
        self.duplicates = set()
        self.links = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                self.duplicates.add(attrs['id'])
            self.ids.add(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])


cache = {path: Page(path) for path in ROOT.rglob('*.html')}
if not cache:
    raise SystemExit('No rendered HTML found. Run the production build first.')
errors = set()
count = 0
for path, page in cache.items():
    route = str(path.relative_to(ROOT)).removesuffix('.html')
    for duplicate in page.duplicates:
        errors.add((route, duplicate, 'duplicate ID'))
    for href in page.links:
        if not href or urlsplit(href).scheme or href.startswith('//'):
            continue
        parsed = urlsplit(urljoin(BASE + route, href))
        if not parsed.path.startswith(BASE):
            errors.add((route, href, 'missing deployment base'))
            continue
        target = ROOT / unquote(parsed.path[len(BASE):])
        if parsed.path.endswith('/'):
            target = target / 'index.html'
        elif not target.suffix:
            target = target.with_suffix('.html')
        if target.suffix != '.html':
            if not target.is_file():errors.add((route,href,'missing download / asset'))
            continue
        count += 1
        if target not in cache:
            errors.add((route, href, 'missing page'))
        elif parsed.fragment and unquote(parsed.fragment) not in cache[target].ids:
            errors.add((route, href, 'missing anchor'))
print(f'Checked {len(cache)} rendered pages and {count} internal links.')
for error in sorted(errors):
    print(*error)
raise SystemExit(bool(errors))
