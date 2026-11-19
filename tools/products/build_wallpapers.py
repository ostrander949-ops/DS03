#!/usr/bin/env python3
"""Angel Wallpaper Pack: each of the 31 portraits as a phone wallpaper (1290 x 2796) and a desktop wallpaper (2560 x 1440).
Usage: python3 tools/products/build_wallpapers.py <folder of full-size portrait jpgs> <out_dir>
Portrait files are named <slug>.jpg (michael.jpg, paulina-tartys.jpg, ...)."""
import os
import sys
import zipfile

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, 'fonts')
GOLD = (233, 207, 140)


def label(slug):
    return slug.replace('paulina-', '').capitalize()


def blurred_bg(src, w, h):
    s = max(w / src.width, h / src.height) * 1.15
    bg = src.resize((int(src.width * s), int(src.height * s)), Image.LANCZOS)
    bg = bg.crop(((bg.width - w) // 2, (bg.height - h) // 2, (bg.width - w) // 2 + w, (bg.height - h) // 2 + h))
    bg = bg.filter(ImageFilter.GaussianBlur(60))
    return ImageEnhance.Brightness(bg).enhance(0.38)


def place(canvas, img, box_size, cx, cy):
    p = img.resize((box_size, box_size), Image.LANCZOS)
    glow = Image.new('L', canvas.size, 0)
    ImageDraw.Draw(glow).rounded_rectangle((cx - box_size // 2 - 20, cy - box_size // 2 - 20, cx + box_size // 2 + 20, cy + box_size // 2 + 20), 60, fill=110)
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    canvas.paste(Image.new('RGB', canvas.size, (255, 214, 140)), (0, 0), glow)
    mask = Image.new('L', (box_size, box_size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, box_size, box_size), 40, fill=255)
    canvas.paste(p, (cx - box_size // 2, cy - box_size // 2), mask)
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((cx - box_size // 2 - 4, cy - box_size // 2 - 4, cx + box_size // 2 + 4, cy + box_size // 2 + 4), 44, outline=GOLD, width=6)
    return d


def phone(img, name):
    """Full-bleed: the painting scaled to the screen height, cropped to the central figure."""
    w, h = 1290, 2796
    p = img.resize((h, h), Image.LANCZOS)
    c = p.crop(((h - w) // 2, 0, (h - w) // 2 + w, h))
    shade = Image.new('L', (w, h), 0)
    sd = ImageDraw.Draw(shade)
    for y in range(h - 700, h):
        sd.line((0, y, w, y), fill=int(200 * (y - (h - 700)) / 700))
    c.paste(Image.new('RGB', (w, h), (6, 8, 18)), (0, 0), shade)
    d = ImageDraw.Draw(c)
    f = ImageFont.truetype(os.path.join(FONT, 'Cinzel-SemiBold.ttf'), 88)
    d.text((w // 2, h - 330), name.upper(), font=f, fill=GOLD, anchor='ma')
    return c


def desktop(img, name):
    w, h = 2560, 1440
    c = blurred_bg(img, w, h)
    d = place(c, img, 1180, w // 2, 650)
    f = ImageFont.truetype(os.path.join(FONT, 'Cinzel-SemiBold.ttf'), 64)
    d.text((w // 2, 1290), name.upper(), font=f, fill=GOLD, anchor='ma')
    return c


def main(src, out):
    os.makedirs(os.path.join(out, 'phone'), exist_ok=True)
    os.makedirs(os.path.join(out, 'desktop'), exist_ok=True)
    files = sorted(f for f in os.listdir(src) if f.endswith('.jpg'))
    for f in files:
        slug = f[:-4]
        img = Image.open(os.path.join(src, f)).convert('RGB')
        if img.width != img.height:
            side = min(img.size)
            top = int((img.height - side) * 0.25) if img.height > img.width else 0
            left = (img.width - side) // 2
            img = img.crop((left, top, left + side, top + side))
        phone(img, label(slug)).save(os.path.join(out, 'phone', slug + '.jpg'), quality=90)
        desktop(img, label(slug)).save(os.path.join(out, 'desktop', slug + '.jpg'), quality=90)
    zp = os.path.join(out, 'Angel-Wallpapers.zip')
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_STORED) as z:
        for sub in ('phone', 'desktop'):
            for f in sorted(os.listdir(os.path.join(out, sub))):
                z.write(os.path.join(out, sub, f), f'Angel Wallpapers/{sub}/{f}')
        z.writestr('Angel Wallpapers/READ ME.txt',
                   'Angel Wallpapers · Discovery Science\n\n31 angels of the days and hours, as phone wallpapers (1290 x 2796) and desktop wallpapers (2560 x 1440).\n'
                   'The portraits are modern devotional artwork painted for Discovery Science with an AI image generator.\n'
                   'For personal use. Please do not resell or redistribute.\n\nFind the angel of this hour: https://www.discovery-science.com/angel-of-the-hour.html\n')
    print(len(files), 'angels →', zp)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
