"""Prompts used to paint the angel portraits (Canva image generation).
Each draws on that angel's sources: the Heptameron, the Ars Paulina, the Sworn Book of Honorius
(colours and bodies of each planet's angels) and Agrippa's Fourth Book (each planet's emblems).
The images are modern devotional artwork, not reproductions of any manuscript."""

STYLE = ('Painted in egg tempera and burnished gold leaf, in the manner of a Byzantine and early Italian Renaissance altarpiece, '
         'reverent, luminous and highly detailed. Full figure, frontal and symmetrical, a calm noble face looking at the viewer, '
         'great wings and a large shining halo. No text, no letters, no inscriptions, no watermark, no frame.')

SEVEN = {
    'michael': 'A sacred devotional icon of the archangel Michael, angel of the Sun and of Sunday. Robes of gold and saffron “like the Sun or gold”, holding a golden sceptre and a sword, a lion resting at his feet and a rooster beside it, a blazing sun behind his head, rays of gold filling a lapis sky.',
    'gabriel': 'A sacred devotional icon of the archangel Gabriel, angel of the Moon and of Monday. Robes of silver and pale green that shimmer “like crystal or a burnished sword, or like ice”, holding a white lily and a silver arrow, a crescent moon behind his head, a white doe at his feet, a moonlit night sky over a dark sea with gentle rain.',
    'samael': 'A sacred devotional icon of the archangel Samael, angel of Mars and of Tuesday. Lean and fierce, his armour and robes glowing red “such as red-hot coals kindled well”, holding a drawn sword and a shield, a grey wolf at his feet and a raven on his shoulder, a red planet and a sky of embers behind him, holy and formidable.',
    'raphael': 'A sacred devotional icon of the archangel Raphael, angel of Mercury and of Wednesday, the healer of the Book of Tobit. His garment of changeable shimmering colours, his figure “clear like glass, or like a flame of white fire”, holding a pilgrim’s staff and a small flask, a fish at his feet for Tobias, a magpie nearby, a dawn sky of silver clouds.',
    'sachiel': 'A sacred devotional icon of the archangel Sachiel, also called Zadkiel, angel of Jupiter and of Thursday. Robes of azure “like the color of the sky, or of crystal”, crowned with laurel and flowers, holding a royal sceptre, a peacock with open tail and a stag at his feet, a bright Jupiter shining above, a calm sky with distant lightning.',
    'anael': 'A sacred devotional icon of the archangel Anael, angel of Venus and of Friday. Gentle and beautiful, robes “as white as snow” and green with gold above, holding a garland of roses, white doves flying around her, flowers springing at her feet, the evening star shining in a rose and turquoise twilight sky.',
    'cassiel': 'A sacred devotional icon of the archangel Cassiel, angel of Saturn and of Saturday. Tall, long and slender and pale, in a black robe edged with gold, holding a sickle and an hourglass, an owl perched beside him, a small dragon coiled at his feet, a juniper tree, a cold sky of snow and stars.',
}

DAY_LIGHT = ['first light of dawn, rose and pale gold', 'early morning, clear gold and blue', 'bright morning light', 'mid-morning sun',
             'late morning radiance', 'the blazing light of noon', 'early afternoon gold', 'warm afternoon light', 'late afternoon amber',
             'the long golden light before sunset', 'sunset, crimson and gold', 'dusk, violet and fading gold']
NIGHT_LIGHT = ['twilight just after sunset, indigo with a last band of gold', 'the first stars of evening', 'deep blue evening with a rising moon',
               'night, deep indigo and many stars', 'late night, starlight and silver', 'midnight, the darkest blue, a river of stars',
               'after midnight, silent stars and a pale moon', 'the deep night, violet and silver', 'the small hours, cold blue starlight',
               'the hour before dawn, deep blue turning violet', 'the pre-dawn, a faint glow on the horizon', 'the last hour of night, the morning star rising']
ATTRIBUTE = ['an hourglass', 'an open book', 'a lantern', 'a censer with rising incense', 'a golden key', 'a scroll', 'a lit candle',
             'a chalice', 'a star held in his palm', 'a trumpet', 'a lily', 'a set of scales', 'a staff topped with a star',
             'a crystal sphere', 'a silver bowl of water', 'a burning lamp', 'a crown held in both hands', 'a bell', 'a shield',
             'a quill and tablet', 'a branch of olive', 'a mirror', 'a sword held point downward', 'a ring of keys']


def pauline(index, angel, period, no, hour_name, dukes):
    light = (DAY_LIGHT if period == 'day' else NIGHT_LIGHT)[no - 1]
    return (f'A sacred devotional icon of the angel {angel}, who in the Ars Paulina rules the {no}{"st" if no == 1 else "nd" if no == 2 else "rd" if no == 3 else "th"} '
            f'hour of the {period}, the hour called {hour_name}. He stands in {light}, holding {ATTRIBUTE[index]}, '
            f'with a host of {min(dukes, 24)} smaller angels, his dukes, arrayed behind him in rows of light. '
            f'His wings and robes take the colours of that hour of the {period}.')
