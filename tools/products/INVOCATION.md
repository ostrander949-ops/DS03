# Personal Angel Invocation: fulfilling an order

Gumroad products: `angel-invocation` ($24) and `angel-invocation-gift` ($29). Checkout asks for:
first name (as it should appear), birth date, birth time (or "unknown"), birth city and country, city they live in now,
and for the gift edition the giver's name.

For each order:

1. Look up latitude, longitude and time zone (IANA name, e.g. America/New_York) for the birth city, and for the current city if different.
2. Run:

       python3 tools/products/build_invocation.py --name "Mary" --date 1990-12-25 --time 07:30 \
         --lat 42.36 --lon -71.06 --tz America/New_York \
         [--live-lat .. --live-lon .. --live-tz ..] [--gift-from "Anne"] --out orders/

   Leave out --time if the birth time is unknown (the hour angel is then left out).
3. Send the zip (PDF book, sigil card, phone wallpaper) to the buyer from Gumroad ("Send a file" on the sale), or by email.

The calculation code is shared with the free page: tools/birth_angel.py.
