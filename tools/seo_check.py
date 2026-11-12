#!/usr/bin/env python3
"""Static SEO checks for the Discovery Science site. Standard library only.

Usage: python3 tools/seo_check.py [site_root]
Exit code 1 if any ERROR is found. WARN lines are advisory.
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..'))
ORIGIN = 'https://www.discovery-science.com'
SKIP_DIRS = {'.git', 'legacy-monty-site', 'tools', 'node_modules'}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ''
        self._in_title = False
        self.meta = {}
        self.canonical = None
        self.h1 = 0
        self.h_levels = []
        self.imgs_no_alt = 0
        self.links = []
        self.jsonld = []
        self._in_ld = False
        self._ld = ''

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'title':
            self._in_title = True
        elif tag == 'meta':
            k = a.get('name') or a.get('property')
            if k:
                self.meta[k.lower()] = a.get('content', '')
        elif tag == 'link' and (a.get('rel') or '').lower() == 'canonical':
            self.canonical = a.get('href')
        elif re.fullmatch(r'h[1-6]', tag):
            self.h_levels.append(int(tag[1]))
            if tag == 'h1':
                self.h1 += 1
        elif tag == 'img' and 'alt' not in a:
            self.imgs_no_alt += 1
        elif tag == 'a' and a.get('href'):
            self.links.append(a['href'])
        elif tag == 'script' and (a.get('type') or '') == 'application/ld+json':
            self._in_ld, self._ld = True, ''

    def handle_endtag(self, tag):
        if tag == 'title':
            self._in_title = False
        elif tag == 'script' and self._in_ld:
            self._in_ld = False
            self.jsonld.append(self._ld)

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_ld:
            self._ld += data


def html_files():
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            if f.endswith('.html'):
                yield os.path.relpath(os.path.join(d, f), ROOT).replace(os.sep, '/')


def url_for(rel):
    return ORIGIN + ('/' if rel == 'index.html' else '/' + rel)


def exists(path):
    path = path.split('#')[0].split('?')[0]
    if path in ('', '/'):
        return True
    p = os.path.join(ROOT, path.lstrip('/'))
    return os.path.isfile(p) or os.path.isfile(os.path.join(p, 'index.html'))


def main():
    errors, warns = [], []
    pages = {}
    for rel in sorted(html_files()):
        p = Page()
        with open(os.path.join(ROOT, rel), encoding='utf-8') as fh:
            p.feed(fh.read())
        pages[rel] = p

    titles, descs = {}, {}
    for rel, p in pages.items():
        noindex = 'noindex' in p.meta.get('robots', '')
        t = p.title.strip()
        d = p.meta.get('description', '').strip()
        if not t:
            errors.append(f'{rel}: missing <title>')
        elif not noindex:
            titles.setdefault(t, []).append(rel)
            if len(t) > 70:
                warns.append(f'{rel}: title {len(t)} chars (>70 may truncate)')
        if not noindex:
            if not d:
                errors.append(f'{rel}: missing meta description')
            else:
                descs.setdefault(d, []).append(rel)
                if len(d) > 170:
                    warns.append(f'{rel}: description {len(d)} chars (>170 may truncate)')
            if not p.canonical:
                errors.append(f'{rel}: missing canonical')
            elif not p.canonical.startswith(ORIGIN + '/'):
                errors.append(f'{rel}: canonical not on {ORIGIN}: {p.canonical}')
            elif p.canonical.split('#')[0] != url_for(rel):
                warns.append(f'{rel}: canonical points elsewhere -> {p.canonical}')
            if p.h1 != 1:
                errors.append(f'{rel}: {p.h1} <h1> elements (expected 1)')
            ogu = p.meta.get('og:url')
            if ogu and p.canonical and ogu != p.canonical:
                errors.append(f'{rel}: og:url {ogu} != canonical {p.canonical}')
        if p.imgs_no_alt:
            errors.append(f'{rel}: {p.imgs_no_alt} <img> without alt')
        for i, ld in enumerate(p.jsonld):
            try:
                obj = json.loads(ld)
                for o in (obj if isinstance(obj, list) else [obj]):
                    if '@context' not in o or '@type' not in o:
                        errors.append(f'{rel}: JSON-LD #{i} missing @context/@type')
            except ValueError as e:
                errors.append(f'{rel}: JSON-LD #{i} invalid JSON: {e}')
        for href in p.links:
            u = urlparse(href)
            if u.scheme in ('mailto', 'tel', 'javascript') or href.startswith('#'):
                continue
            if u.netloc and u.netloc not in ('www.discovery-science.com', 'discovery-science.com'):
                continue
            path = (u.path or '/') if u.netloc else href
            if not path.startswith('/'):
                path = os.path.normpath(os.path.join(os.path.dirname('/' + rel), path))
            if not exists(path):
                errors.append(f'{rel}: broken internal link {href}')

    for t, rels in titles.items():
        if len(rels) > 1:
            errors.append(f'duplicate title "{t}": {", ".join(rels)}')
    for d, rels in descs.items():
        if len(rels) > 1:
            warns.append(f'duplicate description on: {", ".join(rels)}')

    # sitemap
    sm = os.path.join(ROOT, 'sitemap.xml')
    try:
        tree = ET.parse(sm)
        ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        locs = [e.text.strip() for e in tree.getroot().findall('s:url/s:loc', ns)]
        if len(locs) != len(set(locs)):
            errors.append('sitemap: duplicate <loc>')
        for loc in locs:
            rel = 'index.html' if loc == ORIGIN + '/' else loc[len(ORIGIN) + 1:]
            if not loc.startswith(ORIGIN + '/'):
                errors.append(f'sitemap: non-canonical host {loc}')
            elif rel not in pages:
                errors.append(f'sitemap: {loc} has no file')
            else:
                p = pages[rel]
                if 'noindex' in p.meta.get('robots', ''):
                    errors.append(f'sitemap: {loc} is noindex')
                if p.canonical and p.canonical != loc:
                    errors.append(f'sitemap: {loc} canonicalises to {p.canonical}')
        listed = set(locs)
        for rel, p in pages.items():
            if p.canonical == url_for(rel) and url_for(rel) not in listed and 'privacy' not in rel and rel != '404.html':
                warns.append(f'sitemap: indexable page not listed: {rel}')
        print(f'sitemap: {len(locs)} URLs')
    except (OSError, ET.ParseError) as e:
        errors.append(f'sitemap: {e}')

    rb = open(os.path.join(ROOT, 'robots.txt')).read()
    if 'Sitemap: ' + ORIGIN + '/sitemap.xml' not in rb:
        errors.append('robots.txt: missing Sitemap line')
    if re.search(r'^Disallow:\s*/\s*$', rb, re.M):
        errors.append('robots.txt: blocks the whole site')

    print(f'pages: {len(pages)}')
    for w in warns:
        print('WARN ', w)
    for e in errors:
        print('ERROR', e)
    print(f'{len(errors)} errors, {len(warns)} warnings')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
