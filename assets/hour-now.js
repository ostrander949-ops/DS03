/* Planetary Hour Now. Everything is computed in the browser; no location or other data is sent anywhere.
   Sunrise/sunset: simplified NOAA sunrise equation (upper limb, standard refraction -0.833 deg).
   Moon phase: mean synodic month from the new moon of 2000-01-06 18:14 UTC (approximate, within about half a day). */
(function () {
  'use strict';
  var root = document.getElementById('hn');
  if (!root) return;

  // ---------------------------------------------------------------- data
  var ORDER = ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon']; // Chaldean order
  var DAY_RULER = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']; // Sunday..Saturday
  var P = {
    Saturn:  { g: '♄', angel: 'Cassiel', day: 'Saturday',  latin: 'dies Saturni',  metal: 'lead',        word: 'Saturday keeps Saturn’s name.', app: 'cassiel', appName: 'Cassiel: Angel of Saturn', hue: '#9aa4b8' },
    Jupiter: { g: '♃', angel: 'Sachiel', day: 'Thursday',  latin: 'dies Iovis',    metal: 'tin',         word: 'Thursday is Thor’s day, the Germanic stand-in for Jupiter; French keeps jeudi.', app: 'sachiel', appName: 'Sachiel/Zadkiel: Jupiter Angel', hue: '#b9a3ff' },
    Mars:    { g: '♂', angel: 'Samael',  day: 'Tuesday',   latin: 'dies Martis',   metal: 'iron',        word: 'Tuesday is Tiw’s day, the Germanic god matched with Mars; French keeps mardi.', app: 'samael', appName: 'Samael: Archangel of Mars', hue: '#e0805a' },
    Sun:     { g: '☉', angel: 'Michael', day: 'Sunday',    latin: 'dies Solis',    metal: 'gold',        word: 'Sunday keeps the Sun’s name.', app: 'michael', appName: 'Michael: Archangel of the Sun', hue: '#f0d79a' },
    Venus:   { g: '♀', angel: 'Anael',   day: 'Friday',    latin: 'dies Veneris',  metal: 'copper',      word: 'Friday is Frigg’s day, the Germanic goddess matched with Venus; French keeps vendredi.', app: 'anael', appName: 'Anael: Angel of Venus', hue: '#8fd6b0' },
    Mercury: { g: '☿', angel: 'Raphael', day: 'Wednesday', latin: 'dies Mercurii', metal: 'quicksilver', word: 'Wednesday is Woden’s day, the Germanic god matched with Mercury; French keeps mercredi.', app: 'raphael', appName: 'Raphael: Angel of Mercury', hue: '#9fd0f0' },
    Moon:    { g: '☽', angel: 'Gabriel', day: 'Monday',    latin: 'dies Lunae',    metal: 'silver',      word: 'Monday keeps the Moon’s name.', app: 'gabriel', appName: 'Gabriel: Angel of the Moon', hue: '#dfe3ee' }
  };
  var CITIES = [
    ['Auckland', -36.85, 174.76, 'Pacific/Auckland'], ['Athens', 37.98, 23.73, 'Europe/Athens'],
    ['Baghdad', 33.31, 44.36, 'Asia/Baghdad'], ['Bangkok', 13.76, 100.5, 'Asia/Bangkok'],
    ['Berlin', 52.52, 13.4, 'Europe/Berlin'], ['Buenos Aires', -34.6, -58.38, 'America/Argentina/Buenos_Aires'],
    ['Cairo', 30.04, 31.24, 'Africa/Cairo'], ['Chicago', 41.88, -87.63, 'America/Chicago'],
    ['Delhi', 28.61, 77.21, 'Asia/Kolkata'], ['Denver', 39.74, -104.99, 'America/Denver'],
    ['Dubai', 25.2, 55.27, 'Asia/Dubai'], ['Dublin', 53.35, -6.26, 'Europe/Dublin'],
    ['Hong Kong', 22.32, 114.17, 'Asia/Hong_Kong'], ['Honolulu', 21.31, -157.86, 'Pacific/Honolulu'],
    ['Istanbul', 41.01, 28.98, 'Europe/Istanbul'], ['Jerusalem', 31.78, 35.22, 'Asia/Jerusalem'],
    ['Johannesburg', -26.2, 28.05, 'Africa/Johannesburg'], ['Lagos', 6.52, 3.38, 'Africa/Lagos'],
    ['London', 51.51, -0.13, 'Europe/London'], ['Los Angeles', 34.05, -118.24, 'America/Los_Angeles'],
    ['Madrid', 40.42, -3.7, 'Europe/Madrid'], ['Manila', 14.6, 120.98, 'Asia/Manila'],
    ['Melbourne', -37.81, 144.96, 'Australia/Melbourne'], ['Mexico City', 19.43, -99.13, 'America/Mexico_City'],
    ['Moscow', 55.76, 37.62, 'Europe/Moscow'], ['Mumbai', 19.08, 72.88, 'Asia/Kolkata'],
    ['New York', 40.71, -74.01, 'America/New_York'], ['Paris', 48.86, 2.35, 'Europe/Paris'],
    ['Phoenix', 33.45, -112.07, 'America/Phoenix'], ['Rome', 41.9, 12.5, 'Europe/Rome'],
    ['São Paulo', -23.55, -46.63, 'America/Sao_Paulo'], ['Seoul', 37.57, 126.98, 'Asia/Seoul'],
    ['Singapore', 1.35, 103.82, 'Asia/Singapore'], ['Sydney', -33.87, 151.21, 'Australia/Sydney'],
    ['Tokyo', 35.68, 139.69, 'Asia/Tokyo'], ['Toronto', 43.65, -79.38, 'America/Toronto'],
    ['Vancouver', 49.28, -123.12, 'America/Vancouver'],
    ['Amsterdam', 52.37, 4.9, 'Europe/Amsterdam'], ['Anchorage', 61.22, -149.9, 'America/Anchorage'],
    ['Beijing', 39.9, 116.41, 'Asia/Shanghai'], ['Bogotá', 4.71, -74.07, 'America/Bogota'],
    ['Brisbane', -27.47, 153.03, 'Australia/Brisbane'], ['Brussels', 50.85, 4.35, 'Europe/Brussels'],
    ['Dhaka', 23.81, 90.41, 'Asia/Dhaka'], ['Edmonton', 53.55, -113.49, 'America/Edmonton'],
    ['Halifax', 44.65, -63.57, 'America/Halifax'], ['Helsinki', 60.17, 24.94, 'Europe/Helsinki'],
    ['Jakarta', -6.21, 106.85, 'Asia/Jakarta'], ['Karachi', 24.86, 67.01, 'Asia/Karachi'],
    ['Lima', -12.05, -77.04, 'America/Lima'], ['Lisbon', 38.72, -9.14, 'Europe/Lisbon'],
    ['Nairobi', -1.29, 36.82, 'Africa/Nairobi'], ['Oslo', 59.91, 10.75, 'Europe/Oslo'],
    ['Perth', -31.95, 115.86, 'Australia/Perth'], ['Santiago', -33.45, -70.67, 'America/Santiago'],
    ['Stockholm', 59.33, 18.07, 'Europe/Stockholm'], ['Taipei', 25.03, 121.57, 'Asia/Taipei'],
    ['Tehran', 35.69, 51.39, 'Asia/Tehran'], ['Vienna', 48.21, 16.37, 'Europe/Vienna'],
    ['Warsaw', 52.23, 21.01, 'Europe/Warsaw'], ['Zurich', 47.37, 8.54, 'Europe/Zurich']
  ].sort(function (a, b) { return a[0].localeCompare(b[0]); });
  var DEVICE_TZ = (function () { try { return Intl.DateTimeFormat().resolvedOptions().timeZone; } catch (e) { return 'UTC'; } })();
  var $ = function (id) { return document.getElementById(id); };
  var store = {
    get: function (k) { try { return JSON.parse(localStorage.getItem('ds-hn-' + k)); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem('ds-hn-' + k, JSON.stringify(v)); } catch (e) { /* storage unavailable */ } }
  };

  // ---------------------------------------------------------------- astronomy
  function sun(y, m, d, lat, lon) {
    var rad = Math.PI / 180;
    var n = Math.round((Date.UTC(y, m - 1, d, 12) - Date.UTC(2000, 0, 1, 12)) / 864e5);
    var J = n - lon / 360;
    var M = (357.5291 + 0.98560028 * J) % 360;
    var C = 1.9148 * Math.sin(M * rad) + 0.02 * Math.sin(2 * M * rad) + 0.0003 * Math.sin(3 * M * rad);
    var L = (M + C + 180 + 102.9372) % 360;
    var Jt = 2451545 + J + 0.0053 * Math.sin(M * rad) - 0.0069 * Math.sin(2 * L * rad);
    var sd = Math.sin(L * rad) * Math.sin(23.4397 * rad), cd = Math.cos(Math.asin(sd));
    var cw = (Math.sin(-0.833 * rad) - Math.sin(lat * rad) * sd) / (Math.cos(lat * rad) * cd);
    if (cw < -1 || cw > 1) return null;
    var w = Math.acos(cw) / rad / 360;
    var toDate = function (j) { return new Date((j - 2440587.5) * 864e5); };
    return { rise: toDate(Jt - w), set: toDate(Jt + w) };
  }
  var SYNODIC = 29.530588853, NEW_MOON_2000 = Date.UTC(2000, 0, 6, 18, 14);
  function moon(t) {
    var age = ((t - NEW_MOON_2000) / 864e5) % SYNODIC;
    if (age < 0) age += SYNODIC;
    var f = age / SYNODIC, k = Math.cos(2 * Math.PI * f);
    var names = ['New Moon', 'Waxing Crescent', 'First Quarter', 'Waxing Gibbous', 'Full Moon', 'Waning Gibbous', 'Last Quarter', 'Waning Crescent'];
    return { age: age, f: f, k: k, lit: (1 - k) / 2, name: names[Math.floor(f * 8 + 0.5) % 8] };
  }

  // ---------------------------------------------------------------- time helpers
  function ymdIn(t, tz) {
    var p = new Intl.DateTimeFormat('en-CA', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(t);
    var o = {}; p.forEach(function (x) { o[x.type] = +x.value; });
    return [o.year, o.month, o.day];
  }
  function addDays(ymd, n) { var d = new Date(Date.UTC(ymd[0], ymd[1] - 1, ymd[2] + n)); return [d.getUTCFullYear(), d.getUTCMonth() + 1, d.getUTCDate()]; }
  function weekday(ymd) { return new Date(Date.UTC(ymd[0], ymd[1] - 1, ymd[2])).getUTCDay(); }
  var fmtCache = {};
  function fmt(t, tz, opts) {
    var key = tz + JSON.stringify(opts);
    if (!fmtCache[key]) fmtCache[key] = new Intl.DateTimeFormat(undefined, Object.assign({ timeZone: tz }, opts));
    return fmtCache[key].format(t);
  }
  function hm(t, tz) { return fmt(t, tz, { hour: 'numeric', minute: '2-digit' }); }
  function dur(ms) {
    var s = Math.max(0, Math.round(ms / 1000)), h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), sec = s % 60;
    return h ? h + 'h ' + m + 'm' : m + 'm ' + (sec < 10 ? '0' : '') + sec + 's';
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  // ---------------------------------------------------------------- planetary days
  function planetaryDays(loc, now) {
    var today = ymdIn(now, loc.tz), days = [], suns = [];
    for (var i = -1; i <= 2; i++) { var ymd = addDays(today, i); suns.push({ ymd: ymd, s: sun(ymd[0], ymd[1], ymd[2], loc.lat, loc.lon) }); }
    for (var j = 0; j < 3; j++) {
      var a = suns[j], b = suns[j + 1];
      if (!a.s || !b.s) continue;
      var ruler = DAY_RULER[weekday(a.ymd)], first = ORDER.indexOf(ruler);
      var dl = (a.s.set - a.s.rise) / 12, nl = (b.s.rise - a.s.set) / 12, hours = [];
      for (var h = 0; h < 24; h++) {
        var st = h < 12 ? +a.s.rise + h * dl : +a.s.set + (h - 12) * nl;
        hours.push({ i: h, start: new Date(st), end: new Date(st + (h < 12 ? dl : nl)), planet: ORDER[(first + h) % 7], night: h >= 12 });
      }
      days.push({ ymd: a.ymd, ruler: ruler, rise: a.s.rise, set: a.s.set, next: b.s.rise, hours: hours });
    }
    return days;
  }

  // ---------------------------------------------------------------- rendering
  function sector(r0, r1, a0, a1) {
    var p = function (r, a) { return (r * Math.cos(a)).toFixed(2) + ' ' + (r * Math.sin(a)).toFixed(2); };
    var large = a1 - a0 > Math.PI ? 1 : 0;
    return 'M' + p(r1, a0) + 'A' + r1 + ' ' + r1 + ' 0 ' + large + ' 1 ' + p(r1, a1) + 'L' + p(r0, a1) + 'A' + r0 + ' ' + r0 + ' 0 ' + large + ' 0 ' + p(r0, a0) + 'Z';
  }
  function wheel(day, cur, now, tz) {
    var span = day.next - day.rise, ang = function (t) { return Math.PI + 2 * Math.PI * (t - day.rise) / span; };
    var out = '<svg viewBox="-150 -150 300 300" role="img" aria-label="Planetary clock: the 24 unequal planetary hours from sunrise to the next sunrise, with the current hour highlighted">';
    out += '<circle r="142" fill="none" stroke="var(--line2)"/>';
    day.hours.forEach(function (h) {
      var a0 = ang(h.start) + 0.004, a1 = ang(h.end) - 0.004, isCur = h === cur, mid = (a0 + a1) / 2;
      out += '<path d="' + sector(84, 134, a0, a1) + '" fill="' + (isCur ? 'rgba(212,174,98,.85)' : h.night ? 'rgba(16,26,44,.95)' : 'rgba(38,50,78,.9)') + '" stroke="' + (isCur ? '#f0d79a' : 'rgba(42,56,88,.9)') + '"><title>' + esc((h.night ? 'Night ' + (h.i - 11) : 'Day ' + (h.i + 1)) + ': ' + h.planet + ', ' + hm(h.start, tz) + '–' + hm(h.end, tz)) + '</title></path>';
      out += '<text x="' + (109 * Math.cos(mid)).toFixed(1) + '" y="' + (109 * Math.sin(mid)).toFixed(1) + '" text-anchor="middle" dominant-baseline="central" font-size="13" fill="' + (isCur ? '#1a1408' : P[h.planet].hue) + '" opacity="' + (isCur ? 1 : 0.85) + '">' + P[h.planet].g + '</text>';
    });
    [[day.rise, 'sunrise'], [day.set, 'sunset']].forEach(function (m) {
      var a = ang(m[0]);
      out += '<line x1="' + (80 * Math.cos(a)).toFixed(1) + '" y1="' + (80 * Math.sin(a)).toFixed(1) + '" x2="' + (146 * Math.cos(a)).toFixed(1) + '" y2="' + (146 * Math.sin(a)).toFixed(1) + '" stroke="#f0d79a" stroke-width="1.4"/>';
    });
    var an = ang(now);
    out += '<g id="hn-needle" style="transform:rotate(' + (an * 180 / Math.PI).toFixed(3) + 'deg)"><line x1="0" y1="0" x2="140" y2="0" stroke="#f0d79a" stroke-width="2"/><circle cx="140" cy="0" r="4" fill="#f0d79a"/></g><circle r="5" fill="#f0d79a"/>';
    out += '<text x="0" y="-38" text-anchor="middle" font-family="var(--mono)" font-size="8" letter-spacing="2" fill="var(--muted)">DAY</text><text x="0" y="46" text-anchor="middle" font-family="var(--mono)" font-size="8" letter-spacing="2" fill="var(--muted)">NIGHT</text>';
    return out + '</svg>';
  }
  function moonSvg(m, south) {
    var r = 40, rx = (r * Math.abs(m.k)).toFixed(2), waxing = m.f < 0.5, d;
    if (waxing) d = 'M0 -' + r + 'A' + r + ' ' + r + ' 0 0 1 0 ' + r + 'A' + rx + ' ' + r + ' 0 0 ' + (m.k > 0 ? 0 : 1) + ' 0 -' + r + 'Z';
    else d = 'M0 -' + r + 'A' + r + ' ' + r + ' 0 0 0 0 ' + r + 'A' + rx + ' ' + r + ' 0 0 ' + (m.k > 0 ? 1 : 0) + ' 0 -' + r + 'Z';
    return '<svg viewBox="-50 -50 100 100" role="img" aria-label="' + esc(m.name + ', about ' + Math.round(m.lit * 100) + '% lit') + '"><circle r="' + r + '" fill="#1b2438"/><path d="' + d + '" fill="#ece5d3"' + (south ? ' transform="scale(-1 1)"' : '') + '/><circle r="' + r + '" fill="none" stroke="rgba(236,229,211,.25)"/></svg>';
  }

  // ---------------------------------------------------------------- state & UI
  var loc = store.get('loc'), state = {}, chime = !!store.get('chime'), audio = null, baseTitle = document.title;
  function offsetMin(tz, t) {
    try {
      var p = new Intl.DateTimeFormat('en-US', { timeZone: tz, hourCycle: 'h23', year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric' }).formatToParts(t), o = {};
      p.forEach(function (x) { o[x.type] = +x.value; });
      return Math.round((Date.UTC(o.year, o.month - 1, o.day, o.hour, o.minute) - Math.floor(t / 6e4) * 6e4) / 6e4);
    } catch (e) { return 0; }
  }
  function defaultLoc() {
    var exact = CITIES.filter(function (x) { return x[3] === DEVICE_TZ; })[0], c = exact;
    if (!c) { // nearest listed city by current UTC offset
      var now = Date.now(), mine = offsetMin(DEVICE_TZ, now), best = 1e9;
      var region = DEVICE_TZ.split('/')[0];
      var south = /^(Australia|Antarctica)\/|Auckland|Fiji|Tonga|Chatham|Argentina|Sao_Paulo|Santiago|Montevideo|Asuncion|La_Paz|Lima|Johannesburg|Maputo|Harare|Lusaka|Windhoek|Gaborone|Antananarivo|Mauritius|Reunion|Noumea|Port_Moresby/.test(DEVICE_TZ);
      CITIES.forEach(function (x) {
        // closest offset first; on ties prefer the same region, then the likely hemisphere
        var dlt = Math.abs(offsetMin(x[3], now) - mine) * 4 + (x[3].split('/')[0] === region ? 0 : 2) + ((x[1] < 0) === south ? 0 : 1) + Math.abs(Math.abs(x[1]) - (south ? 32 : 42)) / 100;
        if (dlt < best) { best = dlt; c = x; }
      });
    }
    return { name: c[0], lat: c[1], lon: c[2], tz: c[3], guessed: !exact };
  }
  if (!loc || typeof loc.lat !== 'number') loc = defaultLoc();

  function compute() {
    var now = new Date(), days = planetaryDays(loc, now), day = null, cur = null;
    days.forEach(function (d) { if (now >= d.rise && now < d.next) day = d; });
    if (day) day.hours.forEach(function (h) { if (now >= h.start && now < h.end) cur = h; });
    state = { now: now, days: days, day: day, cur: cur };
  }

  function render() {
    compute();
    var tz = loc.tz, d = state.day, h = state.cur;
    $('hn-place').textContent = loc.name + (loc.guessed ? ' (nearest to your time zone; choose your city below)' : '');
    if (!d || !h) {
      $('hn-main').innerHTML = '<p class="lede">At this latitude the Sun does not both rise and set today, so there are no planetary hours to divide. Choose another place below.</p>';
      $('hn-wheel').innerHTML = ''; $('hn-next').innerHTML = ''; $('hn-sched').innerHTML = '';
      return;
    }
    var p = P[h.planet], dr = P[d.ruler];
    root.style.setProperty('--hn', p.hue);
    $('hn-main').innerHTML =
      '<div class="hn-glyph" aria-hidden="true">' + p.g + '</div>' +
      '<div><div class="eyebrow">' + (h.night ? 'Night hour ' + (h.i - 11) : 'Day hour ' + (h.i + 1)) + ' of 12 · ' + esc(dr.day) + ', the day of ' + esc(d.ruler === 'Sun' || d.ruler === 'Moon' ? 'the ' + d.ruler : d.ruler) + '</div>' +
      '<h2 class="hn-title">The hour of <em>' + esc(h.planet === 'Sun' || h.planet === 'Moon' ? 'the ' + h.planet : h.planet) + '</em></h2>' +
      '<p class="hn-angel">Angel of ' + esc(h.planet === 'Sun' || h.planet === 'Moon' ? 'the ' + h.planet : h.planet) + ' in the Heptameron: <b>' + esc(p.angel) + '</b> · traditional metal: ' + esc(p.metal) + '</p>' +
      '<div class="hn-count"><svg viewBox="0 0 44 44" aria-hidden="true"><circle cx="22" cy="22" r="19" fill="none" stroke="var(--line2)" stroke-width="3"/><circle id="hn-ring" cx="22" cy="22" r="19" fill="none" stroke="var(--hn)" stroke-width="3" stroke-linecap="round" stroke-dasharray="119.38" transform="rotate(-90 22 22)"/></svg>' +
      '<div><b id="hn-left"></b> left · ends at ' + esc(hm(h.end, tz)) + '<br><span class="muted">This hour lasts ' + Math.round((h.end - h.start) / 6e4) + ' minutes ' + (Math.abs((h.end - h.start) / 6e4 - 60) < 2 ? '(near an equinox, almost an even hour)' : (h.end - h.start) / 6e4 > 60 ? '(longer than a clock hour)' : '(shorter than a clock hour)') + '</span></div></div>' +
      '<div class="hn-app"><a class="btn gold small" href="https://play.google.com/store/apps/details?id=com.discoveryscience.' + p.app + '" rel="noopener">' + esc(p.appName) + ' · Google Play</a> <a class="btn ghost small" href="/app/angelarium.html">Every angel, every hour: Angelarium</a></div>' +
      '</div>';
    $('hn-wheel').innerHTML = wheel(d, h, state.now, tz) +
      '<p class="fine" style="text-align:center;margin:6px 0 0">Sunrise ' + esc(hm(d.rise, tz)) + ' · sunset ' + esc(hm(d.set, tz)) + ' · next sunrise ' + esc(hm(d.next, tz)) + '</p>';

    // Next hour of each planet
    var all = [], seen = {}, chips = '';
    state.days.forEach(function (x) { all = all.concat(x.hours); });
    all.forEach(function (x) { if (x.start > state.now && !seen[x.planet]) seen[x.planet] = x; });
    ORDER.slice().sort(function (p1, p2) { return (seen[p1] ? +seen[p1].start : 9e15) - (seen[p2] ? +seen[p2].start : 9e15); }).forEach(function (pl) {
      var x = seen[pl]; if (!x) return;
      var sameDay = ymdIn(x.start, tz).join() === ymdIn(state.now, tz).join();
      chips += '<li><span class="g" style="color:' + P[pl].hue + '">' + P[pl].g + '</span><b>' + pl + '</b><span>' + (sameDay ? '' : esc(fmt(x.start, tz, { weekday: 'short' })) + ' ') + esc(hm(x.start, tz)) + '</span><span class="muted">in ' + dur(x.start - state.now) + '</span></li>';
    });
    $('hn-next').innerHTML = chips;

    // Full schedule
    var rows = '';
    d.hours.forEach(function (x) {
      rows += '<tr' + (x === h ? ' class="now" aria-current="time"' : '') + '><td>' + (x.night ? 'Night ' + (x.i - 11) : 'Day ' + (x.i + 1)) + '</td><td>' + esc(hm(x.start, tz)) + '</td><td>' + esc(hm(x.end, tz)) + '</td><td class="pl"><span style="color:' + P[x.planet].hue + '">' + P[x.planet].g + '</span> ' + x.planet + '</td><td>' + P[x.planet].angel + '</td></tr>';
    });
    $('hn-sched').innerHTML = rows;

    // Day name and Moon
    $('hn-dayname').innerHTML = '<b>' + esc(dr.day) + '</b> was <i>' + esc(dr.latin) + '</i> in Latin. ' + esc(dr.word) + ' The planetary day began at sunrise, ' + esc(hm(d.rise, tz)) + ', in the first hour of ' + esc(d.ruler === 'Sun' || d.ruler === 'Moon' ? 'the ' + d.ruler : d.ruler) + '.';
    var m = moon(state.now);
    $('hn-moon').innerHTML = moonSvg(m, loc.lat < 0) + '<div><b>' + m.name + '</b><br><span class="muted">About ' + Math.round(m.lit * 100) + '% lit · day ' + Math.floor(m.age) + ' of the lunar month' + (loc.lat < 0 ? ' · drawn as seen from the southern hemisphere' : '') + '</span></div>';
    state.planetAnnounced = h.planet;
    tick();
  }

  function tick() {
    var h = state.cur, now = new Date();
    if (!h) return;
    if (now >= h.end) {
      render();
      if (chime) ring();
      $('hn-live').textContent = 'The hour has changed: it is now the hour of ' + state.cur.planet + '.';
      return;
    }
    var left = h.end - now, frac = 1 - left / (h.end - h.start);
    var el = $('hn-left'); if (el) el.textContent = dur(left);
    var ring2 = $('hn-ring'); if (ring2) ring2.setAttribute('stroke-dashoffset', (119.38 * frac).toFixed(2));
    var nd = $('hn-needle');
    if (nd && state.day) nd.style.transform = 'rotate(' + ((Math.PI + 2 * Math.PI * (now - state.day.rise) / (state.day.next - state.day.rise)) * 180 / Math.PI).toFixed(3) + 'deg)';
    if (document.visibilityState === 'hidden') document.title = P[h.planet].g + ' ' + h.planet + ' · ' + dur(left) + ' left';
  }

  function ring() {
    try {
      audio = audio || new (window.AudioContext || window.webkitAudioContext)();
      var t = audio.currentTime;
      [[528, 0.18], [792, 0.08], [1056, 0.04]].forEach(function (p) {
        var o = audio.createOscillator(), g = audio.createGain();
        o.type = 'sine'; o.frequency.value = p[0];
        g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(p[1], t + 0.02); g.gain.exponentialRampToValueAtTime(0.0001, t + 3.2);
        o.connect(g); g.connect(audio.destination); o.start(t); o.stop(t + 3.3);
      });
    } catch (e) { /* audio unavailable */ }
  }

  // ---------------------------------------------------------------- controls
  var sel = $('hn-city');
  sel.innerHTML = '<option value="">Choose a city…</option>' + CITIES.map(function (c, i) { return '<option value="' + i + '">' + esc(c[0]) + '</option>'; }).join('');
  sel.addEventListener('change', function () {
    if (sel.value === '') return;
    var c = CITIES[+sel.value];
    loc = { name: c[0], lat: c[1], lon: c[2], tz: c[3] }; store.set('loc', loc); $('hn-status').textContent = ''; render();
  });
  $('hn-geo').addEventListener('click', function () {
    var st = $('hn-status');
    if (!navigator.geolocation) { st.textContent = 'This browser cannot share a location. Choose a city instead.'; return; }
    st.textContent = 'Asking your device for its location…';
    navigator.geolocation.getCurrentPosition(function (pos) {
      loc = { name: 'Your location (' + pos.coords.latitude.toFixed(2) + '°, ' + pos.coords.longitude.toFixed(2) + '°)', lat: pos.coords.latitude, lon: pos.coords.longitude, tz: DEVICE_TZ };
      store.set('loc', loc); st.textContent = 'Calculated on this device. Your location is not sent anywhere.'; sel.value = ''; render();
    }, function () { st.textContent = 'Location was not shared. Choose a city instead.'; }, { maximumAge: 6e5, timeout: 15000 });
  });
  var cb = $('hn-chime');
  cb.checked = chime;
  cb.addEventListener('change', function () { chime = cb.checked; store.set('chime', chime); if (chime) ring(); });
  $('hn-share').addEventListener('click', function () {
    var h = state.cur, st = $('hn-status');
    var text = h ? 'It is the hour of ' + h.planet + ' ' + P[h.planet].g + ' (angel: ' + P[h.planet].angel + ') in ' + loc.name.replace(/ \(.*$/, '') + '. Find your planetary hour:' : 'Find your planetary hour:';
    var url = location.origin + location.pathname;
    if (navigator.share) { navigator.share({ title: 'Planetary Hour Now', text: text, url: url }).catch(function () {}); }
    else if (navigator.clipboard) { navigator.clipboard.writeText(text + ' ' + url).then(function () { st.textContent = 'Copied to your clipboard.'; }, function () { st.textContent = url; }); }
    else st.textContent = url;
  });
  document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'visible') document.title = baseTitle; else tick(); });

  root.classList.add('ready');
  render();
  setInterval(tick, 1000);
  window.__hn = { sun: sun, moon: moon, planetaryDays: planetaryDays, state: function () { return state; } }; // for testing
})();
