/* Discovery Science angel artwork: original, procedurally drawn devotional icons (SVG).
   Each angel's figure is seeded from its name, so it is always the same and always its own.
   These are modern works of art, not reproductions of any manuscript figure. */
(function () {
  'use strict';
  var GLYPH = { Saturn: '♄', Jupiter: '♃', Mars: '♂', Sun: '☉', Venus: '♀', Mercury: '☿', Moon: '☽' };
  var HEB_PLANET = { Saturn: 'שבתאי', Jupiter: 'צדק', Mars: 'מאדים', Sun: 'שמש', Venus: 'נוגה', Mercury: 'כוכב', Moon: 'לבנה' }; // Agrippa II.10
  var HUE = { Saturn: ['#8e9ab4', '#2a3046'], Jupiter: ['#b7a2ff', '#2b2058'], Mars: ['#ff8a5c', '#4a1a14'], Sun: ['#ffd27a', '#4a3210'],
              Venus: ['#8fe0b4', '#123a2c'], Mercury: ['#9fd6ff', '#14304a'], Moon: ['#e6ecff', '#1e2638'] };
  var ORDER = ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon'];
  var uid = 0;

  function hash(s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function rng(seed) { return function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; var t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function f(n) { return n.toFixed(1); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function pol(r, a) { return [r * Math.cos(a), r * Math.sin(a)]; }

  // One feather: a long leaf from the root to the tip, with a central quill.
  function feather(x0, y0, ang, len, wid, bend) {
    var tx = x0 + len * Math.cos(ang), ty = y0 + len * Math.sin(ang);
    var nx = -Math.sin(ang), ny = Math.cos(ang), mx = x0 + len * 0.55 * Math.cos(ang) + nx * bend, my = y0 + len * 0.55 * Math.sin(ang) + ny * bend;
    var d = 'M' + f(x0) + ' ' + f(y0) + 'Q' + f(mx + nx * wid) + ' ' + f(my + ny * wid) + ' ' + f(tx) + ' ' + f(ty) +
            'Q' + f(mx - nx * wid * 0.55) + ' ' + f(my - ny * wid * 0.55) + ' ' + f(x0) + ' ' + f(y0) + 'Z';
    var q = 'M' + f(x0) + ' ' + f(y0) + 'Q' + f(mx) + ' ' + f(my) + ' ' + f(tx) + ' ' + f(ty);
    return { d: d, q: q, tx: tx, ty: ty };
  }

  // A wing built like a bird's: feathers rooted along a curved arm from shoulder S to wrist W.
  // Long flight feathers first (secondaries near the body, primaries at the tip), then two rows of coverts,
  // then a scalloped leading edge. Drawn for the right side and mirrored.
  function bez(a, c, b, t) { var u = 1 - t; return [u * u * a[0] + 2 * u * t * c[0] + t * t * b[0], u * u * a[1] + 2 * u * t * c[1] + t * t * b[1]]; }
  function wing(R, p, id, w, eyes) {
    var S = w.s, W = w.w, C = w.c, out = '', n = w.n;
    var rows = [ // [feather count factor, length factor, width, angle shift, fill row]
      [1.0, 1.0, 34, 0, 0],
      [0.85, 0.6, 38, 0.10, 1],
      [0.65, 0.36, 40, 0.18, 2]
    ];
    rows.forEach(function (row, ri) {
      var m = Math.max(4, Math.round(n * row[0]));
      for (var j = 0; j < m; j++) {
        var t = m === 1 ? 1 : j / (m - 1), tt = ri ? 0.08 + t * 0.92 : t;
        var root = bez(S, C, W, tt);
        var a = w.a0 + (w.a1 - w.a0) * Math.pow(t, 0.9) + row[3] * (ri ? 1 : 0) * (w.a1 > w.a0 ? -1 : 1) + (R() - 0.5) * 0.04;
        var L = (w.l0 + (w.l1 - w.l0) * Math.pow(t, 1.4)) * row[1] * (0.95 + R() * 0.1);
        var fe = feather(root[0], root[1], a, L, row[2] * (0.85 + R() * 0.3), (R() - 0.5) * 10 + (w.a1 > w.a0 ? -6 : 6));
        out += '<path d="' + fe.d + '" fill="url(#' + id + 'fe' + row[4] + ')" stroke="url(#' + id + 'gold)" stroke-width="' + (ri ? 0.7 : 0.9) + '" stroke-opacity=".8"/>';
        if (!ri && !w.lite) out += '<path d="' + fe.q + '" fill="none" stroke="#fff6dc" stroke-opacity=".45" stroke-width=".7"/>';
        if (eyes && ri === 1 && j % 2 === 1) {
          var e = bez(S, C, W, tt), ex = e[0] + L * 0.5 * Math.cos(a), ey = e[1] + L * 0.5 * Math.sin(a);
          out += '<g transform="translate(' + f(ex) + ' ' + f(ey) + ') rotate(' + f(a * 180 / Math.PI) + ')"><path d="M-8 0Q0 -6 8 0Q0 6 -8 0Z" fill="#0b0f1a" stroke="#f3dfa6" stroke-width=".8"/><circle r="2.3" fill="' + p[0] + '"/><circle r=".9" cx=".8" cy="-.8" fill="#fff"/></g>';
        }
      }
    });
    // leading edge: small scallops along the arm
    var edge = '';
    for (var k = 0; k <= 14; k++) {
      var q = bez(S, C, W, k / 14), q2 = bez(S, C, W, Math.min(1, (k + 1) / 14));
      edge += '<path d="M' + f(q[0]) + ' ' + f(q[1]) + 'Q' + f((q[0] + q2[0]) / 2 + (w.a1 > w.a0 ? 4 : -4)) + ' ' + f((q[1] + q2[1]) / 2 + 9) + ' ' + f(q2[0]) + ' ' + f(q2[1]) + '" fill="url(#' + id + 'fe0)" stroke="url(#' + id + 'gold)" stroke-width="1.2"/>';
    }
    out += '<path d="M' + f(S[0]) + ' ' + f(S[1]) + 'Q' + f(C[0]) + ' ' + f(C[1]) + ' ' + f(W[0]) + ' ' + f(W[1]) + '" fill="none" stroke="url(#' + id + 'gold)" stroke-width="3" stroke-linecap="round"/>' + edge;
    return out;
  }

  function ringText(id, r, text, size, cls, rev, fill, family) {
    var c = 2 * Math.PI * r, path = rev ? 'M ' + r + ' 0 A ' + r + ' ' + r + ' 0 1 0 ' + (-r) + ' 0 A ' + r + ' ' + r + ' 0 1 0 ' + r + ' 0'
                                       : 'M ' + (-r) + ' 0 A ' + r + ' ' + r + ' 0 1 1 ' + r + ' 0 A ' + r + ' ' + r + ' 0 1 1 ' + (-r) + ' 0';
    return '<g class="' + cls + '"><path id="' + id + '" d="' + path + '" fill="none"/><text font-size="' + size + '" fill="' + fill + '" letter-spacing="' + (size * 0.28).toFixed(1) + '" font-family="' + (family || 'Cormorant Garamond, Georgia, serif') + '"><textPath href="#' + id + '" textLength="' + f(c * 0.995) + '" lengthAdjust="spacing">' + esc(text) + '</textPath></text></g>';
  }

  /* angel({name, planet, subtitle, hebrew, kind: 'day'|'pauline', period: 'day'|'night', hour}) -> SVG string */
  function angel(o) {
    var id = 'aa' + (++uid) + '_', R = rng(hash(o.name + (o.kind || ''))), planet = o.planet || 'Sun', p = HUE[planet];
    var night = o.period === 'night', kind = o.kind || 'day';
    var deep = night ? '#070a1c' : p[1];
    var s = '<svg class="aa" viewBox="-500 -500 1000 1000" role="img" aria-label="' + esc(o.label || ('Devotional artwork of the angel ' + o.name)) + '"><defs>' +
      '<radialGradient id="' + id + 'bg" cx="0" cy="-60" r="560" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="' + p[0] + '" stop-opacity=".55"/><stop offset=".35" stop-color="' + deep + '" stop-opacity=".95"/><stop offset="1" stop-color="#03040a"/></radialGradient>' +
      '<radialGradient id="' + id + 'halo" cx="0" cy="-150" r="210" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fffaf0"/><stop offset=".35" stop-color="#ffe7a8" stop-opacity=".85"/><stop offset=".7" stop-color="' + p[0] + '" stop-opacity=".25"/><stop offset="1" stop-color="' + p[0] + '" stop-opacity="0"/></radialGradient>' +
      '<linearGradient id="' + id + 'gold" x1="0" y1="-1" x2="0" y2="1"><stop offset="0" stop-color="#fff4cc"/><stop offset=".45" stop-color="#e2bd6c"/><stop offset="1" stop-color="#8a6526"/></linearGradient>' +
      '<linearGradient id="' + id + 'body" x1="0" y1="-260" x2="0" y2="330" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fffdf6"/><stop offset=".4" stop-color="#fbeac0"/><stop offset=".8" stop-color="' + p[0] + '" stop-opacity=".75"/><stop offset="1" stop-color="' + p[0] + '" stop-opacity="0"/></linearGradient>';
    for (var r = 0; r < 3; r++) s += '<linearGradient id="' + id + 'fe' + r + '" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fffaf0" stop-opacity="' + (0.95 - r * 0.15) + '"/><stop offset=".6" stop-color="' + p[0] + '" stop-opacity="' + (0.75 - r * 0.15) + '"/><stop offset="1" stop-color="' + p[0] + '" stop-opacity="' + (0.25 - r * 0.05) + '"/></linearGradient>';
    s += '<filter id="' + id + 'glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>' +
         '<filter id="' + id + 'soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>' +
         '<clipPath id="' + id + 'clip"><circle r="498"/></clipPath></defs>';
    s += '<g clip-path="url(#' + id + 'clip)"><circle r="500" fill="url(#' + id + 'bg)"/>';

    // stars
    var st = '';
    for (var i = 0; i < (o.lite ? 36 : 90); i++) { var a = R() * 6.283, rr = 150 + R() * 340, q = pol(rr, a); st += '<circle class="aa-tw" style="animation-delay:' + f(R() * 6) + 's" cx="' + f(q[0]) + '" cy="' + f(q[1]) + '" r="' + f(0.6 + R() * 1.6) + '" fill="#fff8e6" opacity="' + f(0.25 + R() * 0.6) + '"/>'; }
    s += st;

    // gilded rays
    var nr = 48 + Math.floor(R() * 4) * 12, rays = '<g class="aa-rays" opacity=".55">';
    for (i = 0; i < nr; i++) {
      var a0 = i / nr * 6.283, w = 0.012 + (i % 2 ? 0 : 0.01), L = i % 2 ? 360 : 470;
      var A = pol(110, a0 - w), B = pol(L, a0), C = pol(110, a0 + w);
      rays += '<path d="M' + f(A[0]) + ' ' + f(A[1]) + 'L' + f(B[0]) + ' ' + f(B[1]) + 'L' + f(C[0]) + ' ' + f(C[1]) + 'Z" fill="url(#' + id + 'gold)" opacity="' + (i % 2 ? 0.35 : 0.6) + '"/>';
    }
    s += rays + '</g>';

    // sacred geometry: the heptagram of the seven planets (day angels) or the star of twelve hours (hour angels)
    var geo = '<g class="aa-geo" fill="none" stroke="url(#' + id + 'gold)" stroke-width="1.2" opacity=".6">';
    if (kind === 'day') {
      var pts = ORDER.map(function (_, k) { return pol(392, -Math.PI / 2 + k * 2 * Math.PI / 7); });
      var d = '';
      for (k = 0; k <= 7; k++) { var P2 = pts[(k * 3) % 7]; d += (k ? 'L' : 'M') + f(P2[0]) + ' ' + f(P2[1]); }
      geo += '<path d="' + d + '"/><circle r="392" stroke-opacity=".5"/>';
      ORDER.forEach(function (pl, k) {
        var q = pol(392, -Math.PI / 2 + k * 2 * Math.PI / 7), on = pl === planet;
        geo += '<circle cx="' + f(q[0]) + '" cy="' + f(q[1]) + '" r="' + (on ? 22 : 16) + '" fill="' + (on ? '#1a1408' : '#05070e') + '" stroke-opacity="' + (on ? 1 : 0.7) + '"/><text x="' + f(q[0]) + '" y="' + f(q[1] + (on ? 8 : 6)) + '" text-anchor="middle" font-size="' + (on ? 24 : 18) + '" fill="' + (on ? '#ffe7a8' : HUE[pl][0]) + '" stroke="none">' + GLYPH[pl] + '</text>';
      });
    } else {
      var n12 = 12, d12 = '';
      for (var k = 0; k <= n12; k++) { var q12 = pol(392, -Math.PI / 2 + ((k * 5) % n12) * 2 * Math.PI / n12); d12 += (k ? 'L' : 'M') + f(q12[0]) + ' ' + f(q12[1]); }
      geo += '<path d="' + d12 + '"/><circle r="392" stroke-opacity=".5"/>';
      for (k = 0; k < 12; k++) {
        var qh = pol(392, -Math.PI / 2 + k * 2 * Math.PI / 12), on2 = k + 1 === o.hour;
        geo += '<circle cx="' + f(qh[0]) + '" cy="' + f(qh[1]) + '" r="' + (on2 ? 17 : 11) + '" fill="' + (on2 ? '#ffe7a8' : '#05070e') + '"/>';
        if (on2) geo += '<text x="' + f(qh[0]) + '" y="' + f(qh[1] + 6) + '" text-anchor="middle" font-size="16" fill="#1a1408" stroke="none" font-family="IBM Plex Mono, monospace">' + o.hour + '</text>';
      }
    }
    s += geo + '</g>';

    // outer rings of names
    var ring1 = (o.ring || (o.name.toUpperCase() + ' ✦ ')).repeat(1);
    var reps = Math.max(1, Math.round(2 * Math.PI * 452 / (ring1.length * 16)));
    s += '<circle r="470" fill="none" stroke="url(#' + id + 'gold)" stroke-width="1.4" opacity=".8"/><circle r="432" fill="none" stroke="url(#' + id + 'gold)" stroke-width=".8" opacity=".6"/>';
    s += ringText(id + 'r1', 446, new Array(reps + 1).join(ring1), 22, 'aa-ring1', false, '#f3dfa6');
    if (o.hebrew) {
      var hb = o.hebrew + ' · ' + (HEB_PLANET[planet] || '') + ' · ';
      var reps2 = Math.max(1, Math.round(2 * Math.PI * 412 / (hb.length * 15)));
      s += ringText(id + 'r2', 412, new Array(reps2 + 1).join(hb), 20, 'aa-ring2', true, '#d9c48c', 'Frank Ruhl Libre, David, Times New Roman, serif');
    }

    // wings: six for the angels of the days (after the seraphim of Isaiah 6:2), four for the angels of the hours
    var eyes = kind === 'day', wings = '<g class="aa-wings" filter="url(#' + id + 'soft)">';
    var W6 = [
      { s: [34, -118], c: [80, -270], w: [170, -300], a0: -0.85, a1: -2.05, l0: 110, l1: 200, n: 13 },   // upper pair, raised over the head
      { s: [58, -70], c: [180, -150], w: [270, -130], a0: 1.25, a1: -0.45, l0: 140, l1: 215, n: 15 },     // middle pair, spread
      { s: [52, 20], c: [150, 70], w: [200, 170], a0: 1.75, a1: 0.65, l0: 100, l1: 175, n: 12 }           // lower pair, folded downward
    ];
    var W4 = night ? [
      { s: [56, -96], c: [150, -240], w: [260, -230], a0: 0.75, a1: -1.0, l0: 140, l1: 225, n: 15 },
      { s: [52, 0], c: [160, 50], w: [230, 150], a0: 1.75, a1: 0.45, l0: 115, l1: 195, n: 13 }
    ] : [
      { s: [50, -104], c: [120, -280], w: [230, -300], a0: 0.2, a1: -1.5, l0: 130, l1: 225, n: 15 },
      { s: [58, -50], c: [190, -90], w: [270, -40], a0: 1.35, a1: 0.0, l0: 130, l1: 210, n: 14 }
    ];
    (kind === 'day' ? W6 : W4).forEach(function (w) {
      w.lite = o.lite; var one = wing(R, p, id, w, eyes);
      wings += '<g>' + one + '</g><g transform="scale(-1 1)">' + one + '</g>';
    });
    s += wings + '</g>';

    // glow, halo and the luminous figure in its mandorla
    s += '<g class="aa-glow"><circle cy="-40" r="210" fill="' + p[0] + '" opacity=".35" filter="url(#' + id + 'glow)"/></g>';
    s += '<ellipse cx="0" cy="40" rx="150" ry="300" fill="none" stroke="url(#' + id + 'gold)" stroke-width="2.5" opacity=".75"/><ellipse cx="0" cy="40" rx="162" ry="312" fill="none" stroke="url(#' + id + 'gold)" stroke-width=".8" opacity=".5"/>';
    var robe = 'M0 -96 C26 -96 40 -82 64 -72 C92 -60 96 -30 98 10 C104 120 124 220 150 300 Q0 334 -150 300 C-124 220 -104 120 -98 10 C-96 -30 -92 -60 -64 -72 C-40 -82 -26 -96 0 -96Z';
    s += '<path d="' + robe + '" fill="url(#' + id + 'body)"/>';
    var folds = '';
    for (i = -4; i <= 4; i++) folds += '<path d="M' + f(i * 12) + ' -40 C' + f(i * 16 + (R() - 0.5) * 12) + ' 80 ' + f(i * 24) + ' 200 ' + f(i * 32) + ' 305" stroke="' + p[1] + '" stroke-opacity=".22" stroke-width="2" fill="none"/>';
    s += folds;
    // gilded stole with small crosses, and the planet as a medallion on the breast
    s += '<path d="M-16 -88 L16 -88 L22 300 L-22 300Z" fill="url(#' + id + 'gold)" opacity=".85"/>';
    for (i = 0; i < 6; i++) { var cy = 40 + i * 44; s += '<path d="M-6 ' + cy + 'h12M0 ' + (cy - 6) + 'v12" stroke="#5a4214" stroke-width="2.4"/>'; }
    s += '<circle cy="-18" r="46" fill="#120d05" stroke="url(#' + id + 'gold)" stroke-width="4"/><circle cy="-18" r="38" fill="none" stroke="url(#' + id + 'gold)" stroke-width="1" opacity=".7"/>';
    if (o.medallion) s += '<text y="0" text-anchor="middle" font-size="' + (o.medallion.length > 2 ? 30 : 40) + '" fill="url(#' + id + 'gold)" font-family="Cormorant Garamond, Georgia, serif" font-weight="600" class="aa-glyph">' + esc(o.medallion) + '</text>';
    else s += '<text y="14" text-anchor="middle" font-size="62" fill="url(#' + id + 'gold)" class="aa-glyph">' + GLYPH[planet] + '</text>';
    s += '<circle cy="-150" r="150" fill="url(#' + id + 'halo)"/>';
    s += '<circle cy="-150" r="78" fill="none" stroke="url(#' + id + 'gold)" stroke-width="5"/><circle cy="-150" r="66" fill="none" stroke="url(#' + id + 'gold)" stroke-width="1" opacity=".7"/>';
    var pearls = '';
    for (i = 0; i < 24; i++) { var qp = pol(72, i / 24 * 6.283); pearls += '<circle cx="' + f(qp[0]) + '" cy="' + f(qp[1] - 150) + '" r="2.2" fill="#fff6dc"/>'; }
    s += pearls + '<circle cy="-150" r="44" fill="#fffdf4" opacity=".95" filter="url(#' + id + 'soft)"/>';
    if (o.subtitle) {
      s += '<path d="M-190 330 L-150 312 L150 312 L190 330 L150 348 L-150 348Z" fill="#120d05" stroke="url(#' + id + 'gold)" stroke-width="2.5"/>' +
           '<path d="M-150 312 L-170 300 L-232 318 L-196 330 L-232 342 L-150 348Z" fill="#0c0904" stroke="url(#' + id + 'gold)" stroke-width="2"/>' +
           '<path d="M150 312 L170 300 L232 318 L196 330 L232 342 L150 348Z" fill="#0c0904" stroke="url(#' + id + 'gold)" stroke-width="2"/>' +
           '<text y="338" text-anchor="middle" font-size="26" letter-spacing="7" fill="#f3dfa6" font-family="Cormorant Garamond, Georgia, serif" font-weight="600">' + esc(o.subtitle.toUpperCase()) + '</text>';
    }
    s += '</g></svg>';
    return s;
  }

  /* seal({name, lines: [ring text], planet}) -> SVG: a seal drawn from the letters of the name on a rose of the alphabet. */
  function seal(o) {
    var id = 'as' + (++uid) + '_', p = HUE[o.planet || 'Sun'], R0 = 150, letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    var pos = {}; letters.split('').forEach(function (c, i) { pos[c] = pol(R0, -Math.PI / 2 + i / 26 * 2 * Math.PI); });
    var seq = o.name.toUpperCase().replace(/[^A-Z]/g, '').split('').filter(function (c, i, a) { return i === 0 || c !== a[i - 1]; });
    var d = seq.map(function (c, i) { var q = pos[c]; return (i ? 'L' : 'M') + f(q[0]) + ' ' + f(q[1]); }).join('');
    var a = pos[seq[0]], z = pos[seq[seq.length - 1]], b = seq.length > 1 ? pos[seq[seq.length - 2]] : [0, 0];
    var ang = Math.atan2(z[1] - b[1], z[0] - b[0]), bx = -Math.sin(ang) * 14, by = Math.cos(ang) * 14;
    var s = '<svg class="as" viewBox="-250 -250 500 500" role="img" aria-label="' + esc('A seal drawn from the letters of ' + o.name) + '"><defs><linearGradient id="' + id + 'g" x1="0" y1="-1" x2="0" y2="1"><stop offset="0" stop-color="#fff4cc"/><stop offset="1" stop-color="#b8903f"/></linearGradient>' +
      '<filter id="' + id + 'f"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>' +
      '<circle r="245" fill="#06080f"/><circle r="236" fill="none" stroke="url(#' + id + 'g)" stroke-width="3"/><circle r="198" fill="none" stroke="url(#' + id + 'g)" stroke-width="1.2"/>';
    s += ringText(id + 'r', 216, o.lines.join(' ✦ ') + ' ✦ ', 17, 'as-ring', false, '#e9d49a', 'IBM Plex Mono, monospace');
    letters.split('').forEach(function (c) { var q = pos[c], on = seq.indexOf(c) >= 0; s += '<text x="' + f(q[0] * 1.13) + '" y="' + f(q[1] * 1.13 + 5) + '" text-anchor="middle" font-size="14" fill="' + (on ? '#ffe7a8' : '#4b5470') + '" font-family="Cormorant Garamond, Georgia, serif">' + c + '</text>'; });
    s += '<circle r="' + R0 + '" fill="none" stroke="#2a3858" stroke-width="1"/>';
    s += '<text y="26" text-anchor="middle" font-size="76" fill="' + p[0] + '" opacity=".22">' + GLYPH[o.planet || 'Sun'] + '</text>';
    s += '<g filter="url(#' + id + 'f)"><path class="as-line" d="' + d + '" fill="none" stroke="url(#' + id + 'g)" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round" pathLength="1000"/>' +
         '<circle cx="' + f(a[0]) + '" cy="' + f(a[1]) + '" r="8" fill="none" stroke="#ffe7a8" stroke-width="3"/>' +
         '<path d="M' + f(z[0] - bx) + ' ' + f(z[1] - by) + 'L' + f(z[0] + bx) + ' ' + f(z[1] + by) + '" stroke="#ffe7a8" stroke-width="3.4" stroke-linecap="round"/></g></svg>';
    return s;
  }

  window.DSAngelArt = { angel: angel, seal: seal, GLYPH: GLYPH, HUE: HUE };
})();
