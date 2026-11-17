#!/usr/bin/env python3
"""One navigation and one footer for the whole site.

The menu and footer are defined once here and written into every page:
  - pages built on assets/site.js: the script's menu/footer lists are rewritten, and plain
    crawlable copies are placed inside the #nav / #footer placeholders (the script replaces them);
  - pages with a written-in <nav> (homepage, app pages, catalogue, shop...): the link list is
    replaced, a Menu button is added for phones (assets/nav.js + assets/nav.css), and the footer
    links are replaced.
Privacy policies and the /links/ hub are left as they are. Re-run after any page is regenerated:
  python3 tools/apply_nav.py
"""
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAV = [  # (href, label, key)
    ('/google-play.html', 'Apps', 'play'),
    ('/angels.html', 'Angels', 'angels'),
    ('/angel-of-the-hour.html', 'Angel of the Hour', 'angelhour'),
    ('/planetary-hour-now.html', 'Planetary Hours', 'hours'),
    ('/archive.html', 'Archive', 'archive'),
    ('/library.html', 'Library', 'library'),
    ('/shop.html', 'Shop', 'shop'),
]
# which pages count as "inside" each menu item, for highlighting
SECTION = {
    'play': ['google-play.html', 'coming-soon.html', 'new.html', 'catalog.html', 'apps.html', 'almanac.html', 'app/'],
    'angels': ['angels.html', 'seven-angels.html'],
    'angelhour': ['angel-of-the-hour.html'],
    'hours': ['planetary-hour-now.html', 'planetary-hours.html'],
    'archive': ['archive.html'],
    'library': ['library.html'],
    'shop': ['shop.html', 'gifts/'],
}
FOOTER = [
    ('Apps', [('/google-play.html', 'All apps on Google Play'), ('/coming-soon.html', 'New and coming soon'),
              ('/new.html', 'Apps by tradition'), ('/catalog.html', 'The full catalogue'), ('/angels.html', 'The Angelic Hall'),
              ('/seven-angels.html', 'The Seven Angels'), ('/almanac.html', 'The Almanac'),
              ('https://apps.apple.com/us/developer/montgomery-ostrander/id6804113840', 'On the App Store')]),
    ('Live tools and study', [('/angel-of-the-hour.html', 'Angel of the Hour'), ('/planetary-hour-now.html', 'Planetary Hour Now'),
                              ('/planetary-hours.html', 'Planetary hours guide'), ('/archive.html', 'The Archive'),
                              ('/library.html', 'Library of sources'), ('/entrainment.html', 'Research: entrainment'),
                              ('/neuro.html', 'Live EEG editions'), ('/obe.html', 'OBE Induction'), ('/oracle.html', 'ORACLE')]),
    ('More', [('/shop.html', 'Shop'), ('/gifts/', 'Gift guides'), ('/links/', 'Links'), ('/privacy.html', 'Privacy'),
              ('mailto:montgomery@discovery-science.com', 'Contact')]),
]
SKIP = ('privacy', 'links/', '404.html', 'legacy-monty-site', 'tools/', 'node_modules')


def e(s):
    return html.escape(s, quote=True)


def key_for(rel):
    for k, prefixes in SECTION.items():
        for p in prefixes:
            if rel == p or (p.endswith('/') and rel.startswith(p)):
                return k
    return ''


def ul(active):
    return '<ul id="ds-links">' + ''.join(
        f'<li><a href="{h}"' + (' aria-current="page"' if k == active else '') + f'>{e(l)}</a></li>' for h, l, k in NAV) + '</ul>'


def footer_groups():
    return '<div class="ds-foot">' + ''.join(
        f'<div><h5>{e(t)}</h5>' + ''.join(
            f'<a href="{h}"' + (' rel="noopener"' if h.startswith('http') else '') + f'>{e(l)}</a>' for h, l in links) + '</div>'
        for t, links in FOOTER) + '</div>'


def static_fallback_nav(active):
    return ('<nav class="top" aria-label="Main"><div class="wrap"><a class="brand" href="/">DISCOVERY SCIENCE</a><div class="links">' +
            ''.join(f'<a href="{h}"' + (' class="on"' if k == active else '') + f'>{e(l)}</a>' for h, l, k in NAV) + '</div></div></nav>')


# ------------------------------------------------------------------ 1. assets/site.js
p = os.path.join(ROOT, 'assets', 'site.js')
s = open(p, encoding='utf-8').read()
L = 'var L=[' + ','.join(f"['{h}','{l}','{k}']" for h, l, k in NAV) + '];'
s = re.sub(r"var L=\[\[.*?\]\];", lambda m: L, s, count=1)
groups_js = ''.join(
    f'<div><h5>{e(t)}</h5>' + ''.join(
        f'<a href="{h}"' + (' target="_blank" rel="noopener"' if h.startswith('http') else '') + f'>{e(l)}</a>' for h, l in links if not h.startswith('mailto')) +
    ('<a href="mailto:\'+EMAIL+\'">\'+EMAIL+\'</a>' if t == 'More' else '') + '</div>'
    for t, links in FOOTER)
start = s.index('</p></div><div><h5>') + len('</p></div>')
end = s.index('</div></div><p class="fine" style="margin-top:34px">')
s = s[:start] + groups_js + s[end:]
open(p, 'w', encoding='utf-8').write(s)

# ------------------------------------------------------------------ 2. every page
changed = 0
for d, dirs, files in os.walk(ROOT):
    dirs[:] = [x for x in dirs if x not in {'.git', 'legacy-monty-site', 'tools', 'node_modules'}]
    for f in files:
        if not f.endswith('.html'):
            continue
        rel = os.path.relpath(os.path.join(d, f), ROOT).replace(os.sep, '/')
        if any(x in rel for x in SKIP):
            continue
        s0 = s = open(os.path.join(ROOT, rel), encoding='utf-8').read()
        active = key_for(rel)
        # (a) script-built pages: crawlable fallback inside the placeholders (between marker comments)
        s = re.sub(r'<div id="nav">(?:<!--ds-nav-->.*?<!--/ds-nav-->)?</div>', lambda m: '<div id="nav"><!--ds-nav-->' + static_fallback_nav(active) + '<!--/ds-nav--></div>', s, count=1, flags=re.S)
        s = re.sub(r'<div id="footer">(?:<!--ds-foot-->.*?<!--/ds-foot-->)?</div>', lambda m: '<div id="footer"><!--ds-foot--><footer><div class="wrap">' + footer_groups() + '</div></footer><!--/ds-foot--></div>', s, count=1, flags=re.S)
        # (b) pages with a written-in menu
        m = re.search(r'(<nav(?: class="top")?><div class="wrap"><a class="brand"[^>]*>.*?</a>)\s*(?:<button class="ds-menu"[^>]*>Menu</button>)?\s*<ul[^>]*>.*?</ul>', s, re.S)
        if m:
            s = s[:m.start()] + m.group(1) + '<button class="ds-menu" type="button" aria-expanded="false" aria-controls="ds-links">Menu</button>' + ul(active) + s[m.end():]
            if '/assets/nav.css' not in s:
                s = s.replace('</head>', '<link rel="stylesheet" href="/assets/nav.css">\n</head>', 1)
            if '/assets/nav.js' not in s:
                s = s.replace('</body>', '<script src="/assets/nav.js" defer></script>\n</body>', 1)
            # footer: replace the first block of links (or a previous ds-foot) with the standard groups
            s = re.sub(r'(<footer><div class="wrap">)(?:<div class="ds-foot">.*?</div></div>|<div>(?:<a [^>]*>[^<]*</a>)+</div>)', lambda mm: mm.group(1) + footer_groups(), s, count=1, flags=re.S)
        if s != s0:
            changed += 1
            open(os.path.join(ROOT, rel), 'w', encoding='utf-8').write(s)
print('pages updated:', changed)
