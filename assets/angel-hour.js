/* Angel of the Hour: the Ars Paulina angel of the hour, the Heptameron angels of the day and of the planet,
   the planet's place in the visitor's sky, a seal for the moment and a contemplation mode.
   Everything is computed in the browser; no location or other data leaves the device. */
(function () {
  'use strict';
  var D = window.DS_ANGELS, ART = window.DSAngelArt, EPH = window.DSEphemeris, CITIES = window.DS_CITIES || [];
  var stage = document.getElementById('ah-stage');
  if (!D || !ART || !stage) return;

  var ORDER = ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon'];
  var DAY_RULER = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'];
  var DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  var ORD = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth'];
  var ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII'];
  var POINTS = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
  var GLYPH = ART.GLYPH, HUE = ART.HUE;
  var DEVICE_TZ = (function () { try { return Intl.DateTimeFormat().resolvedOptions().timeZone; } catch (e) { return 'UTC'; } })();
  var $ = function (id) { return document.getElementById(id); };
  var store = {
    get: function (k) { try { return JSON.parse(localStorage.getItem('ds-hn-' + k)); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem('ds-hn-' + k, JSON.stringify(v)); } catch (e) { /* unavailable */ } }
  };
  function the(p) { return p === 'Sun' || p === 'Moon' ? 'the ' + p : p; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  // ------------------------------------------------------------ sun and the planetary day
  function sun(y, m, d, lat, lon) {
    var rad = Math.PI / 180, n = Math.round((Date.UTC(y, m - 1, d, 12) - Date.UTC(2000, 0, 1, 12)) / 864e5), J = n - lon / 360;
    var M = (357.5291 + 0.98560028 * J) % 360, C = 1.9148 * Math.sin(M * rad) + 0.02 * Math.sin(2 * M * rad) + 0.0003 * Math.sin(3 * M * rad);
    var L = (M + C + 180 + 102.9372) % 360, Jt = 2451545 + J + 0.0053 * Math.sin(M * rad) - 0.0069 * Math.sin(2 * L * rad);
    var sd = Math.sin(L * rad) * Math.sin(23.4397 * rad), cd = Math.cos(Math.asin(sd));
    var cw = (Math.sin(-0.833 * rad) - Math.sin(lat * rad) * sd) / (Math.cos(lat * rad) * cd);
    if (cw < -1 || cw > 1) return null;
    var w = Math.acos(cw) / rad / 360, toDate = function (j) { return new Date((j - 2440587.5) * 864e5); };
    return { rise: toDate(Jt - w), set: toDate(Jt + w) };
  }
  function ymdIn(t, tz) {
    var o = {}; new Intl.DateTimeFormat('en-CA', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(t).forEach(function (x) { o[x.type] = +x.value; });
    return [o.year, o.month, o.day];
  }
  function addDays(ymd, n) { var d = new Date(Date.UTC(ymd[0], ymd[1] - 1, ymd[2] + n)); return [d.getUTCFullYear(), d.getUTCMonth() + 1, d.getUTCDate()]; }
  function weekday(ymd) { return new Date(Date.UTC(ymd[0], ymd[1] - 1, ymd[2])).getUTCDay(); }
  var fc = {};
  function fmt(t, tz, o) { var k = tz + JSON.stringify(o); if (!fc[k]) fc[k] = new Intl.DateTimeFormat(undefined, Object.assign({ timeZone: tz }, o)); return fc[k].format(t); }
  function hm(t, tz) { return fmt(t, tz, { hour: 'numeric', minute: '2-digit' }); }
  function dur(ms) { var s = Math.max(0, Math.round(ms / 1000)), h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), x = s % 60; return h ? h + 'h ' + m + 'm' : m + 'm ' + (x < 10 ? '0' : '') + x + 's'; }

  function planetaryDays(loc, now) {
    var today = ymdIn(now, loc.tz), suns = [], days = [];
    for (var i = -1; i <= 2; i++) { var ymd = addDays(today, i); suns.push({ ymd: ymd, s: sun(ymd[0], ymd[1], ymd[2], loc.lat, loc.lon) }); }
    for (var j = 0; j < 3; j++) {
      var a = suns[j], b = suns[j + 1];
      if (!a.s || !b.s) continue;
      var wd = weekday(a.ymd), ruler = DAY_RULER[wd], first = ORDER.indexOf(ruler), dl = (a.s.set - a.s.rise) / 12, nl = (b.s.rise - a.s.set) / 12, hours = [];
      for (var h = 0; h < 24; h++) {
        var st = h < 12 ? +a.s.rise + h * dl : +a.s.set + (h - 12) * nl;
        hours.push({ i: h, start: new Date(st), end: new Date(st + (h < 12 ? dl : nl)), planet: ORDER[(first + h) % 7], ruler: ruler, wd: wd });
      }
      days.push({ ymd: a.ymd, wd: wd, ruler: ruler, rise: a.s.rise, set: a.s.set, next: b.s.rise, hours: hours });
    }
    return days;
  }

  // ------------------------------------------------------------ state
  var loc = null, S = {}, timer = null, lastHourKey = '';
  var saved = store.get('loc');

  function compute() {
    var now = new Date(), days = planetaryDays(loc, now), day = null, cur = null;
    days.forEach(function (d) { if (now >= d.rise && now < d.next) day = d; });
    if (day) day.hours.forEach(function (h) { if (now >= h.start && now < h.end) cur = h; });
    S = { now: now, days: days, day: day, cur: cur };
    if (cur) { S.pa = D.paulina[cur.i]; S.dayAngel = D.seven[day.ruler]; S.hourAngel = D.seven[cur.planet]; }
  }

  function paulinaArt(pa, planet, lite) {
    return ART.angel({ name: pa.angel, planet: planet, kind: 'pauline', period: pa.period, hour: pa.no, subtitle: pa.angel, lite: lite,
      ring: pa.angel.toUpperCase() + ' ✦ THE ' + ORD[pa.no - 1].toUpperCase() + ' HOUR OF THE ' + pa.period.toUpperCase() + ' ✦ ' + pa.hour.toUpperCase() + ' ✦ SERVING ' + the(planet).toUpperCase() + ' ✦ ',
      label: 'Devotional artwork of ' + pa.angel + ', angel of the ' + ORD[pa.no - 1] + ' hour of the ' + pa.period + ', serving ' + the(planet) });
  }
  function dayArt(planet, lite) {
    var a = D.seven[planet];
    return ART.angel({ name: a.angel, planet: planet, hebrew: a.hebrew, kind: 'day', subtitle: a.angel, lite: lite,
      ring: a.angel.toUpperCase() + ' ✦ ANGEL OF ' + the(planet).toUpperCase() + ' ✦ ' + a.day.toUpperCase() + ' ✦ ',
      label: 'Devotional artwork of ' + a.angel + ', angel of ' + the(planet) });
  }

  // ------------------------------------------------------------ rendering
  function render() {
    compute();
    var tz = loc.tz, d = S.day, h = S.cur;
    if (!d || !h) {
      $('ah-live').hidden = false;
      $('ah-title').textContent = 'No hours here today';
      $('ah-sub').textContent = 'At this latitude the Sun does not both rise and set today, so the day cannot be divided into hours. Choose another place.';
      return;
    }
    var pa = S.pa;
    document.documentElement.style.setProperty('--ah', HUE[h.planet][0]);
    $('ah-art').innerHTML = paulinaArt(pa, h.planet, false);
    $('ah-eyebrow').textContent = ROMAN[pa.no - 1] + ' · the ' + ORD[pa.no - 1] + ' hour of the ' + pa.period + ', called ' + pa.hour;
    $('ah-title').textContent = pa.angel;
    $('ah-sub').innerHTML = 'Serving <b style="color:var(--ah)">' + GLYPH[h.planet] + ' ' + the(h.planet) + '</b> this hour, on ' + DAYS[d.wd] + ', the day of ' + the(d.ruler) + ' and of ' + esc(S.dayAngel.angel) + '. In the manuscript he has ' + esc(pa.retinue) + '.';
    $('ah-read').href = '#' + pa.slug;
    document.querySelectorAll('.codex.now').forEach(function (x) { x.classList.remove('now'); });
    [pa.slug, 'angel-' + S.dayAngel.slug, 'angel-' + S.hourAngel.slug].forEach(function (sl) { var el = $(sl); if (el) el.classList.add('now'); });
    renderChain(); renderNextHour(); renderAlign(); renderSky(); renderSeal(); renderNext();
    lastHourKey = +h.start;
    tick();
  }

  function sky(planet) { return EPH ? EPH.altAz(planet, new Date(), loc.lat, loc.lon) : null; }
  function skyText(p) {
    if (!p) return '';
    var pt = POINTS[Math.round(p.az / 22.5) % 16];
    return p.alt >= 0 ? Math.round(p.alt) + '° up in the ' + pt : 'below the horizon, ' + pt;
  }

  function renderChain() {
    var h = S.cur, d = S.day, pa = S.pa, da = S.dayAngel, p = sky(h.planet);
    var you = '<svg viewBox="-50 -50 100 100" style="width:62%;height:62%"><circle r="40" fill="none" stroke="#f0d79a" stroke-opacity=".5"/><circle r="6" fill="#f0d79a"/><circle r="18" fill="none" stroke="#f0d79a" stroke-opacity=".3"/><path d="M0 -40v-6M0 40v6M-40 0h-6M40 0h6" stroke="#f0d79a"/></svg>';
    $('ah-chain').innerHTML =
      '<svg class="flow" viewBox="0 0 400 80" preserveAspectRatio="none" aria-hidden="true"><path d="M50 40 C120 0 160 80 200 40 S280 0 350 40" fill="none" stroke="var(--ah)" stroke-width="2"/></svg>' +
      '<div class="node"><div class="disc"><span class="g">' + GLYPH[h.planet] + '</span></div><b>' + the(h.planet) + '</b><span>Planet of the hour · its angel ' + esc(S.hourAngel.angel) + ' · ' + esc(skyText(p)) + '</span></div>' +
      '<div class="node"><div class="disc">' + paulinaArt(pa, h.planet, true) + '</div><b>' + esc(pa.angel) + '</b><span>Angel of the ' + ORD[pa.no - 1] + ' hour (Ars Paulina), doing the work of ' + the(h.planet) + '</span></div>' +
      '<div class="node"><div class="disc">' + dayArt(d.ruler, true) + '</div><b>' + esc(da.angel) + '</b><span>Archangel of the day · ' + DAYS[d.wd] + ' · ' + GLYPH[d.ruler] + ' ' + the(d.ruler) + '</span></div>' +
      '<div class="node"><div class="disc">' + you + '</div><b>You</b><span>' + esc(loc.name.replace(/ \(.*$/, '')) + '</span></div>';
  }

  function nextHourObj() {
    var all = []; S.days.forEach(function (d) { all = all.concat(d.hours); });
    for (var i = 0; i < all.length; i++) if (all[i].start >= S.cur.end - 1000 && all[i].start > S.now) return all[i];
    return null;
  }
  function renderNextHour() {
    var n = nextHourObj(), tz = loc.tz, box = $('ah-nexthour');
    if (!n) { box.hidden = true; return; }
    box.hidden = false;
    var pa = D.paulina[n.i], aligned = n.planet === n.ruler;
    box.innerHTML = '<div class="disc">' + paulinaArt(pa, n.planet, true) + '</div>' +
      '<div><div class="eyebrow">Next hour · ' + ROMAN[pa.no - 1] + ' of the ' + pa.period + ', ' + esc(pa.hour) + '</div><b>' + esc(pa.angel) + '</b>' +
      '<span class="muted">serving <span style="color:' + HUE[n.planet][0] + '">' + GLYPH[n.planet] + ' ' + the(n.planet) + '</span>' + (aligned ? ' · <span style="color:var(--gold2)">aligned with ' + esc(D.seven[n.ruler].angel) + ', the archangel of the day</span>' : '') + '</span></div>' +
      '<div class="when"><big id="ah-next-in">' + dur(n.start - new Date()) + '</big>at ' + esc(hm(n.start, tz)) + '</div>';
    S.next = n;
  }

  function nextAlignment() {
    var all = []; S.days.forEach(function (d) { all = all.concat(d.hours); });
    for (var i = 0; i < all.length; i++) if (all[i].start > S.now && all[i].planet === all[i].ruler) return all[i];
    return null;
  }
  function hourLabel(x) { return x.i < 12 ? 'the ' + ORD[x.i] + ' hour of the day' : 'the ' + ORD[x.i - 12] + ' hour of the night'; }

  function renderAlign() {
    var h = S.cur, d = S.day, on = h.planet === d.ruler, nx = nextAlignment(), tz = loc.tz;
    var box = $('ah-align');
    box.classList.toggle('on', on);
    var mid = on
      ? '<div class="ring">✦</div><b style="font-family:var(--serif);font-size:22px;color:var(--gold2)">Aligned now</b><p class="fine" style="margin:6px 0 0">' + the(h.planet) + ' rules both the day and the hour. ' + esc(S.dayAngel.angel) + ' keeps both.</p>'
      : '<div class="ring">' + GLYPH[d.ruler] + '·' + GLYPH[h.planet] + '</div><b style="font-family:var(--serif);font-size:20px">Not aligned</b><p class="fine" style="margin:6px 0 0">The day belongs to ' + the(d.ruler) + ', this hour to ' + the(h.planet) + '.</p>';
    box.innerHTML =
      '<div class="med"><div class="disc">' + dayArt(d.ruler, true) + '</div><b>' + esc(S.dayAngel.angel) + '</b><span class="fine">Archangel of the day · ' + DAYS[d.wd] + ' · ' + GLYPH[d.ruler] + '</span></div>' +
      '<div class="mid">' + mid + '</div>' +
      '<div class="med"><div class="disc">' + dayArt(h.planet, true) + '</div><b>' + esc(S.hourAngel.angel) + '</b><span class="fine">Angel of the hour’s planet · ' + GLYPH[h.planet] + '</span></div>' +
      (nx ? '<p class="bignext" style="grid-column:1/-1">' + (on ? 'After this, the next alignment' : 'Next alignment') + ' in <b id="ah-align-in">' + dur(nx.start - new Date()) + '</b><br><span class="fine">' + esc(D.seven[nx.ruler].angel) + ' with ' + esc(D.seven[nx.planet].angel) + ', ' + esc((nx.wd !== d.wd ? fmt(nx.start, tz, { weekday: 'long' }) + ' ' : '') + hm(nx.start, tz)) + ', ' + hourLabel(nx) + '</span></p>' : '');
    S.nextAlign = nx;
    // today's four alignment hours (day I and VIII, night III and X), then the next day's first two
    var list = [], di = S.days.indexOf(d);
    [0, 7, 14, 21].forEach(function (k) { list.push(d.hours[k]); });
    if (S.days[di + 1]) [0, 7].forEach(function (k) { list.push(S.days[di + 1].hours[k]); });
    var items = list.map(function (x) {
      var st = S.now >= x.end ? 'past' : S.now >= x.start ? 'now' : (nx && x === nx ? 'next' : '');
      var lab = x.i < 12 ? 'Day ' + ROMAN[x.i] : 'Night ' + ROMAN[x.i - 12];
      return '<div class="' + st + '"><em>' + (st === 'now' ? 'Now' : st === 'next' ? 'Next' : st === 'past' ? 'Passed' : DAYS[x.wd]) + ' · ' + lab + '</em><b>' + esc((x.wd !== d.wd ? fmt(x.start, tz, { weekday: 'short' }) + ' ' : '') + hm(x.start, tz)) + '</b><span>' + GLYPH[x.ruler] + ' ' + esc(D.seven[x.ruler].angel) + ' with ' + esc(D.paulina[x.i].angel) + '</span></div>';
    }).join('');
    $('ah-alignlist').innerHTML = items;
  }

  function quarterOf(az) { return az >= 45 && az < 135 ? 'East' : az >= 135 && az < 225 ? 'South' : az >= 225 && az < 315 ? 'West' : 'North'; }
  var SIGNS = ['♈', '♉', '♊', '♋', '♌', '♍', '♎', '♏', '♐', '♑', '♒', '♓'].map(function (g) { return g + '\uFE0E'; }); // text, not emoji
  function renderSky() {
    var h = S.cur, R = 190, pts = {}, now = new Date(), f1 = function (n) { return n.toFixed(1); };
    ORDER.forEach(function (pl) { pts[pl] = sky(pl); });
    var sunAlt = pts.Sun ? pts.Sun.alt : -30, day = sunAlt > 0, twi = !day && sunAlt > -12;
    var top = day ? '#2a5a9c' : twi ? '#3a2c6a' : '#0e1838', bot = day ? '#0f2648' : twi ? '#120c26' : '#03050c';
    var starOp = day ? 0.12 : twi ? 0.5 : 1;
    var xy = function (alt, az, rr) { var r = rr != null ? rr : R * (1 - alt / 90), a = (az - 90) * Math.PI / 180; return [r * Math.cos(a), r * Math.sin(a)]; };
    var out = '<svg viewBox="-260 -260 520 520" role="img" aria-label="Your sky now: the Sun, Moon and planets as seen from your location, north at the top, the zenith in the centre">' +
      '<defs><radialGradient id="ahsk" r=".75"><stop offset="0" stop-color="' + top + '"/><stop offset="1" stop-color="' + bot + '"/></radialGradient>' +
      '<radialGradient id="ahhz" r=".5"><stop offset=".86" stop-color="' + (twi ? '#ff9a5c' : day ? '#9fd0ff' : '#5a6fb0') + '" stop-opacity="0"/><stop offset=".97" stop-color="' + (twi ? '#ff9a5c' : day ? '#9fd0ff' : '#5a6fb0') + '" stop-opacity=".45"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>' +
      '<filter id="ahglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>' +
      '<linearGradient id="ahbeam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff6dc" stop-opacity=".0"/><stop offset="1" stop-color="' + HUE[h.planet][0] + '" stop-opacity=".95"/></linearGradient>' +
      ORDER.map(function (pl) { return '<radialGradient id="aho' + pl + '"><stop offset="0" stop-color="#ffffff"/><stop offset=".35" stop-color="' + HUE[pl][0] + '"/><stop offset="1" stop-color="' + HUE[pl][0] + '" stop-opacity="0"/></radialGradient>'; }).join('') +
      '<clipPath id="ahclip"><circle r="' + R + '"/></clipPath></defs>';
    // compass rose behind everything
    var rose = '', rp = '';
    for (var k = 0; k < 32; k++) {
      var ak = k * Math.PI / 16 - Math.PI / 2, rk = k % 2 ? R + 8 : (k % 8 === 0 ? 252 : k % 4 === 0 ? 234 : 216);
      rp += (k ? 'L' : 'M') + f1(rk * Math.cos(ak)) + ' ' + f1(rk * Math.sin(ak));
    }
    rose = '<path d="' + rp + 'Z" fill="#d4ae62" fill-opacity=".16" stroke="#f0d79a" stroke-opacity=".55" stroke-width="1"/>';
    out += '<g>' + rose + '</g><circle r="' + (R + 26) + '" fill="url(#ahhz)"/>';
    out += '<circle r="' + R + '" fill="url(#ahsk)" stroke="#d4ae62" stroke-width="1.6"/>';
    // stars, fixed per day so they don't jump around
    var seed = Math.floor(now / 864e5), rnd = function () { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; }, stars = '<g clip-path="url(#ahclip)" opacity="' + starOp + '">';
    for (k = 0; k < 170; k++) { var rr = Math.sqrt(rnd()) * R, aa = rnd() * 6.283; stars += '<circle class="sky-tw" style="animation-delay:' + f1(rnd() * 4) + 's" cx="' + f1(rr * Math.cos(aa)) + '" cy="' + f1(rr * Math.sin(aa)) + '" r="' + f1(0.4 + rnd() * 1.3) + '" fill="#fff8e6"/>'; }
    out += stars + '</g>';
    // altitude rings
    [30, 60].forEach(function (alt) { out += '<circle r="' + f1(R * (1 - alt / 90)) + '" fill="none" stroke="#b9c6ff" stroke-opacity=".22" stroke-dasharray="2 5"/><text x="4" y="' + f1(-R * (1 - alt / 90) - 3) + '" font-family="IBM Plex Mono, monospace" font-size="9" fill="#b9c6ff" opacity=".55">' + alt + '°</text>'; });
    // the ecliptic, the road of the Sun, Moon and planets, with the twelve signs
    if (EPH.eclipticAltAz) {
      var seg = '', path = '', signs = '';
      for (var l = 0; l <= 360; l += 3) {
        var e = EPH.eclipticAltAz(l, now, loc.lat, loc.lon);
        if (e.alt >= 0) { var q = xy(e.alt, e.az); seg += (seg ? 'L' : 'M') + f1(q[0]) + ' ' + f1(q[1]); }
        else if (seg) { path += seg; seg = ''; }
        if (l % 30 === 15 && e.alt > 4) { var qs = xy(e.alt, e.az); signs += '<text x="' + f1(qs[0]) + '" y="' + f1(qs[1] + 6) + '" text-anchor="middle" font-size="18" fill="#f0d79a" opacity=".7">' + SIGNS[(l - 15) / 30] + '</text>'; }
      }
      path += seg;
      out += '<g clip-path="url(#ahclip)"><path d="' + path + '" fill="none" stroke="#f0d79a" stroke-opacity=".55" stroke-width="1.4" stroke-dasharray="6 4"/>' + signs + '</g>';
    }
    out += '<text x="0" y="4" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="8" letter-spacing="2" fill="#c9d2f0" opacity=".6">ZENITH</text>';
    // degree ticks and cardinal points
    for (k = 0; k < 72; k++) { var at = (k * 5 - 90) * Math.PI / 180, l1 = k % 18 === 0 ? 14 : k % 2 ? 4 : 8;
      out += '<line x1="' + f1(R * Math.cos(at)) + '" y1="' + f1(R * Math.sin(at)) + '" x2="' + f1((R + l1) * Math.cos(at)) + '" y2="' + f1((R + l1) * Math.sin(at)) + '" stroke="#d4ae62" stroke-opacity=".8"/>'; }
    [['N', 0], ['E', 90], ['S', 180], ['W', 270]].forEach(function (c) { var q = xy(0, c[1], R + 36); out += '<text x="' + f1(q[0]) + '" y="' + f1(q[1] + 8) + '" text-anchor="middle" font-family="Cormorant Garamond, Georgia, serif" font-size="26" font-weight="600" fill="#f0d79a">' + c[0] + '</text>'; });
    // bodies: the other six first, the planet of the hour last and largest
    ORDER.filter(function (pl) { return pl !== h.planet; }).concat([h.planet]).forEach(function (pl) {
      var p = pts[pl]; if (!p) return;
      var up = p.alt >= 0, on = pl === h.planet, q = up ? xy(p.alt, p.az) : xy(0, p.az, R + 58), r = on ? 15 : pl === 'Sun' || pl === 'Moon' ? 11 : 8;
      if (on) {
        var rim = xy(0, p.az, R);
        out += '<line x1="0" y1="0" x2="' + f1(up ? q[0] : rim[0]) + '" y2="' + f1(up ? q[1] : rim[1]) + '" stroke="url(#ahbeam)" stroke-width="3" filter="url(#ahglow)"/>' +
               '<line x1="0" y1="0" x2="' + f1(up ? q[0] : rim[0]) + '" y2="' + f1(up ? q[1] : rim[1]) + '" stroke="' + HUE[pl][0] + '" stroke-width="1.2"/>' +
               '<circle class="sky-pulse" cx="' + f1(q[0]) + '" cy="' + f1(q[1]) + '" r="' + r + '" fill="none" stroke="' + HUE[pl][0] + '" stroke-width="2"/>';
      }
      out += '<g opacity="' + (up ? 1 : 0.45) + '"><circle cx="' + f1(q[0]) + '" cy="' + f1(q[1]) + '" r="' + (r * 2.2) + '" fill="url(#aho' + pl + ')" opacity=".55"/>' +
             '<circle cx="' + f1(q[0]) + '" cy="' + f1(q[1]) + '" r="' + r + '" fill="#06080f" stroke="' + HUE[pl][0] + '" stroke-width="' + (on ? 2.4 : 1.2) + '"/>' +
             '<text x="' + f1(q[0]) + '" y="' + f1(q[1] + r * 0.42) + '" text-anchor="middle" font-size="' + f1(r * 1.25) + '" fill="' + HUE[pl][0] + '">' + GLYPH[pl] + '</text>' +
             '<text x="' + f1(q[0]) + '" y="' + f1(q[1] + r + 13) + '" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="' + (on ? 11 : 9) + '" letter-spacing="1" fill="' + (on ? '#fff3d6' : '#c9d2f0') + '">' + pl.toUpperCase() + (up ? '' : ' ↓') + '</text></g>';
    });
    $('ah-compass').innerHTML = out + '</svg>';

    var p = pts[h.planet], qn = p ? quarterOf(p.az) : null, da = S.dayAngel;
    var html = '<p style="color:var(--text);font-size:19px;margin:0 0 6px"><b style="color:var(--ah)">' + GLYPH[h.planet] + ' ' + the(h.planet) + '</b>, planet of this hour, is ' + esc(p ? (p.alt >= 0 ? Math.round(p.alt) + '° above the horizon' : Math.round(-p.alt) + '° below the horizon') + ', toward the ' + POINTS[Math.round(p.az / 22.5) % 16] + ' (' + Math.round(p.az) + '°)' : '') + '.</p>' +
      '<p class="muted" style="margin:0 0 6px">' + (day ? 'Daylight' : twi ? 'Twilight' : 'Night') + ' sky. The zenith is at the centre and the horizon at the gold ring; bodies outside it are below the horizon. The dashed line is the ecliptic, the road of the Sun, Moon and planets through the twelve signs.</p>';
    if (da.quarters) {
      html += '<h3 style="font-size:22px;margin:16px 0 4px">Angels of the four quarters, ' + DAYS[S.day.wd] + '</h3><p class="fine" style="margin:0 0 6px">The Heptameron names these angels of the day “to be called from the four parts of the world”. The planet of the hour now lies in the ' + (qn || '') + '.</p><div class="quarters">' +
        ['East', 'South', 'West', 'North'].map(function (q) { return '<div' + (q === qn ? ' class="on"' : '') + '><b>' + q + (q === qn ? ' · the planet is here' : '') + '</b><span>' + esc(da.quarters[q].join(', ')) + '</span></div>'; }).join('') + '</div>';
    } else {
      html += '<p class="fine">On ' + DAYS[S.day.wd] + ' the Heptameron gives prayers for the four quarters instead of angels, because, it says, no angels rule the air above the fifth heaven.</p>';
    }
    $('ah-quarters').innerHTML = html;
  }

  function renderSeal() {
    var h = S.cur, pa = S.pa, tz = loc.tz;
    var date = fmt(h.start, tz, { day: 'numeric', month: 'short', year: 'numeric' }).toUpperCase();
    $('ah-seal').innerHTML = ART.seal({ name: pa.angel, planet: h.planet, lines: [pa.angel.toUpperCase(), pa.hour.toUpperCase(), date, hm(h.start, tz) + '–' + hm(h.end, tz), the(h.planet).toUpperCase()] });
    var svg = $('ah-seal').querySelector('svg'); if (svg) requestAnimationFrame(function () { svg.classList.add('draw'); });
  }

  function renderNext() {
    var all = [], tz = loc.tz, out = '';
    S.days.forEach(function (d) { all = all.concat(d.hours); });
    all.filter(function (x) { return x.start > S.now; }).slice(0, 8).forEach(function (x) {
      var pa = D.paulina[x.i];
      out += '<li><span class="t">' + esc((x.wd !== S.day.wd ? fmt(x.start, tz, { weekday: 'short' }) + ' ' : '') + hm(x.start, tz)) + '</span><span style="color:' + HUE[x.planet][0] + ';font-size:20px">' + GLYPH[x.planet] + '</span><span><b>' + esc(pa.angel) + '</b> <span class="fine">serving ' + the(x.planet) + '</span></span>' + (x.planet === x.ruler ? '<span class="al">ALIGNED</span>' : '<span></span>') + '</li>';
    });
    $('ah-next').innerHTML = out;
  }

  function tick() {
    if (!S.cur) return;
    var now = new Date();
    if (now >= S.cur.end) { render(); return; }
    $('ah-count').textContent = dur(S.cur.end - now) + ' left in this hour · until ' + hm(S.cur.end, loc.tz) + ' · ' + loc.name.replace(/ \(.*$/, '');
    var ni = $('ah-next-in'); if (ni && S.next) ni.textContent = dur(S.next.start - now);
    var ai = $('ah-align-in'); if (ai && S.nextAlign) ai.textContent = dur(S.nextAlign.start - now);
    if (document.visibilityState === 'hidden') document.title = S.pa.angel + ' · ' + dur(S.cur.end - now);
  }

  // ------------------------------------------------------------ reveal
  function reveal(l) {
    loc = l; store.set('loc', l);
    $('ah-reveal').style.display = 'none';
    stage.classList.add('ah-veil');
    $('ah-live').hidden = false;
    render();
    requestAnimationFrame(function () { setTimeout(function () { stage.classList.add('lifted'); }, 60); });
    if (!timer) timer = setInterval(tick, 1000);
    if (!window.__ahSky) window.__ahSky = setInterval(function () { if (S.cur) { renderSky(); renderChain(); } }, 60000);
  }
  function cityLoc(c) { return { name: c[0], lat: c[1], lon: c[2], tz: c[3] }; }

  var sel = $('ah-city');
  sel.innerHTML = '<option value="">…or choose a city</option>' + CITIES.map(function (c, i) { return '<option value="' + i + '">' + esc(c[0]) + '</option>'; }).join('');
  sel.addEventListener('change', function () { if (sel.value !== '') reveal(cityLoc(CITIES[+sel.value])); });
  if (saved && typeof saved.lat === 'number') {
    var alt = document.createElement('button'); alt.type = 'button'; alt.className = 'btn ghost small'; alt.textContent = 'Reveal for ' + saved.name.replace(/ \(.*$/, '');
    alt.addEventListener('click', function () { reveal(saved); });
    $('ah-reveal').insertBefore(alt, sel);
  }
  $('ah-go').addEventListener('click', function () {
    var btn = this;
    if (!navigator.geolocation) { btn.textContent = 'Location unavailable: choose a city'; return; }
    btn.textContent = 'Finding your sky…';
    navigator.geolocation.getCurrentPosition(function (pos) {
      reveal({ name: 'Your location (' + pos.coords.latitude.toFixed(2) + '°, ' + pos.coords.longitude.toFixed(2) + '°)', lat: pos.coords.latitude, lon: pos.coords.longitude, tz: DEVICE_TZ });
    }, function () { btn.textContent = 'Location not shared: choose a city below'; }, { maximumAge: 6e5, timeout: 15000 });
  });
  $('ah-relocate').addEventListener('click', function () { $('ah-reveal').style.display = ''; stage.classList.remove('lifted'); $('ah-go').textContent = 'Reveal the angel of this hour'; stage.scrollIntoView({ behavior: 'smooth' }); });
  $('ah-share').addEventListener('click', function () {
    var st = $('ah-status'); if (!S.pa) return;
    var text = 'The angel of this hour is ' + S.pa.angel + ', serving ' + the(S.cur.planet) + ' ' + GLYPH[S.cur.planet] + ', on the day of ' + S.dayAngel.angel + '. Find yours:';
    var url = location.origin + location.pathname;
    if (navigator.share) navigator.share({ title: 'Angel of the Hour', text: text, url: url }).catch(function () {});
    else if (navigator.clipboard) navigator.clipboard.writeText(text + ' ' + url).then(function () { st.textContent = 'Copied to your clipboard.'; }, function () { st.textContent = url; });
  });

  // ------------------------------------------------------------ point the phone
  var facing = false;
  function onOrient(e) {
    var heading = typeof e.webkitCompassHeading === 'number' ? e.webkitCompassHeading : (e.absolute || e.type === 'deviceorientationabsolute') && e.alpha != null ? 360 - e.alpha : null;
    if (heading == null) return;
    var svg = $('ah-compass').querySelector('svg'); if (svg) svg.style.transform = 'rotate(' + (-heading).toFixed(1) + 'deg)';
    var p = S.cur && sky(S.cur.planet);
    if (p) { var diff = ((p.az - heading) + 540) % 360 - 180; $('ah-status').textContent = Math.abs(diff) < 10 ? 'You are facing ' + the(S.cur.planet) + '.' : 'Turn ' + (diff > 0 ? 'right' : 'left') + ' ' + Math.round(Math.abs(diff)) + '° to face ' + the(S.cur.planet) + '.'; }
  }
  $('ah-face').addEventListener('click', function () {
    var btn = this;
    if (facing) { facing = false; window.removeEventListener('deviceorientationabsolute', onOrient); window.removeEventListener('deviceorientation', onOrient); btn.textContent = 'Point my phone'; $('ah-status').textContent = ''; var svg = $('ah-compass').querySelector('svg'); if (svg) svg.style.transform = ''; return; }
    var start = function () { facing = true; btn.textContent = 'Stop pointing'; window.addEventListener('deviceorientationabsolute', onOrient); window.addEventListener('deviceorientation', onOrient); $('ah-status').textContent = 'Hold your phone flat and turn slowly.'; };
    if (window.DeviceOrientationEvent && typeof DeviceOrientationEvent.requestPermission === 'function') {
      DeviceOrientationEvent.requestPermission().then(function (r) { if (r === 'granted') start(); else $('ah-status').textContent = 'Compass access was not allowed.'; }).catch(function () { $('ah-status').textContent = 'This device has no compass available to the browser.'; });
    } else if ('ondeviceorientationabsolute' in window || 'ondeviceorientation' in window) start();
    else $('ah-status').textContent = 'This device has no compass available to the browser.';
  });

  // ------------------------------------------------------------ sit with the angel
  var sanct = $('ah-sanct'), showDay = false, audio = null, nodes = null, cueTimer = null;
  function sanctArt() { $('ah-sanct-art').innerHTML = showDay ? dayArt(S.day.ruler, false) : paulinaArt(S.pa, S.cur.planet, false); $('ah-swap').textContent = showDay ? 'Show the angel of the hour' : 'Show the angel of the day'; }
  function cue() { var t = (Date.now() % 10000) / 1000; $('ah-cue').textContent = t < 4 ? 'Breathe in' : 'Breathe out'; }
  function toneOff() { if (nodes) { nodes.forEach(function (n) { try { n.stop(); } catch (e) { /* stopped */ } }); nodes = null; } $('ah-tone').textContent = 'Soft tone: off'; }
  $('ah-sit').addEventListener('click', function () {
    if (!S.pa) return; showDay = false; sanctArt(); sanct.classList.add('open'); document.body.style.overflow = 'hidden';
    cue(); cueTimer = setInterval(cue, 250); $('ah-close').focus();
  });
  function closeSanct() { sanct.classList.remove('open'); document.body.style.overflow = ''; clearInterval(cueTimer); toneOff(); $('ah-sit').focus(); }
  $('ah-close').addEventListener('click', closeSanct);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && sanct.classList.contains('open')) closeSanct(); });
  $('ah-swap').addEventListener('click', function () { showDay = !showDay; sanctArt(); });
  $('ah-tone').addEventListener('click', function () {
    if (nodes) { toneOff(); return; }
    try {
      audio = audio || new (window.AudioContext || window.webkitAudioContext)();
      var g = audio.createGain(); g.gain.value = 0; g.connect(audio.destination);
      g.gain.linearRampToValueAtTime(0.05, audio.currentTime + 3);
      nodes = [110, 165, 220.5].map(function (f, i) { var o = audio.createOscillator(); o.type = 'sine'; o.frequency.value = f; var gg = audio.createGain(); gg.gain.value = [0.6, 0.3, 0.15][i]; o.connect(gg); gg.connect(g); o.start(); return o; });
      $('ah-tone').textContent = 'Soft tone: on';
    } catch (e) { /* audio unavailable */ }
  });

  // ------------------------------------------------------------ codex artwork, drawn when scrolled into view
  var arts = document.querySelectorAll('.codex-art[data-art]');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (x) {
        var el = x.target;
        if (x.isIntersecting && !el.dataset.drawn) { el.innerHTML = ART.angel(JSON.parse(el.getAttribute('data-art'))); el.dataset.drawn = '1'; }
        el.classList.toggle('paused', !x.isIntersecting);
      });
    }, { rootMargin: '300px' });
    arts.forEach(function (a) { io.observe(a); });
  } else arts.forEach(function (el) { el.innerHTML = ART.angel(JSON.parse(el.getAttribute('data-art'))); });

  // the veiled figure before the reveal
  $('ah-art').innerHTML = ART.angel({ name: 'Angel of the Hour', planet: 'Sun', kind: 'pauline', period: 'day', subtitle: '', ring: 'THE ANGEL OF THIS HOUR ✦ ARS PAULINA ✦ ', label: 'A veiled angel, waiting to be revealed' });
  document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'visible' && S.pa) document.title = document.querySelector('title').getAttribute('data-base') || document.title; });
  var t = document.querySelector('title'); t.setAttribute('data-base', t.textContent);
  window.__ah = { state: function () { return S; }, reveal: reveal };
})();
