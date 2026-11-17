/* Homepage: the live planetary hour, its angels and a countdown. Computed in the browser; nothing is sent anywhere.
   Uses the visitor's saved place from the hour tools, or a city matched to the device's time zone. */
(function () {
  'use strict';
  var D = window.DS_ANGELS, ART = window.DSAngelArt, CITIES = window.DS_CITIES || [];
  var box = document.getElementById('hour-now');
  if (!D || !ART || !box) return;
  var ORDER = ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon'], DAY_RULER = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'];
  var DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  var ORD = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth'];
  var $ = function (id) { return document.getElementById(id); };
  function the(p) { return p === 'Sun' || p === 'Moon' ? 'the ' + p : p; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var TZ = (function () { try { return Intl.DateTimeFormat().resolvedOptions().timeZone; } catch (e) { return 'UTC'; } })();
  var loc = null;
  try { loc = JSON.parse(localStorage.getItem('ds-hn-loc')); } catch (e) { loc = null; }
  if (!loc || typeof loc.lat !== 'number') {
    var c = CITIES.filter(function (x) { return x[3] === TZ; })[0];
    loc = c ? { name: c[0], lat: c[1], lon: c[2], tz: c[3] } : { name: 'London', lat: 51.51, lon: -0.13, tz: 'Europe/London', guessed: true };
  }

  function sun(y, m, d, lat, lon) {
    var rad = Math.PI / 180, n = Math.round((Date.UTC(y, m - 1, d, 12) - Date.UTC(2000, 0, 1, 12)) / 864e5), J = n - lon / 360;
    var M = (357.5291 + 0.98560028 * J) % 360, C = 1.9148 * Math.sin(M * rad) + 0.02 * Math.sin(2 * M * rad) + 0.0003 * Math.sin(3 * M * rad);
    var L = (M + C + 180 + 102.9372) % 360, Jt = 2451545 + J + 0.0053 * Math.sin(M * rad) - 0.0069 * Math.sin(2 * L * rad);
    var sd = Math.sin(L * rad) * Math.sin(23.4397 * rad), cd = Math.cos(Math.asin(sd)), cw = (Math.sin(-0.833 * rad) - Math.sin(lat * rad) * sd) / (Math.cos(lat * rad) * cd);
    if (cw < -1 || cw > 1) return null;
    var w = Math.acos(cw) / rad / 360, t = function (j) { return new Date((j - 2440587.5) * 864e5); };
    return { rise: t(Jt - w), set: t(Jt + w) };
  }
  function ymd(t, tz) { var o = {}; new Intl.DateTimeFormat('en-CA', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(t).forEach(function (x) { o[x.type] = +x.value; }); return [o.year, o.month, o.day]; }
  function add(a, n) { var d = new Date(Date.UTC(a[0], a[1] - 1, a[2] + n)); return [d.getUTCFullYear(), d.getUTCMonth() + 1, d.getUTCDate()]; }
  function hm(t) { return new Intl.DateTimeFormat(undefined, { timeZone: loc.tz, hour: 'numeric', minute: '2-digit' }).format(t); }
  function dur(ms) { var s = Math.max(0, Math.round(ms / 1000)), h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), x = s % 60; return h ? h + 'h ' + m + 'm' : m + 'm ' + (x < 10 ? '0' : '') + x + 's'; }

  var cur = null;
  function compute() {
    var now = new Date(), today = ymd(now, loc.tz);
    for (var k = -1; k <= 0; k++) {
      var a = add(today, k), b = add(today, k + 1), sa = sun(a[0], a[1], a[2], loc.lat, loc.lon), sb = sun(b[0], b[1], b[2], loc.lat, loc.lon);
      if (!sa || !sb || now < sa.rise || now >= sb.rise) continue;
      var wd = new Date(Date.UTC(a[0], a[1] - 1, a[2])).getUTCDay(), ruler = DAY_RULER[wd], night = now >= sa.set;
      var len = night ? (sb.rise - sa.set) / 12 : (sa.set - sa.rise) / 12, base = night ? sa.set : sa.rise;
      var i = Math.floor((now - base) / len) + (night ? 12 : 0);
      return { i: i, planet: ORDER[(ORDER.indexOf(ruler) + i) % 7], ruler: ruler, wd: wd, end: new Date(+base + (Math.floor((now - base) / len) + 1) * len) };
    }
    return null;
  }
  function render() {
    cur = compute();
    if (!cur) return;
    var pa = D.paulina[cur.i], ha = D.seven[cur.planet], da = D.seven[cur.ruler];
    $('hn-h').innerHTML = 'The hour of <em>' + esc(the(cur.planet)) + '</em>';
    $('hn-l').innerHTML = '<b style="color:var(--text,#ece5d3)">' + esc(pa.angel) + '</b>, angel of the ' + ORD[pa.no - 1] + ' hour of the ' + pa.period + ' in the Ars Paulina, is doing the work of ' + the(cur.planet) + '. ' +
      esc(ha.angel) + ' keeps ' + the(cur.planet) + ', and ' + esc(da.angel) + ' rules all of ' + DAYS[cur.wd] + '.' + (cur.planet === cur.ruler ? ' <b style="color:var(--gold)">The day and the hour are aligned.</b>' : '');
    $('hn-app').innerHTML = 'Keep ' + esc(ha.angel) + ' on your home screen: <a href="https://play.google.com/store/apps/details?id=com.discoveryscience.' + ha.app + '" rel="noopener">' + esc(ha.angel) + ' on Google Play</a>';
    var art = $('hn-art');
    art.innerHTML = '<a href="/angel-of-the-hour.html" aria-label="Meet ' + esc(pa.angel) + ', the angel of this hour">' + ART.angel({ name: pa.angel, planet: cur.planet, kind: 'pauline', period: pa.period, hour: pa.no, subtitle: pa.angel,
      ring: pa.angel.toUpperCase() + ' ✦ THE ' + ORD[pa.no - 1].toUpperCase() + ' HOUR OF THE ' + pa.period.toUpperCase() + ' ✦ ' + pa.hour.toUpperCase() + ' ✦ SERVING ' + the(cur.planet).toUpperCase() + ' ✦ ',
      label: 'Devotional artwork of ' + pa.angel + ', angel of this hour' }) + '</a>';
    tick();
  }
  function tick() {
    if (!cur) return;
    if (new Date() >= cur.end) { render(); return; }
    $('hn-c').textContent = dur(cur.end - new Date()) + ' left in this hour · until ' + hm(cur.end) + ' · ' + loc.name.replace(/ \(.*$/, '') + (loc.guessed ? ' (choose your city in the clock)' : '');
  }
  render();
  setInterval(tick, 1000);
})();
