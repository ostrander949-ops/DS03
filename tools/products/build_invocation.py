#!/usr/bin/env python3
"""The Personal Angel Invocation: an illustrated PDF (6 x 9 in), a printable card and a phone wallpaper, made from one person's
name, birth date, birth time and birthplace.

Usage:
  python3 tools/products/build_invocation.py --name "Mary" --date 1990-12-25 --time 07:30 \
      --lat 42.36 --lon -71.06 --tz America/New_York [--live-lat .. --live-lon .. --live-tz ..] \
      [--gift-from "Anne"] [--year 2026] --out <dir>
--time may be omitted (noon is used and the hour angel is left out). --live-* is where they live now (for the hours ahead);
it defaults to the birthplace. Writes <out>/<Name>-Angel-Invocation.zip with the PDF, card and wallpaper."""
import argparse
import datetime as dt
import os
import sys
import tempfile
import zipfile
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, Image as RLImage, PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.doctemplate import NextPageTemplate

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import angels_data as A  # noqa: E402
import birth_angel as B  # noqa: E402

FONT = os.path.join(HERE, 'fonts')
IMG = os.path.join(ROOT, 'assets', 'img', 'angels')
PAGE = (6 * inch, 9 * inch)
NAVY, GOLD, INK, MUTED = colors.HexColor('#0b0f1f'), colors.HexColor('#b8903f'), colors.HexColor('#1d1a14'), colors.HexColor('#6b6252')
GOLD_RGB = (243, 220, 158)
ORD = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth']
WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
GLYPH = {'Saturn': '♄', 'Jupiter': '♃', 'Mars': '♂', 'Sun': '☉', 'Venus': '♀', 'Mercury': '☿', 'Moon': '☽'}

for nm, f in (('Cinzel', 'Cinzel-SemiBold.ttf'), ('Cormorant', 'Cormorant-Regular.ttf'), ('CormorantSB', 'Cormorant-SemiBold.ttf'),
              ('CormorantI', 'Cormorant-Italic.ttf')):
    pdfmetrics.registerFont(TTFont(nm, os.path.join(FONT, f)))
pdfmetrics.registerFontFamily('Cormorant', normal='Cormorant', bold='CormorantSB', italic='CormorantI', boldItalic='CormorantI')
S = {
    'title': ParagraphStyle('t', fontName='Cinzel', fontSize=21, leading=27, alignment=TA_CENTER, textColor=INK, spaceAfter=4),
    'eyebrow': ParagraphStyle('e', fontName='Cinzel', fontSize=8.5, leading=12, alignment=TA_CENTER, textColor=GOLD, spaceAfter=4),
    'h2': ParagraphStyle('h2', fontName='Cinzel', fontSize=9.5, leading=13, textColor=GOLD, spaceBefore=8, spaceAfter=3),
    'body': ParagraphStyle('b', fontName='Cormorant', fontSize=11.6, leading=15.2, textColor=INK, spaceAfter=6),
    'lede': ParagraphStyle('l', fontName='CormorantI', fontSize=13.5, leading=18, alignment=TA_CENTER, textColor=INK, spaceAfter=8),
    'prayer': ParagraphStyle('p', fontName='CormorantI', fontSize=12.8, leading=17.5, textColor=INK, spaceAfter=9, leftIndent=8, rightIndent=8),
    'small': ParagraphStyle('s', fontName='Cormorant', fontSize=9.5, leading=12.5, textColor=MUTED, spaceAfter=4),
    'cell': ParagraphStyle('c', fontName='Cormorant', fontSize=10.5, leading=12.5, textColor=INK),
}


# Gift-appropriate summaries of each planet's work (the old books' darker offices for Mars and Saturn are left out of a personal gift).
GIFT = {
    'Sun': ('Warmth and good fortune, the goodwill of others, the end of quarrels, honour and health.', ['Favour', 'Honour', 'Health']),
    'Moon': ('Safe journeys, secrets gently brought to light, intuition, dreams and a clear, remembering mind.', ['Journeys', 'Intuition', 'Memory']),
    'Mars': ('Courage, strength and protection, the will to finish what has been begun, and vigour of body and mind.', ['Courage', 'Strength', 'Protection']),
    'Mercury': ('Learning and lost knowledge recovered, good counsel, healing, and doors that were locked opened.', ['Knowledge', 'Counsel', 'Healing']),
    'Jupiter': ('Joy and good cheer, love, peace in place of strife, healing, and losses averted.', ['Joy', 'Peace', 'Healing']),
    'Venus': ('Love and friendship, reconciliation, beauty, pleasure, laughter and health.', ['Love', 'Reconciliation', 'Beauty']),
    'Saturn': ('Patience and endurance, the wisdom that comes with time, and the strength to close what must be closed and keep what must be kept.',
               ['Patience', 'Endurance', 'Wisdom']),
}


def the(p):
    return 'the ' + p if p in ('Sun', 'Moon') else p


def symbol_font(size):
    for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/dejavu/DejaVuSans.ttf'):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.truetype(os.path.join(FONT, 'Cormorant-Regular.ttf'), size)


def draw_sigil(name, planet, size=1600, numbers=True, bg=(9, 12, 28)):
    sq = B.KAMEA[planet]
    n = len(sq)
    im = Image.new('RGB', (size, size), bg)
    d = ImageDraw.Draw(im)
    pad = size * 0.06
    cs = (size - 2 * pad) / n
    nf = ImageFont.truetype(os.path.join(FONT, 'Cormorant-Regular.ttf'), int(cs * 0.34))
    for r in range(n):
        for c in range(n):
            x0, y0 = pad + c * cs, pad + r * cs
            d.rectangle((x0, y0, x0 + cs, y0 + cs), outline=(80, 70, 45), width=max(1, size // 600))
            if numbers:
                d.text((x0 + cs / 2, y0 + cs / 2), str(sq[r][c]), font=nf, fill=(110, 95, 60), anchor='mm')
    cells = B.sigil_path(name, planet)
    pts = [(pad + c * cs + cs / 2, pad + r * cs + cs / 2) for r, c in cells]
    w = max(6, size // 110)
    glow = Image.new('L', im.size, 0)
    g = ImageDraw.Draw(glow)
    if len(pts) > 1:
        g.line(pts, fill=255, width=w * 3, joint='curve')
    glow = glow.filter(ImageFilter.GaussianBlur(w * 2))
    im.paste((233, 190, 100), (0, 0), glow.point(lambda v: int(v * 0.55)))
    d = ImageDraw.Draw(im)
    if len(pts) > 1:
        d.line(pts, fill=GOLD_RGB, width=w, joint='curve')
    if pts:
        x, y = pts[0]
        rr = w * 2.4
        d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=GOLD_RGB, width=w)
        (ax, ay), (bx, by) = pts[-1], (pts[-2] if len(pts) > 1 else (pts[-1][0] - 1, pts[-1][1]))
        L = max(1e-6, ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5)
        nx, ny = -(ay - by) / L * w * 2.8, (ax - bx) / L * w * 2.8
        d.line((ax + nx, ay + ny, ax - nx, ay - ny), fill=GOLD_RGB, width=w)
    return im


def card(name, info, sigil):
    W, H = 825, 1425
    im = Image.new('RGB', (W, H), (9, 12, 28))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((22, 22, W - 22, H - 22), 26, outline=(233, 207, 140), width=5)
    d.rounded_rectangle((36, 36, W - 36, H - 36), 18, outline=(166, 128, 58), width=2)
    f = lambda n, s: ImageFont.truetype(os.path.join(FONT, n), s)  # noqa: E731
    d.text((W / 2, 90), info['day_planet'].upper() + ' · ' + info['angel'].upper(), font=f('Cinzel-SemiBold.ttf', 30), fill=(233, 207, 140), anchor='mm')
    s = sigil.resize((660, 660), Image.LANCZOS)
    im.paste(s, ((W - 660) // 2, 150))
    d.text((W / 2, 880), name.upper(), font=f('Cinzel-SemiBold.ttf', 70), fill=(244, 236, 216), anchor='mm')
    d.text((W / 2, 960), f'under {info["angel"]}, of the {info["choir"]}', font=f('Cormorant-Italic.ttf', 42), fill=(233, 207, 140), anchor='mm')
    lines = [f'born {info["born_text"]}', f'day angel {info["day_angel"]}' + (f' · hour angel {info["hour_angel"]}' if info.get('hour_angel') else '')]
    for k, ln in enumerate(lines):
        d.text((W / 2, 1050 + k * 52), ln, font=f('Cormorant-Regular.ttf', 38), fill=(214, 206, 186), anchor='mm')
    d.text((W / 2, 1200), GLYPH[info['day_planet']], font=symbol_font(70), fill=(233, 207, 140), anchor='mm')
    d.text((W / 2, H - 78), 'DISCOVERY SCIENCE · PERSONAL INVOCATION', font=f('Cinzel-SemiBold.ttf', 18), fill=(166, 128, 58), anchor='mm')
    return im


def wallpaper(name, info, sigil):
    W, H = 1290, 2796
    im = Image.new('RGB', (W, H), (8, 10, 24))
    g = Image.new('L', (W, H), 0)
    ImageDraw.Draw(g).ellipse((W / 2 - 900, 1300 - 900, W / 2 + 900, 1300 + 900), fill=90)
    im.paste((40, 44, 82), (0, 0), g.filter(ImageFilter.GaussianBlur(220)))
    s = draw_sigil(name, info['day_planet'], 1100, numbers=False, bg=(0, 0, 0))
    mask = s.convert('L').point(lambda v: min(255, v * 2))
    im.paste(s, ((W - 1100) // 2, 760), mask)
    d = ImageDraw.Draw(im)
    f = lambda n, s_: ImageFont.truetype(os.path.join(FONT, n), s_)  # noqa: E731
    d.text((W / 2, 2050), info['angel'].upper(), font=f('Cinzel-SemiBold.ttf', 96), fill=(233, 207, 140), anchor='mm')
    d.text((W / 2, 2160), f'{info["day_angel"]} · {info["day_planet"]}', font=f('Cormorant-Italic.ttf', 64), fill=(220, 214, 196), anchor='mm')
    return im


def hours_ahead(planet, lat, lon, tz, start, days=28):
    """The planet's own day in the coming weeks, and its four aligned hours (1st and 8th of the day, 3rd and 10th of the night)."""
    out = []
    z = ZoneInfo(tz)
    for k in range(days):
        day = start + dt.timedelta(days=k)
        if B.DAY_RULER[day.weekday()] != planet:
            continue
        st, nx = B.sun_times(day, lat, lon), B.sun_times(day + dt.timedelta(days=1), lat, lon)
        if not st or not nx:
            continue
        rise, sset = st
        dh, nh = (sset - rise) / 12, (nx[0] - sset) / 12
        times = [rise, rise + 7 * dh, sset + 2 * nh, sset + 9 * nh]
        out.append((day, [t.astimezone(z) for t in times]))
    return out


def tfmt(t):
    return t.strftime('%I:%M %p').lstrip('0').lower()


def build(a):
    tz = ZoneInfo(a.tz)
    y, m, dd = map(int, a.date.split('-'))
    hh, mm = map(int, (a.time or '12:00').split(':'))
    born = dt.datetime(y, m, dd, hh, mm, tzinfo=tz)
    info = B.birth_angel(born, bool(a.time))
    info['angel'] = info['name']
    planet = B.DAY_RULER[born.weekday()]
    info['day_planet'], info['day_angel'] = planet, B.DAY_ANGEL[planet]
    ph = B.planetary_hour(born, a.lat, a.lon) if a.time else None
    hour = None
    if ph:
        ruler, idx, hplanet, is_day = ph
        period, no, hname, hangel = A.PAULINA[idx][:4]
        hour = dict(planet=hplanet, period=period, no=no, name=hname, angel=hangel, ruler=ruler)
        info['hour_angel'] = hangel
        planet_of_day_for_hours = ruler   # before sunrise the planetary day is the previous day's
        if planet_of_day_for_hours != planet:
            planet, info['day_planet'], info['day_angel'] = ruler, ruler, B.DAY_ANGEL[ruler]
    info['born_text'] = f'{born:%B} {born.day}, {born.year}' + (f', {tfmt(born)}' if a.time else '')
    seven = A.SEVEN[planet]
    office = {'plain': GIFT[planet][0], 'tags': GIFT[planet][1]}
    name = a.name.strip()
    tmp = tempfile.mkdtemp()
    sig = draw_sigil(name, planet)
    sig_path = os.path.join(tmp, 'sigil.jpg')
    sig.save(sig_path, quality=90)

    def portrait(slug, px=700):
        p = os.path.join(tmp, slug + '.jpg')
        Image.open(os.path.join(IMG, slug + '.webp')).convert('RGB').resize((px, px), Image.LANCZOS).save(p, quality=86)
        return p

    out_dir = a.out
    os.makedirs(out_dir, exist_ok=True)
    safe = ''.join(ch for ch in name if ch.isalnum()) or 'Friend'
    pdf_path = os.path.join(tmp, f'{safe}-Personal-Angel-Invocation.pdf')

    def on_page(c, doc):
        c.saveState()
        c.setFillColor(colors.HexColor('#fbf7ee'))
        c.rect(0, 0, PAGE[0], PAGE[1], fill=1, stroke=0)
        c.setFont('Cinzel', 7)
        c.setFillColor(MUTED)
        c.drawCentredString(PAGE[0] / 2, 0.45 * inch, f'THE PERSONAL INVOCATION OF {name.upper()} · {doc.page}')
        c.restoreState()

    def on_cover(c, doc):
        c.saveState()
        c.setFillColor(NAVY)
        c.rect(0, 0, PAGE[0], PAGE[1], fill=1, stroke=0)
        c.drawImage(sig_path, 1.0 * inch, 2.7 * inch, 4 * inch, 4 * inch)
        c.setFillColor(colors.HexColor('#e9cf8c'))
        c.setFont('Cinzel', 9)
        c.drawCentredString(PAGE[0] / 2, 8.3 * inch, 'DISCOVERY SCIENCE')
        c.setFont('Cinzel', 12)
        c.drawCentredString(PAGE[0] / 2, 7.75 * inch, 'THE PERSONAL INVOCATION OF')
        c.setFont('Cinzel', 26)
        c.drawCentredString(PAGE[0] / 2, 7.25 * inch, name.upper())
        c.setFont('CormorantI', 15)
        c.drawCentredString(PAGE[0] / 2, 2.2 * inch, f'under {info["angel"]}, {info["day_angel"]}' + (f' and {hour["angel"]}' if hour and hour['angel'] != info['day_angel'] else '')
                            if hour and hour['angel'] != info['day_angel'] else f'under {info["angel"]} and {info["day_angel"]}')
        c.setFont('Cormorant', 11)
        c.setFillColor(colors.HexColor('#c9c2b0'))
        c.drawCentredString(PAGE[0] / 2, 1.8 * inch, f'born {info["born_text"]}')
        c.restoreState()

    doc = BaseDocTemplate(pdf_path, pagesize=PAGE, leftMargin=0.7 * inch, rightMargin=0.7 * inch, topMargin=0.65 * inch,
                          bottomMargin=0.75 * inch, title=f'The Personal Invocation of {name}', author='Discovery Science')
    fr = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')
    doc.addPageTemplates([PageTemplate('cover', [fr], onPage=on_cover), PageTemplate('page', [fr], onPage=on_page)])
    st = [NextPageTemplate('page'), PageBreak()]

    if a.gift_from:
        st += [Spacer(1, 2.2 * inch), Paragraph('FOR', S['eyebrow']), Paragraph(name, S['title']), Spacer(1, 10),
               Paragraph(f'with love from {a.gift_from}', S['lede']), Paragraph(f'Christmas {a.year}', S['eyebrow']), Spacer(1, 30),
               Paragraph('“For he shall give his angels charge over thee, to keep thee in all thy ways.”', S['lede']),
               Paragraph('PSALM 91:11', S['eyebrow']), PageBreak()]

    # the three angels
    st += [Paragraph('YOUR ANGELS', S['eyebrow']), Paragraph(f'The Angels of {name}', S['title']),
           Paragraph(f'Born {info["born_text"]}, when the Sun stood at {int(info["deg"])}° {info["sign"]}.', S['lede'])]
    st += [Paragraph(f'I · YOUR BIRTH ANGEL: {info["angel"].upper()}', S['h2']),
           Paragraph(f'Of the seventy-two angels of the <i>Shem ha-Mephorash</i>, each keeps five degrees of the Sun’s yearly path. '
                     f'You were born in the degrees kept by <b>{info["angel"]}</b>, angel number {info["number"]} of 72, from '
                     f'{info["from_deg"] % 30}° to {info["from_deg"] % 30 + 5}° of {info["sign"]}. {info["angel"]} is one of the eight angels of the '
                     f'<b>{info["choir"]}</b>, the choir ruled by the archangel {info["archangel"]} in {info["sephira"]}. Tradition gives the '
                     f'{info["choir"]} {info["governs"]}.', S['body'])]
    if info['cusp']:
        st.append(Paragraph(f'You were born very close to the edge of these degrees; the angel next door is {info["neighbour"]}.', S['small']))
    st += [Paragraph(f'II · YOUR BIRTH-DAY ANGEL: {info["day_angel"].upper()}', S['h2']),
           Table([[RLImage(portrait(seven['slug']), 1.05 * inch, 1.05 * inch),
                   Paragraph(f'You were born on a {seven["day"]}, the day of {the(planet)}. The <i>Heptameron</i> gives this day to the archangel '
                             f'<b>{info["day_angel"]}</b>, who rules from the {seven["heaven_no"]} heaven, called {seven["heaven"]}. '
                             f'{office["plain"]}', S['body'])]],
                 colWidths=[1.2 * inch, None], style=[('VALIGN', (0, 0), (-1, -1), 'TOP')])]
    if hour:
        st += [Paragraph(f'III · YOUR HOUR ANGEL: {hour["angel"].upper()}', S['h2']),
               Table([[RLImage(portrait('paulina-' + hour['angel'].lower()), 1.05 * inch, 1.05 * inch),
                       Paragraph(f'You were born in the {ORD[hour["no"] - 1]} hour of the {hour["period"]}, the hour the <i>Ars Paulina</i> calls '
                                 f'<i>{hour["name"]}</i>, kept by the angel <b>{hour["angel"]}</b>. On that day the hour belonged to {the(hour["planet"])}, '
                                 f'so {hour["angel"]} came to you carrying the work of {the(hour["planet"])}: '
                                 f'{", ".join(GIFT[hour["planet"]][1]).lower()}.' + (
                                     f' Your hour angel shares a name with your day angel: you were born in an hour of {the(planet)} on {the(planet)}’s own day, '
                                     f'one of the four strongest hours of its week.' if hour['angel'] == info['day_angel'] else ''), S['body'])]],
                     colWidths=[1.2 * inch, None], style=[('VALIGN', (0, 0), (-1, -1), 'TOP')])]
    st += [Paragraph(f'YOUR FACE OF THE ZODIAC', S['h2']),
           Paragraph(f'Your Sun fell in the {ORD[info["face"] - 1]} face, or decan, of {info["sign"]}, ten degrees given to {info["face_ruler"]}.', S['body']), PageBreak()]

    # the sigil
    vals = B.name_values(name)
    top = len(B.KAMEA[planet]) ** 2
    st += [Paragraph('YOUR SIGIL', S['eyebrow']), Paragraph(f'The Sigil of {name}', S['title']),
           Paragraph(f'traced on the magic square of {the(planet)}', S['lede']), RLImage(sig_path, 3.9 * inch, 3.9 * inch), Spacer(1, 6),
           Paragraph(f'Agrippa gives each planet a magic square, whose rows, columns and diagonals all add to the same number. '
                     f'To make a sigil, each letter of a name is given the number of the Hebrew letter it stands for, reduced to fit the square, '
                     f'and a line is drawn from number to number, beginning at the circle and ending at the bar. Your name gives '
                     f'{", ".join(str(B.reduce_to(v, top)) for v in vals)} on the square of {the(planet)}, the planet of the day you were born.', S['body']),
           PageBreak()]

    # the invocation
    if hour and hour['angel'] == info['day_angel']:
        hour_line = f'you who keep also the {ORD[hour["no"] - 1]} hour of the {hour["period"]}, in which I first drew breath, '
    elif hour:
        hour_line = f'and you, <b>{hour["angel"]}</b>, who keep the {ORD[hour["no"] - 1]} hour of the {hour["period"]}, in which I first drew breath, '
    else:
        hour_line = ''
    st += [Paragraph('THE INVOCATION', S['eyebrow']), Paragraph('A Prayer to Your Angels', S['title']),
           Paragraph(f'To be said in the hour of {the(planet)}, with a candle lit and this sigil before you.', S['lede'])]
    prayer = [
        f'In the name of the One who is above every name, the beginning and the end of all things: I, <b>{name}</b>, '
        f'born when the Sun stood in {info["sign"]}, come before you in peace.',
        f'I call upon you, <b>{info["angel"]}</b>, of the holy choir of the {info["choir"]}, who kept the Sun’s path on the day I was born. '
        f'You who serve under {info["archangel"]} in {info["sephira"].split(",")[0]}, be near me.',
        f'I call upon you, <b>{info["day_angel"]}</b>, great angel of {seven["day"]}, who rule in the heaven of {seven["heaven"]}, '
        f'{hour_line}watch over me as you watched over the day of my birth.',
        f'Teach me {info["governs"].replace(" and ", ", and ", 1) if info["governs"].count(" and ") == 1 else info["governs"]}. '
        f'Guard my going out and my coming in. Lend me {", ".join(office["tags"][:3]).lower()} for what is good, and keep me from harm.',
        'As this sign is traced, so let my name be held in the light, and let me walk in the way that was set before me. Amen.',
    ]
    st += [Paragraph(p, S['prayer']) for p in prayer]
    st += [Paragraph('HOW TO USE IT', S['h2']),
           Paragraph(f'Choose an hour of {the(planet)} (the list on the next page gives the strongest ones near you), light a candle, and set the sigil card '
                     f'before you. Trace the sigil slowly with a finger, from the circle to the bar, then read the prayer aloud. Sit in silence for a while '
                     f'afterwards. Traditionally the perfume of {the(planet)} is {seven["perfume"]}.', S['body']), PageBreak()]

    # hours ahead
    start = dt.date.today() if not a.start else dt.date.fromisoformat(a.start)
    lat, lon, ltz = a.live_lat if a.live_lat is not None else a.lat, a.live_lon if a.live_lon is not None else a.lon, a.live_tz or a.tz
    rows = [[Paragraph(f'<b>{h}</b>', S['cell']) for h in ('Day', '1st hour', '8th hour', 'Night 3rd', 'Night 10th')]]
    for day, ts in hours_ahead(planet, lat, lon, ltz, start, 35):
        rows.append([Paragraph(f'{day:%a %b} {day.day}', S['cell'])] + [Paragraph(tfmt(t), S['cell']) for t in ts])
    tbl = Table(rows, colWidths=[1.25 * inch] + [1.0 * inch] * 4)
    tbl.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, 0), 0.8, GOLD), ('LINEBELOW', (0, 1), (-1, -1), 0.25, colors.HexColor('#d9cfb8')),
                             ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
    st += [Paragraph('YOUR HOURS', S['eyebrow']), Paragraph(f'The Hours of {the(planet).title()}', S['title']),
           Paragraph('the strongest times to pray to your angels in the weeks ahead', S['lede']),
           Paragraph(f'Each {seven["day"]}, four hours belong wholly to {the(planet)}: the first and eighth after sunrise, and the third and tenth after sunset. '
                     f'These are their starting times where you live ({ltz.replace("_", " ")}). Each lasts about an hour, longer or shorter with the season. '
                     f'For any other day, the live clock at discovery-science.com/angel-of-the-hour shows the hour and its angel.', S['body']),
           Spacer(1, 4), tbl, PageBreak()]

    st += [Paragraph('NOTES', S['eyebrow']), Paragraph('Sources', S['title'])]
    for p in [
        'The seventy-two angels: the names drawn from Exodus 14:19–21 as the <i>Shem ha-Mephorash</i>, with their five-degree spans of the zodiac and their '
        'choirs as given in the French tradition of the eighteenth and nineteenth centuries.',
        'The angels of the days: the <i>Heptameron</i>, attributed to Peter of Abano (printed 1559). The angels of the hours: the <i>Ars Paulina</i>, '
        'the third book of the <i>Lemegeton</i> (seventeenth century, Sloane MS 3825).',
        'The planetary squares and the tracing of names upon them: Henry Cornelius Agrippa, <i>De occulta philosophia</i> (1533), Book II, chapter 22.',
        'Sun positions are calculated for your birth time and place; planetary hours from the times of sunrise and sunset.',
        'This invocation is devotional art made for you. It describes a tradition, for reflection and prayer, and makes no promise of any outcome.',
    ]:
        st.append(Paragraph(p, S['body']))
    st.append(Paragraph('© Discovery Science · discovery-science.com', S['small']))
    doc.build(st)

    card_path = os.path.join(tmp, f'{safe}-Sigil-Card.png')
    card(name, info, draw_sigil(name, planet, 1100)).save(card_path, dpi=(300, 300))
    wp_path = os.path.join(tmp, f'{safe}-Sigil-Wallpaper.jpg')
    wallpaper(name, info, sig).save(wp_path, quality=90)
    zp = os.path.join(out_dir, f'{safe}-Angel-Invocation.zip')
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in (pdf_path, card_path, wp_path):
            z.write(p, os.path.basename(p))
    print(zp, '|', info['angel'], info['day_angel'], hour['angel'] if hour else '-')
    return zp, pdf_path, card_path, wp_path


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--name', required=True)
    ap.add_argument('--date', required=True)
    ap.add_argument('--time')
    ap.add_argument('--lat', type=float, required=True)
    ap.add_argument('--lon', type=float, required=True)
    ap.add_argument('--tz', required=True)
    ap.add_argument('--live-lat', type=float)
    ap.add_argument('--live-lon', type=float)
    ap.add_argument('--live-tz')
    ap.add_argument('--gift-from')
    ap.add_argument('--year', default=str(dt.date.today().year))
    ap.add_argument('--start')
    ap.add_argument('--out', required=True)
    build(ap.parse_args())
