"""The Discovery Science Angelic Tarot: the 22 Major Arcana, each given to an angel.
Pairings follow the usual Golden Dawn attributions of the trumps (element, planet or sign),
with the angel Agrippa assigns to that element, planet or sign (De Occulta Philosophia II.7, II.10, II.14).
The paintings are new devotional artwork; no historical deck is copied."""

STYLE = ('Painted in egg tempera and burnished gold leaf, in the manner of a Byzantine and early Italian Renaissance altarpiece, '
         'reverent, luminous and highly detailed, a tarot card painting with a strong central composition. '
         'No text, no letters, no numbers, no inscriptions, no watermark, no border, no frame.')

# (number, card, attribution, angel, angel's source, upright meaning, reversed meaning, scene for the painting)
MAJORS = [
    (0, 'The Fool', 'Air', 'Cherub', 'Agrippa’s ruler of the element of Air',
     'beginnings, trust, the leap into the unknown', 'recklessness, hesitation, a journey refused',
     'a young angel with light wings stepping joyfully from a high cliff edge into open sky, a white rose in one hand, a small white dog leaping beside, wind in the robes, dawn light'),
    (1, 'The Magician', 'Mercury', 'Raphael', 'angel of Mercury',
     'skill, will, the power to make things happen', 'trickery, scattered energy, talent unused',
     'the archangel Raphael standing at an altar holding a wand raised to heaven, on the altar a cup, a sword, a golden coin and a staff, lilies and roses growing around, a figure-eight of light above his head'),
    (2, 'The High Priestess', 'the Moon', 'Gabriel', 'angel of the Moon',
     'intuition, mystery, hidden knowledge', 'secrets kept, ignoring the inner voice',
     'the archangel Gabriel seated between a black and a white pillar, a crescent moon at the feet, a veil of pomegranates behind, holding a closed scroll, moonlit blue and silver robes'),
    (3, 'The Empress', 'Venus', 'Anael', 'angel of Venus',
     'abundance, love, fertility, nurture', 'dependence, creative block, neglect',
     'the angel Anael enthroned in a blossoming garden, crowned with twelve stars, wheat growing at her feet, a waterfall behind, doves around her, robes of green and rose'),
    (4, 'The Emperor', 'Aries', 'Malchidiel', 'Agrippa’s angel of Aries',
     'authority, structure, protection', 'domination, rigidity, loss of control',
     'the angel Malchidiel enthroned on a stone throne carved with rams’ heads, holding a golden sceptre and orb, red mountains behind, armour beneath crimson robes'),
    (5, 'The Hierophant', 'Taurus', 'Asmodel', 'Agrippa’s angel of Taurus',
     'tradition, teaching, blessing', 'dogma, rebellion, empty ritual',
     'the angel Asmodel in rich vestments with a triple crown, raising a hand in blessing, two kneeling figures before him, crossed golden keys at his feet, a white bull resting nearby'),
    (6, 'The Lovers', 'Gemini', 'Ambriel', 'Agrippa’s angel of Gemini',
     'love, union, a choice of the heart', 'disharmony, a wrong choice, imbalance',
     'the angel Ambriel hovering above a man and a woman in a garden with wings outspread in blessing, a radiant sun behind, a fruit tree and a flowering tree on either side'),
    (7, 'The Chariot', 'Cancer', 'Muriel', 'Agrippa’s angel of Cancer',
     'victory, willpower, forward motion', 'lack of direction, defeat, inner conflict',
     'the angel Muriel standing in a silver chariot drawn by a black and a white sphinx, a starry canopy overhead, crescent moons on the shoulders, a walled city behind'),
    (8, 'Strength', 'Leo', 'Verchiel', 'Agrippa’s angel of Leo',
     'courage, gentle strength, compassion', 'self-doubt, weakness, force used badly',
     'the angel Verchiel gently closing the jaws of a golden lion with bare hands, a garland of flowers around both, a sign of infinity glowing above, golden afternoon light'),
    (9, 'The Hermit', 'Virgo', 'Hamaliel', 'Agrippa’s angel of Virgo',
     'solitude, inner guidance, wisdom sought', 'isolation, withdrawal, being lost',
     'the angel Hamaliel in grey hooded robes on a snowy mountain peak at night, holding up a lantern with a six-pointed star of light inside, leaning on a staff'),
    (10, 'Wheel of Fortune', 'Jupiter', 'Sachiel', 'angel of Jupiter',
     'cycles, fortune, turning points', 'bad luck, resistance to change',
     'the angel Sachiel above a great golden wheel turning among the clouds, a sphinx atop the wheel, the four living creatures in the corners (angel, eagle, lion, bull) reading books, azure sky'),
    (11, 'Justice', 'Libra', 'Zuriel', 'Agrippa’s angel of Libra',
     'fairness, truth, cause and effect', 'injustice, dishonesty, avoiding accountability',
     'the angel Zuriel seated between two pillars holding upright a sword in the right hand and balanced scales in the left, a purple veil behind, red and gold robes'),
    (12, 'The Hanged Man', 'Water', 'Tharsis', 'Agrippa’s ruler of the element of Water',
     'surrender, a new perspective, pause', 'stalling, needless sacrifice',
     'a serene angel suspended upside down by one foot from a living tree, the other leg crossed, hands behind the back, a golden halo shining around the head, deep blue water below'),
    (13, 'Death', 'Scorpio', 'Barbiel', 'Agrippa’s angel of Scorpio',
     'endings, transformation, transition', 'resistance to change, stagnation',
     'the angel Barbiel in black armour on a pale white horse carrying a black banner with a white rose, a sunrise between two towers in the distance, figures bowing, solemn but not frightening'),
    (14, 'Temperance', 'Sagittarius', 'Adnachiel', 'Agrippa’s angel of Sagittarius',
     'balance, patience, healing, moderation', 'excess, imbalance, haste',
     'the angel Adnachiel with great wings standing with one foot on land and one in a pool, pouring water between two golden cups, irises growing beside, a path leading to a crown of light on distant mountains'),
    (15, 'The Devil', 'Capricorn', 'Hanael', 'Agrippa’s angel of Capricorn',
     'bondage, temptation, shadow; and the strength to break free', 'release, breaking chains, reclaiming power',
     'the angel Hanael standing in light above a dark cave where two figures sit with loose chains around their necks that they could lift off, an inverted pentagram of shadow fading, a goat-shaped darkness retreating from the angel'),
    (16, 'The Tower', 'Mars', 'Samael', 'angel of Mars',
     'sudden change, revelation, upheaval', 'disaster averted, fear of change',
     'the archangel Samael in red armour striking a tall stone tower on a crag with a bolt of lightning, a golden crown flung from its top, flames from the windows, a stormy night sky'),
    (17, 'The Star', 'Aquarius', 'Gambiel', 'Agrippa’s angel of Aquarius',
     'hope, renewal, inspiration, peace', 'despair, lost faith, disconnection',
     'the angel Gambiel kneeling by a pool under a night sky with one great eight-pointed star and seven small stars, pouring water from two jars, one onto the land and one into the pool, a bird in a tree'),
    (18, 'The Moon', 'Pisces', 'Barchiel', 'Agrippa’s angel of Pisces',
     'dreams, illusion, intuition, the unconscious', 'confusion lifting, fear released',
     'the angel Barchiel above a great moon with a calm face, a winding path between two towers, a dog and a wolf howling at the moon, a crayfish rising from a pool, dew falling'),
    (19, 'The Sun', 'the Sun', 'Michael', 'angel of the Sun',
     'joy, success, vitality, clarity', 'temporary sadness, delay',
     'the archangel Michael radiant before a huge golden sun with a face and rays, a joyful child on a white horse holding a red banner, sunflowers over a garden wall'),
    (20, 'Judgement', 'Fire', 'Seraph', 'Agrippa’s ruler of the element of Fire',
     'awakening, renewal, a calling', 'self-doubt, refusing the call',
     'a fiery six-winged seraph in the clouds sounding a golden trumpet with a banner bearing a red cross, figures below rising from open tombs with arms raised in joy, snowy mountains behind'),
    (21, 'The World', 'Saturn', 'Cassiel', 'angel of Saturn',
     'completion, wholeness, fulfilment', 'loose ends, delay in completion',
     'the angel Cassiel dancing within a great oval laurel wreath tied with red ribbons, holding two wands, the four living creatures (angel, eagle, lion, bull) in the corners among clouds, deep indigo sky'),
]


def prompt(m):
    n, card, attr, angel, src, up, rev, scene = m
    return f'A sacred devotional tarot painting for the card {card}, given to the angel {angel}: {scene}. {STYLE}'
