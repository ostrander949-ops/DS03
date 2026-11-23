#!/usr/bin/env python3
"""Adds a "Find your birth angel" banner to the angel and planetary-hours pages, between <!--ds-ba--> markers,
just before the newsletter block. Re-run after those pages are regenerated (after apply_newsletter.py)."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ['index.html', 'angel-of-the-hour.html', 'planetary-hour-now.html', 'planetary-hours.html', 'angels.html', 'seven-angels.html',
         'newsletter.html', 'shop.html']
BLOCK = ('<!--ds-ba--><section style="padding:34px 0"><div class="wrap" style="max-width:860px"><a href="/birth-angel.html" '
         'style="display:flex;gap:18px;align-items:center;text-decoration:none;border:1px solid rgba(226,189,108,.4);border-radius:18px;'
         'padding:18px 22px;background:radial-gradient(ellipse at 20% 0,rgba(226,189,108,.14),transparent 70%)">'
         '<img src="/assets/img/angels/michael-640.webp" alt="" width="72" height="72" loading="lazy" style="border-radius:12px;flex:none">'
         '<span><span style="display:block;font:500 11px/1.4 \'IBM Plex Mono\',monospace;letter-spacing:.2em;text-transform:uppercase;color:#e2bd6c">'
         'Free · new</span><span style="display:block;font-family:\'Cormorant Garamond\',Georgia,serif;font-size:26px;color:#f3ecd9;line-height:1.2">'
         'Find your birth angel</span><span style="color:#b9b4a6">Which of the 72 angels kept the Sun on your birthday, the angel of your birth day, '
         'and your own sigil after Agrippa →</span></span></a></div></section><!--/ds-ba-->')
n = 0
for page in PAGES:
    p = os.path.join(ROOT, page)
    if not os.path.exists(p):
        continue
    s0 = s = open(p, encoding='utf-8').read()
    s = re.sub(r'<!--ds-ba-->.*?<!--/ds-ba-->', '', s, flags=re.S)
    if '<!--ds-news-->' in s:
        s = s.replace('<!--ds-news-->', BLOCK + '<!--ds-news-->', 1)
    if s != s0:
        open(p, 'w', encoding='utf-8').write(s)
        n += 1
print('birth angel banner on', n, 'pages')
