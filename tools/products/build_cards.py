#!/usr/bin/env python3
"""Printable Angel Cards: 31 cards (7 day archangels, 24 hour angels) plus a card back and a short guide.
Output: a print-at-home PDF (US Letter, 6 cards per page with cut marks) and a folder of single card PNGs.
Usage: python3 tools/products/build_cards.py <out_dir>
Cards are 2.75 x 4.75 in at 300 dpi (tarot size)."""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import angels_data as A  # noqa: E402
from angel_portrait_prompts import ATTRIBUTE  # noqa: E402

FONT = os.path.join(HERE, 'fonts')
IMG = os.path.join(ROOT, 'assets', 'img', 'angels')
W, H = 825, 1425
GOLD, GOLD_D, INK, NAVY, NAVY2 = (233, 207, 140), (166, 128, 58), (244, 236, 216), (9, 12, 28), (24, 30, 58)
GLYPH = {'Saturn': '♄', 'Jupiter': '♃', 'Mars': '♂', 'Sun': '☉', 'Venus': '♀', 'Mercury': '☿', 'Moon': '☽'}
ORD = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth']
ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT, name), size)


def symbol_font(size):
    for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/dejavu/DejaVuSans.ttf'):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return font('Cormorant-Regular.ttf', size)


def the(p):
    return 'the ' + p if p in ('Sun', 'Moon') else p


def background():
    im = Image.new('RGB', (W, H), NAVY)
    g = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(g)
    for r in range(900, 0, -6):
        d.ellipse((W / 2 - r, 420 - r, W / 2 + r, 420 + r), fill=int(70 * (1 - r / 900)))
    im = Image.composite(Image.new('RGB', (W, H), NAVY2), im, g)
    d = ImageDraw.Draw(im)
    import random
    rnd = random.Random(7)
    for _ in range(160):
        x, y, s = rnd.random() * W, rnd.random() * H, rnd.random() * 1.8 + 0.4
        c = int(140 + rnd.random() * 100)
        d.ellipse((x - s, y - s, x + s, y + s), fill=(c, c, int(c * 0.9)))
    return im


def frame(d, inset=22):
    d.rounded_rectangle((inset, inset, W - inset, H - inset), 26, outline=GOLD, width=5)
    d.rounded_rectangle((inset + 14, inset + 14, W - inset - 14, H - inset - 14), 18, outline=GOLD_D, width=2)
    for cx, cy in ((inset + 14, inset + 14), (W - inset - 14, inset + 14), (inset + 14, H - inset - 14), (W - inset - 14, H - inset - 14)):
        d.regular_polygon((cx, cy, 11), 4, rotation=45, fill=GOLD)


def centered(d, y, text, f, fill=INK, spacing=0):
    if spacing:
        widths = [d.textlength(c, font=f) for c in text]
        total = sum(widths) + spacing * (len(text) - 1)
        x = (W - total) / 2
        for c, w in zip(text, widths):
            d.text((x, y), c, font=f, fill=fill)
            x += w + spacing
        return
    d.text((W / 2, y), text, font=f, fill=fill, anchor='ma')


def wrap(d, text, f, width):
    words, lines, line = text.split(), [], ''
    for w in words:
        t = (line + ' ' + w).strip()
        if d.textlength(t, font=f) <= width:
            line = t
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def portrait(slug, size):
    im = Image.open(os.path.join(IMG, slug + '.webp')).convert('RGB').resize((size, size), Image.LANCZOS)
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size, size), 24, fill=255)
    return im, mask


def card(c):
    im = background()
    d = ImageDraw.Draw(im)
    frame(d)
    # eyebrow
    eb = font('Cinzel-SemiBold.ttf', 30)
    centered(d, 70, c['eyebrow'], eb, GOLD, spacing=3)
    # portrait
    size = 640
    p, m = portrait(c['slug'], size)
    x, y = (W - size) // 2, 122
    glow = Image.new('L', (W, H), 0)
    ImageDraw.Draw(glow).rounded_rectangle((x - 8, y - 8, x + size + 8, y + size + 8), 30, fill=150)
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    im.paste(Image.new('RGB', (W, H), (255, 214, 140)), (0, 0), Image.eval(glow, lambda v: v // 3))
    im.paste(p, (x, y), m)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x - 3, y - 3, x + size + 3, y + size + 3), 26, outline=GOLD, width=5)
    # glyph medallion
    cy = y + size
    d.ellipse((W / 2 - 42, cy - 42, W / 2 + 42, cy + 42), fill=NAVY, outline=GOLD, width=4)
    d.text((W / 2, cy + 2), c['glyph'], font=c.get('glyph_font') or symbol_font(46), fill=GOLD, anchor='mm')
    # name and subtitle
    centered(d, cy + 62, c['name'].upper(), font('Cinzel-SemiBold.ttf', 76), INK)
    yy = cy + 160
    for ln in wrap(d, c['subtitle'], font('Cormorant-Italic.ttf', 38), W - 150):
        centered(d, yy, ln, font('Cormorant-Italic.ttf', 38), GOLD)
        yy += 44
    # divider
    yy += 10
    d.line((W / 2 - 120, yy, W / 2 - 20, yy), fill=GOLD_D, width=2)
    d.line((W / 2 + 20, yy, W / 2 + 120, yy), fill=GOLD_D, width=2)
    d.regular_polygon((W / 2, yy, 7), 4, rotation=45, fill=GOLD)
    yy += 22
    # keywords
    kf = font('Cinzel-SemiBold.ttf', 31)
    for ln in wrap(d, ' · '.join(c['keys']).upper(), kf, W - 150):
        centered(d, yy, ln, kf, INK)
        yy += 42
    # reflection line
    yy += 6
    rf = font('Cormorant-Regular.ttf', 40)
    for ln in wrap(d, c['line'], rf, W - 150)[:4]:
        centered(d, yy, ln, rf, (214, 206, 186))
        yy += 46
    centered(d, H - 78, 'DISCOVERY SCIENCE · ANGELIC CARDS', font('Cinzel-SemiBold.ttf', 18), GOLD_D, spacing=2)
    return im


def back():
    im = background()
    d = ImageDraw.Draw(im)
    frame(d)
    cx, cy, R = W / 2, H / 2, 300
    for r, w in ((R + 40, 4), (R + 26, 2), (R - 50, 2)):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=GOLD, width=w)
    pts = [(cx + R * math.cos(-math.pi / 2 + k * 2 * math.pi / 7), cy + R * math.sin(-math.pi / 2 + k * 2 * math.pi / 7)) for k in range(7)]
    d.line([pts[(k * 3) % 7] for k in range(8)], fill=GOLD, width=4, joint='curve')
    sf = symbol_font(40)
    for k, pl in enumerate(['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon']):
        x, y = pts[k]
        d.ellipse((x - 34, y - 34, x + 34, y + 34), fill=NAVY, outline=GOLD, width=3)
        d.text((x, y + 1), GLYPH[pl], font=sf, fill=GOLD, anchor='mm')
    for k in range(24):
        a = k * math.pi / 12
        r2 = 120 if k % 2 == 0 else 85
        d.polygon([(cx + 40 * math.cos(a - 0.12), cy + 40 * math.sin(a - 0.12)), (cx + r2 * math.cos(a), cy + r2 * math.sin(a)),
                   (cx + 40 * math.cos(a + 0.12), cy + 40 * math.sin(a + 0.12))], fill=GOLD)
    d.ellipse((cx - 46, cy - 46, cx + 46, cy + 46), fill=(255, 238, 190), outline=GOLD, width=3)
    im2 = im.filter(ImageFilter.GaussianBlur(0))
    centered(ImageDraw.Draw(im2), H - 150, 'ANGELIC CARDS', font('Cinzel-SemiBold.ttf', 40), GOLD, spacing=6)
    return im2


def cards():
    out = []
    week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    for i, planet in enumerate(['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']):
        v, o = A.SEVEN[planet], A.OFFICES[planet]
        out.append({'slug': v['slug'], 'name': v['angel'], 'glyph': GLYPH[planet],
                    'eyebrow': f"{v['day'].upper()} · {the(planet).upper()}",
                    'subtitle': f"Angel of {the(planet)} and of {v['day']}",
                    'keys': o['tags'], 'line': o['plain']})
    for i, (period, no, hname, angel, retinue, dukes, note) in enumerate(A.PAULINA):
        out.append({'slug': 'paulina-' + angel.lower(), 'name': angel, 'glyph': ROMAN[no - 1],
                    'glyph_font': font('Cinzel-SemiBold.ttf', 34),
                    'eyebrow': f"THE HOURS OF THE {period.upper()} · {ROMAN[no - 1]}",
                    'subtitle': f"Angel of the {ORD[no - 1]} hour of the {period}, the hour called {hname}",
                    'keys': [f"emblem: {ATTRIBUTE[i]}"],
                    'line': 'In his hour he serves whichever planet rules it, and does the work of that planet.'})
    return out


def guide_page(c, pw, ph):
    c.setFillColorRGB(0.035, 0.047, 0.11)
    c.rect(0, 0, pw, ph, fill=1, stroke=0)
    c.setFillColorRGB(0.91, 0.81, 0.55)
    c.setFont('Cinzel', 26)
    c.drawCentredString(pw / 2, ph - 1.3 * inch, 'ANGELIC CARDS')
    c.setFont('CormorantI', 15)
    c.drawCentredString(pw / 2, ph - 1.65 * inch, 'Thirty-one angels of the days and the hours')
    text = [
        ('How to print', 'Print the card pages on heavy matte card stock (250–300 gsm), at 100% scale (“actual size”), single-sided. '
         'Cut along the marks. For backs, print the back page on the reverse of each sheet, or print it separately and glue.'),
        ('What is in the deck', 'Seven cards for the angels of the seven days, from the Heptameron: Michael (Sunday, the Sun), Gabriel (Monday, the Moon), '
         'Samael (Tuesday, Mars), Raphael (Wednesday, Mercury), Sachiel (Thursday, Jupiter), Anael (Friday, Venus) and Cassiel (Saturday, Saturn). '
         'Each lists what the old books say the angels of that planet can do. Twenty-four cards for the angels of the hours of the day and night, '
         'from the Ars Paulina, each with the name of his hour.'),
        ('Ways to use them', 'Draw one of the seven in the morning as the angel to keep in mind for the day; or lay out the card for today’s ruling angel. '
         'Draw one of the twenty-four to sit with during an hour of prayer or meditation. Find the angel ruling the present hour at '
         'discovery-science.com/angel-of-the-hour.'),
        ('A note', 'The names and offices come from the Heptameron, the Ars Paulina, the Sworn Book of Honorius and Agrippa. '
         'The portraits are modern devotional artwork, painted for Discovery Science with an AI image generator. '
         'These cards are for reflection and devotion; they make no promise of any outcome.'),
    ]
    y = ph - 2.4 * inch
    for head, body in text:
        c.setFont('Cinzel', 13)
        c.setFillColorRGB(0.91, 0.81, 0.55)
        c.drawString(1.1 * inch, y, head.upper())
        y -= 0.3 * inch
        c.setFont('Cormorant', 13.5)
        c.setFillColorRGB(0.93, 0.9, 0.83)
        words, line = body.split(), ''
        for w in words:
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


def sheet(c, imgs, pw, ph):
    cw, ch = 2.75 * inch, 4.75 * inch
    x0, y0 = (pw - 3 * cw) / 2, (ph - 2 * ch) / 2
    c.setFillColorRGB(1, 1, 1)
    for k, p in enumerate(imgs):
        col, row = k % 3, k // 3
        c.drawImage(p, x0 + col * cw, y0 + (1 - row) * ch, cw, ch)
    c.setStrokeColorRGB(0.4, 0.4, 0.4)
    c.setLineWidth(0.4)
    for i in range(4):
        x = x0 + i * cw
        c.line(x, y0 - 0.3 * inch, x, y0 - 0.08 * inch)
        c.line(x, y0 + 2 * ch + 0.08 * inch, x, y0 + 2 * ch + 0.3 * inch)
    for j in range(3):
        y = y0 + j * ch
        c.line(x0 - 0.3 * inch, y, x0 - 0.08 * inch, y)
        c.line(x0 + 3 * cw + 0.08 * inch, y, x0 + 3 * cw + 0.3 * inch, y)
    c.showPage()


def main(out):
    os.makedirs(os.path.join(out, 'cards'), exist_ok=True)
    pdfmetrics.registerFont(TTFont('Cinzel', os.path.join(FONT, 'Cinzel-SemiBold.ttf')))
    pdfmetrics.registerFont(TTFont('Cormorant', os.path.join(FONT, 'Cormorant-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('CormorantI', os.path.join(FONT, 'Cormorant-Italic.ttf')))
    paths = []
    for k, cd in enumerate(cards()):
        p = os.path.join(out, 'cards', f'{k + 1:02d}-{cd["slug"]}.png')
        im = card(cd)
        im.save(p, dpi=(300, 300))
        j = p[:-4] + '.jpg'
        im.save(j, quality=90, dpi=(300, 300))
        paths.append(j)
    bp = os.path.join(out, 'cards', '00-card-back.png')
    b = back()
    b.save(bp, dpi=(300, 300))
    bp = bp[:-4] + '.jpg'
    b.save(bp, quality=90, dpi=(300, 300))
    pw, ph = letter
    c = canvas.Canvas(os.path.join(out, 'Angelic-Cards-print.pdf'), pagesize=letter)
    c.setTitle('Angelic Cards · Discovery Science')
    guide_page(c, pw, ph)
    for i in range(0, len(paths), 6):
        sheet(c, paths[i:i + 6], pw, ph)
    sheet(c, [bp] * 6, pw, ph)
    c.save()
    for f in os.listdir(os.path.join(out, 'cards')):
        if f.endswith('.jpg'):
            os.remove(os.path.join(out, 'cards', f))
    print('cards:', len(paths), '→', out)


if __name__ == '__main__':
    main(sys.argv[1])
