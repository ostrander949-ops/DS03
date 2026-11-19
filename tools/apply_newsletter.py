#!/usr/bin/env python3
"""Adds the "Angels of the Week" newsletter signup to the main pages, between marker comments
<!--ds-news--> ... <!--/ds-news--> placed just before the footer. Re-run after a page is regenerated:
  python3 tools/apply_newsletter.py
The form posts to Buttondown. BUTTONDOWN is the newsletter's Buttondown username."""
import os
import re

BUTTONDOWN = 'discoveryscience'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ['index.html', 'angel-of-the-hour.html', 'planetary-hour-now.html', 'planetary-hours.html', 'angels.html',
         'seven-angels.html', 'archive.html', 'shop.html', 'newsletter.html']

CSS = ('<style>.dsn{padding:56px 0;border-top:1px solid rgba(226,189,108,.18);background:radial-gradient(ellipse at 50% 0,rgba(226,189,108,.10),transparent 70%)}'
       '.dsn .wrap{max-width:760px;margin:0 auto;padding:0 20px;text-align:center}'
       '.dsn .eb{font:500 11px/1.4 "IBM Plex Mono",monospace;letter-spacing:.22em;text-transform:uppercase;color:#e2bd6c}'
       '.dsn h2{font-family:"Cormorant Garamond",Georgia,serif;font-weight:500;font-size:clamp(28px,4.6vw,40px);line-height:1.1;margin:10px 0 10px;color:#f3ecd9}'
       '.dsn h2 em{color:#e9cf8c}.dsn p{color:#b9b4a6;margin:0 auto 18px;max-width:600px;line-height:1.6}'
       '.dsn form{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin:0 auto;max-width:520px}'
       '.dsn input[type=email]{flex:1 1 240px;min-width:0;padding:13px 16px;border-radius:999px;border:1px solid rgba(226,189,108,.45);background:#0b0f1d;color:#f3ecd9;font:inherit;font-size:16px}'
       '.dsn button{padding:13px 22px;border-radius:999px;border:0;background:linear-gradient(#f3dc9e,#c99a45);color:#1a1206;font-weight:600;cursor:pointer;font:inherit;font-weight:600}'
       '.dsn small{display:block;margin-top:12px;color:#8a8576;font-size:12.5px}.dsn small a{color:#cdb57a}</style>')


def block(page):
    src = page.replace('.html', '').replace('index', 'home')
    return ('<!--ds-news--><section class="dsn" id="newsletter" aria-labelledby="dsn-h">' + CSS +
            '<div class="wrap"><div class="eb">Free · every Sunday</div>'
            '<h2 id="dsn-h">The Angels of <em>the Week</em></h2>'
            '<p>Each Sunday: the seven angels ruling the coming days, what the old books say each can do, an hour angel to meet each day, '
            'the Moon’s phases and a card of the week from the Angelic Tarot.</p>'
            f'<form action="https://buttondown.com/api/emails/embed-subscribe/{BUTTONDOWN}" method="post" target="_blank" '
            'onsubmit="window.va&&window.va(\'event\',{name:\'Newsletter Signup\',data:{page:location.pathname}})">'
            '<label for="dsn-e" style="position:absolute;left:-9999px">Email address</label>'
            '<input type="email" name="email" id="dsn-e" placeholder="you@example.com" required autocomplete="email">'
            f'<input type="hidden" name="tag" value="site-{src}"><input type="hidden" value="1" name="embed">'
            '<button type="submit">Send me the angels</button></form>'
            f'<small>One email a week. Unsubscribe any time. <a href="/newsletter.html">See a sample issue</a> · <a href="/privacy.html">Privacy</a></small>'
            '</div></section><!--/ds-news-->')


changed = 0
for page in PAGES:
    p = os.path.join(ROOT, page)
    if not os.path.exists(p):
        continue
    s0 = s = open(p, encoding='utf-8').read()
    s = re.sub(r'<!--ds-news-->.*?<!--/ds-news-->', '', s, flags=re.S)
    b = block(page)
    if '<div id="footer">' in s:
        s = s.replace('<div id="footer">', b + '<div id="footer">', 1)
    elif '<footer' in s:
        i = s.index('<footer')
        s = s[:i] + b + s[i:]
    if s != s0:
        open(p, 'w', encoding='utf-8').write(s)
        changed += 1
print('newsletter block on', changed, 'pages')
