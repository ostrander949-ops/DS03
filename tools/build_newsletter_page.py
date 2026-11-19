#!/usr/bin/env python3
"""Builds newsletter.html: what the weekly newsletter is, a signup form, and this week's issue as a sample.
Borrows the page shell (head, menu, footer) from shop.html. Run after weekly_reading.py changes, then
  python3 tools/apply_nav.py && python3 tools/apply_newsletter.py && python3 tools/apply_seo.py"""
import datetime as dt
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from weekly_reading import issue  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def md_inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\*(.+?)\*', r'<i>\1</i>', t)
    t = re.sub(r'(https://www\.discovery-science\.com(/[^\s<]*[^\s<.,;:)])?)', lambda m: f'<a href="{m.group(2) or "/"}">{m.group(2) or "discovery-science.com"}</a>', t)
    return t


def md_to_html(md):
    out, items = [], []
    for line in md.split('\n'):
        if line.startswith('- '):
            items.append(f'<li>{md_inline(line[2:])}</li>')
            continue
        if items:
            out.append('<ul>' + ''.join(items) + '</ul>')
            items = []
        if line.startswith('# '):
            out.append(f'<h3 class="ish">{md_inline(line[2:])}</h3>')
        elif line.startswith('## '):
            out.append(f'<h4>{md_inline(line[3:])}</h4>')
        elif line.strip() == '---':
            out.append('<hr>')
        elif line.strip():
            out.append(f'<p>{md_inline(line)}</p>')
    if items:
        out.append('<ul>' + ''.join(items) + '</ul>')
    return '\n'.join(out)


shop = open(os.path.join(ROOT, 'shop.html'), encoding='utf-8').read()
head = shop[:shop.index('<header')]
foot = shop[shop.index('<footer'):]
title = 'The Angels of the Week: a free weekly newsletter — Discovery Science'
desc = ('A free email every Sunday: the seven angels ruling the coming week, what the old books say each can do, '
        'an hour angel to meet each day, the Moon’s phases and a card of the week from the Angelic Tarot.')
head = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title)}</title>', head, count=1)
head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(desc)}">', head, count=1)
head = head.replace('https://www.discovery-science.com/shop.html', 'https://www.discovery-science.com/newsletter.html')
head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{html.escape(title)}">', head, count=1)
head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{html.escape(desc)}">', head, count=1)
head = head.replace(' aria-current="page"', '')

_t = dt.date.today()
md, sunday = issue(_t + dt.timedelta(days=(6 - _t.weekday()) % 7 or 7))  # the coming Sunday’s issue
body = f'''<header class="lhero"><div class="wrap"><div class="eyebrow">Free newsletter · every Sunday</div>
<h1>The Angels of <em>the Week.</em></h1>
<p class="lead">{html.escape(desc)}</p>
<p><a class="btn" href="#newsletter">Subscribe free</a></p></div></header>
<section><div class="wrap" style="max-width:760px">
<div class="eyebrow">The coming week’s issue, as a sample</div>
<style>.issue h3.ish{{font-family:"Cormorant Garamond",Georgia,serif;font-weight:500;font-size:30px;margin:10px 0 14px}}
.issue h4{{font-family:"Cormorant Garamond",Georgia,serif;font-weight:500;font-size:23px;color:#e9cf8c;margin:30px 0 8px}}
.issue p,.issue li{{line-height:1.7;color:#d6d0c2}}.issue hr{{border:0;border-top:1px solid rgba(226,189,108,.25);margin:30px 0}}
.issue a{{color:#e2bd6c}}</style>
<article class="issue">
{md_to_html(md)}
</article></div></section>
'''
open(os.path.join(ROOT, 'newsletter.html'), 'w', encoding='utf-8').write(head + body + foot)
print('built newsletter.html for the week of', sunday)
