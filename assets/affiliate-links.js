/* Discovery Science affiliate links: the ONE place to add affiliate IDs.
 *
 * Every product link on /gifts/* carries data-product="<key>" and data-merchant="<program>".
 * Until a program approves you, leave its value empty: links stay plain product URLs.
 *
 * 1) Amazon Associates: put your NEW Store ID in amazonTag (e.g. "yourname-20").
 *    Do NOT use the old closed tag. Every data-merchant="amazon" link gets ?tag=<id>.
 * 2) Other programs (Gaiam, Healing Sounds, HubSpot, Pipedrive, Chewy, Etsy...) give you
 *    a per-product tracking/deep link. Paste it in overrides under the product key,
 *    e.g. overrides["gaiam-zafu"] = "https://<network deep link>".
 * Keys are listed in /gifts/products.json.
 */
window.DS_AFFILIATE = {
  amazonTag: "",
  overrides: {
    // "gaiam-zafu": "",
    // "hs-solfeggio-9": "",
    // "hs-otto-4": "",
    // "hubspot-crm": "",
    // "pipedrive": ""
  }
};
(function () {
  var cfg = window.DS_AFFILIATE || {};
  var links = document.querySelectorAll("a[data-product]");
  for (var i = 0; i < links.length; i++) {
    var a = links[i], key = a.getAttribute("data-product"), m = a.getAttribute("data-merchant");
    var o = cfg.overrides && cfg.overrides[key];
    if (o) { a.href = o; continue; }
    if (m === "amazon" && cfg.amazonTag) {
      try { var u = new URL(a.href); u.searchParams.set("tag", cfg.amazonTag); a.href = u.toString(); } catch (e) {}
    }
  }
})();
