#!/usr/bin/env python3
"""Builds coming-soon.html: newly released and upcoming Discovery Science apps.
Edit the lists below, then run: python3 tools/build_coming_soon.py
For apps not yet released, the line describes the source text or tradition only (not app features)."""
import html
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPDATED = '17 November 2026'

# Live on Google Play (verified listing titles), released most recently
JUST_RELEASED = [
    ('Advent Angels: Days of Light', 'com.discoveryscience.adventangels'),
    ('369 Ritual: 33-Day Scripting', 'com.discoveryscience.ritual369'),
    ('13 Wishes: Twelve Nights', 'com.discoveryscience.thirteenwishes'),
    ('Picatrix: 28 Lunar Mansions', 'com.discoveryscience.picatrixmansions'),
    ('Book of Enoch: The Watchers', 'com.discoveryscience.enochwatchers'),
    ('Enoch: Parables & Son of Man', 'com.discoveryscience.enochparables'),
    ('Epistle of Enoch: 10 Weeks', 'com.discoveryscience.enochepistle'),
    ('Book of Jubilees', 'com.discoveryscience.jubilees'),
    ('Pistis Sophia', 'com.discoveryscience.pistissophia'),
    ('Gospel of Mary Magdalene', 'com.discoveryscience.marymagdalene'),
    ('Gospel of Thomas: Side by Side', 'com.discoveryscience.thomasparallels'),
]

IN_REVIEW = [
    ('36 Decans', 'The thirty-six star groups of the Egyptian night sky, later the decans of Hellenistic astrology.'),
    ('Enoch Calendar', 'The 364-day solar calendar of the Astronomical Book of 1 Enoch.'),
    ('Dream Visions', 'The two dream visions of 1 Enoch 83–90, including the Animal Apocalypse.'),
    ('2 Enoch', 'The Slavonic Book of Enoch, Enoch’s journey through the heavens.'),
]

COMING_NEXT = [
    ('Mimetic Mirror', None), ('Scapegoat Watch', None), ('Jubilee Clock', None), ('Katechon', None),
    ('Enochian Grimoire', 'The angelic system recorded by John Dee and Edward Kelley.'),
    ('Odes of Solomon', 'An early Christian hymnbook of forty-two odes.'),
    ('3 Enoch', 'The Hebrew Book of Enoch, a Hekhalot text in which Enoch becomes the angel Metatron.'),
    ('Gospel of Philip', 'A text from the Nag Hammadi library.'),
    ('Secret Book of John', 'The Apocryphon of John, a Gnostic revelation preserved at Nag Hammadi.'),
    ('Apocalypse of Abraham', 'A Jewish apocalypse surviving in Old Church Slavonic.'),
    ('Twelve Patriarchs', 'The Testaments of the Twelve Patriarchs, the farewell words of the sons of Jacob.'),
    ('Psalms for Every Need', 'The Psalms gathered by purpose, after the old tradition of praying them for particular needs.'),
    ('Ars Notoria', 'The Notory Art, a medieval Solomonic rite of prayers for learning and memory.'),
    ('Amesha Spentas', 'The Bounteous Immortals of Zoroastrianism.'),
    ('Geomancy', 'Divination by the sixteen figures, practised from the medieval Arabic world to Renaissance Europe.'),
    ('Amduat', 'The Egyptian book of “what is in the underworld”: the Sun’s journey through the twelve hours of the night.'),
]

PLANNED = [
    ('Hildegard', 'Hildegard of Bingen, twelfth-century visionary, composer and healer.'),
    ('Eleusis', 'The Mysteries of Demeter and Persephone at Eleusis.'),
    ('Mithras', 'The Roman mysteries of Mithras.'),
    ('Ifá', 'The Yoruba system of divination.'),
    ('Chymical Wedding', 'The Chymical Wedding of Christian Rosenkreutz, the Rosicrucian allegory of 1616.'),
    ('Bardo', 'The Tibetan teachings on the intermediate states between death and rebirth.'),
    ('Tzolk’in', 'The 260-day sacred calendar of the Maya.'),
    ('Ars Memoriae', 'The classical and Renaissance art of memory.'),
    ('Sacred Geometry Studio', None),
    ('Celestial Hierarchy', 'The nine choirs of angels of Pseudo-Dionysius the Areopagite.'),
    ('Gayatri', 'The Gayatri mantra of the Rig Veda.'),
    ('Delphic Maxims', 'The sayings inscribed at the temple of Apollo at Delphi.'),
    ('Norito', 'The ritual prayers of Shinto.'),
    ('Nada Yoga', 'The yoga of inner sound.'),
    ('Poimandres', 'The first treatise of the Corpus Hermeticum.'),
    ('Ignatian Examen', 'The daily prayer of review taught by Ignatius of Loyola.'),
    ('Awen', 'The poetic inspiration of Welsh and bardic tradition.'),
    ('Zohar', 'The central work of Kabbalah.'),
    ('Bahir', 'The Book of Brightness, one of the earliest Kabbalistic texts.'),
    ('Counting the Omer', 'The forty-nine days counted between Passover and Shavuot.'),
    ('Tzimtzum', 'The divine contraction of Lurianic Kabbalah.'),
    ('Hermetic Planetary Seals', None),
    ('Enochian Watchtowers', 'The four Watchtowers of the Dee–Kelley angelic system.'),
    ('Theban Alphabet', 'The magical alphabet first printed in the early sixteenth century by Trithemius and Agrippa.'),
    ('Orphic Hymns', 'The eighty-seven hymns of the Orphic tradition.'),
    ('Chaldean Oracles', 'The late antique oracles at the heart of theurgy.'),
    ('Abramelin', 'The Book of Abramelin and its long retreat for the Holy Guardian Angel.'),
    ('Kybalion', 'The 1908 handbook of seven Hermetic principles.'),
    ('Raziel', 'Sefer Raziel HaMalakh, the Book of the Angel Raziel.'),
]

IOS = [
    ('Quietwave: Binaural Calm', 'https://apps.apple.com/us/app/quietwave-binaural-calm/id6804113997'),
    ('Presence: Lectio', 'https://apps.apple.com/us/app/presence-lectio/id6804113838'),
]
IOS_DEVELOPER = 'https://apps.apple.com/us/developer/montgomery-ostrander/id6804113840'


def e(s):
    return html.escape(s, quote=True)


def cards(items, badge):
    out = ''
    for name, about in items:
        out += f'<li><span class="badge">{badge}</span><b>{e(name)}</b>' + (f'<span>{e(about)}</span>' if about else '') + '</li>'
    return out


released = ''.join(
    f'<li><span class="badge live">On Google Play</span><b>{e(n)}</b><a class="btn gold small" href="https://play.google.com/store/apps/details?id={i}" rel="noopener">Get it on Google Play</a></li>'
    for n, i in JUST_RELEASED)
ios = ''.join(f'<li><span class="badge live">App Store</span><b>{e(n)}</b><a class="btn ghost small" href="{u}" rel="noopener">Download on the App Store</a></li>' for n, u in IOS)

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>New &amp; Coming Soon: Upcoming Discovery Science Apps</title>
<meta name="description" content="The newest Discovery Science apps on Google Play and the ones on their way: Enoch, Nag Hammadi, Hermetic, Kabbalistic and mystery-tradition apps in review, built and planned.">
<link rel="canonical" href="https://www.discovery-science.com/coming-soon.html">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Discovery Science">
<meta property="og:title" content="New and Coming Soon from Discovery Science">
<meta property="og:description" content="The newest apps on Google Play and the ones on their way.">
<meta property="og:url" content="https://www.discovery-science.com/coming-soon.html">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
<style>
.cs{{list-style:none;padding:0;margin:18px 0 0;display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}}
.cs li{{border:1px solid var(--line);border-radius:18px;padding:18px;background:linear-gradient(180deg,rgba(13,20,34,.92),rgba(9,14,24,.92));display:flex;flex-direction:column;gap:8px}}
.cs b{{font-family:var(--serif);font-size:23px;font-weight:500;color:var(--text);line-height:1.15}}
.cs span:not(.badge){{color:var(--soft);font-size:14.5px}}
.cs .btn{{align-self:flex-start;margin-top:auto}}
.badge{{align-self:flex-start;font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;padding:3px 9px;border-radius:999px;border:1px solid var(--line2);color:var(--muted)}}
.badge.live{{color:#1a1408;background:var(--gold2);border-color:var(--gold2)}}
.badge.review{{color:var(--gold2);border-color:rgba(212,174,98,.5)}}
.cs-sec{{padding:56px 0 0}}
.cs-sec h2{{font-size:clamp(30px,4.2vw,48px);margin:8px 0 6px}}
</style>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://www.discovery-science.com/"}},{{"@type":"ListItem","position":2,"name":"On Google Play","item":"https://www.discovery-science.com/google-play.html"}},{{"@type":"ListItem","position":3,"name":"New and Coming Soon","item":"https://www.discovery-science.com/coming-soon.html"}}]}}</script>
</head>
<body data-page="play">
<canvas id="sky"></canvas>
<div id="nav"></div>
<header class="hero" style="min-height:auto;padding:90px 0 30px"><div class="wrap">
  <div class="folio"><a href="/google-play.html" style="color:inherit">The library on Google Play</a> · Updated {UPDATED}</div>
  <h1>New, and <em>coming soon.</em></h1>
  <p class="lede">106 Discovery Science apps are on Google Play today. Here are the newest, and the {len(IN_REVIEW) + len(COMING_NEXT) + len(PLANNED)} on their way: the books of Enoch and the Nag Hammadi library, the Hermetic and Kabbalistic classics, and the mystery traditions of the ancient world.</p>
  <div class="btns" style="margin-top:24px"><a class="btn gold" href="/google-play.html">See all 106 live apps</a><a class="btn ghost" href="#review">In review</a><a class="btn ghost" href="#next">Coming next</a><a class="btn ghost" href="#planned">Planned</a></div>
</div></header>

<section class="cs-sec" style="padding-top:20px"><div class="wrap">
  <div class="eyebrow">Just released</div>
  <h2>New on <em>Google Play</em></h2>
  <ul class="cs">{released}</ul>
</div></section>

<section class="cs-sec" id="review"><div class="wrap">
  <div class="eyebrow">In review</div>
  <h2>With Google Play <em>now</em></h2>
  <p class="muted">Submitted and waiting for Google’s review.</p>
  <ul class="cs">{cards(IN_REVIEW, '<span>In review</span>').replace('<span class="badge"><span>In review</span></span>', '<span class="badge review">In review</span>')}</ul>
</div></section>

<section class="cs-sec" id="next"><div class="wrap">
  <div class="eyebrow">Coming next</div>
  <h2>Built and <em>waiting to launch</em></h2>
  <p class="muted">These are finished. Google Play limits how many new apps a developer can publish each week, so they will appear over the coming weeks, roughly in this order.</p>
  <ul class="cs">{cards(COMING_NEXT, 'Coming next')}</ul>
</div></section>

<section class="cs-sec" id="planned"><div class="wrap">
  <div class="eyebrow">Planned</div>
  <h2>On the <em>calendar</em></h2>
  <p class="muted">Scheduled for release about three times a week, beginning with Hildegard in late November and ending with Raziel at the start of February.</p>
  <ul class="cs">{cards(PLANNED, 'Planned')}</ul>
</div></section>

<section class="cs-sec" id="ios"><div class="wrap">
  <div class="eyebrow">iPhone and iPad</div>
  <h2>On the <em>App Store</em></h2>
  <ul class="cs">{ios}</ul>
  <p style="margin-top:16px"><a href="{IOS_DEVELOPER}" rel="noopener">See every Discovery Science app on the App Store →</a></p>
  <p class="fine" style="margin-top:28px;padding-bottom:40px">Names, order and timing of upcoming apps may change. For apps not yet released, the description names the source text or tradition each one is built on.</p>
</div></section>

<div id="footer"></div>
<script src="/assets/site.js"></script>
<script src="/assets/track.js" defer></script>
</body>
</html>
'''
with open(os.path.join(ROOT, 'coming-soon.html'), 'w', encoding='utf-8') as fh:
    fh.write(page)
print('built coming-soon.html:', len(JUST_RELEASED), 'released,', len(IN_REVIEW), 'in review,', len(COMING_NEXT), 'next,', len(PLANNED), 'planned')
