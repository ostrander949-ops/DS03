#!/usr/bin/env python3
"""Writes one issue of the weekly newsletter, "The Angels of the Week", as Markdown.
Usage: python3 tools/weekly_reading.py [YYYY-MM-DD]   (any date; the issue covers the Sunday-to-Saturday week containing it)

Each issue has: the week's moon phases, a card of the week from the Angelic Tarot, and for each day the ruling angel,
what the old books give that angel, the aligned hours, the hour angels who serve them, and a short reflection.
Moon phases use Meeus' algorithm (Astronomical Algorithms, ch. 49), accurate to a few minutes."""
import datetime as dt
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import angels_data as A  # noqa: E402
from tarot_data import MAJORS  # noqa: E402

SITE = 'https://www.discovery-science.com'
WEEK = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
DAY_RULER = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
CHALDEAN = ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon']
ORD = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth']

# Short reflections for each planet's day: suggestions for prayer or attention, never predictions. Rotated week by week.
REFLECT = {
    'Sun': ['Name one thing you would like to be known for, and do one small act toward it today.',
            'Thank someone whose goodwill has helped you, out loud or in writing.',
            'Step into the light for a few minutes: morning sun on your face, eyes closed, and a word of gratitude.'],
    'Moon': ['Write down last night’s dream, or the first thought you woke with, before it fades.',
             'If you are travelling, ask for a safe road; if not, walk somewhere you have not walked before.',
             'Sit with water: a bath, a river, or a glass held in both hands, and let the mind go quiet.'],
    'Mars': ['Choose one hard thing you have been avoiding and give it twenty honest minutes.',
             'Move your body until you feel your strength, then ask for courage used well.',
             'Where there is conflict in your life, ask for clean victory or a clean end, without cruelty.'],
    'Mercury': ['Learn one new thing today and teach it to someone before the day is out.',
                'Write the letter or message you have been putting off.',
                'Ask for clear sight on a question that has confused you, then listen in the quiet that follows.'],
    'Jupiter': ['Give something away freely, with no thought of return.',
                'Make peace with one person, even if only in your own heart.',
                'Count what is going well, slowly, and let joy have its full weight.'],
    'Venus': ['Tell someone you love them, plainly.',
              'Make one thing more beautiful: a table, a corner of a room, a page.',
              'If a friendship has cooled, reach out first.'],
    'Saturn': ['Finish something. Close a loop you have left open.',
               'Sit for ten minutes in silence and let what needs to end, end.',
               'Set one firm boundary, kindly, and keep it.'],
}


def moon_phases(start, end):
    """New, first-quarter, full and last-quarter moons between two dates (UTC), after Meeus ch. 49."""
    out = []
    k0 = math.floor((start.year + (start.timetuple().tm_yday / 365.25) - 2000) * 12.3685) - 1
    for i in range(0, 12):
        for q, name in ((0, 'New moon'), (0.25, 'First quarter'), (0.5, 'Full moon'), (0.75, 'Last quarter')):
            k = k0 + i + q
            T = k / 1236.85
            jde = 2451550.09766 + 29.530588861 * k + 0.00015437 * T * T
            E = 1 - 0.002516 * T
            M = math.radians((2.5534 + 29.10535670 * k) % 360)
            Mp = math.radians((201.5643 + 385.81693528 * k) % 360)
            F = math.radians((160.7108 + 390.67050284 * k) % 360)
            Om = math.radians((124.7746 - 1.56375588 * k) % 360)
            if q in (0, 0.5):
                c = (-0.4072 if q == 0 else -0.40614) * math.sin(Mp) + (0.17241 if q == 0 else 0.17302) * E * math.sin(M) \
                    + 0.01608 * math.sin(2 * Mp) + 0.01039 * math.sin(2 * F) + 0.00739 * E * math.sin(Mp - M) \
                    - 0.00514 * E * math.sin(Mp + M) + 0.00208 * E * E * math.sin(2 * M) - 0.00111 * math.sin(Mp - 2 * F) \
                    - 0.00057 * math.sin(Mp + 2 * F) + 0.00056 * E * math.sin(2 * Mp + M) - 0.00042 * math.sin(3 * Mp) \
                    - 0.00017 * math.sin(Om)
            else:
                c = -0.62801 * math.sin(Mp) + 0.17172 * E * math.sin(M) - 0.01183 * E * math.sin(Mp + M) + 0.00862 * math.sin(2 * Mp) \
                    + 0.00804 * math.sin(2 * F) + 0.00454 * E * math.sin(Mp - M) + 0.00204 * E * E * math.sin(2 * M) \
                    - 0.0018 * math.sin(Mp - 2 * F) - 0.0007 * math.sin(Mp + 2 * F) - 0.0004 * math.sin(3 * Mp) - 0.00034 * E * math.sin(2 * Mp - M) \
                    - 0.00017 * math.sin(Om)
                W = 0.00306 - 0.00038 * E * math.cos(M) + 0.00026 * math.cos(Mp) - 0.00002 * math.cos(Mp - M) + 0.00002 * math.cos(Mp + M) + 0.00002 * math.cos(2 * F)
                c += W if q == 0.25 else -W
            jde += c
            t = dt.datetime(2000, 1, 1, 12, tzinfo=dt.timezone.utc) + dt.timedelta(days=jde - 2451545.0)
            if start <= t.date() <= end:
                out.append((t, name))
    return sorted(set(out))


def the(p):
    return 'the ' + p if p in ('Sun', 'Moon') else p


def hour_angels(planet, ruler):
    """The Pauline angels who keep the hours of `planet` on the day ruled by `ruler`."""
    out = []
    for i in range(24):
        if CHALDEAN[(CHALDEAN.index(ruler) + i) % 7] == planet:
            period, no, hname, angel = A.PAULINA[i][:4]
            out.append((period, no, angel, hname))
    return out


def issue(any_day):
    sunday = any_day - dt.timedelta(days=(any_day.weekday() + 1) % 7)
    saturday = sunday + dt.timedelta(days=6)
    wk = int(sunday.strftime('%U')) + sunday.year * 53
    card = MAJORS[wk % 22]
    n, cname, attr, cangel, csrc, up, rev, scene = card
    lines = [f'# The Angels of the Week · {sunday:%B} {sunday.day}–{saturday.day if saturday.month == sunday.month else saturday.strftime("%B ") + str(saturday.day)}, {saturday.year}', '',
             'Seven angels rule the seven days in the old books, and twenty-four more keep the hours. Here is who is keeping this week, '
             'what the books say each can do, and when their hours are strongest. '
             f'For the exact hours where you live, open the live clock: {SITE}/angel-of-the-hour.html', '',
             '**The aligned hours.** On every day, four hours belong to the same planet as the day itself: the first and eighth hours after sunrise '
             'and the third and tenth after sunset. Tradition counts them as the strongest hours for the day’s work. In the Ars Paulina they are always kept by '
             'the same four angels: Samael, Osmadiel, Serquanich and Iassuarim.', '']
    phases = moon_phases(sunday, saturday)
    if phases:
        lines += ['## The Moon this week', ''] + [f'- **{name}**: {t:%A %B} {t.day}, {t:%H:%M} UTC' for t, name in phases] + ['']
    lines += [f'## Card of the week: {cname}', '',
              f'From the Angelic Tarot, the card {cname} is given to **{cangel}**, {csrc}. Upright it speaks of {up}; reversed, of {rev}. '
              'Keep it in mind as a thread through the week.', '']
    for d in range(7):
        day = sunday + dt.timedelta(days=d)
        planet = DAY_RULER[d]
        v, o = A.SEVEN[planet], A.OFFICES[planet]
        r = REFLECT[planet][wk % 3]
        i = (wk * 7 + d * 5) % 24
        period, no, hname, angel = A.PAULINA[i][:4]
        serves = CHALDEAN[(CHALDEAN.index(planet) + i) % 7]
        lines += [f'## {WEEK[d]} {day:%B} {day.day} · {v["angel"]}, angel of {the(planet)}', '',
                  f'**{" · ".join(o["tags"])}**', '',
                  f'{o["plain"]} The Heptameron says the spirits of {WEEK[d]} have power “{o["heptameron"]}”.', '',
                  f'*An hour angel to meet:* **{angel}**, who keeps the {ORD[no - 1]} hour of the {period} (the hour called *{hname}*). '
                  f'Today he serves {the(serves)}, so his hour carries the work of {the(serves)}: {" · ".join(A.OFFICES[serves]["tags"]).lower()}. '
                  f'{SITE}/angel-of-the-hour.html#paulina-{angel.lower()}', '',
                  f'*Reflection:* {r}', '']
    lines += ['---', '',
              'The angels’ portraits, the live clock and the long-form entries for every angel are at '
              f'{SITE}/angel-of-the-hour.html. Printable angel cards, wallpapers and the illustrated Book of the Angels are in the shop: {SITE}/shop.html#angels', '',
              '*This newsletter describes a tradition drawn from the Heptameron, the Ars Paulina, the Sworn Book of Honorius and Agrippa. '
              'It is for reflection and devotion and makes no promise of any outcome.*']
    return '\n'.join(lines), sunday


if __name__ == '__main__':
    d = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date.today()
    md, _ = issue(d)
    print(md)
