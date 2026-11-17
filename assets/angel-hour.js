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
    renderChain(); renderAlign(); renderSky(); renderSeal(); renderNext();
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
    var h = S.cur, pa = S.pa, ha = S.hourAngel, p = sky(h.planet);
    var you = '<svg viewBox="-50 -50 100 100" style="width:62%;height:62%"><circle r="40" fill="none" stroke="#f0d79a" stroke-opacity=".5"/><circle r="6" fill="#f0d79a"/><circle r="18" fill="none" stroke="#f0d79a" stroke-opacity=".3"/><path d="M0 -40v-6M0 40v6M-40 0h-6M40 0h6" stroke="#f0d79a"/></svg>';
    $('ah-chain').innerHTML =
      '<svg class="flow" viewBox="0 0 400 80" preserveAspectRatio="none" aria-hidden="true"><path d="M50 40 C120 0 160 80 200 40 S280 0 350 40" fill="none" stroke="var(--ah)" stroke-width="2"/></svg>' +
      '<div class="node"><div class="disc"><span class="g">' + GLYPH[h.planet] + '</span></div><b>' + the(h.planet) + '</b><span>The planet of the hour · ' + esc(skyText(p)) + '</span></div>' +
      '<div class="node"><div class="disc">' + dayArt(h.planet, true) + '</div><b>' + esc(ha.angel) + '</b><span>Its angel in the Heptameron</span></div>' +
      '<div class="node"><div class="disc">' + paulinaArt(pa, h.planet, true) + '</div><b>' + esc(pa.angel) + '</b><span>Angel of the ' + ORD[pa.no - 1] + ' hour (Ars Paulina), doing its work</span></div>' +
      '<div class="node"><div class="disc">' + you + '</div><b>You</b><span>' + esc(loc.name.replace(/ \(.*$/, '')) + '</span></div>';
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
      ? '<div class="ring">✦</div><b style="font-family:var(--serif);font-size:22px;color:var(--gold2)">Aligned</b><p class="fine" style="margin:6px 0 0">' + the(h.planet) + ' rules both the day and the hour. ' + esc(S.dayAngel.angel) + ' keeps both.</p>'
      : '<div class="ring">' + GLYPH[d.ruler] + '·' + GLYPH[h.planet] + '</div><b style="font-family:var(--serif);font-size:20px">Not aligned</b>' +
        (nx ? '<p class="fine" style="margin:6px 0 0">Next: ' + esc(D.seven[nx.ruler].angel) + ' with ' + esc(D.seven[nx.planet].angel) + ' at ' + esc((nx.wd !== d.wd ? fmt(nx.start, tz, { weekday: 'short' }) + ' ' : '') + hm(nx.start, tz)) + ', ' + hourLabel(nx) + ' (in ' + dur(nx.start - S.now) + ')</p>' : '');
    box.innerHTML =
      '<div class="med"><div class="disc">' + dayArt(d.ruler, true) + '</div><b>' + esc(S.dayAngel.angel) + '</b><span class="fine">Angel of the day · ' + DAYS[d.wd] + ' · ' + GLYPH[d.ruler] + '</span></div>' +
      '<div class="mid">' + mid + '</div>' +
      '<div class="med"><div class="disc">' + dayArt(h.planet, true) + '</div><b>' + esc(S.hourAngel.angel) + '</b><span class="fine">Angel of the hour’s planet · ' + GLYPH[h.planet] + '</span></div>' +
      '<p class="fine" style="grid-column:1/-1;margin:8px 0 0;text-align:center">The day’s own planet returns in the first and eighth hours of the day and the third and tenth of the night: the hours the Ars Paulina names for its observances on Sunday, Monday, Wednesday and Saturday.</p>';
  }

  function quarterOf(az) { return az >= 45 && az < 135 ? 'East' : az >= 135 && az < 225 ? 'South' : az >= 225 && az < 315 ? 'West' : 'North'; }
  function renderSky() {
    var h = S.cur, R = 170, pts = {}, out = '';
    ORDER.forEach(function (pl) { pts[pl] = sky(pl); });
    out += '<svg viewBox="-230 -230 460 460" role="img" aria-label="Sky chart: the positions of the Sun, Moon and planets from your location, north at the top"><defs><radialGradient id="ahsky"><stop offset="0" stop-color="#16203a"/><stop offset="1" stop-color="#070a14"/></radialGradient></defs>';
    out += '<circle r="' + R + '" fill="url(#ahsky)" stroke="var(--gold)" stroke-opacity=".6"/><circle r="' + (R * 2 / 3) + '" fill="none" stroke="#2a3858"/><circle r="' + (R / 3) + '" fill="none" stroke="#2a3858"/>';
    for (var k = 0; k < 16; k++) { var a = (k * 22.5 - 90) * Math.PI / 180; out += '<line x1="' + (R * Math.cos(a)).toFixed(1) + '" y1="' + (R * Math.sin(a)).toFixed(1) + '" x2="' + ((R + (k % 4 ? 6 : 12)) * Math.cos(a)).toFixed(1) + '" y2="' + ((R + (k % 4 ? 6 : 12)) * Math.sin(a)).toFixed(1) + '" stroke="var(--gold)"/>'; }
    [['N', 0], ['E', 90], ['S', 180], ['W', 270]].forEach(function (c) { var a = (c[1] - 90) * Math.PI / 180; out += '<text x="' + (205 * Math.cos(a)).toFixed(1) + '" y="' + (205 * Math.sin(a) + 7).toFixed(1) + '" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="18" fill="var(--gold2)">' + c[0] + '</text>'; });
    out += '<text x="0" y="5" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="9" fill="#5b6688">ZENITH</text>';
    ORDER.forEach(function (pl) {
      var p = pts[pl]; if (!p) return;
      var up = p.alt >= 0, r = up ? R * (1 - p.alt / 90) : R + 22, a = (p.az - 90) * Math.PI / 180, x = r * Math.cos(a), y = r * Math.sin(a), on = pl === h.planet;
      if (on) out += '<line x1="0" y1="0" x2="' + x.toFixed(1) + '" y2="' + y.toFixed(1) + '" stroke="' + HUE[pl][0] + '" stroke-dasharray="3 5"/><circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="22" fill="' + HUE[pl][0] + '" opacity=".25"/>';
      out += '<text x="' + x.toFixed(1) + '" y="' + (y + (on ? 9 : 6)).toFixed(1) + '" text-anchor="middle" font-size="' + (on ? 26 : 17) + '" fill="' + HUE[pl][0] + '" opacity="' + (up ? 1 : 0.35) + '">' + GLYPH[pl] + '</text>';
    });
    $('ah-compass').innerHTML = out + '</svg>';
    var p = pts[h.planet], qn = p ? quarterOf(p.az) : null, da = S.dayAngel;
    var html = '<p style="color:var(--text);font-size:18px;margin:0 0 6px"><b style="color:var(--ah)">' + GLYPH[h.planet] + ' ' + the(h.planet) + '</b> is ' + esc(p ? (p.alt >= 0 ? Math.round(p.alt) + '° above the horizon' : Math.round(-p.alt) + '° below the horizon') + ', toward the ' + POINTS[Math.round(p.az / 22.5) % 16] + ' (' + Math.round(p.az) + '°)' : '') + '.</p>' +
      '<p class="muted" style="margin:0 0 14px">Planets near the centre are high overhead; those outside the ring are below your horizon.</p>';
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
