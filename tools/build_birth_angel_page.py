#!/usr/bin/env python3
"""Builds birth-angel.html: the free "Find your birth angel" tool, the table of the 72 angels with their dates,
and the offer of the personal invocation. Shell (head, menu, footer) borrowed from shop.html. Run, then
  python3 tools/apply_nav.py && python3 tools/apply_newsletter.py && python3 tools/apply_seo.py"""
import datetime as dt
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import birth_angel as B  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUY = 'https://ostrander5.gumroad.com/l/angel-invocation'
GIFT = 'https://ostrander5.gumroad.com/l/angel-invocation-gift'


def dates_2026():
    """The day the Sun enters each five-degree span in 2026 (dates shift by about a day from year to year)."""
    out = []
    t = dt.datetime(2026, 3, 15, 12, tzinfo=dt.timezone.utc)
    for i in range(72):
        target = 5 * i
        while not (0 <= (B.sun_longitude(t) - target) % 360 < 180):
            t += dt.timedelta(hours=6)
        out.append(t)
    return out


def fmt(t):
    return f'{t:%B} {t.day}'


starts = dates_2026()
rows = []
for i, name in enumerate(B.ANGELS):
    a, b = starts[i], starts[(i + 1) % 72] - dt.timedelta(days=1)
    rows.append(f'<tr><td>{i + 1}</td><td><b>{name}</b></td><td>{fmt(a)} – {fmt(b)}</td><td>{B.SIGNS[i // 6]} {5 * (i % 6)}°–{5 * (i % 6) + 5}°</td>'
                f'<td>{B.CHOIRS[i // 8][0]}</td></tr>')

data = {'angels': B.ANGELS, 'choirs': B.CHOIRS, 'signs': B.SIGNS, 'kamea': B.KAMEA, 'digraphs': B.DIGRAPHS, 'letters': B.LETTERS,
        'dayAngel': B.DAY_ANGEL, 'buy': BUY, 'gift': GIFT}

shop = open(os.path.join(ROOT, 'shop.html'), encoding='utf-8').read()
head = shop[:shop.index('<header')]
foot = shop[shop.index('<footer'):]
title = 'Find Your Birth Angel: the 72 Angels by Birth Date, with Your Personal Sigil — Discovery Science'
desc = ('Free: find your birth angel among the 72 angels of the Shem ha-Mephorash from your birth date, the angel of the day you '
        'were born, and your personal sigil traced on your planet’s magic square, after Agrippa.')
head = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title)}</title>', head, count=1)
head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(desc)}">', head, count=1)
head = head.replace('https://www.discovery-science.com/shop.html', 'https://www.discovery-science.com/birth-angel.html')
head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{html.escape(title)}">', head, count=1)
head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{html.escape(desc)}">', head, count=1)
head = head.replace(' aria-current="page"', '')

faq = [
    ('What is a birth angel?', 'In the tradition of the 72 angels of the Shem ha-Mephorash, each angel is set over five degrees of the zodiac. '
     'Your birth angel is the one whose five degrees the Sun was passing through when you were born.'),
    ('Where do the 72 angels come from?', 'Their names are drawn from three verses of Exodus (14:19–21), each 72 letters long, read in a pattern '
     'that yields 72 three-letter names. To each the suffix -iah or -el is added. The assignment to five-degree spans and to the nine '
     'choirs is the French tradition of the 18th and 19th centuries.'),
    ('Why does my birth time matter?', 'The Sun moves about one degree a day, so for most people the date is enough. If you were born on the day the '
     'Sun crossed from one five-degree span to the next, your birth time decides which angel is yours.'),
    ('How is the sigil made?', 'Following Agrippa (De occulta philosophia, Book II, chapter 22), each letter of your name is given the number of the '
     'Hebrew letter it stands for, reduced to fit the magic square of the planet that ruled the day you were born, and a line is drawn from '
     'number to number across the square.'),
]
faq_ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
    {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]}, ensure_ascii=False)
head = head.replace('</head>', f'<script type="application/ld+json">{faq_ld}</script>\n</head>', 1)

body = f'''<header class="lhero"><div class="wrap"><div class="eyebrow">Free tool · the 72 angels</div>
<h1>Find your <em>birth angel.</em></h1>
<p class="lead">Enter your birth date to find which of the 72 angels of the Shem ha-Mephorash was keeping the Sun’s path when you were born,
the angel of your birth day, and your own sigil traced on your planet’s magic square, after Agrippa.</p></div></header>
<style>
.ba-form{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;max-width:760px;margin:0 auto 10px}}
.ba-form label{{display:block;font:500 11px/1.4 "IBM Plex Mono",monospace;letter-spacing:.16em;text-transform:uppercase;color:#cdb57a;margin-bottom:6px}}
.ba-form input{{width:100%;box-sizing:border-box;padding:12px 14px;border-radius:12px;border:1px solid rgba(226,189,108,.45);background:#0b0f1d;color:#f3ecd9;font:inherit;font-size:16px}}
.ba-go{{display:block;margin:16px auto 0;padding:14px 28px;border-radius:999px;border:0;background:linear-gradient(#f3dc9e,#c99a45);color:#1a1206;font:inherit;font-weight:600;cursor:pointer}}
#ba-out{{max-width:900px;margin:34px auto 0;display:none}}
.ba-card{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:26px;align-items:center;border:1px solid rgba(226,189,108,.35);
border-radius:18px;padding:26px;background:radial-gradient(ellipse at 30% 0,rgba(226,189,108,.12),transparent 70%)}}
@media (max-width:720px){{.ba-card{{grid-template-columns:1fr}}}}
.ba-card h2{{font-family:"Cormorant Garamond",Georgia,serif;font-weight:500;font-size:clamp(34px,6vw,52px);margin:4px 0 6px;color:#f3ecd9}}
.ba-card .k{{font:500 11px/1.4 "IBM Plex Mono",monospace;letter-spacing:.2em;text-transform:uppercase;color:#e2bd6c}}
.ba-card p{{color:#d6d0c2;line-height:1.65;margin:8px 0}}
.ba-sig{{background:#0b0f1d;border-radius:14px;border:1px solid rgba(226,189,108,.3);padding:12px}}
.ba-sig svg{{width:100%;height:auto;display:block}}
.ba-day{{display:flex;gap:14px;align-items:center;margin-top:14px}}.ba-day img{{width:84px;height:84px;border-radius:12px;border:1px solid rgba(226,189,108,.4)}}
.ba-offer{{margin-top:22px;border:1px solid rgba(226,189,108,.45);border-radius:18px;padding:24px;text-align:center;background:rgba(226,189,108,.06)}}
.ba-offer h3{{font-family:"Cormorant Garamond",Georgia,serif;font-weight:500;font-size:30px;margin:0 0 8px;color:#f3ecd9}}
.ba-offer ul{{text-align:left;max-width:560px;margin:10px auto 16px;color:#d6d0c2;line-height:1.7}}
.ba-btns{{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}}
.ba-btns a{{padding:13px 22px;border-radius:999px;text-decoration:none;font-weight:600}}
.ba-btns a.p{{background:linear-gradient(#f3dc9e,#c99a45);color:#1a1206}}.ba-btns a.s{{border:1px solid rgba(226,189,108,.6);color:#f3dc9e}}
.ba-table{{width:100%;border-collapse:collapse;font-size:15px}}.ba-table td,.ba-table th{{padding:7px 8px;border-bottom:1px solid rgba(226,189,108,.15);text-align:left}}
.ba-table th{{font:500 11px/1.4 "IBM Plex Mono",monospace;letter-spacing:.14em;text-transform:uppercase;color:#e2bd6c}}
.ba-scroll{{overflow-x:auto}}
</style>
<section><div class="wrap">
<form class="ba-form" id="ba-form" onsubmit="return false">
<div><label for="ba-name">Your first name</label><input id="ba-name" required placeholder="e.g. Mary" autocomplete="given-name"></div>
<div><label for="ba-date">Birth date</label><input id="ba-date" type="date" required></div>
<div><label for="ba-time">Birth time (optional)</label><input id="ba-time" type="time"></div>
</form>
<button class="ba-go" id="ba-go" type="button">Find my angel</button>
<div id="ba-out" aria-live="polite"></div>
</div></section>
<section><div class="wrap" style="max-width:820px">
<div class="eyebrow">The tradition</div><h2>The 72 angels and your birthday</h2>
<p>Three verses of Exodus (14:19–21) each have exactly 72 Hebrew letters. Read together in a particular pattern they give 72 three-letter names,
the <i>Shem ha-Mephorash</i>, the “explicit name” of God. Adding <i>-iah</i> or <i>-el</i> to each gives the names of 72 angels. In the
French tradition of the 18th and 19th centuries the 72 were spread around the zodiac, five degrees each, starting from the first degree of Aries
at the spring equinox, and grouped eight to a choir through the nine choirs of angels, from the Seraphim to the Angels.</p>
<p>Your birth angel is the one whose five degrees the Sun was crossing on the day you were born. The angel of your birth day comes from an older book,
the <i>Heptameron</i>, which gives each day of the week to an archangel and a planet. Your sigil follows Agrippa: your name traced as a line across
the magic square of that planet. The live <a href="/angel-of-the-hour.html">Angel of the Hour</a> clock shows when each planet’s hours fall today.</p>
<h3 style="margin-top:28px">The 72 angels and their dates</h3>
<p style="color:#a9a395">Dates are for 2026 and can shift by a day in other years; the degrees never change.</p>
<div class="ba-scroll"><table class="ba-table"><thead><tr><th>#</th><th>Angel</th><th>Dates</th><th>Degrees</th><th>Choir</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
<h3 style="margin-top:28px">Questions</h3>
{''.join(f'<h4>{html.escape(q)}</h4><p>{html.escape(a)}</p>' for q, a in faq)}
<p style="color:#8a8576;font-size:14px;margin-top:22px">This page describes a tradition, for reflection and devotion. It makes no promise of any outcome.</p>
</div></section>
<script>window.BA={json.dumps(data, ensure_ascii=False)};</script>
<script src="/assets/birth-angel.js" defer></script>
'''
open(os.path.join(ROOT, 'birth-angel.html'), 'w', encoding='utf-8').write(head + body + foot)
print('built birth-angel.html')
