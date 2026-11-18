#!/usr/bin/env python3
"""The Book of the Angels of the Days and Hours: an illustrated PDF e-book (6 x 9 in)
built from tools/angels_data.py and the painted portraits.
Usage: python3 tools/products/build_book.py <out_dir>"""
import os
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether, PageBreak, PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import angels_data as A  # noqa: E402

FONT = os.path.join(HERE, 'fonts')
IMG = os.path.join(ROOT, 'assets', 'img', 'angels')
PAGE = (6 * inch, 9 * inch)
NAVY, GOLD, INK, MUTED = colors.HexColor('#0b0f1f'), colors.HexColor('#b8903f'), colors.HexColor('#1d1a14'), colors.HexColor('#6b6252')
ORD = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth']
ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
CHALDEAN = ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon']
DAY_RULER = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
WEEK = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

for name, file in (('Cinzel', 'Cinzel-SemiBold.ttf'), ('Cormorant', 'Cormorant-Regular.ttf'), ('CormorantSB', 'Cormorant-SemiBold.ttf'),
                   ('CormorantI', 'Cormorant-Italic.ttf')):
    pdfmetrics.registerFont(TTFont(name, os.path.join(FONT, file)))
pdfmetrics.registerFontFamily('Cormorant', normal='Cormorant', bold='CormorantSB', italic='CormorantI', boldItalic='CormorantI')

S = {
    'title': ParagraphStyle('t', fontName='Cinzel', fontSize=24, leading=30, alignment=TA_CENTER, textColor=INK, spaceAfter=6),
    'eyebrow': ParagraphStyle('e', fontName='Cinzel', fontSize=8.5, leading=12, alignment=TA_CENTER, textColor=GOLD, spaceAfter=4),
    'h2': ParagraphStyle('h2', fontName='Cinzel', fontSize=10, leading=14, textColor=GOLD, spaceBefore=10, spaceAfter=4),
    'body': ParagraphStyle('b', fontName='Cormorant', fontSize=11.5, leading=15.5, textColor=INK, spaceAfter=7),
    'lede': ParagraphStyle('l', fontName='CormorantI', fontSize=13, leading=17, alignment=TA_CENTER, textColor=INK, spaceAfter=10),
    'quote': ParagraphStyle('q', fontName='CormorantI', fontSize=11.5, leading=15, textColor=INK, leftIndent=14, rightIndent=8, spaceAfter=2),
    'cite': ParagraphStyle('c', fontName='Cinzel', fontSize=6.5, leading=9, textColor=MUTED, leftIndent=14, spaceAfter=8),
    'small': ParagraphStyle('s', fontName='Cormorant', fontSize=9.5, leading=12.5, textColor=MUTED, spaceAfter=4),
    'cell': ParagraphStyle('cell', fontName='Cormorant', fontSize=9.5, leading=11.5, textColor=INK),
    'tiny': ParagraphStyle('tiny', fontName='Cormorant', fontSize=8.3, leading=9.6, textColor=INK, alignment=TA_CENTER),
}


def the(p):
    return 'the ' + p if p in ('Sun', 'Moon') else p


_CACHE = {}


def jpg(slug, px=900):
    """Embed portraits as JPEG (reportlab would store the WebP losslessly)."""
    if slug not in _CACHE:
        import tempfile
        from PIL import Image as PImage
        f = os.path.join(tempfile.gettempdir(), f'book-{slug}-{px}.jpg')
        PImage.open(os.path.join(IMG, slug + '.webp')).convert('RGB').resize((px, px), PImage.LANCZOS).save(f, quality=84)
        _CACHE[slug] = f
    return _CACHE[slug]


def portrait(slug, w):
    return Image(jpg(slug), width=w, height=w)


def on_page(c, doc):
    c.saveState()
    c.setFillColor(colors.HexColor('#fbf7ee'))
    c.rect(0, 0, PAGE[0], PAGE[1], fill=1, stroke=0)
    if doc.page > 1:
        c.setFont('Cinzel', 7)
        c.setFillColor(MUTED)
        c.drawCentredString(PAGE[0] / 2, 0.45 * inch, f'THE BOOK OF THE ANGELS · {doc.page}')
    c.restoreState()


def on_cover(c, doc):
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE[0], PAGE[1], fill=1, stroke=0)
    c.drawImage(jpg('michael', 1000), 0.75 * inch, 2.6 * inch, 4.5 * inch, 4.5 * inch)
    c.setStrokeColor(colors.HexColor('#e9cf8c'))
    c.setLineWidth(2)
    c.rect(0.72 * inch, 2.57 * inch, 4.56 * inch, 4.56 * inch)
    c.setFillColor(colors.HexColor('#e9cf8c'))
    c.setFont('Cinzel', 9)
    c.drawCentredString(PAGE[0] / 2, 8.3 * inch, 'DISCOVERY SCIENCE')
    c.setFont('Cinzel', 22)
    c.drawCentredString(PAGE[0] / 2, 1.95 * inch, 'THE BOOK OF THE ANGELS')
    c.setFont('CormorantI', 14)
    c.drawCentredString(PAGE[0] / 2, 1.6 * inch, 'of the days and the hours')
    c.setFont('Cormorant', 10)
    c.setFillColor(colors.HexColor('#c9c2b0'))
    c.drawCentredString(PAGE[0] / 2, 1.05 * inch, 'From the Heptameron, the Ars Paulina, the Sworn Book of Honorius and Agrippa')
    c.restoreState()


def build(out):
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, 'The-Book-of-the-Angels.pdf')
    doc = BaseDocTemplate(path, pagesize=PAGE, leftMargin=0.7 * inch, rightMargin=0.7 * inch, topMargin=0.7 * inch, bottomMargin=0.75 * inch,
                          title='The Book of the Angels of the Days and Hours', author='Discovery Science')
    fr = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')
    doc.addPageTemplates([PageTemplate('cover', [fr], onPage=on_cover), PageTemplate('page', [fr], onPage=on_page)])
    st = []
    from reportlab.platypus.doctemplate import NextPageTemplate
    st += [NextPageTemplate('page'), PageBreak()]

    # ---------------- introduction
    st += [Paragraph('INTRODUCTION', S['eyebrow']), Paragraph('Thirty-One Angels', S['title']),
           Paragraph('Seven who rule the days, and twenty-four who keep the hours.', S['lede'])]
    for p in [
        'Two old books divide time among the angels. The <i>Heptameron</i>, printed in the sixteenth century under the name of Peter of Abano, '
        'gives each day of the week to an angel and a planet: Michael and the Sun on Sunday, Gabriel and the Moon on Monday, Samael and Mars on Tuesday, '
        'Raphael and Mercury on Wednesday, Sachiel and Jupiter on Thursday, Anael and Venus on Friday, Cassiel and Saturn on Saturday.',
        'The <i>Ars Paulina</i>, the third book of the <i>Lemegeton</i>, compiled in the seventeenth century, goes further. It names an angel for each of the '
        'twelve hours of the day, counted from sunrise, and each of the twelve hours of the night, counted from sunset, each with a court of dukes and servants. '
        'These angels have no planet of their own. In the manuscript’s words, their offices are “to doe all things that are attributed to the 7 planetts”, '
        'and which planet that is changes with the day.',
        'This book gathers what the sources say about each of them: their names, their days and hours, their companions, what the old books claim they can do, '
        'and how they were said to appear. Each is shown in a modern devotional portrait painted for Discovery Science.',
        'It describes a tradition. It does not claim that angels or planetary hours influence events, and nothing here is a promise of any result.',
    ]:
        st.append(Paragraph(p, S['body']))
    st.append(Paragraph('HOW THE PLANETARY HOURS WORK', S['h2']))
    for p in [
        'The day from sunrise to sunset is divided into twelve equal parts, and the night from sunset to the next sunrise into twelve more. '
        'So the hours are long in summer days and short in winter ones. The first hour of each day belongs to the planet that rules the day; '
        'the rest follow in the old “Chaldean” order of the planets, from the slowest to the fastest: Saturn, Jupiter, Mars, the Sun, Venus, Mercury, the Moon, and round again.',
        'When the planet of the hour is the same as the planet of the day (in the first, eighth, fifteenth and twenty-second hours) the hour is “aligned”. '
        'Tradition counts these as the strongest hours for the work of that planet. The table at the end of this book shows the ruler of every hour of the week. '
        'To find the hours for where you are today, with your own sunrise and sunset, use the live calculator at discovery-science.com/planetary-hour-now.',
    ]:
        st.append(Paragraph(p, S['body']))

    # ---------------- the seven
    st += [PageBreak(), Paragraph('PART ONE', S['eyebrow']), Paragraph('The Angels of the Seven Days', S['title']),
           Paragraph('From the Heptameron, with the Sworn Book of Honorius and Agrippa.', S['lede'])]
    for i, planet in enumerate(DAY_RULER):
        v, o = A.SEVEN[planet], A.OFFICES[planet]
        st += [PageBreak(), Paragraph(f"{v['day'].upper()} · ANGEL OF {the(planet).upper()}", S['eyebrow']), Paragraph(v['angel'], S['title']),
               portrait(v['slug'], 2.45 * inch), Spacer(1, 10), Paragraph(' · '.join(o['tags']), S['lede'])]
        for p in v['essay']:
            st.append(Paragraph(p, S['body']))
        st += [Paragraph('WHAT THE OLD BOOKS SAY HE CAN DO', S['h2']), Paragraph(o['plain'], S['body']),
               Paragraph('“' + o['heptameron'][0].upper() + o['heptameron'][1:] + '.”', S['quote']),
               Paragraph(f"HEPTAMERON, ON THE SPIRITS OF {v['day'].upper()}", S['cite']),
               Paragraph('“Their nature is ' + o['honorius'] + '.”', S['quote']),
               Paragraph(f"SWORN BOOK OF HONORIUS, ON THE ANGELS OF {the(planet).upper()}", S['cite']),
               Paragraph(f'HOW THE ANGELS OF {the(planet).upper()} APPEAR', S['h2']), Paragraph(o['looks'], S['body']),
               Paragraph(f"Agrippa’s Fourth Book gives the emblems of {the(planet)}: {o['emblems']}.", S['body'])]
        facts = [('Day', f"{v['day']}, the day of {the(planet)}"),
                 ('Name', f"{v['angel']}, {v['meaning']}"),
                 ('Companions on his day', ', '.join(v['companions'])),
                 ('Heaven', f"{v['heaven']}, the {v['heaven_no']}" if v['heaven'] else 'none is named for Saturday'),
                 ('King of the air', f"{v['air_king']}, with his ministers {', '.join(v['air_ministers'])}"),
                 ('Wind', f"the {v['wind']} wind"), ('Perfume of the day', v['perfume'])]
        st.append(Paragraph('IN THE HEPTAMERON', S['h2']))
        rows = [[Paragraph(f'<b>{a}</b>', S['cell']), Paragraph(b, S['cell'])] for a, b in facts]
        t = Table(rows, colWidths=[1.35 * inch, doc.width - 1.35 * inch])
        t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LINEBELOW', (0, 0), (-1, -1), 0.4, colors.HexColor('#d9cfb8')),
                               ('BOTTOMPADDING', (0, 0), (-1, -1), 4), ('TOPPADDING', (0, 0), (-1, -1), 4)]))
        st += [t, Spacer(1, 8), Paragraph(v['agrippa'], S['small']), Paragraph(v['paulina'], S['small'])]

    # ---------------- the 24
    st += [PageBreak(), Paragraph('PART TWO', S['eyebrow']), Paragraph('The Angels of the Twenty-Four Hours', S['title']),
           Paragraph('From the Ars Paulina (British Library, Sloane MS 3825).', S['lede']),
           Paragraph('“' + A.PAULINA_RULE + '”', S['quote']), Paragraph('ARS PAULINA, BOOK ONE', S['cite']),
           Paragraph('So the angel of an hour does the work of whichever planet rules that hour on that day. The table under each angel shows which planet he serves on each day of the week.', S['body'])]
    for idx, (period, no, hname, angel, retinue, dukes, note) in enumerate(A.PAULINA):
        hour = idx % 12 if period == 'day' else idx - 12
        served = [CHALDEAN[(CHALDEAN.index(DAY_RULER[d]) + (hour if period == 'day' else 12 + hour)) % 7] for d in range(7)]
        block = [PageBreak(), Paragraph(f"{ROMAN[no - 1]} · THE {ORD[no - 1].upper()} HOUR OF THE {period.upper()}", S['eyebrow']),
                 Paragraph(angel, S['title']), portrait('paulina-' + angel.lower(), 2.45 * inch), Spacer(1, 6),
                 Paragraph(f'Ruler of the {ORD[no - 1]} hour of every {period}, the hour called <i>{hname}</i>. In the manuscript he has {retinue}.', S['body'])]
        if note:
            block.append(Paragraph(note, S['small']))
        rows = [[Paragraph(f'<b>{WEEK[d]}</b>', S['cell']), Paragraph(('The ' + served[d]) if served[d] in ('Sun', 'Moon') else served[d], S['cell']),
                 Paragraph(' · '.join(A.OFFICES[served[d]]['tags']), S['cell'])] for d in range(7)]
        t = Table(rows, colWidths=[0.95 * inch, 0.8 * inch, doc.width - 1.75 * inch])
        t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LINEBELOW', (0, 0), (-1, -1), 0.4, colors.HexColor('#d9cfb8')),
                               ('BOTTOMPADDING', (0, 0), (-1, -1), 3), ('TOPPADDING', (0, 0), (-1, -1), 3)]))
        block += [Paragraph('WHOM HE SERVES THROUGH THE WEEK', S['h2']), t,
                  Paragraph('HIS CHIEF DUKES', S['h2']), Paragraph(', '.join(dukes) + '.', S['small'])]
        st += block

    # ---------------- table of hours
    st += [PageBreak(), Paragraph('APPENDIX', S['eyebrow']), Paragraph('The Rulers of the Hours', S['title']),
           Paragraph('Hours 1–12 run from sunrise to sunset; 13–24 from sunset to the next sunrise.', S['lede'])]
    head = [Paragraph('<b>Hour</b>', S['tiny'])] + [Paragraph(f'<b>{w[:3]}</b>', S['tiny']) for w in WEEK]
    rows = [head]
    for h in range(24):
        rows.append([Paragraph(('Day ' if h < 12 else 'Night ') + str(h % 12 + 1), S['tiny'])] +
                    [Paragraph(CHALDEAN[(CHALDEAN.index(DAY_RULER[d]) + h) % 7], S['tiny']) for d in range(7)])
    t = Table(rows, colWidths=[0.75 * inch] + [(doc.width - 0.75 * inch) / 7] * 7, repeatRows=1)
    style = [('LINEBELOW', (0, 0), (-1, -1), 0.3, colors.HexColor('#d9cfb8')), ('TOPPADDING', (0, 0), (-1, -1), 1.2), ('BOTTOMPADDING', (0, 0), (-1, -1), 1.2), ('LEFTPADDING', (0, 0), (-1, -1), 1), ('RIGHTPADDING', (0, 0), (-1, -1), 1)]
    for h in range(24):
        for d in range(7):
            if (CHALDEAN.index(DAY_RULER[d]) + h) % 7 == CHALDEAN.index(DAY_RULER[d]):
                style.append(('BACKGROUND', (d + 1, h + 1), (d + 1, h + 1), colors.HexColor('#f1e2b8')))
    t.setStyle(TableStyle(style))
    st += [t, Spacer(1, 6), Paragraph('Shaded cells are the aligned hours, when the planet of the hour is the planet of the day.', S['small'])]

    st += [PageBreak(), Paragraph('SOURCES', S['eyebrow']), Paragraph('Sources and a Note on the Art', S['title'])]
    for p in [
        '<i>Heptameron, or Magical Elements</i>, attributed to Peter of Abano; English translation by Robert Turner (London, 1655), with corrections from Joseph H. Peterson’s edition (esotericarchives.com).',
        '<i>Ars Paulina</i>, the third book of the <i>Lemegeton</i>, British Library Sloane MS 3825, as edited by Joseph H. Peterson in <i>The Lesser Key of Solomon</i> (Weiser, 2001).',
        '<i>The Sworn Book of Honorius (Liber Iuratus Honorii)</i>, translated by Joseph H. Peterson (Ibis, 2016).',
        'Heinrich Cornelius Agrippa, <i>Three Books of Occult Philosophy</i> (1533; English 1651), Book II, and the <i>Fourth Book of Occult Philosophy</i> attributed to him (English 1655).',
        'The portraits are modern devotional artwork painted for Discovery Science with an AI image generator, from descriptions drawn from these texts. '
        'They do not reproduce any manuscript figure.',
        '© Discovery Science. For personal use; please do not resell or redistribute. Live tools: discovery-science.com/angel-of-the-hour and discovery-science.com/planetary-hour-now.',
    ]:
        st.append(Paragraph(p, S['body']))
    doc.build(st)
    print('book →', path)


if __name__ == '__main__':
    build(sys.argv[1])
