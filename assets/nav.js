/* Phone menu for pages with a written-in <nav> (see tools/apply_nav.py) */
(function () {
  var btn = document.querySelector('.ds-menu'), list = document.getElementById('ds-links');
  if (!btn || !list) return;
  btn.addEventListener('click', function () { var open = list.classList.toggle('open'); btn.setAttribute('aria-expanded', open); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { list.classList.remove('open'); btn.setAttribute('aria-expanded', false); } });
})();
