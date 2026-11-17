/* Compact ephemeris for the Sun, Moon and five classical planets, after Paul Schlyter's
   "How to compute planetary positions" (orbital elements with the main perturbations).
   Accuracy is about a degree or better for the Moon and a few arcminutes for the planets:
   ample for a compass direction and an altitude. Exposes window.DSEphemeris.altAz(planet, date, lat, lon). */
(function (root) {
  'use strict';
  var RAD = Math.PI / 180;
  function rev(x) { return x - Math.floor(x / 360) * 360; }
  function sind(x) { return Math.sin(x * RAD); }
  function cosd(x) { return Math.cos(x * RAD); }
  function atan2d(y, x) { return Math.atan2(y, x) / RAD; }

  function elements(name, d) {
    switch (name) {
      case 'Sun': return { N: 0, i: 0, w: 282.9404 + 4.70935e-5 * d, a: 1, e: 0.016709 - 1.151e-9 * d, M: 356.0470 + 0.9856002585 * d };
      case 'Moon': return { N: 125.1228 - 0.0529538083 * d, i: 5.1454, w: 318.0634 + 0.1643573223 * d, a: 60.2666, e: 0.0549, M: 115.3654 + 13.0649929509 * d };
      case 'Mercury': return { N: 48.3313 + 3.24587e-5 * d, i: 7.0047 + 5.0e-8 * d, w: 29.1241 + 1.01444e-5 * d, a: 0.387098, e: 0.205635 + 5.59e-10 * d, M: 168.6562 + 4.0923344368 * d };
      case 'Venus': return { N: 76.6799 + 2.4659e-5 * d, i: 3.3946 + 2.75e-8 * d, w: 54.891 + 1.38374e-5 * d, a: 0.72333, e: 0.006773 - 1.302e-9 * d, M: 48.0052 + 1.6021302244 * d };
      case 'Mars': return { N: 49.5574 + 2.11081e-5 * d, i: 1.8497 - 1.78e-8 * d, w: 286.5016 + 2.92961e-5 * d, a: 1.523688, e: 0.093405 + 2.516e-9 * d, M: 18.6021 + 0.5240207766 * d };
      case 'Jupiter': return { N: 100.4542 + 2.76854e-5 * d, i: 1.303 - 1.557e-7 * d, w: 273.8777 + 1.64505e-5 * d, a: 5.20256, e: 0.048498 + 4.469e-9 * d, M: 19.895 + 0.0830853001 * d };
      case 'Saturn': return { N: 113.6634 + 2.3898e-5 * d, i: 2.4886 - 1.081e-7 * d, w: 339.3939 + 2.97661e-5 * d, a: 9.55475, e: 0.055546 - 9.499e-9 * d, M: 316.967 + 0.0334442282 * d };
    }
  }
  function orbit(el) {
    var M = rev(el.M), E = M + (180 / Math.PI) * el.e * sind(M) * (1 + el.e * cosd(M));
    for (var k = 0; k < 8; k++) E = E - (E - (180 / Math.PI) * el.e * sind(E) - M) / (1 - el.e * cosd(E));
    var x = el.a * (cosd(E) - el.e), y = el.a * Math.sqrt(1 - el.e * el.e) * sind(E);
    var r = Math.sqrt(x * x + y * y), v = atan2d(y, x);
    var N = el.N, i = el.i, w = el.w;
    return {
      r: r,
      x: r * (cosd(N) * cosd(v + w) - sind(N) * sind(v + w) * cosd(i)),
      y: r * (sind(N) * cosd(v + w) + cosd(N) * sind(v + w) * cosd(i)),
      z: r * sind(v + w) * sind(i)
    };
  }
  function dayNumber(date) { return date.getTime() / 864e5 + 2440587.5 - 2451543.5; }

  // Geocentric equatorial RA/Dec in degrees
  function radec(name, date) {
    var d = dayNumber(date), ecl = 23.4393 - 3.563e-7 * d;
    var sun = elements('Sun', d), so = orbit(sun), lonsun = rev(atan2d(so.y, so.x));
    var xs = so.r * cosd(lonsun), ys = so.r * sind(lonsun), xg, yg, zg;
    if (name === 'Sun') { xg = xs; yg = ys; zg = 0; }
    else {
      var el = elements(name, d), o = orbit(el);
      var lon = atan2d(o.y, o.x), lat = atan2d(o.z, Math.sqrt(o.x * o.x + o.y * o.y)), r = o.r;
      var Ms = rev(sun.M), Mj = rev(19.895 + 0.0830853001 * d), Msat = rev(316.967 + 0.0334442282 * d);
      if (name === 'Moon') {
        var Mm = rev(el.M), Ls = rev(sun.M + sun.w), Lm = rev(el.M + el.w + el.N), D = Lm - Ls, F = Lm - el.N;
        lon += -1.274 * sind(Mm - 2 * D) + 0.658 * sind(2 * D) - 0.186 * sind(Ms) - 0.059 * sind(2 * Mm - 2 * D) - 0.057 * sind(Mm - 2 * D + Ms)
             + 0.053 * sind(Mm + 2 * D) + 0.046 * sind(2 * D - Ms) + 0.041 * sind(Mm - Ms) - 0.035 * sind(D) - 0.031 * sind(Mm + Ms)
             - 0.015 * sind(2 * F - 2 * D) + 0.011 * sind(Mm - 4 * D);
        lat += -0.173 * sind(F - 2 * D) - 0.055 * sind(Mm - F - 2 * D) - 0.046 * sind(Mm + F - 2 * D) + 0.033 * sind(F + 2 * D) + 0.017 * sind(2 * Mm + F);
        r += -0.58 * cosd(Mm - 2 * D) - 0.46 * cosd(2 * D);
        // geocentric already (Earth radii); convert to rectangular, no Sun offset
        xg = r * cosd(lon) * cosd(lat); yg = r * sind(lon) * cosd(lat); zg = r * sind(lat);
      } else {
        if (name === 'Jupiter') lon += -0.332 * sind(2 * Mj - 5 * Msat - 67.6) - 0.056 * sind(2 * Mj - 2 * Msat + 21) + 0.042 * sind(3 * Mj - 5 * Msat + 21)
             - 0.036 * sind(Mj - 2 * Msat) + 0.022 * cosd(Mj - Msat) + 0.023 * sind(2 * Mj - 3 * Msat + 52) - 0.016 * sind(Mj - 5 * Msat - 69);
        if (name === 'Saturn') {
          lon += 0.812 * sind(2 * Mj - 5 * Msat - 67.6) - 0.229 * cosd(2 * Mj - 4 * Msat - 2) + 0.119 * sind(Mj - 2 * Msat - 3)
               + 0.046 * sind(2 * Mj - 6 * Msat - 69) + 0.014 * sind(Mj - 3 * Msat + 32);
          lat += -0.02 * cosd(2 * Mj - 4 * Msat - 2) + 0.018 * sind(2 * Mj - 6 * Msat - 49);
        }
        xg = r * cosd(lon) * cosd(lat) + xs; yg = r * sind(lon) * cosd(lat) + ys; zg = r * sind(lat);
      }
    }
    var xe = xg, ye = yg * cosd(ecl) - zg * sind(ecl), ze = yg * sind(ecl) + zg * cosd(ecl);
    return { ra: rev(atan2d(ye, xe)), dec: atan2d(ze, Math.sqrt(xe * xe + ye * ye)), d: d, sunM: sun.M, sunW: sun.w };
  }

  // Altitude and azimuth (degrees, azimuth from north through east) for an observer
  function altAz(name, date, lat, lon) {
    var p = radec(name, date);
    var Ls = rev(p.sunM + p.sunW), ut = (date.getUTCHours() + date.getUTCMinutes() / 60 + date.getUTCSeconds() / 3600);
    var lst = rev(Ls + 180 + ut * 15 + lon), ha = lst - p.ra;
    var x = cosd(ha) * cosd(p.dec), y = sind(ha) * cosd(p.dec), z = sind(p.dec);
    var xh = x * sind(lat) - z * cosd(lat), zh = x * cosd(lat) + z * sind(lat);
    var az = rev(atan2d(y, xh) + 180), alt = atan2d(zh, Math.sqrt(xh * xh + y * y));
    if (name === 'Moon') alt -= 0.95 * cosd(alt); // approximate topocentric parallax
    return { alt: alt, az: az, ra: p.ra, dec: p.dec };
  }

  var api = { altAz: altAz, radec: radec };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.DSEphemeris = api;
})(this);
