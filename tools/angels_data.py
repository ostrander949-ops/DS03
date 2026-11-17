"""Source data for the Angel of the Hour page.

Every fact here is taken from:
  - Ars Paulina (Lemegeton III), ed. J. H. Peterson, esotericarchives.com/solomon/paulina.htm
    (British Library Sloane MS 3825), CC-BY 4.0 transcription. Bracketed forms are Peterson's
    alternate readings from the other manuscripts.
  - Heptameron (attrib. Peter of Abano, first printed 1559), ed. J. H. Peterson,
    esotericarchives.com/solomon/heptamer.htm (English of 1655 with Peterson's notes).
  - Agrippa, De occulta philosophia II.10 "The Scale of the Number seven",
    esotericarchives.com/agrippa/agrippa2.htm
  - Biblical references as cited.
"""

PLANETS = ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon']  # Chaldean order

# ------------------------------------------------------------------ the seven angels of the days
SEVEN = {
    'Sun': dict(
        angel='Michael', slug='michael', day='Sunday', hebrew='מיכאל', meaning='“Who is like God?”',
        companions=['Dardiel', 'Huratapel'], heaven='Machen', heaven_no='fourth', air_king='Varcan',
        air_ministers=['Tus', 'Andas', 'Cynabal'], wind='North', perfume='red sanders (printed as “red wheat”)',
        quarters={'East': ['Samael', 'Baciel', 'Atel', 'Fabriel', 'Vionatraba'],
                  'West': ['Anael', 'Pabel', 'Ustael', 'Burchat', 'Suceratos', 'Capabali'],
                  'North': ['Aiel', 'Aniel (or Aquiel)', 'Masgabriel', 'Sapiel', 'Matuyel'],
                  'South': ['Haludiel', 'Machasiel', 'Charsiel', 'Uriel', 'Naromiel']},
        agrippa='Agrippa’s “scale of the number seven” gives the Sun to Raphael and moves Michael to Mercury.',
        paulina='In the second part of the Ars Paulina, Michael governs the spirits of the fiery signs “towards the South”, to be observed on Sunday in the first and eighth hours of the day and the third and tenth of the night. They are said to appear “in Royal Robes holding scepters in their hands, oft Ryding on a Lion or a Cock.”',
        essay=[
            'Michael is one of only two angels named in the Hebrew Bible. In the Book of Daniel he is “one of the chief princes” (10:13) and “the great prince which standeth for the children of thy people” (12:1). The New Testament calls him “Michael the archangel”, disputing with the devil over the body of Moses (Jude 9), and in Revelation “Michael and his angels fought against the dragon” (12:7). His name is a question: who is like God?',
            'The Heptameron makes him the angel of Sunday and of the Sun. On his day he rules with two companions, Dardiel and Huratapel; the spirits of the air are under a king called Varcan and his ministers Tus, Andas and Cynabal, all subject to the North wind; and his heaven is Machen, the fourth. The book prescribes a perfume for the day, printed in the 1655 English as “red wheat” and corrected by Peterson to red sanders.',
        ]),
    'Moon': dict(
        angel='Gabriel', slug='gabriel', day='Monday', hebrew='גבריאל', meaning='usually explained as “God is my strength”',
        companions=['Michael', 'Samael'], heaven='Shamain', heaven_no='first', air_king='Arcan',
        air_ministers=['Bilet', 'Missabu', 'Abuzaba'], wind='West', perfume='aloes',
        quarters={'East': ['Gabriel', 'Gabrael', 'Madiel', 'Deamiel', 'Janael'],
                  'West': ['Sachiel', 'Zaniel', 'Habaiel', 'Bachanael', 'Corabael'],
                  'North': ['Mael', 'Vuael', 'Valnum', 'Baliel', 'Balay', 'Humastrau'],
                  'South': ['Curaniel', 'Dabriel', 'Darquiel', 'Hanun', 'Anayl', 'Vetuel']},
        agrippa='Agrippa agrees: Gabriel is the angel of the Moon.',
        paulina='In the second part of the Ars Paulina, Gabriel governs the spirits of the watery signs “towards the north”, with three mighty princes under him: Samael, Madiel and Mael. They are observed on Monday at the first and eighth hours of the day and the third and tenth of the night.',
        essay=[
            'Gabriel is the other angel named in the Hebrew Bible. He explains Daniel’s visions (Daniel 8:16; 9:21), and in the Gospel of Luke he announces two births: “I am Gabriel, that stand in the presence of God” (Luke 1:19), and then to Mary in Nazareth (Luke 1:26). In Islam, as Jibril, he brings the revelation to Muhammad.',
            'In the Heptameron he is the angel of Monday and the Moon, ruling with Michael and Samael. The spirits of the air are under King Arcan and his ministers Bilet, Missabu and Abuzaba, subject to the West wind; his heaven is Shamain, the first and lowest, the heaven of the Moon. The perfume of the day is aloes.',
        ]),
    'Mars': dict(
        angel='Samael', slug='samael', day='Tuesday', hebrew='סמאל', meaning='a name of uncertain meaning in rabbinic tradition',
        companions=['Satael', 'Amabiel'], heaven='Machon', heaven_no='fifth', air_king='Samax',
        air_ministers=['Carmax', 'Ismoli', 'Paffran'], wind='East', perfume='pepper',
        quarters={'East': ['Friagne', 'Guael', 'Damael', 'Calzas', 'Arragon'],
                  'West': ['Lama', 'Astagna', 'Lobquin', 'Soncas', 'Jazel', 'Isiael', 'Irel'],
                  'North': ['Rahumel', 'Hyniel', 'Rayel', 'Seraphiel', 'Mathiel', 'Fraciel'],
                  'South': ['Sacriel', 'Janiel', 'Galdel', 'Osael', 'Vianuel', 'Zaliel']},
        agrippa='Agrippa gives Mars to Camael (כמאל) instead.',
        paulina='Samael is everywhere in the Ars Paulina: the manuscript names him (as “Samuel”, corrected to Samael) the angel of the first hour of every day, and in its second part he is one of the three princes under Gabriel.',
        essay=[
            'Samael does not appear in the Bible. He comes from later Jewish literature, where he is a great prince of heaven associated with the accuser and with death; the midrash Pirkei de-Rabbi Eliezer tells of Samael in the Garden of Eden. The grimoires keep the fierceness but put him to work as the angel of Mars.',
            'The Heptameron makes him the angel of Tuesday, ruling with Satael and Amabiel. The spirits of the air are under King Samax and his ministers Carmax, Ismoli and Paffran, subject to the East wind; his heaven is Machon, the fifth. The perfume of the day is pepper.',
        ]),
    'Mercury': dict(
        angel='Raphael', slug='raphael', day='Wednesday', hebrew='רפאל', meaning='“God heals”',
        companions=['Miel', 'Seraphiel'], heaven='Raquie', heaven_no='second', air_king='Mediat (or Modiat)',
        air_ministers=['Suquinos', 'Sallales'], wind='Southwest', perfume='mastick',
        quarters={'East': ['Mathlai', 'Tarmiel', 'Baraborat'],
                  'West': ['Jeresous', 'Mitraton'],
                  'North': ['Thiel', 'Rael', 'Jariahel', 'Venahel', 'Velel', 'Abuiori', 'Ucirnuel'],
                  'South': ['Milliel', 'Nelapa', 'Babel', 'Caluel', 'Vel', 'Laquel']},
        agrippa='Agrippa’s scale swaps him with Michael: Raphael for the Sun, Michael for Mercury.',
        paulina='In the second part of the Ars Paulina, Raphael is the “sovereign prince” of the spirits of the airy signs, to be observed “towards the east” on Wednesday, with two princes under him, Miel and Seraphiel, the same two companions the Heptameron gives him.',
        essay=[
            'Raphael is the healer. In the Book of Tobit he travels in disguise with young Tobias, binds a demon and cures his father’s blindness, then reveals himself: “I am Raphael, one of the seven holy angels” (Tobit 12:15). The Book of Enoch lists him among the archangels and has him bind the fallen Azazel (1 Enoch 10).',
            'The Heptameron makes him the angel of Wednesday and Mercury, ruling with Miel and Seraphiel. The spirits of the air are under King Mediat, or Modiat, and his ministers Suquinos and Sallales, subject to the Southwest wind; his heaven is Raquie, the second. The perfume of the day is mastick.',
        ]),
    'Jupiter': dict(
        angel='Sachiel', slug='sachiel', day='Thursday', hebrew='צדקיאל', hebrew_label='Zadkiel', meaning='other copies spell him Sadkiel or Satquiel; Agrippa’s Zadkiel means “righteousness of God”',
        companions=['Castiel', 'Asasiel'], heaven='Zebul', heaven_no='sixth', air_king='Suth',
        air_ministers=['Maguth', 'Gutrix'], wind='South', perfume='saffron', quarters=None,
        agrippa='Agrippa names Jupiter’s angel Zadkiel (צדקיאל). Peterson notes that other manuscripts of the Heptameron read Sadkiel and Satquiel, which is why Sachiel and Zadkiel are so often treated as one angel.',
        paulina='In the second part of the Ars Paulina, Sachiel is one of the three princes under Uriel, who governs the spirits of the earthy signs towards the West.',
        essay=[
            'Sachiel is a grimoire angel: he is not in the Bible, and his name has come down in several spellings. The printed Heptameron reads Sachiel; Peterson records the forms Sadkiel and Satquiel in other manuscripts. Agrippa’s table of seven gives Jupiter to Zadkiel, and the two are now usually treated as one angel of Jupiter, the planet of kingship, law and abundance.',
            'The Heptameron makes him the angel of Thursday, ruling with Castiel and Asasiel. The spirits of the air are under King Suth and his ministers Maguth and Gutrix, subject to the South wind; his heaven is Zebul, the sixth. For the four quarters on Thursday the book gives prayers instead of angels, because “there are no Angels ruling the Air, above the fifth heaven.” The perfume of the day is saffron.',
        ]),
    'Venus': dict(
        angel='Anael', slug='anael', day='Friday', hebrew='האניאל', hebrew_label='Haniel', meaning='Agrippa gives the form Haniel',
        companions=['Rachiel', 'Sachiel'], heaven='Sagun', heaven_no='third', air_king='Sarabotres',
        air_ministers=['Amabiel', 'Aba', 'Abalidoth', 'Flaef'], wind='West', perfume='pepperwort',
        quarters={'East': ['Setchiel', 'Chedisutaniel', 'Corat', 'Tamael', 'Tenaciel'],
                  'West': ['Turiel', 'Coniel', 'Rabiel', 'Kadie', 'Maltiel', 'Huphaltiel'],
                  'North': ['Peniel', 'Pemael', 'Penat', 'Raphael', 'Raniel', 'Doremiel'],
                  'South': ['Porna', 'Sachiel', 'Chermiel', 'Samael', 'Santaniel', 'Famiel']},
        agrippa='Agrippa names Venus’s angel Haniel (האניאל).',
        paulina='In the Ars Paulina, Anael rules the second hour of every day, the hour called Cevorym, with 70 chief dukes in the other manuscripts (20 in Sloane 3825) and 100 lesser dukes.',
        essay=[
            'Anael is the angel of Venus, of love, beauty and friendship in the old correspondences. Like Sachiel he is a figure of the magical literature rather than the Bible; Agrippa gives the form Haniel. He is one of the few angels who appears in both the Heptameron and the Ars Paulina, ruling a day in one and an hour in the other.',
            'The Heptameron makes him the angel of Friday, ruling with Rachiel and Sachiel. The spirits of the air are under King Sarabotres and his ministers Amabiel, Aba, Abalidoth and Flaef, subject to the West wind; his heaven is Sagun, the third. The perfume of the day is pepperwort.',
        ]),
    'Saturn': dict(
        angel='Cassiel', slug='cassiel', day='Saturday', hebrew='צפקיאל', hebrew_label='Zaphkiel', meaning='a marginal note adds “or Caphriel”',
        companions=['Machatan', 'Uriel'], heaven=None, heaven_no=None, air_king='Maymon',
        air_ministers=['Abumalith', 'Assaibi', 'Balidet'], wind='Southwest', perfume='sulphur', quarters=None,
        agrippa='Agrippa gives Saturn to Zaphkiel (צפקיאל).',
        paulina='In the second part of the Ars Paulina, Cassiel is one of the three princes under Uriel, governing the spirits of the earthy signs towards the West, observed on Saturday.',
        essay=[
            'Cassiel is the angel of Saturn, the slowest and most distant of the seven, the planet of time, limits and solitude. A marginal note in the printed text adds “or Caphriel”, and other manuscripts read Caphael, Cafriel or Capciel.',
            'The Heptameron makes him the angel of Saturday, ruling with Machatan and Uriel. The spirits of the air are under King Maymon and his ministers Abumalith, Assaibi and Balidet, subject to the Southwest wind. No heaven is named for Saturday, and for the four quarters the book refers back to the prayers of Thursday. The perfume of the day is sulphur.',
        ]),
}

# ------------------------------------------------------------------ the 24 angels of the hours (Ars Paulina)
# (period, hour no., hour name, angel, retinue as the manuscript gives it, named dukes, note)
PAULINA = [
    ('day', 1, 'Barim', 'Samael', 'many dukes and servants; 8 chief dukes named, with 444 servants apiece',
     ['Ameniel', 'Charpon', 'Darosiel', 'Monasiel', 'Brumiel', 'Nestoriel', 'Chremas', 'Meresyn'],
     'Sloane 3825 spells him “Samuel”, corrected to Samael. The name of the hour is not given in the manuscript; “Barim” is supplied from Wolfgang Heidel.'),
    ('day', 2, 'Cevorym', 'Anael', '20 [70] chief dukes and 100 lesser dukes; 9 named, with 330 servants apiece',
     ['Menarchos', 'Archiel', 'Chardiel', 'Orphiel', 'Cursiel', 'Elmoym', 'Quosiel', 'Ermaziel', 'Granyel'], None),
    ('day', 3, 'Dansor', 'Vequaniel', '20 chief dukes and 200 lesser dukes; 12 named, with 1,760 servants',
     ['Asmiel', 'Persiel', 'Mursiel', 'Zoesiel', 'Drelmech', 'Sadiniel', 'Parniel', 'Comadiel', 'Gemary', 'Xantiel', 'Serviel', 'Furiel'], None),
    ('day', 4, 'Elechym', 'Vathmiel', '10 chief dukes and 100 lesser dukes; 15 named, with 1,550 servants',
     ['Armmyel', 'Larmich', 'Marfiel', 'Ormyel', 'Zardiel', 'Emarfiel', 'Permiel', 'Queriel', 'Strubiel', 'Diviel', 'Jermiel', 'Thuros', 'Vanesiel', 'Zasviel', 'Hermiel'], None),
    ('day', 5, 'Fealech', 'Sasquiel', '10 chief dukes and 100 lesser dukes; 15 named, with 5,550 servants',
     ['Damiel', 'Araniel', 'Maroch', 'Saraphiel', 'Putisiel', 'Jameriel', 'Futiniel', 'Rameriel', 'Amisiel', 'Uraniel', 'Omerach', 'Lameros', 'Zachiel', 'Fustiel', 'Camiel'], None),
    ('day', 6, 'Genapherim', 'Saniel', '10 chief dukes and 100 lesser dukes; 15 named, with 5,550 servants',
     ['Arnebiel', 'Charuch', 'Medusiel', 'Nathmiel', 'Pemiel', 'Gamyel', 'Jenotriel', 'Sameon', 'Trasiel', 'Xamyon', 'Nedabor', 'Permon', 'Brasiel', 'Camosiel', 'Evadar'], None),
    ('day', 7, 'Hamarym', 'Barquiel', '10 chief dukes and 100 lesser dukes; 15 named, with 600 servants',
     ['Abrasiel', 'Farmos', 'Nestorii', 'Manuel', 'Sagiel', 'Harmiel', 'Nastrus', 'Varmay', 'Tulmas', 'Crosiel', 'Pasriel', 'Venesiel', 'Evarym', 'Drufiel', 'Kathos'], None),
    ('day', 8, 'Jafanym', 'Osmadiel', '100 [10] chief dukes and 100 lesser dukes; 15 named, with 1,100 servants',
     ['Sarfiel', 'Amalym', 'Chroel', 'Mesial', 'Lantrhots', 'Demarot', 'Janofiel', 'Larfuty', 'Vemael', 'Thribiel', 'Mariel', 'Remasyn', 'Theoriel', 'Framion', 'Ermiel'], None),
    ('day', 9, 'Karron', 'Quabriel', '10 greater and 100 lesser dukes, who have 192,980 servants in 10 orders; 15 named',
     ['Astroniel', 'Charmy', 'Pamory', 'Damyel', 'Nadriel', 'Kranos', 'Menas', 'Brasiel', 'Nefarym', 'Zoymiel', 'Trubas', 'Xermiel', 'Lameson', 'Zasnor', 'Janediel'], None),
    ('day', 10, 'Lamarhon', 'Oriel', 'dukes and servants in 10 orders, 5,600 spirits in all; 15 named, with 1,100 servants',
     ['Armosy', 'Drabiel', 'Penaly', 'Mesriel', 'Choreb', 'Lemur', 'Ormas', 'Charny', 'Zazyor', 'Naveron', 'Xantros', 'Basilon', 'Nameron', 'Kranoti', 'Alfrael'], None),
    ('day', 11, 'Maneloym', 'Bariel', 'dukes and servants in 10 parts, 5,600 in all; 15 named, with 1,100 servants',
     ['Almarizel', 'Prasiniel', 'Chadros', 'Turmiel', 'Lamiel', 'Menafiel', 'Demasor', 'Omary', 'Helmas', 'Zemoel', 'Almas', 'Perman', 'Comial', 'Temas', 'Lanifiel'], None),
    ('day', 12, 'Nahalon', 'Beratiel', 'dukes and servants in 12 degrees, 3,700 spirits in all; 15 named, with 1,100 servants',
     ['Camaron', 'Astrofiel', 'Penatiel', 'Demarac', 'Famaras', 'Plamiel', 'Nerostiel', 'Emarson', 'Quirix', 'Sameron', 'Edriel', 'Choriel', 'Romiel', 'Fenosiel', 'Harmary'], None),
    ('night', 1, 'Omalharien', 'Sabrathan', '1,540 dukes and servants in 10 orders; 15 named, with 2,000 servants',
     ['Domaras', 'Amerany', 'Penoles', 'Mardiel', 'Nastul', 'Ramesiel', 'Omedriel', 'Franedac', 'Chrasiel', 'Dormason', 'Hayzoym', 'Emalon', 'Turtiel', 'Quenol', 'Rymaliel'], None),
    ('night', 2, 'Panezur', 'Tartys', '101,550 in 12 degrees; 18 named, with 1,320 servants',
     ['Almodar', 'Famoriel', 'Nedroz', 'Ormezyn', 'Chabriz', 'Praxiel', 'Permaz', 'Vameroz', 'Emaryel', 'Fromezyn', 'Ramaziel', 'Granozyn', 'Gabrinoz', 'Mercoph', 'Tameriel', 'Venomiel', 'Jenaziel', 'Xemyzin'], None),
    ('night', 3, 'Quabrion', 'Serquanich', '101,550 dukes and servants in 12 degrees; 18 named, with 1,320 servants',
     ['Menarym', 'Chrusiel', 'Penargos', 'Amriel', 'Demanoz', 'Nestoroz', 'Evanuel', 'Sarmozyn', 'Haylon', 'Quabriel', 'Thurmytz', 'Fronyzon', 'Vanosyr', 'Lemaron', 'Almonoyz', 'Janothyel', 'Melrotz', 'Xanthyozod'], None),
    ('night', 4, 'Ramersy', 'Jefischa', '101,550 dukes and servants in 12 orders; 18 named, with 7,260 servants',
     ['Armosiel', 'Nedruan', 'Maneyloz', 'Ormael', 'Phorsiel', 'Rimezyn', 'Rayziel', 'Gemezin', 'Fremiel', 'Hamayz', 'Japuriel', 'Jasphiel', 'Lamediel', 'Adroziel', 'Zodiel', 'Bramiel', 'Coreziel', 'Enatriel'], None),
    ('night', 5, 'Sanayfar', 'Abasdarhon', '101,550 dukes and servants in 12 degrees; 24 named, with 3,200 servants',
     ['Meniel', 'Charaby', 'Appiniel', 'Deinatz', 'Nechorym', 'Hameriel', 'Vulcaniel', 'Samelon', 'Gemary', 'Vanescor', 'Samerym', 'Xantropy', 'Herphatz', 'Chrymas', 'Patrozyn', 'Nameton', 'Barmas', 'Platiel', 'Neszomy', 'Quesdor', 'Caremaz', 'Umariel', 'Kralym', 'Habalon'], None),
    ('night', 6, 'Thaazaron', 'Zaazenach', '101,550 dukes and servants in 12 orders; 18 named, with 2,400 servants',
     ['Amonazy', 'Menoriel', 'Prenostix', 'Namedor', 'Cherasiel', 'Dramaz', 'Tuberiel', 'Humaziel', 'Lanoziel', 'Lamerotzod', 'Xerphiel', 'Zeziel', 'Pammon', 'Dracon', 'Gematzod', 'Enariel', 'Rudefor', 'Sarmon'], None),
    ('night', 7, 'Venaydor', 'Mendrion', '101,550 dukes and servants in 12 orders; 18 named, with 1,860 servants',
     ['Ammiel', 'Choriel', 'Genarytz', 'Pandroz', 'Menesiel', 'Sameriel', 'Ventariel', 'Zachariel', 'Dubraz', 'Marchiel', 'Jonadriel', 'Pemoniel', 'Rayziel', 'Tarmytz', 'Anapion', 'Jmonyel', 'Framoth', 'Machmag'], None),
    ('night', 8, 'Xymalim', 'Narcoriel', '101,550 dukes and servient spirits in 12 degrees; 18 named, with 30,200 [36,200] servants',
     ['Cambiel', 'Nedarym', 'Astrocon', 'Marifiel', 'Dramozyn', 'Lustifion', 'Amelson', 'Lemozar', 'Xernifiel', 'Kanorsiel', 'Bufanotz', 'Jamedroz', 'Xanoriz', 'Jastrion', 'Themaz', 'Hobraiym', 'Zymeloz', 'Gamsiel'], None),
    ('night', 9, 'Zeschar', 'Pamyel', '101,550 dukes and servants in 12 parts; 18 chief dukes named, with 1,320 servants',
     ['Demaor', 'Nameal', 'Adrapan', 'Chermel', 'Fenadros', 'Vemasiel', 'Comary', 'Matiel', 'Zenoroz', 'Brandiel', 'Evandiel', 'Tameriel', 'Befranzy', 'Jachoroz', 'Xanthir', 'Armapy', 'Druchas', 'Sardiel'], None),
    ('night', 10, 'Malcho', 'Iassuarim', '100 chief dukes and 100 lesser dukes; 6 named, with 1,620 servants',
     ['Lapheriel', 'Emarziel', 'Nameroyz', 'Chameray', 'Hazaniel', 'Uraniel'], None),
    ('night', 11, 'Aalacho', 'Dardariel', 'many servants and dukes; 21 named, with 420 servants',
     ['Cardiel', 'Permon', 'Armiel', 'Nastoriel', 'Casmiroz', 'Dameriel', 'Furamiel', 'Mafriel', 'Hariaz', 'Damar', 'Alachuc', 'Emeriel', 'Naveroz', 'Alaphar', 'Nermas', 'Druchas', 'Carman', 'Elamyz', 'Jatroziel', 'Lamersy', 'Hamarytzod'],
     'Of his dukes the manuscript says: “They are all good and obey gods lawes.”'),
    ('night', 12, 'Xephan', 'Sarandiel', 'many dukes and servants; 21 named (“cheefe and good Dukes”), with 420 servants',
     ['Adoniel', 'Damasiel', 'Ambriel', 'Meriel', 'Denaryz', 'Emarion', 'Kabriel', 'Marachy', 'Chabrion', 'Nestoriel', 'Zachriel', 'Naveriel', 'Damery', 'Namael', 'Hardiel', 'Nefrias', 'Irmanotzod', 'Gerthiel', 'Dromiel', 'Ladrotzod', 'Melanas'], None),
]

PAULINA_RULE = ('The Nature of these 24 Angells of the day and night changeth every day: and their offices is to doe all things '
                'that are attributed to the 7 planetts. But that changeth every day also.')
