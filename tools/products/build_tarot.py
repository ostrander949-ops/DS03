#!/usr/bin/env python3
"""The Angelic Tarot: the 22 Major Arcana as a print-at-home deck and an illustrated guidebook.
Usage: python3 tools/products/build_tarot.py <folder of paintings 00.jpg … 21.jpg> <out_dir>
Writes:
  Angelic-Tarot-print.pdf      US Letter, 6 tarot-size cards (2.75 x 4.75 in) per page with cut marks, and a page of backs
  Angelic-Tarot-Guidebook.pdf  6 x 9 in guidebook: the pairings, a page for every card, spreads and sources
  cards/NN-slug.png            each card face at 300 dpi, plus the back
The card back is the same either way up, so reversed cards can be read."""
import math
import os
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFilter
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, Image as RLImage, KeepTogether, PageBreak, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle)
from reportlab.platypus.doctemplate import NextPageTemplate

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from build_cards import (GLYPH, GOLD, GOLD_D, H, INK, NAVY, W, background, centered, font, frame, sheet,  # noqa: E402
                         symbol_font, wrap)
from tarot_data import MAJORS  # noqa: E402

FONT = os.path.join(HERE, 'fonts')
ROMAN = ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII',
         'XIX', 'XX', 'XXI']
SIGN = {'Aries': '♈', 'Taurus': '♉', 'Gemini': '♊', 'Cancer': '♋', 'Leo': '♌', 'Virgo': '♍', 'Libra': '♎', 'Scorpio': '♏',
        'Sagittarius': '♐', 'Capricorn': '♑', 'Aquarius': '♒', 'Pisces': '♓'}
SIGN_DATES = {'Aries': '21 March – 19 April', 'Taurus': '20 April – 20 May', 'Gemini': '21 May – 20 June', 'Cancer': '21 June – 22 July',
              'Leo': '23 July – 22 August', 'Virgo': '23 August – 22 September', 'Libra': '23 September – 22 October',
              'Scorpio': '23 October – 21 November', 'Sagittarius': '22 November – 21 December', 'Capricorn': '22 December – 19 January',
              'Aquarius': '20 January – 18 February', 'Pisces': '19 February – 20 March'}
PLANET_DAY = {'Sun': 'Sunday', 'Moon': 'Monday', 'Mars': 'Tuesday', 'Mercury': 'Wednesday', 'Jupiter': 'Thursday', 'Venus': 'Friday',
              'Saturn': 'Saturday'}
ELEMENTS = ('Air', 'Water', 'Fire')
QUESTION = [
    'Where is life inviting you to begin before you feel ready?',
    'What do you already hold in your hands that you have not yet used?',
    'What does your quiet inner voice already know?',
    'What in your life is asking to be tended so that it can grow?',
    'Where would a little more order make you freer?',
    'Which teaching is still feeding you, and which has gone dry?',
    'What would you choose if your heart and your values chose together?',
    'Where are two forces in you pulling different ways, and how could they pull together?',
    'Where could gentleness do what force cannot?',
    'What would you hear if you stepped away from the noise for an hour?',
    'What is turning in your life, and how can you move with it rather than against it?',
    'Where is honesty asking to be restored?',
    'What would you see if you let yourself look at this from the other side?',
    'What is ready to end, so that something new can begin?',
    'Where do you need to blend, to slow down, or to find the middle way?',
    'What chain around you is looser than it looks?',
    'What false structure would you be relieved to see fall?',
    'What gives you hope, and how could you pour some of it out for someone else?',
    'What fear might be a shadow rather than a fact?',
    'What simple joy can you let yourself have today?',
    'What is calling you to rise and answer?',
    'What has come full circle, and how will you mark it?',
]


def planet(attr):
    return attr.replace('the ', '')


def slug(name):
    return name.lower().replace('the ', '').replace(' ', '-')


def square(path):
    im = Image.open(path).convert('RGB')
    if im.width != im.height:
        s = min(im.size)
        top = int((im.height - s) * 0.35)
        left = (im.width - s) // 2
        im = im.crop((left, top, left + s, top + s))
    return im


# ---------------------------------------------------------------- card faces

def draw_glyph(d, attr, cx, cy):
    if attr in ELEMENTS:   # the alchemical triangles: Fire and Air point up, Water down; Air is crossed
        r = 24
        up = attr in ('Fire', 'Air')
        pts = [(cx, cy - r), (cx - r * 0.95, cy + r * 0.65), (cx + r * 0.95, cy + r * 0.65)] if up else \
              [(cx, cy + r), (cx - r * 0.95, cy - r * 0.65), (cx + r * 0.95, cy - r * 0.65)]
        d.polygon(pts, outline=GOLD, width=4)
        if attr == 'Air':
            d.line((cx - r * 0.75, cy + 2, cx + r * 0.75, cy + 2), fill=GOLD, width=4)
        return
    g = SIGN.get(attr) or GLYPH[planet(attr)]
    d.text((cx, cy + 2), g, font=symbol_font(44), fill=GOLD, anchor='mm')


def fit(d, text, name, size, width):
    while size > 20 and d.textlength(text, font=font(name, size)) > width:
        size -= 2
    return font(name, size)


def face(m, painting):
    n, cname, attr, angel, src, up, rev, scene = m
    im = background()
    d = ImageDraw.Draw(im)
    frame(d)
    centered(d, 58, ROMAN[n], font('Cinzel-SemiBold.ttf', 46), GOLD)
    size = 680
    p = painting.resize((size, size), Image.LANCZOS)
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size, size), 24, fill=255)
    x, y = (W - size) // 2, 126
    glow = Image.new('L', (W, H), 0)
    ImageDraw.Draw(glow).rounded_rectangle((x - 8, y - 8, x + size + 8, y + size + 8), 30, fill=150)
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    im.paste(Image.new('RGB', (W, H), (255, 214, 140)), (0, 0), Image.eval(glow, lambda v: v // 3))
    im.paste(p, (x, y), mask)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x - 3, y - 3, x + size + 3, y + size + 3), 26, outline=GOLD, width=5)
    cy = y + size
    d.ellipse((W / 2 - 42, cy - 42, W / 2 + 42, cy + 42), fill=NAVY, outline=GOLD, width=4)
    draw_glyph(d, attr, W / 2, cy)
    title = cname.upper()
    centered(d, cy + 62, title, fit(d, title, 'Cinzel-SemiBold.ttf', 70, W - 130), INK)
    centered(d, cy + 156, f'given to {angel}', font('Cormorant-Italic.ttf', 44), GOLD)
    yy = cy + 222
    d.line((W / 2 - 120, yy, W / 2 - 20, yy), fill=GOLD_D, width=2)
    d.line((W / 2 + 20, yy, W / 2 + 120, yy), fill=GOLD_D, width=2)
    d.regular_polygon((W / 2, yy, 7), 4, rotation=45, fill=GOLD)
    yy += 24
    kf = font('Cinzel-SemiBold.ttf', 29)
    for ln in wrap(d, up.upper(), kf, W - 160)[:3]:
        centered(d, yy, ln, kf, INK)
        yy += 40
    yy += 8
    rf = font('Cormorant-Regular.ttf', 36)
    centered(d, yy, f'{attr[0].upper() + attr[1:]} · {src}', fit(d, f'{attr} · {src}', 'Cormorant-Regular.ttf', 36, W - 150), (214, 206, 186))
    centered(d, H - 78, 'DISCOVERY SCIENCE · ANGELIC TAROT', font('Cinzel-SemiBold.ttf', 18), GOLD_D, spacing=2)
    return im


def back():
    """Symmetric under a half turn, so a reversed card cannot be told from its back."""
    im = background()
    im = Image.blend(im, im.rotate(180), 0.5)
    d = ImageDraw.Draw(im)
    frame(d)
    cx, cy = W / 2, H / 2
    R = 290
    for r, w in ((R + 44, 4), (R + 30, 2), (R - 48, 2)):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=GOLD, width=w)
    # twelve points for the signs, seven for the planets, three for the elements: 22 rays in all
    for k in range(22):
        a = -math.pi / 2 + k * 2 * math.pi / 22
        r2 = R - 60 if k % 2 == 0 else R - 110
        d.polygon([(cx + 52 * math.cos(a - 0.09), cy + 52 * math.sin(a - 0.09)), (cx + r2 * math.cos(a), cy + r2 * math.sin(a)),
                   (cx + 52 * math.cos(a + 0.09), cy + 52 * math.sin(a + 0.09))], fill=GOLD)
    for k in range(22):
        a = -math.pi / 2 + k * 2 * math.pi / 22
        x, y = cx + (R + 7) * math.cos(a), cy + (R + 7) * math.sin(a)
        d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=GOLD)
    d.ellipse((cx - 50, cy - 50, cx + 50, cy + 50), fill=(255, 238, 190), outline=GOLD, width=3)
    lbl = font('Cinzel-SemiBold.ttf', 36)
    centered(d, H - 150, 'ANGELIC TAROT', lbl, GOLD, spacing=6)
    top = Image.new('RGBA', (W, 120), (0, 0, 0, 0))
    td = ImageDraw.Draw(top)
    widths = [td.textlength(c, font=lbl) for c in 'ANGELIC TAROT']
    xx = (W - sum(widths) - 6 * 12) / 2
    for c, w in zip('ANGELIC TAROT', widths):
        td.text((xx, 10), c, font=lbl, fill=GOLD)
        xx += w + 6
    top = top.rotate(180)
    im.paste(top, (0, 40), top)   # the bottom label turned through 180°, mirrored to the top
    return im


def guide_page(c, pw, ph):
    c.setFillColorRGB(0.035, 0.047, 0.11)
    c.rect(0, 0, pw, ph, fill=1, stroke=0)
    c.setFillColorRGB(0.91, 0.81, 0.55)
    c.setFont('Cinzel', 26)
    c.drawCentredString(pw / 2, ph - 1.3 * inch, 'THE ANGELIC TAROT')
    c.setFont('CormorantI', 15)
    c.drawCentredString(pw / 2, ph - 1.65 * inch, 'The twenty-two Major Arcana and their angels')
    text = [
        ('How to print', 'Print the four card pages on heavy matte card stock (250–300 gsm) at 100% scale (“actual size”), single-sided. '
         'Cut along the marks. For backs, print the last page on the reverse of each card sheet, or print it separately and glue. '
         'The back is the same either way up, so you can read reversed cards.'),
        ('What is in the deck', 'The twenty-two trumps of the tarot, from the Fool to the World, each given to an angel. '
         'Each card is paired by its traditional attribution (an element, a planet or a sign of the zodiac) with the angel '
         'Agrippa sets over that element, planet or sign. The guidebook explains every pairing and gives a page to each card.'),
        ('A note', 'The paintings are new devotional artwork painted for Discovery Science with an AI image generator; no historical deck is copied. '
         'The deck is for reflection and devotion and makes no promise of any outcome.'),
    ]
    y = ph - 2.5 * inch
    for head, body in text:
        c.setFont('Cinzel', 13)
        c.setFillColorRGB(0.91, 0.81, 0.55)
        c.drawString(1.1 * inch, y, head.upper())
        y -= 0.3 * inch
        c.setFont('Cormorant', 13.5)
        c.setFillColorRGB(0.93, 0.9, 0.83)
        line = ''
        for w in body.split():
            t = (line + ' ' + w).strip()
            if pdfmetrics.stringWidth(t, 'Cormorant', 13.5) > pw - 2.2 * inch:
                c.drawString(1.1 * inch, y, line)
                y -= 0.24 * inch
                line = w
            else:
                line = t
        c.drawString(1.1 * inch, y, line)
        y -= 0.45 * inch
    c.setFont('Cormorant', 10)
    c.setFillColorRGB(0.6, 0.55, 0.45)
    c.drawCentredString(pw / 2, 0.6 * inch, '© Discovery Science · For personal use. Please do not resell or redistribute.')
    c.showPage()


# ---------------------------------------------------------------- guidebook

PAGE = (6 * inch, 9 * inch)
BNAVY, BGOLD, BINK, MUTED = colors.HexColor('#0b0f1f'), colors.HexColor('#b8903f'), colors.HexColor('#1d1a14'), colors.HexColor('#6b6252')
S = {
    'title': ParagraphStyle('t', fontName='Cinzel', fontSize=22, leading=28, alignment=TA_CENTER, textColor=BINK, spaceAfter=4),
    'eyebrow': ParagraphStyle('e', fontName='Cinzel', fontSize=8.5, leading=12, alignment=TA_CENTER, textColor=BGOLD, spaceAfter=4),
    'h2': ParagraphStyle('h2', fontName='Cinzel', fontSize=9, leading=12, textColor=BGOLD, spaceBefore=6, spaceAfter=1),
    'body': ParagraphStyle('b', fontName='Cormorant', fontSize=11.3, leading=14.6, textColor=BINK, spaceAfter=4),
    'lede': ParagraphStyle('l', fontName='CormorantI', fontSize=13, leading=17, alignment=TA_CENTER, textColor=BINK, spaceAfter=8),
    'q': ParagraphStyle('q', fontName='CormorantI', fontSize=12.5, leading=16, alignment=TA_CENTER, textColor=BINK, spaceBefore=4),
    'small': ParagraphStyle('s', fontName='Cormorant', fontSize=9.5, leading=12.5, textColor=MUTED, spaceAfter=4),
    'cell': ParagraphStyle('cell', fontName='Cormorant', fontSize=10, leading=12, textColor=BINK),
}


def on_page(c, doc):
    c.saveState()
    c.setFillColor(colors.HexColor('#fbf7ee'))
    c.rect(0, 0, PAGE[0], PAGE[1], fill=1, stroke=0)
    c.setFont('Cinzel', 7)
    c.setFillColor(MUTED)
    c.drawCentredString(PAGE[0] / 2, 0.45 * inch, f'THE ANGELIC TAROT · {doc.page}')
    c.restoreState()


class Spread(Flowable):
    """A little diagram of card positions: list of (x, y, label) in card units."""

    def __init__(self, cells, w=4.4 * inch, cw=0.48 * inch):
        super().__init__()
        self.cells, self.w, self.cw = cells, w, cw
        self.ch = cw * 1.7
        xs = [x for x, _, _ in cells]
        ys = [y for _, y, _ in cells]
        self.cols, self.rows = max(xs) + 1, max(ys) + 1
        self.h = self.rows * (self.ch + 0.12 * inch)

    def wrap(self, aw, ah):
        return self.w, self.h

    def draw(self):
        c = self.canv
        step = self.cw + 0.14 * inch
        x0 = (self.w - (self.cols * step - 0.14 * inch)) / 2
        for x, y, lab in self.cells:
            px = x0 + x * step
            py = self.h - (y + 1) * (self.ch + 0.12 * inch)
            c.setFillColor(BNAVY)
            c.setStrokeColor(BGOLD)
            c.roundRect(px, py, self.cw, self.ch, 4, fill=1, stroke=1)
            c.setFillColor(colors.HexColor('#e9cf8c'))
            c.setFont('Cinzel', 9)
            c.drawCentredString(px + self.cw / 2, py + self.ch / 2 - 3, str(lab))


def build_guide(paint_jpgs, cover_png, out):
    path = os.path.join(out, 'Angelic-Tarot-Guidebook.pdf')
    doc = BaseDocTemplate(path, pagesize=PAGE, leftMargin=0.7 * inch, rightMargin=0.7 * inch, topMargin=0.65 * inch, bottomMargin=0.75 * inch,
                          title='The Angelic Tarot: Guidebook', author='Discovery Science')

    def on_cover(c, d):
        c.saveState()
        c.setFillColor(BNAVY)
        c.rect(0, 0, PAGE[0], PAGE[1], fill=1, stroke=0)
        c.drawImage(cover_png, 1.6 * inch, 2.45 * inch, 2.8 * inch, 2.8 * inch * H / W)
        c.setFillColor(colors.HexColor('#e9cf8c'))
        c.setFont('Cinzel', 9)
        c.drawCentredString(PAGE[0] / 2, 8.35 * inch, 'DISCOVERY SCIENCE')
        c.setFont('Cinzel', 24)
        c.drawCentredString(PAGE[0] / 2, 1.75 * inch, 'THE ANGELIC TAROT')
        c.setFont('CormorantI', 14)
        c.drawCentredString(PAGE[0] / 2, 1.4 * inch, 'A guidebook to the twenty-two Major Arcana and their angels')
        c.restoreState()

    fr = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')
    doc.addPageTemplates([PageTemplate('cover', [fr], onPage=on_cover), PageTemplate('page', [fr], onPage=on_page)])
    st = [NextPageTemplate('page'), PageBreak()]

    # introduction
    st += [Paragraph('INTRODUCTION', S['eyebrow']), Paragraph('Twenty-Two Doors', S['title']),
           Paragraph('The trumps of the tarot, each given to an angel.', S['lede'])]
    for p in [
        'The twenty-two trumps, or Major Arcana, are the picture cards of the tarot: the Fool, the Magician, the High Priestess and the rest, '
        'down to the World. Since the nineteenth century they have been read as a path, a sequence of doors a soul passes through, '
        'and each has been tied to a letter of the Hebrew alphabet and through it to an element, a planet or a sign of the zodiac.',
        'This deck follows those attributions as the Hermetic Order of the Golden Dawn set them down, and asks a simple question of each: '
        'which angel do the old books set over that element, planet or sign? The answers come from Henry Cornelius Agrippa’s '
        '<i>Three Books of Occult Philosophy</i> (1533), which names the angels of the seven planets, of the twelve signs and of the elements. '
        'The result is a deck in which every trump has an angel: Raphael, angel of Mercury, is the Magician; Gabriel, angel of the Moon, '
        'is the High Priestess; Michael, angel of the Sun, is the Sun.',
        'The pairing of trumps with these angels is made for this deck, built on traditional attributions; no older deck is copied, '
        'and the paintings are new devotional artwork. The deck is for reflection, prayer and conversation with yourself. '
        'Nothing in it is a prediction or a promise of any outcome.',
    ]:
        st.append(Paragraph(p, S['body']))
    st.append(Paragraph('THE THREE KINDS OF CARD', S['h2']))
    for p in [
        '<b>Three cards of the elements.</b> The Fool is Air, the Hanged Man is Water, and Judgement is Fire. (In the old scheme Earth has no trump of its own.) '
        'Agrippa names the rulers of the elements as Seraph of Fire, Cherub of Air and Tharsis of Water.',
        '<b>Seven cards of the planets.</b> The Magician is Mercury, the High Priestess the Moon, the Empress Venus, the Wheel of Fortune Jupiter, '
        'the Tower Mars, the Sun the Sun and the World Saturn. Their angels are the seven of the days of the week: Raphael, Gabriel, Anael, Sachiel, '
        'Samael, Michael and Cassiel. Each card is strongest, if you like, on its angel’s day.',
        '<b>Twelve cards of the signs.</b> From the Emperor (Aries) to the Moon (Pisces), each is given to the angel Agrippa sets over its sign: '
        'Malchidiel, Asmodel, Ambriel, Muriel, Verchiel, Hamaliel, Zuriel, Barbiel, Adnachiel, Hanael, Gambiel and Barchiel. '
        'Each is strongest in its own month of the year.',
    ]:
        st.append(Paragraph(p, S['body']))
    st.append(PageBreak())

    # table of cards
    st += [Paragraph('THE DECK AT A GLANCE', S['eyebrow']), Paragraph('The Twenty-Two', S['title']), Spacer(1, 4)]
    rows = [[Paragraph(f'<b>{h}</b>', S['cell']) for h in ('', 'Card', 'Attribution', 'Angel')]]
    for m in MAJORS:
        rows.append([Paragraph(ROMAN[m[0]], S['cell']), Paragraph(m[1], S['cell']), Paragraph(m[2][0].upper() + m[2][1:], S['cell']),
                     Paragraph(m[3], S['cell'])])
    t = Table(rows, colWidths=[0.6 * inch, 1.6 * inch, 1.2 * inch, 1.25 * inch])
    t.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, 0), 0.8, BGOLD), ('LINEBELOW', (0, 1), (-1, -1), 0.25, colors.HexColor('#d9cfb8')),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('TOPPADDING', (0, 0), (-1, -1), 2.2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2)]))
    st += [t, PageBreak()]

    # one page per card
    for m, pj in zip(MAJORS, paint_jpgs):
        n, cname, attr, angel, src, up, rev, scene = m
        A = attr[0].upper() + attr[1:]
        if attr in ELEMENTS:
            when = f'The card of the element of {attr}. Draw on it whenever the work of {attr.lower()} is needed: ' + \
                   {'Air': 'new thought, breath, a fresh start.', 'Water': 'feeling, surrender, cleansing.', 'Fire': 'will, courage, purification.'}[attr]
        elif attr in SIGN:
            when = f'{angel} watches over {attr}, roughly {SIGN_DATES[attr]}, when the Sun is in that sign.'
        else:
            pl = planet(attr)
            when = f'{angel} rules {PLANET_DAY[pl]}, the day of {attr}, and the hours of {attr} on every day. ' \
                   f'Find them at discovery-science.com/planetary-hour-now.'
        page = [Paragraph(f'{ROMAN[n]} · {A.upper()}', S['eyebrow']), Paragraph(cname, S['title']),
                Paragraph(f'given to {angel}, {src}', S['lede']), RLImage(pj, width=2.85 * inch, height=2.85 * inch), Spacer(1, 2),
                Paragraph('UPRIGHT', S['h2']), Paragraph(up[0].upper() + up[1:] + '.', S['body']),
                Paragraph('REVERSED', S['h2']), Paragraph(rev[0].upper() + rev[1:] + '.', S['body']),
                Paragraph('IN THE PAINTING', S['h2']), Paragraph(scene[0].upper() + scene[1:] + '.', S['body']),
                Paragraph('THE ANGEL’S TIME', S['h2']), Paragraph(when, S['body']),
                Paragraph(QUESTION[n], S['q'])]
        st += [KeepTogether(page), PageBreak()]

    # spreads
    st += [Paragraph('READING THE CARDS', S['eyebrow']), Paragraph('Four Spreads', S['title']), Spacer(1, 4)]
    spreads = [
        ('The angel for today', [(0, 0, '1')],
         'Shuffle with a question or simply with the day in mind, and draw one card. Read its page, sit with its question, '
         'and keep its angel in mind until evening.'),
        ('Three cards', [(0, 0, '1'), (1, 0, '2'), (2, 0, '3')],
         '1, what is: the situation as it stands. 2, what helps: the counsel or the gift on offer. 3, what may come: where things lead if nothing changes.'),
        ('The cross of the elements', [(1, 0, '1'), (0, 1, '2'), (2, 1, '3'), (1, 2, '4')],
         'For a decision. 1, Fire: what you want. 2, Air: what you think. 3, Water: what you feel. 4, Earth: what you can actually do. '
         'Read the four together and see where they agree.'),
        ('The week of angels', [(k, 0, d) for k, d in enumerate(['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'])],
         'On Sunday, lay out seven cards, one for each day of the coming week. Each day, turn that day’s card over in the morning and read it '
         'alongside the day’s angel: Michael on Sunday, Gabriel on Monday, Samael on Tuesday, Raphael on Wednesday, Sachiel on Thursday, '
         'Anael on Friday and Cassiel on Saturday. The free weekly newsletter, The Angels of the Week, gives a card of the week and each day’s angel.'),
    ]
    for name, cells, text in spreads:
        st.append(KeepTogether([Paragraph(name.upper(), S['h2']), Spread(cells), Spacer(1, 4), Paragraph(text, S['body'])]))
    st.append(Paragraph('ON REVERSALS', S['h2']))
    st.append(Paragraph('The card backs look the same either way up, so if you shuffle by turning cards you will draw some upside down. '
                        'You may read these with the reversed meanings, or as the upright meaning blocked, delayed or turned inward; '
                        'or you may turn every card upright and ignore reversals altogether. All three are old customs.', S['body']))
    st.append(PageBreak())

    # sources
    st += [Paragraph('NOTES', S['eyebrow']), Paragraph('Sources', S['title'])]
    for p in [
        '<b>Henry Cornelius Agrippa</b>, <i>De occulta philosophia libri tres</i> (1533), book II, chapters 7, 10 and 14: the scales of the numbers four, '
        'seven and twelve, giving the rulers of the elements (Seraph, Cherub, Tharsis, Ariel), the angels of the seven planets and the angels of the twelve signs. '
        'English translation by J. F., <i>Three Books of Occult Philosophy</i> (London, 1651).',
        '<b>The Heptameron</b>, attributed to Peter of Abano (printed 1559), for the angels of the days of the week.',
        '<b>The Hermetic Order of the Golden Dawn</b>, the attributions of the trumps to the Hebrew letters and to the elements, planets and signs, '
        'as published by S. L. MacGregor Mathers and A. E. Waite and later in Israel Regardie’s <i>The Golden Dawn</i> (1937–40).',
        'The upright and reversed meanings follow common modern usage. The paintings are new devotional artwork, painted for Discovery Science '
        'with an AI image generator; no historical deck is copied.',
        'This deck and guidebook describe a tradition. They are for reflection and devotion, and make no promise of any outcome.',
    ]:
        st.append(Paragraph(p, S['body']))
    st += [Spacer(1, 10), Paragraph('Find the angel of this hour: discovery-science.com/angel-of-the-hour', S['small']),
           Paragraph('© Discovery Science. For personal use. Please do not resell or redistribute.', S['small'])]
    doc.build(st)
    return path


# ---------------------------------------------------------------- main

def main(src, out):
    for name, file in (('Cinzel', 'Cinzel-SemiBold.ttf'), ('Cormorant', 'Cormorant-Regular.ttf'), ('CormorantSB', 'Cormorant-SemiBold.ttf'),
                       ('CormorantI', 'Cormorant-Italic.ttf')):
        pdfmetrics.registerFont(TTFont(name, os.path.join(FONT, file)))
    pdfmetrics.registerFontFamily('Cormorant', normal='Cormorant', bold='CormorantSB', italic='CormorantI', boldItalic='CormorantI')
    cards_dir = os.path.join(out, 'cards')
    os.makedirs(cards_dir, exist_ok=True)
    tmp = tempfile.mkdtemp()
    faces, paints = [], []
    for m in MAJORS:
        n = m[0]
        sq = square(os.path.join(src, f'{n:02d}.jpg'))
        pj = os.path.join(tmp, f'paint-{n:02d}.jpg')
        sq.resize((1000, 1000), Image.LANCZOS).save(pj, quality=84)
        paints.append(pj)
        im = face(m, sq)
        im.save(os.path.join(cards_dir, f'{n:02d}-{slug(m[1])}.png'), dpi=(300, 300))
        j = os.path.join(tmp, f'face-{n:02d}.jpg')
        im.save(j, quality=90, dpi=(300, 300))
        faces.append(j)
    b = back()
    b.save(os.path.join(cards_dir, '99-card-back.png'), dpi=(300, 300))
    bj = os.path.join(tmp, 'back.jpg')
    b.save(bj, quality=90, dpi=(300, 300))

    pw, ph = letter
    c = canvas.Canvas(os.path.join(out, 'Angelic-Tarot-print.pdf'), pagesize=letter)
    c.setTitle('The Angelic Tarot · Discovery Science')
    guide_page(c, pw, ph)
    for i in range(0, len(faces), 6):
        sheet(c, faces[i:i + 6], pw, ph)
    sheet(c, [bj] * 6, pw, ph)
    c.save()
    build_guide(paints, faces[19], out)
    print('tarot:', len(faces), 'cards →', out)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
