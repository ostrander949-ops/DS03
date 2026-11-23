/* Find your birth angel: the 72 angels by the Sun's degree, the Heptameron angel of the birth day, and a name sigil
   traced on the day planet's magic square (Agrippa II.22). Data in window.BA, built by tools/build_birth_angel_page.py. */
(function () {
  var B = window.BA;
  var CHALDEAN = ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon'];
  var DAY_RULER = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']; // JS getDay(): Sunday = 0
  var WEEK = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  var SLUG = {Michael: 'michael', Gabriel: 'gabriel', Samael: 'samael', Raphael: 'raphael', Sachiel: 'sachiel', Anael: 'anael', Cassiel: 'cassiel'};
  var rad = Math.PI / 180;

  function jd(ms) { return ms / 86400000 + 2440587.5; }
  function sunLon(ms) {
    var T = (jd(ms) - 2451545) / 36525;
    var L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T * T;
    var M = (357.52911 + 35999.05029 * T - 0.0001537 * T * T) * rad;
    var C = (1.914602 - 0.004817 * T - 0.000014 * T * T) * Math.sin(M) + (0.019993 - 0.000101 * T) * Math.sin(2 * M) + 0.000289 * Math.sin(3 * M);
    var om = (125.04 - 1934.136 * T) * rad;
    var l = (L0 + C - 0.00569 - 0.00478 * Math.sin(om)) % 360;
    return l < 0 ? l + 360 : l;
  }
  function values(name) {
    var s = name.toUpperCase().replace(/[^A-Z]/g, ''), out = [], i = 0;
    while (i < s.length) {
      var d = s.substr(i, 2);
      if (B.digraphs[d]) { out.push(B.digraphs[d]); i += 2; }
      else { if (B.letters[s[i]]) out.push(B.letters[s[i]]); i += 1; }
    }
    return out;
  }
  function path(name, planet) {
    var sq = B.kamea[planet], n = sq.length, top = n * n, where = {}, cells = [];
    for (var r = 0; r < n; r++) for (var c = 0; c < n; c++) where[sq[r][c]] = [r, c];
    values(name).forEach(function (v) {
      while (v > top) v = Math.floor(v / 10);
      var cell = where[v], last = cells[cells.length - 1];
      if (!last || last[0] !== cell[0] || last[1] !== cell[1]) cells.push(cell);
    });
    return cells;
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]; }); }
  function sigil(name, planet) {
    var sq = B.kamea[planet], n = sq.length, S = 360, pad = 20, cs = (S - 2 * pad) / n, cells = path(name, planet);
    var o = '<svg viewBox="0 0 ' + S + ' ' + S + '" role="img" aria-label="Sigil of ' + esc(name) + ' on the square of ' + planet + '">';
    for (var r = 0; r < n; r++) for (var c = 0; c < n; c++) {
      o += '<rect x="' + (pad + c * cs) + '" y="' + (pad + r * cs) + '" width="' + cs + '" height="' + cs + '" fill="none" stroke="rgba(226,189,108,.18)"/>';
      o += '<text x="' + (pad + c * cs + cs / 2) + '" y="' + (pad + r * cs + cs / 2 + cs * 0.12) + '" text-anchor="middle" font-size="' + (cs * 0.32) +
        '" fill="rgba(226,189,108,.35)" font-family="Georgia,serif">' + sq[r][c] + '</text>';
    }
    if (cells.length) {
      var pts = cells.map(function (p) { return [pad + p[1] * cs + cs / 2, pad + p[0] * cs + cs / 2]; });
      o += '<polyline points="' + pts.map(function (p) { return p[0].toFixed(1) + ',' + p[1].toFixed(1); }).join(' ') +
        '" fill="none" stroke="#f3dc9e" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>';
      o += '<circle cx="' + pts[0][0] + '" cy="' + pts[0][1] + '" r="9" fill="none" stroke="#f3dc9e" stroke-width="4"/>';
      var a = pts[pts.length - 1], b = pts.length > 1 ? pts[pts.length - 2] : [a[0] - 1, a[1]];
      var dx = a[0] - b[0], dy = a[1] - b[1], L = Math.hypot(dx, dy) || 1, nx = -dy / L * 11, ny = dx / L * 11;
      o += '<line x1="' + (a[0] + nx) + '" y1="' + (a[1] + ny) + '" x2="' + (a[0] - nx) + '" y2="' + (a[1] - ny) + '" stroke="#f3dc9e" stroke-width="4" stroke-linecap="round"/>';
    }
    return o + '</svg>';
  }
  function go() {
    var name = document.getElementById('ba-name').value.trim() || 'Friend';
    var d = document.getElementById('ba-date').value, tm = document.getElementById('ba-time').value;
    if (!d) { document.getElementById('ba-date').focus(); return; }
    var p = d.split('-').map(Number), hm = tm ? tm.split(':').map(Number) : [12, 0];
    var local = new Date(p[0], p[1] - 1, p[2], hm[0], hm[1]);   // birth time read in this browser's time zone
    var lon = sunLon(local.getTime()), i = Math.floor(lon / 5), into = lon - 5 * i;
    var choir = B.choirs[Math.floor(i / 8)], sign = B.signs[Math.floor(lon / 30)], deg = Math.floor(lon % 30);
    var face = Math.floor((lon % 30) / 10) + 1, faceRuler = CHALDEAN[(CHALDEAN.indexOf('Mars') + Math.floor(lon / 10)) % 7];
    var planet = DAY_RULER[local.getDay()], dayAngel = B.dayAngel[planet];
    var cusp = (!tm && (into < 1 || into > 4)) ? '<p style="color:#e9cf8c">You were born close to the edge between ' + B.angels[i] + ' and ' +
      B.angels[into < 2.5 ? (i + 71) % 72 : (i + 1) % 72] + '. Add your birth time for a sure answer.</p>' : '';
    var nm = esc(name);
    var out = document.getElementById('ba-out');
    out.innerHTML = '<div class="ba-card"><div><div class="k">Your birth angel · number ' + (i + 1) + ' of 72</div><h2>' + B.angels[i] + '</h2>' +
      '<p>The Sun stood at ' + deg + '° ' + sign + ' when you were born, in the five degrees kept by <b>' + B.angels[i] + '</b>, one of the eight angels of the <b>' +
      choir[0] + '</b>, the choir ruled by the archangel ' + choir[1] + ' in ' + choir[2] + '. The ' + choir[0] + ' are given ' + choir[3] + '.</p>' + cusp +
      '<p>Your Sun fell in the ' + ['first', 'second', 'third'][face - 1] + ' face of ' + sign + ', ruled by ' + faceRuler + '.</p>' +
      '<div class="ba-day"><img src="/assets/img/angels/' + SLUG[dayAngel] + '-640.webp" alt="' + dayAngel + '" width="84" height="84"><p>You were born on a <b>' +
      WEEK[local.getDay()] + '</b>, the day of ' + (planet === 'Sun' || planet === 'Moon' ? 'the ' : '') + planet + ', kept in the <i>Heptameron</i> by the archangel <b>' + dayAngel + '</b>.</p></div></div>' +
      '<div><div class="ba-sig">' + sigil(name, planet) + '</div><p style="text-align:center;color:#a9a395;font-size:14px">The sigil of “' + nm + '” on the magic square of ' + planet + '</p></div></div>' +
      '<div class="ba-offer"><div class="k">Personal invocation · instant PDF</div><h3>' + B.angels[i] + ', ' + dayAngel + ' and your hour angel, in one book</h3>' +
      '<p style="color:#d6d0c2">An illustrated personal invocation made from your full birth details:</p><ul>' +
      '<li>Your birth angel, birth-day angel and the angel of the very hour you were born, from your birth time and place</li>' +
      '<li>Your sigil drawn large on your planet’s square, with a printable card and a phone wallpaper</li>' +
      '<li>A prayer of invocation naming your angels, in the form of the old books, in plain English</li>' +
      '<li>Your angels’ hours for the weeks ahead, worked out for where you live</li></ul>' +
      '<div class="ba-btns"><a class="p" href="' + B.buy + '" rel="noopener">Get mine · $24</a><a class="s" href="' + B.gift + '" rel="noopener">Give as a gift · $29</a></div>' +
      '<p style="color:#8a8576;font-size:13px;margin-top:12px">For reflection and devotion. Makes no promise of any outcome.</p></div>';
    out.style.display = 'block';
    out.scrollIntoView({behavior: 'smooth', block: 'start'});
    if (window.va) window.va('event', {name: 'Birth Angel', data: {angel: B.angels[i]}});
  }
  document.getElementById('ba-go').addEventListener('click', go);
  document.getElementById('ba-form').addEventListener('keydown', function (e) { if (e.key === 'Enter') go(); });
})();
