/* Discovery Science: lightweight outbound-click measurement.
   - Loads Vercel Web Analytics (cookieless) if the page has not already loaded it.
   - Records a custom event when a visitor clicks a Google Play, App Store or other external link.
     Event data: the page path, plus the app id or external host. No personal data, no cookies.
   - Adds a Google Play install-referrer (utm_source/utm_medium/utm_campaign) to Play listing links at
     click time, so Play Console's acquisition reports can attribute store-listing visits to the page.
   An outbound click is NOT an install or a purchase. */
(function () {
  if (window.__dsTrack) return;
  window.__dsTrack = 1;
  window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
  if (!document.querySelector('script[src="/_vercel/insights/script.js"]')) {
    var s = document.createElement('script');
    s.defer = true;
    s.src = '/_vercel/insights/script.js';
    document.head.appendChild(s);
  }
  var page = location.pathname.replace(/\/index\.html$/, '/') || '/';
  var campaign = page === '/' ? 'home' : page.replace(/^\/|\.html$/g, '').replace(/\//g, '-');

  function parse(a) {
    try {
      var u = new URL(a.href, location.href);
      if (u.hostname === 'play.google.com' && /^\/store\/apps\/details/.test(u.pathname) && !u.searchParams.get('referrer')) {
        u.searchParams.set('referrer', 'utm_source=discovery-science.com&utm_medium=website&utm_campaign=' + campaign);
        a.href = u.toString();
      }
      return u;
    } catch (e) { return null; }
  }
  function link(e) { return e.target && e.target.closest ? e.target.closest('a[href]') : null; }

  function prime(e) { var a = link(e); if (a) parse(a); }
  function record(e) {
    if (e.type === 'auxclick' && e.button !== 1) return;
    var a = link(e);
    if (!a) return;
    var u = parse(a);
    if (!u || !/^https?:$/.test(u.protocol) || u.hostname === location.hostname) return;
    var name, data = { page: page };
    if (u.hostname === 'play.google.com') {
      var id = u.searchParams.get('id');
      name = id ? 'Play Click' : 'Play Developer Click';
      if (id) data.app = id;
    } else if (u.hostname === 'apps.apple.com') {
      name = 'App Store Click';
      data.app = u.pathname.split('/').pop();
    } else {
      name = 'Outbound Click';
      data.host = u.hostname;
    }
    try { window.va('event', { name: name, data: data }); } catch (err) { /* never block navigation */ }
  }
  document.addEventListener('mousedown', prime, true);
  document.addEventListener('touchstart', prime, { capture: true, passive: true });
  document.addEventListener('contextmenu', prime, true);
  document.addEventListener('click', record, true);
  document.addEventListener('auxclick', record, true);
})();
