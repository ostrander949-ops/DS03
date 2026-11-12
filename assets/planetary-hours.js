/* Planetary hours calculator. Runs entirely in the browser; nothing is sent anywhere.
   Sunrise/sunset: the simplified NOAA sunrise equation (upper limb, standard refraction -0.833°). */
(function () {
  var ORDER = ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon'];
  var GLYPH = { Saturn: '♄', Jupiter: '♃', Mars: '♂', Sun: '☉', Venus: '♀', Mercury: '☿', Moon: '☽' };
  var DAY_RULER = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']; // Sunday..Saturday
  var DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  var $ = function (id) { return document.getElementById(id); };
  var form = $('ph-form');
  if (!form) return;
  var dateIn = $('ph-date'), riseIn = $('ph-rise'), setIn = $('ph-set'), nextIn = $('ph-next');
  var note = $('ph-note'), body = $('ph-out').querySelector('tbody'), cap = $('ph-cap');

  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function hm(d) { return pad(d.getHours()) + ':' + pad(d.getMinutes()); }
  function isoDate(d) { return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
  function parseDate(v) { var p = v.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function at(day, t) { var p = t.split(':'); var d = new Date(day); d.setHours(+p[0], +p[1], 0, 0); return d; }

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

  function render(day, rise, set, next) {
    body.innerHTML = '';
    if (!(rise < set && set < next)) {
      note.textContent = 'Check the times: sunrise must come before sunset, and sunset before the next sunrise.';
      cap.textContent = '';
      return;
    }
    var dayLen = (set - rise) / 12, nightLen = (next - set) / 12;
    var first = ORDER.indexOf(DAY_RULER[day.getDay()]);
    var now = new Date(), rows = '';
    for (var i = 0; i < 24; i++) {
      var s = i < 12 ? new Date(+rise + i * dayLen) : new Date(+set + (i - 12) * nightLen);
      var e = i < 12 ? new Date(+rise + (i + 1) * dayLen) : new Date(+set + (i - 11) * nightLen);
      var p = ORDER[(first + i) % 7];
      var cur = now >= s && now < e;
      rows += '<tr' + (cur ? ' class="now" aria-current="time"' : '') + '><td>' + (i < 12 ? 'Day ' + (i + 1) : 'Night ' + (i - 11)) +
        '</td><td>' + hm(s) + '</td><td>' + hm(e) + '</td><td class="pl">' + GLYPH[p] + ' ' + p + (cur ? ' · now' : '') + '</td></tr>';
    }
    body.innerHTML = rows;
    cap.textContent = DAYS[day.getDay()] + ', ruled by ' + DAY_RULER[day.getDay()] +
      ' · day-hours ' + Math.round(dayLen / 6e4) + ' min · night-hours ' + Math.round(nightLen / 6e4) + ' min';
  }

  function fromInputs() {
    if (!dateIn.value) return;
    var day = parseDate(dateIn.value);
    var next = new Date(day); next.setDate(next.getDate() + 1);
    note.textContent = note.dataset.keep ? note.textContent : '';
    delete note.dataset.keep;
    render(day, at(day, riseIn.value), at(day, setIn.value), at(next, nextIn.value));
  }

  function fromLocation(lat, lon) {
    var day = parseDate(dateIn.value || isoDate(new Date()));
    var nd = new Date(day); nd.setDate(nd.getDate() + 1);
    var a = sun(day.getFullYear(), day.getMonth() + 1, day.getDate(), lat, lon);
    var b = sun(nd.getFullYear(), nd.getMonth() + 1, nd.getDate(), lat, lon);
    if (!a || !b) {
      body.innerHTML = ''; cap.textContent = '';
      note.textContent = 'At this latitude the Sun does not both rise and set on this date, so there are no planetary hours to divide.';
      return;
    }
    riseIn.value = hm(a.rise); setIn.value = hm(a.set); nextIn.value = hm(b.rise);
    note.textContent = 'Sunrise and sunset calculated on this device for ' + lat.toFixed(2) + '°, ' + lon.toFixed(2) + '°. Edit any time to adjust.';
    note.dataset.keep = '1';
    fromInputs();
  }

  dateIn.value = isoDate(new Date());
  $('ph-go').addEventListener('click', fromInputs);
  [dateIn, riseIn, setIn, nextIn].forEach(function (el) { el.addEventListener('change', fromInputs); });
  $('ph-geo').addEventListener('click', function () {
    if (!navigator.geolocation) { note.textContent = 'This browser cannot share a location. Enter the times by hand.'; return; }
    note.textContent = 'Asking your device for its location…';
    navigator.geolocation.getCurrentPosition(function (pos) {
      fromLocation(pos.coords.latitude, pos.coords.longitude);
    }, function () {
      note.textContent = 'Location was not shared. Enter sunrise and sunset by hand.';
    }, { maximumAge: 0, timeout: 15000 });
  });
  fromInputs();
  window.__phSun = sun; // exposed for testing
})();
