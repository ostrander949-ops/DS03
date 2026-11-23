#!/usr/bin/env python3
"""The birth angel: shared data and calculations for the free page (birth-angel.html) and the personal invocation PDF.

Sources
- The 72 angels of the Shem ha-Mephorash, each set over five degrees of the zodiac counted from 0° Aries, in the order
  and with the choirs used by the French tradition (Lenormand, Ambelain): eight angels to each of the nine choirs.
- The seven planetary squares (kameas) and the method of tracing a name across them: Agrippa, De occulta philosophia II.22.
  Letters take their Hebrew values, reduced by the "aiq bekar" rule (dropping zeros) until they fit the square.
- The faces (decans) of the signs and their rulers in the Chaldean order, beginning with Mars for the first face of Aries.
- The angels of the days: the Heptameron.
Sun longitude: Meeus, Astronomical Algorithms, ch. 25 (low accuracy, about 0.01°)."""
import datetime as dt
import math

ANGELS = ['Vehuiah', 'Jeliel', 'Sitael', 'Elemiah', 'Mahasiah', 'Lelahel', 'Achaiah', 'Cahetel',
          'Haziel', 'Aladiah', 'Lauviah', 'Hahaiah', 'Iezalel', 'Mebahel', 'Hariel', 'Hakamiah',
          'Lauviah', 'Caliel', 'Leuviah', 'Pahaliah', 'Nelchael', 'Ieiaiel', 'Melahel', 'Haheuiah',
          'Nith-Haiah', 'Haaiah', 'Ierathel', 'Seheiah', 'Reiiel', 'Omael', 'Lecabel', 'Vasariah',
          'Iehuiah', 'Lehahiah', 'Chavakiah', 'Menadel', 'Aniel', 'Haamiah', 'Rehael', 'Ieiazel',
          'Hahahel', 'Mikael', 'Veuliah', 'Ielahiah', 'Sealiah', 'Ariel', 'Asaliah', 'Mihael',
          'Vehuel', 'Daniel', 'Hahasiah', 'Imamiah', 'Nanael', 'Nithael', 'Mebahiah', 'Poiel',
          'Nemamiah', 'Ieialel', 'Harahel', 'Mitzrael', 'Umabel', 'Iahhel', 'Anauel', 'Mehiel',
          'Damabiah', 'Manakel', 'Eiael', 'Habuhiah', 'Rochel', 'Jabamiah', 'Haiaiel', 'Mumiah']
assert len(ANGELS) == 72

# (choir, archangel who rules it, sephira, what the choir is traditionally said to govern)
CHOIRS = [
    ('Seraphim', 'Metatron', 'Kether, the Crown', 'the will, the first spark of every beginning, and love that burns without consuming'),
    ('Cherubim', 'Raziel', 'Chokmah, Wisdom', 'wisdom, insight and the hidden order of things'),
    ('Thrones', 'Tzaphkiel', 'Binah, Understanding', 'understanding, patience, steadfastness and the shaping of what is to come'),
    ('Dominions', 'Tzadkiel', 'Chesed, Mercy', 'mercy, generosity, order and the gentle exercise of authority'),
    ('Powers', 'Kamael', 'Geburah, Strength', 'courage, justice, protection and the strength to set limits'),
    ('Virtues', 'Raphael', 'Tiphareth, Beauty', 'healing, harmony, grace and the beauty that comes from balance'),
    ('Principalities', 'Haniel', 'Netzach, Victory', 'love, art, friendship and the victory of what is gentle'),
    ('Archangels', 'Michael', 'Hod, Splendour', 'clarity, truth, learning and the right use of words'),
    ('Angels', 'Gabriel', 'Yesod, Foundation', 'dreams, guidance, protection on the way and the care of daily life'),
]
SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
CHALDEAN = ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon']
DAY_RULER = ['Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Sun']  # Python weekday(): Monday = 0
DAY_ANGEL = {'Sun': 'Michael', 'Moon': 'Gabriel', 'Mars': 'Samael', 'Mercury': 'Raphael', 'Jupiter': 'Sachiel', 'Venus': 'Anael',
             'Saturn': 'Cassiel'}

KAMEA = {
    'Saturn': [[4, 9, 2], [3, 5, 7], [8, 1, 6]],
    'Jupiter': [[4, 14, 15, 1], [9, 7, 6, 12], [5, 11, 10, 8], [16, 2, 3, 13]],
    'Mars': [[11, 24, 7, 20, 3], [4, 12, 25, 8, 16], [17, 5, 13, 21, 9], [10, 18, 1, 14, 22], [23, 6, 19, 2, 15]],
    'Sun': [[6, 32, 3, 34, 35, 1], [7, 11, 27, 28, 8, 30], [19, 14, 16, 15, 23, 24], [18, 20, 22, 21, 17, 13],
            [25, 29, 10, 9, 26, 12], [36, 5, 33, 4, 2, 31]],
    'Venus': [[22, 47, 16, 41, 10, 35, 4], [5, 23, 48, 17, 42, 11, 29], [30, 6, 24, 49, 18, 36, 12], [13, 31, 7, 25, 43, 19, 37],
              [38, 14, 32, 1, 26, 44, 20], [21, 39, 8, 33, 2, 27, 45], [46, 15, 40, 9, 34, 3, 28]],
    'Mercury': [[8, 58, 59, 5, 4, 62, 63, 1], [49, 15, 14, 52, 53, 11, 10, 56], [41, 23, 22, 44, 45, 19, 18, 48],
                [32, 34, 35, 29, 28, 38, 39, 25], [40, 26, 27, 37, 36, 30, 31, 33], [17, 47, 46, 20, 21, 43, 42, 24],
                [9, 55, 54, 12, 13, 51, 50, 16], [64, 2, 3, 61, 60, 6, 7, 57]],
    'Moon': [[37, 78, 29, 70, 21, 62, 13, 54, 5], [6, 38, 79, 30, 71, 22, 63, 14, 46], [47, 7, 39, 80, 31, 72, 23, 55, 15],
             [16, 48, 8, 40, 81, 32, 64, 24, 56], [57, 17, 49, 9, 41, 73, 33, 65, 25], [26, 58, 18, 50, 1, 42, 74, 34, 66],
             [67, 27, 59, 10, 51, 2, 43, 75, 35], [36, 68, 19, 60, 11, 52, 3, 44, 76], [77, 28, 69, 20, 61, 12, 53, 4, 45]],
}
for _p, _sq in KAMEA.items():   # every row, column and diagonal must add to the same number
    _n = len(_sq)
    _t = _n * (_n * _n + 1) // 2
    assert all(sum(r) == _t for r in _sq) and all(sum(r[c] for r in _sq) == _t for c in range(_n)), _p
    assert sum(_sq[i][i] for i in range(_n)) == _t and sum(_sq[i][_n - 1 - i] for i in range(_n)) == _t, _p
    assert sorted(v for r in _sq for v in r) == list(range(1, _n * _n + 1)), _p

# Latin letters to the values of the Hebrew letters they stand for (as in transliteration); digraphs first.
DIGRAPHS = {'SH': 300, 'TH': 400, 'CH': 8, 'TZ': 90, 'TS': 90, 'PH': 80}
LETTERS = {'A': 1, 'B': 2, 'G': 3, 'D': 4, 'E': 5, 'H': 5, 'V': 6, 'W': 6, 'O': 6, 'U': 6, 'Z': 7, 'T': 9, 'I': 10, 'Y': 10, 'J': 10,
           'K': 20, 'C': 20, 'L': 30, 'M': 40, 'N': 50, 'S': 60, 'X': 60, 'P': 80, 'F': 80, 'Q': 100, 'R': 200}


def name_values(name):
    s = ''.join(ch for ch in name.upper() if ch.isalpha())
    out, i = [], 0
    while i < len(s):
        if s[i:i + 2] in DIGRAPHS:
            out.append(DIGRAPHS[s[i:i + 2]])
            i += 2
        elif s[i] in LETTERS:
            out.append(LETTERS[s[i]])
            i += 1
        else:
            i += 1
    return out


def reduce_to(v, top):
    while v > top:
        v //= 10   # aiq bekar: 200 -> 20 -> 2
    return v


def sigil_path(name, planet):
    """Cells (row, col) the name passes through on the planet's square, repeated letters merged."""
    sq = KAMEA[planet]
    top = len(sq) ** 2
    where = {v: (r, c) for r, row in enumerate(sq) for c, v in enumerate(row)}
    cells = []
    for v in name_values(name):
        cell = where[reduce_to(v, top)]
        if not cells or cells[-1] != cell:
            cells.append(cell)
    return cells


def julian_day(t):
    t = t.astimezone(dt.timezone.utc)
    y, m = t.year, t.month
    d = t.day + (t.hour + t.minute / 60 + t.second / 3600) / 24
    if m <= 2:
        y, m = y - 1, m + 12
    a = y // 100
    b = 2 - a + a // 4
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + b - 1524.5


def sun_longitude(t):
    T = (julian_day(t) - 2451545.0) / 36525
    L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T * T
    M = math.radians(357.52911 + 35999.05029 * T - 0.0001537 * T * T)
    C = (1.914602 - 0.004817 * T - 0.000014 * T * T) * math.sin(M) + (0.019993 - 0.000101 * T) * math.sin(2 * M) + 0.000289 * math.sin(3 * M)
    om = math.radians(125.04 - 1934.136 * T)
    return (L0 + C - 0.00569 - 0.00478 * math.sin(om)) % 360


def sun_times(date, lat, lon):
    """Sunrise and sunset (UTC datetimes) for a date and place, NOAA method. None at polar day/night."""
    n = date.toordinal() - dt.date(date.year, 1, 1).toordinal() + 1
    g = 2 * math.pi / 365 * (n - 1)
    eqt = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g) - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    decl = 0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g) + 0.000907 * math.sin(2 * g) \
        - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g)
    la = math.radians(lat)
    cos_ha = (math.cos(math.radians(90.833)) / (math.cos(la) * math.cos(decl))) - math.tan(la) * math.tan(decl)
    if abs(cos_ha) > 1:
        return None
    ha = math.degrees(math.acos(cos_ha))
    base = dt.datetime(date.year, date.month, date.day, tzinfo=dt.timezone.utc)
    rise = base + dt.timedelta(minutes=720 - 4 * (lon + ha) - eqt)
    sset = base + dt.timedelta(minutes=720 - 4 * (lon - ha) - eqt)
    return rise, sset


def planetary_hour(t, lat, lon):
    """(planet of the day, hour number 0-23 counted from sunrise, planet of the hour, is_day) for an aware datetime."""
    local = t
    d = local.date()
    st = sun_times(d, lat, lon)
    if st is None:
        return None
    rise, sset = st
    tu = t.astimezone(dt.timezone.utc)
    if tu < rise:        # before sunrise: the night of the previous day
        d = d - dt.timedelta(days=1)
        prev = sun_times(d, lat, lon)
        start, end, offset = prev[1], rise, 12
    elif tu < sset:
        start, end, offset = rise, sset, 0
    else:
        nxt = sun_times(d + dt.timedelta(days=1), lat, lon)
        start, end, offset = sset, nxt[0], 12
    k = int((tu - start) / ((end - start) / 12))
    ruler = DAY_RULER[d.weekday()]
    idx = offset + min(k, 11)
    return ruler, idx, CHALDEAN[(CHALDEAN.index(ruler) + idx) % 7], offset == 0


def birth_angel(t, time_known=True):
    lon = sun_longitude(t)
    i = int(lon // 5)
    edge = min(lon - 5 * i, 5 * (i + 1) - lon)
    sign = SIGNS[int(lon // 30)]
    deg = lon % 30
    face = int(deg // 10)
    face_ruler = CHALDEAN[(CHALDEAN.index('Mars') - 0 + int(lon // 10)) % 7]  # Chaldean order from Mars at 0° Aries
    choir = CHOIRS[i // 8]
    return {
        'number': i + 1, 'name': ANGELS[i], 'from_deg': 5 * i, 'sun': lon, 'sign': sign, 'deg': deg,
        'choir': choir[0], 'archangel': choir[1], 'sephira': choir[2], 'governs': choir[3],
        'face': face + 1, 'face_ruler': face_ruler,
        'cusp': (not time_known and edge < 1.0) or edge < 0.05,
        'neighbour': ANGELS[(i + 1) % 72] if lon - 5 * i > 2.5 else ANGELS[i - 1],
    }


if __name__ == '__main__':
    t = dt.datetime(2026, 3, 21, 12, tzinfo=dt.timezone.utc)
    print(birth_angel(t))
    print(sigil_path('Montgomery', 'Sun'))
