#!/usr/bin/env python3
"""One-shot SEO transform applied to the production snapshot (commit d0bebcd).

Every edit is a targeted string insertion or replacement in <head>, plus a few small
internal-link additions. Re-running is safe: each step checks whether it has already
been applied. Standard library only.
"""
import html
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ORIGIN = 'https://www.discovery-science.com'
TODAY = '2026-11-12'


def rd(p):
    with open(os.path.join(ROOT, p), encoding='utf-8') as f:
        return f.read()


def wr(p, s):
    with open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='') as f:
        f.write(s)


def url_for(p):
    return ORIGIN + '/' if p == 'index.html' else f'{ORIGIN}/{p}'


def esc(s):
    return html.escape(s, quote=True)


def head_insert(s, tags):
    """Insert tags just before </head> (one per line)."""
    if '</head>' in s:
        i = s.index('</head>')
    else:  # some policy pages omit </head>; meta/link before the first body element still parse into <head>
        i = min(x for x in (s.find('<body'), s.find('<main')) if x >= 0)
    return s[:i] + ''.join(t + '\n' for t in tags) + s[i:]


def set_title(s, title):
    return re.sub(r'<title>.*?</title>', '<title>' + esc(title).replace('&#x27;', "'") + '</title>', s, count=1, flags=re.S)


def set_meta(s, attr, key, value):
    """Replace or insert <meta attr="key" content="...">."""
    pat = re.compile(r'<meta\s+' + attr + r'="' + re.escape(key) + r'"\s+content="[^"]*"\s*/?>')
    tag = f'<meta {attr}="{key}" content="{esc(value)}">'
    if pat.search(s):
        return pat.sub(lambda m: tag, s, count=1)
    # keep description right after <title>
    if key == 'description':
        return re.sub(r'(</title>)', r'\1\n' + tag.replace('\\', '\\\\'), s, count=1)
    return head_insert(s, [tag])


def ensure_canonical(s, url):
    if re.search(r'<link rel="canonical"', s):
        return re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', s, count=1)
    return head_insert(s, [f'<link rel="canonical" href="{url}">'])


def ensure_social(s, url, og_type='website', title=None, desc=None):
    """og:url / og:type / og:site_name / twitter:card, plus og:title/description if missing."""
    s = set_meta(s, 'property', 'og:url', url)
    if 'property="og:type"' not in s:
        s = head_insert(s, [f'<meta property="og:type" content="{og_type}">'])
    if 'property="og:site_name"' not in s:
        s = head_insert(s, ['<meta property="og:site_name" content="Discovery Science">'])
    if title and 'property="og:title"' not in s:
        s = head_insert(s, [f'<meta property="og:title" content="{esc(title)}">'])
    if desc and 'property="og:description"' not in s:
        s = head_insert(s, [f'<meta property="og:description" content="{esc(desc)}">'])
    if 'name="twitter:card"' not in s:
        s = head_insert(s, ['<meta name="twitter:card" content="summary">'])
    return s


def add_jsonld(s, obj, marker):
    if marker in s:
        return s
    return head_insert(s, ['<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + '</script>'])


def add_track(s):
    if '/assets/track.js' in s:
        return s
    i = s.rindex('</body>')
    return s[:i] + '<script src="/assets/track.js" defer></script>\n' + s[i:]


# --------------------------------------------------------------------------------------------
# 1. Hub / content pages: titles, descriptions, canonicals, social tags
# --------------------------------------------------------------------------------------------
PAGES = {
    # path: (title, description or None to keep, og:type)
    'index.html': (None, None, 'website'),
    'angels.html': ('Angel Communication Apps: Ars Paulina to John Dee | Discovery Science',
                    'Eight Android apps for angelic communication, rebuilt from the Ars Paulina, the Heptameron, John Dee’s Enochian Calls, the 72 Names, Abramelin and the Hekhalot.', 'website'),
    'archive.html': ('The Archive: How Ancient Rites Actually Worked | Discovery Science',
                     'A research archive of the historical rites behind our apps: the Greek Magical Papyri, Hekhalot, John Dee, the Goetia, the Picatrix, planetary hours, Egypt and Babylon.', 'article'),
    'apps.html': ('App Library: Ritual & Contemplative Apps by Hall | Discovery Science',
                  'Every Discovery Science Android app, shelved by the tradition that wrote it down: ritual, divination and contemplative apps rebuilt from the oldest texts.', 'website'),
    'library.html': ('Sources & Bibliography: The Texts Behind Every App | Discovery Science', None, 'website'),
    'catalog.html': ('Full App Catalogue, Ordered by Who Answers | Discovery Science',
                     'The full Discovery Science catalogue, ordered by who answers: angels, the Throne, the gods, spirits and jinn, Christ, the planetary powers and the contemplative paths.', 'website'),
    'new.html': ('All Discovery Science Apps on Android, by Tradition', None, 'website'),
    'google-play.html': (None, None, 'website'),
    'entrainment.html': ('Binaural Beats, Theta & Entrainment: The Research | Discovery Science',
                         'The physics of binaural beats, 1970s sound laboratories, the Army’s 1983 assessment, shamanic drumming and temple acoustics, and how our rites use sound.', 'article'),
    'neuro.html': ('Live Neurofeedback EEG Editions | Discovery Science',
                   'Every Discovery Science rite in an edition that listens to your brain through OpenBCI or Neurosity Crown: hear theta dominance and gamma bursts in real time.', 'website'),
    'obe.html': ('OBE Induction App: Guided Out-of-Body Ritual | Discovery Science',
                 'OBE Induction for Android: twelve guided protocols, a staged three-threshold binaural progression, ceremonial hours from your own sky and experience markers.', 'website'),
    'oracle.html': ('ORACLE App: Daily and Hourly Readings | Discovery Science', None, 'website'),
    'seven-angels.html': ('The Seven Planetary Angels: Michael to Cassiel | Discovery Science', None, 'website'),
    'almanac.html': ('The Almanac: Gnostic, Witchcraft, Tarot & Divination Apps', None, 'website'),
    'shop.html': (None, None, 'website'),
    'asclepion.html': (None, None, 'website'),
    'dhikr.html': (None, None, 'website'),
    'divining-vessel.html': (None, None, 'website'),
    'ekstasis.html': (None, None, 'website'),
    'kispu.html': (None, None, 'website'),
    'planetary-attunement.html': ('Planetary Attunement: Planetary Hours App | Discovery Science', None, 'website'),
    'spirit-drum.html': (None, None, 'website'),
    'theurgia.html': (None, None, 'website'),
}

for p, (title, desc, og_type) in PAGES.items():
    s = rd(p)
    if title:
        s = set_title(s, title)
        if 'property="og:title"' in s:
            s = set_meta(s, 'property', 'og:title', title.replace(' | Discovery Science', ''))
    if desc:
        s = set_meta(s, 'name', 'description', desc)
        if 'property="og:description"' in s:
            s = set_meta(s, 'property', 'og:description', desc)
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    t = re.search(r'<title>(.*?)</title>', s, re.S).group(1)
    s = ensure_canonical(s, url_for(p))
    s = ensure_social(s, url_for(p), og_type, html.unescape(t).replace(' | Discovery Science', ''), html.unescape(d.group(1)) if d else None)
    s = add_track(s)
    wr(p, s)

# catalog.html: the page had no <h1>; promote its first heading, keeping the h2 look.
s = rd('catalog.html')
s = s.replace('<h2 style="margin-top:18px">Ordered by <em>who answers.</em></h2>',
              '<h1 style="margin:18px 0 0;font-size:clamp(38px,5.4vw,68px)">Ordered by <em>who answers.</em></h1>', 1)
wr('catalog.html', s)

# Homepage: Organization + WebSite structured data; guide link in footer.
s = rd('index.html')
s = add_jsonld(s, {
    '@context': 'https://schema.org', '@type': 'Organization', 'name': 'Discovery Science, Inc.',
    'url': ORIGIN + '/', 'logo': ORIGIN + '/favicon.svg', 'email': 'montgomery@discovery-science.com',
    'sameAs': ['https://play.google.com/store/apps/developer?id=Discovery+Science',
               'https://www.youtube.com/@angeliccommmunication', 'https://www.tiktok.com/@discoveryscience',
               'https://www.instagram.com/discoverysciencetools/', 'https://www.etsy.com/shop/SigilAndWing']},
    '"@type":"Organization"')
s = add_jsonld(s, {'@context': 'https://schema.org', '@type': 'WebSite', 'name': 'Discovery Science', 'url': ORIGIN + '/'}, '"@type":"WebSite"')
s = s.replace('<a href="/archive.html">Archive</a><a href="/privacy.html">Privacy</a></div><div class="soc">',
              '<a href="/archive.html">Archive</a><a href="/planetary-hours.html">Planetary Hours</a><a href="/privacy.html">Privacy</a></div><div class="soc">', 1)
wr('index.html', s)

# Archive: point the planetary-hours chapter at the new guide.
s = rd('archive.html')
anchor = '<h3>Making a talisman, after the Picatrix</h3>'
if '/planetary-hours.html' not in s and anchor in s:
    s = s.replace(anchor, '<p><a href="/planetary-hours.html" style="color:var(--gold2)">Step-by-step guide, weekday tables and a free planetary hours calculator →</a></p>\n      ' + anchor, 1)
wr('archive.html', s)

# 404: never index.
s = rd('404.html')
if 'name="robots"' not in s:
    s = re.sub(r'(<title>.*?</title>)', r'\1\n<meta name="robots" content="noindex">', s, count=1, flags=re.S)
wr('404.html', s)

# --------------------------------------------------------------------------------------------
# 2. App landing pages (/app/*.html)
# --------------------------------------------------------------------------------------------
ARCHIVE = {  # slug -> [(anchor, chapter title)] taken from the chapters that already link each app
    'angelarium': [('angels', 'The Orders of Angels'), ('methods', 'The Six Angelic Methods')],
    'anunnaki': [('mesopotamia', 'Sumer, Akkad & the Anunnaki')],
    'apkallu': [('mesopotamia', 'Sumer, Akkad & the Anunnaki')],
    'ars-astrorum': [('astral', 'Astral Magic & the Planetary Hours')],
    'celestial-above': [('astral', 'Astral Magic & the Planetary Hours'), ('oracle', 'Tarot, the I Ching & the Hours')],
    'celestial-veil': [('astral', 'Astral Magic & the Planetary Hours'), ('angels', 'The Orders of Angels')],
    'djin-invocation': [('solomonic', 'Solomon & the Goetia'), ('jinn', 'The Jinn & the Science of Letters')],
    'egyptian-gods': [('egypt', 'Egypt: Heka & the Temple')],
    'empty-gate': [('paths', 'The Contemplative Lineages')],
    'enochian-calls': [('enochian', 'John Dee & the Enochian Calls'), ('methods', 'The Six Angelic Methods')],
    'greek-gods': [('greek', 'The Greek Gods & the Magical Papyri')],
    'hekhalot-the-seven-palaces': [('hekhalot', 'Hekhalot & the Merkavah'), ('methods', 'The Six Angelic Methods')],
    'merkavah-ezekiels-chariot': [('hekhalot', 'Hekhalot & the Merkavah')],
    'middle-way': [('paths', 'The Contemplative Lineages')],
    'norse-gods': [('norse', 'The North: Blót, Seiðr & Runes')],
    'obe-induction': [('threshold', 'Theta: the Science of the Threshold')],
    'oracle': [('oracle', 'Tarot, the I Ching & the Hours')],
    'rites-of-magic': [('astral', 'Astral Magic & the Planetary Hours'), ('angels', 'The Orders of Angels')],
    'shaman': [('threshold', 'Theta: the Science of the Threshold')],
    'solomonic': [('solomonic', 'Solomon & the Goetia')],
    'the-cloud': [('paths', 'The Contemplative Lineages')],
    'the-great-work': [('hermetic', 'Hermes, Alchemy & True Will')],
    'the-inner-citadel': [('paths', 'The Contemplative Lineages')],
    'the-one': [('paths', 'The Contemplative Lineages')],
    'the-pleroma': [('paths', 'The Contemplative Lineages')],
    'the-signal': [('threshold', 'Theta: the Science of the Threshold')],
    'the-way': [('paths', 'The Contemplative Lineages')],
    'the-witness': [('paths', 'The Contemplative Lineages')],
}
PLANETARY = {'angelarium', 'ars-astrorum', 'celestial-above', 'celestial-veil', 'djin-invocation', 'rites-of-magic'}
EXTRA = {'obe-induction': [('/obe.html', 'The full OBE Induction guide'), ('/entrainment.html', 'Research: binaural entrainment and theta')],
         'shaman': [('/entrainment.html', 'Research: binaural entrainment and theta')],
         'the-signal': [('/entrainment.html', 'Research: binaural entrainment and theta')]}
# The richer flagship page is the canonical for the OBE Induction app.
CANONICAL_OVERRIDE = {'app/obe-induction.html': ORIGIN + '/obe.html'}

for f in sorted(os.listdir(os.path.join(ROOT, 'app'))):
    p = 'app/' + f
    slug = f[:-5]
    s = rd(p)
    if p in CANONICAL_OVERRIDE:
        s = ensure_canonical(s, CANONICAL_OVERRIDE[p])
        s = set_meta(s, 'property', 'og:url', CANONICAL_OVERRIDE[p])
    else:
        s = ensure_social(s, url_for(p), 'website')
    if 'property="og:site_name"' not in s:
        s = head_insert(s, ['<meta property="og:site_name" content="Discovery Science">'])
    if 'name="twitter:card"' not in s:
        s = head_insert(s, ['<meta name="twitter:card" content="summary">'])
    if 'property="og:type"' not in s:
        s = head_insert(s, ['<meta property="og:type" content="website">'])
    # Breadcrumbs from the visible crumb trail: Home > group > app
    name = html.unescape(re.search(r'<h1>(.*?)</h1>', s, re.S).group(1))
    items = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': ORIGIN + '/'},
             {'@type': 'ListItem', 'position': 2, 'name': 'The Apps', 'item': ORIGIN + '/new.html'}]
    items.append({'@type': 'ListItem', 'position': len(items) + 1, 'name': name, 'item': url_for(p)})
    s = add_jsonld(s, {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items}, '"@type":"BreadcrumbList"')
    # Nav + footer: Archive link (homepage nav already has it).
    s = s.replace('<li><a href="/library.html">Library</a></li></ul>',
                  '<li><a href="/library.html">Library</a></li><li><a href="/archive.html">Archive</a></li></ul>', 1) \
        if '<li><a href="/archive.html">Archive</a></li>' not in s else s
    s = s.replace('<a href="/library.html">Library</a><a href="/privacy.html">Privacy</a>',
                  '<a href="/library.html">Library</a><a href="/archive.html">Archive</a><a href="/privacy.html">Privacy</a>', 1)
    # "The history behind it": links into the Archive and the educational guides.
    links = [(f'/archive.html#{a}', f'Archive: {t}') for a, t in ARCHIVE.get(slug, [])]
    if slug in PLANETARY:
        links.append(('/planetary-hours.html', 'Guide: what are planetary hours?'))
    links += EXTRA.get(slug, [])
    if links and 'class="blk hist"' not in s:
        block = ('<section class="blk hist"><div class="wrap"><h2>The history <em>behind it</em></h2><div class="rel">'
                 + ''.join(f'<a href="{h}">{esc(t)}</a>' for h, t in links) + '</div></div></section>')
        i = s.find('<section class="blk"><div class="wrap"><h2>More from')
        if i > 0:
            s = s[:i] + block + s[i:]
    s = add_track(s)
    wr(p, s)

# --------------------------------------------------------------------------------------------
# 3. Privacy policies: indexable, canonical, described, and linked back to the app
# --------------------------------------------------------------------------------------------
PRIVACY = {  # page: (app name, landing page or None)
    'apkallu-privacy.html': ('APKALLU', '/app/apkallu.html'),
    'divining-vessel-privacy.html': ('The Divining Vessel', '/divining-vessel.html'),
    'ekstasis-privacy.html': ('Ekstasis', '/ekstasis.html'),
    'kispu-privacy.html': ('Kispu', '/kispu.html'),
    'neurolink-privacy.html': ('Neuro Link', '/neuro.html'),
    'obe-induction-privacy.html': ('OBE Induction', '/obe.html'),
    'planetary-attunement-privacy.html': ('Planetary Attunement', '/planetary-attunement.html'),
    'spirit-drum-privacy.html': ('Spirit Drum', '/spirit-drum.html'),
    'privacy/72-names.html': ('The 72 Names', '/new.html#names72'),
    'privacy/asclepion.html': ('Asclepion: Dream Temple', '/app/asclepion.html'),
    'privacy/chart-of-the-hour.html': ('Chart of the Hour', '/almanac.html'),
    'privacy/dhikr.html': ('Dhikr: Remembrance', '/dhikr.html'),
    'privacy/four-worlds.html': ('Four Worlds: Kabbalah', '/app/four-worlds.html'),
    'privacy/hour-of-the-rite.html': ('Hour of the Rite', None),
    'privacy/merkavah.html': ("Merkavah: Ezekiel's Chariot", '/app/merkavah-ezekiels-chariot.html'),
    'privacy/petit-lenormand.html': ('Petit Lenormand', '/almanac.html'),
    'privacy/sacred-breath.html': ('Sacred Breath', None),
    'privacy/sacred-flame.html': ('Sacred Flame', None),
    'privacy/sacred-sound.html': ('Sacred Sound', '/google-play.html'),
    'privacy/sefer-yetzirah.html': ('Sefer Yetzirah: Letters', '/app/sefer-yetzirah-letters.html'),
    'privacy/theurgia.html': ('Theurgia: Chaldean Ascent', '/theurgia.html'),
    'privacy/tree-of-life.html': ('Tree of Life: Kabbalah', '/app/tree-of-life.html'),
    'privacy.html': (None, None),
}
for p, (app, landing) in PRIVACY.items():
    s = rd(p)
    if 'name="description"' not in s:
        d = (f'Privacy policy for the {app} Android app by Discovery Science, Inc.' if app
             else 'Privacy at Discovery Science: how our Android apps and this website handle information.')
        s = set_meta(s, 'name', 'description', d)
    s = ensure_canonical(s, url_for(p))
    if 'data-ds-applink' not in s:
        target = landing or '/new.html'
        label = f'About {esc(app)} and the other Discovery Science apps' if app else 'All Discovery Science apps'
        line = (f'<p data-ds-applink style="margin-top:28px;font-size:14px"><a href="{target}">{label} →</a>'
                f' · <a href="/">discovery-science.com</a></p>\n')
        i = s.rindex('</main>') if '</main>' in s else s.rindex('</body>')
        s = s[:i] + line + s[i:]
    wr(p, s)

# --------------------------------------------------------------------------------------------
# 4. The planetary hours guide, built from its template
# --------------------------------------------------------------------------------------------
ORDER = ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon']
GLYPH = {'Saturn': '♄', 'Jupiter': '♃', 'Mars': '♂', 'Sun': '☉', 'Venus': '♀', 'Mercury': '☿', 'Moon': '☽'}
DAYS = [('Sunday', 'Sun'), ('Monday', 'Moon'), ('Tuesday', 'Mars'), ('Wednesday', 'Mercury'),
        ('Thursday', 'Jupiter'), ('Friday', 'Venus'), ('Saturday', 'Saturn')]
rows = []
for h in range(24):
    label = f'Day {h + 1}' if h < 12 else f'Night {h - 11}'
    cells = ''.join(f'<td class="pl">{GLYPH[ORDER[(ORDER.index(r) + h) % 7]]} {ORDER[(ORDER.index(r) + h) % 7]}</td>' for _, r in DAYS)
    rows.append(f'<tr><td>{label}</td>{cells}</tr>')
# self-check: the 25th hour is the next day's ruler
for i, (_, r) in enumerate(DAYS):
    assert ORDER[(ORDER.index(r) + 24) % 7] == DAYS[(i + 1) % 7][1]
week = ('<table class="data"><caption class="fine" style="text-align:left;caption-side:top;padding-bottom:6px">Ruling planet of each planetary hour, by weekday</caption>'
        '<thead><tr><th scope="col">Hour</th>' + ''.join(f'<th scope="col">{d}</th>' for d, _ in DAYS) + '</tr></thead><tbody>'
        + ''.join(rows) + '</tbody></table>')
FAQ = [
    ('What are planetary hours?',
     'Planetary hours divide the daylight into twelve equal parts and the night into twelve more, and assign each part to one of the seven classical planets in the Chaldean order: Saturn, Jupiter, Mars, the Sun, Venus, Mercury and the Moon.'),
    ('Is a planetary hour sixty minutes long?',
     'Only around the equinoxes. A day-hour is one twelfth of the time from sunrise to sunset and a night-hour one twelfth of the time from sunset to the next sunrise, so in summer day-hours are long and night-hours short, and in winter the reverse.'),
    ('Which planet rules the first hour of the day?',
     'The planet that names the weekday: the Sun on Sunday, the Moon on Monday, Mars on Tuesday, Mercury on Wednesday, Jupiter on Thursday, Venus on Friday and Saturn on Saturday. The planetary day begins at sunrise.'),
    ('Why do planetary hour calculators give slightly different times?',
     'Because they define sunrise differently, for example by the upper edge or the centre of the Sun, with or without refraction. Every boundary of the day moves with that choice, usually by a minute or two.'),
    ('Do planetary hours work near the North or South Pole?',
     'Not in the traditional form. When the Sun does not rise or does not set there is no daylight or night to divide into twelve, so the hours cannot be calculated.'),
    ('Is there scientific evidence that planetary hours affect events?',
     'No. The history of the system is well documented, but its effects are a matter of religious and magical tradition, not of scientific evidence. Many people today use the hours as a devotional calendar or a way to structure attention.'),
]
faq_html = ''.join(f'<dt>{esc(q)}</dt><dd>{esc(a)}</dd>' for q, a in FAQ)
faq_ld = '<script type="application/ld+json">' + json.dumps({
    '@context': 'https://schema.org', '@type': 'FAQPage',
    'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]},
    ensure_ascii=False, separators=(',', ':')) + '</script>'
tpl = rd('tools/templates/planetary-hours.src.html')
page = tpl.replace('{{WEEK_TABLE}}', week).replace('{{FAQ_HTML}}', faq_html).replace('{{FAQ_JSONLD}}', faq_ld)
page = add_track(page)
wr('planetary-hours.html', page)

# --------------------------------------------------------------------------------------------
# 5. sitemap.xml: every indexable canonical page (privacy policies and 404 excluded)
# --------------------------------------------------------------------------------------------
SITEMAP = ['index.html', 'new.html', 'angels.html', 'seven-angels.html', 'archive.html', 'planetary-hours.html',
           'library.html', 'catalog.html', 'apps.html', 'almanac.html', 'google-play.html', 'obe.html', 'oracle.html',
           'neuro.html', 'entrainment.html', 'shop.html',
           'asclepion.html', 'dhikr.html', 'divining-vessel.html', 'ekstasis.html', 'kispu.html',
           'planetary-attunement.html', 'spirit-drum.html', 'theurgia.html']
SITEMAP += ['app/' + f for f in sorted(os.listdir(os.path.join(ROOT, 'app'))) if 'app/' + f not in CANONICAL_OVERRIDE]
out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in SITEMAP:
    out.append(f'  <url><loc>{url_for(p)}</loc><lastmod>{TODAY}</lastmod></url>')
out.append('</urlset>')
wr('sitemap.xml', '\n'.join(out) + '\n')
print('sitemap URLs:', len(SITEMAP))

# --------------------------------------------------------------------------------------------
# 6. Repair homepage fragment links. The old homepage (now catalog.html) held these sections;
#    links across the site still pointed at "/#state" etc., which now land at the top of "/".
# --------------------------------------------------------------------------------------------
CAT_IDS = set(re.findall(r'\bid="([^"]+)"', rd('catalog.html')))
fixed = 0
for d, dirs, files in os.walk(ROOT):
    dirs[:] = [x for x in dirs if x not in {'.git', 'legacy-monty-site', 'tools'}]
    for f in files:
        if not f.endswith('.html'):
            continue
        p = os.path.relpath(os.path.join(d, f), ROOT).replace(os.sep, '/')
        s0 = s = rd(p)
        s = re.sub(r'href="/#([A-Za-z0-9-]+)"',
                   lambda m: f'href="/catalog.html#{m.group(1)}"' if m.group(1) in CAT_IDS and m.group(1) != 'apps' else m.group(0), s)
        s = s.replace('href="/#soon"', 'href="/new.html"')
        if s != s0:
            fixed += 1
            wr(p, s)
print('files with repaired fragment links:', fixed)
