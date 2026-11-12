# DISCOVERY_SCIENCE_SEO_HANDOFF.md

Prepared 2026-11-12 by Claude (Claude Code) for independent review by ChatGPT.
Scope: technical SEO, app landing pages, organic content and Google Play click measurement for https://www.discovery-science.com.

**Status in one paragraph.** The live site was not in any GitHub repository. It is deployed by the Vercel CLI from a local folder, across **two** Vercel projects (`ds-03` and `ds-home`) joined by nine project-level rewrite rules. I reconstructed the exact production files and verified them byte-for-byte against Vercel's deploy hashes. I committed that snapshot, then implemented and validated the SEO changes on a branch. **Nothing has been deployed or pushed yet.** Pushing is blocked because the Claude GitHub App is not installed on the repository, and the deploy needs owner actions, described in section F.

---

## A. Project identification

| Item | Finding |
|---|---|
| Primary domain | `https://www.discovery-science.com` (apex `discovery-science.com` redirects to www with a **307**) |
| Vercel team | `discovery-sciences-projects` (`team_r3As3Lwzc4j1H5JMMBCNaUa6`) |
| Vercel project (production domain) | `ds-03`, ID `prj_dNJRxR0TDu8HP1xrTjycWi4nGI5P`, framework: none (static HTML) |
| Current production deployment | `dpl_GBzT2mpnucoV2fvdwLgPZSpTWwme`, source: **CLI** (no Git link) |
| Second project in the request path | `ds-home`, ID `prj_ImNfPRA3mp2dH5y92boJPEm4wFqU`, deployment `dpl_5SfAxuJEh4CLCwFmrWdDCjf9ebtn`, also CLI-deployed; static files plus 3 serverless functions (`api/app.js`, `api/apps.js`, `api/archive.js`) |
| GitHub repository | `https://github.com/ostrander949-ops/DS03`. **It did not contain the live site before this work.** Its previous contents were an older, unrelated site (a "neuroregulation / mental fitness" site, last deployed to production months ago). Those files are preserved under `legacy-monty-site/` and excluded from deploys. |
| Work branch | `seo/production-sync-and-technical-seo` (2 commits on top of `176e851`) |

### Request routing (verified via the Vercel API)
`ds-03` has 9 project-level rewrites that proxy these paths to `ds-home.vercel.app`:
`/`, `/index.html`, `/sitemap.xml`, `/app/*.html`, `/archive(.html)` (www host only), `/almanac`, `/library.html`, `/catalog.html`, `/seven-angels.html`, `/new.html`, `/shop.html`, `/asclepion`, `/site.css`, `/sigil.js`, `/apps.css`, `/assets/ds-extra.css`.

`ds-home/vercel.json` then rewrites `/app/:slug.html` to `/api/app`, `/new.html` to `/api/apps` and `/archive.html` to `/api/archive`. `api/app.js` holds its own embedded copy of the app-page data.

**Key verification:** every URL the site serves today is byte-identical to the file of the same name in the `ds-03` deployment. The only exception is `/archive.html`, where `ds-home` wraps ds-03's archive and adds chapters XVI–XVII. I captured that served version. The repository root therefore reproduces the entire live site as plain static files.

**Consequence:** while the nine rewrites exist, edits to the rewritten paths (homepage, sitemap, app pages, archive and so on) **will not go live** from `ds-03` alone. See F.

Other repos named DiscoveryScience, Discovery-Science, Discovery-Science01 and DS02 are older experiments; none is connected to production.

---

## B. SEO audit (before changes)

### Analytics reality check (Vercel Web Analytics, 2026-10-13 → 11-12)
- 124 of ~130 visitors have **no referrer**: direct visits, apps, or stripped referrers. Organic Google: **1 visit**. Google Scholar: **4 visits**, all to legacy `/papers/*` URLs that now return 404.
- Top paths: `/apkallu-privacy.html` 24 visitors (almost certainly from the Google Play listing's privacy link, not search), `/archive.html` 23, `/` 14, `/entrainment.html` 14 (the brief's "entertainment.html" is this page), then legacy URLs (`/about.html`, `/how-it-works.html`, `/programs.html`, `/publications.html`, `/papers/*`).
- **Measurement gap:** the homepage, all 35 `/app/*.html` pages, `/new.html`, `/catalog.html`, `/library.html`, `/almanac.html`, `/seven-angels.html` and `/shop.html` **do not load Vercel Analytics at all**. They use `sigil.js`, which has no analytics loader. Only the older-design pages (`assets/site.js`) were measured, so the "125 visitors" figure undercounts and the page ranking is skewed toward older pages.
- Custom events recorded to date: **0**.

### Technical issues found
| # | Issue | Severity |
|---|---|---|
| 1 | Live source exists only in Vercel CLI uploads, split across two projects with rewrites; no version control | High (operational) |
| 2 | Sitemap (served from ds-home) listed 42 URLs and **omitted** `/angels.html`, `/obe.html`, `/oracle.html`, `/neuro.html`, `/entrainment.html`, `/google-play.html`, `/catalog.html`, `/apps.html` and all 8 collection app pages (`/spirit-drum.html`, `/ekstasis.html`, `/kispu.html`, `/dhikr.html`, `/divining-vessel.html`, `/theurgia.html`, `/planetary-attunement.html`, `/asclepion.html`) | High |
| 3 | Missing canonicals on `/angels.html`, `/archive.html`, `/apps.html`, `/entrainment.html`, `/google-play.html`, `/neuro.html`, `/obe.html`, `/oracle.html` and all 23 privacy pages | Medium |
| 4 | Duplicate titles: `apps.html` and `library.html` ("The Library — Discovery Science"); `catalog.html` and `new.html` ("The Apps — Discovery Science") | Medium |
| 5 | `catalog.html` had no `<h1>` and its `og:url` pointed at the homepage (it is the former homepage) | Medium |
| 6 | **About 180 links across 37 pages** (app-page nav "The State", "EEG", "Coming Soon", breadcrumbs `/#gods` and similar) pointed at homepage anchors that moved to `catalog.html`, so visitors landed at the top of the new homepage | Medium (UX/engagement) |
| 7 | Legacy URLs from the old site return 404 but still receive visits (and Scholar referrals) | Medium |
| 8 | Apex domain redirects with **307** (temporary) instead of 308/301 | Low–Medium |
| 9 | 13 of 23 privacy pages had no meta description; privacy pages were dead ends with no link to the app | Low (but they are the top entry page) |
| 10 | No Organization/WebSite structured data; app pages had `MobileApplication` + `FAQPage` JSON-LD but no breadcrumbs | Low |
| 11 | `404.html` not marked noindex | Low |
| 12 | Three overlapping "all apps" hubs (`new.html`, `apps.html`, `google-play.html`) plus `catalog.html` | Low–Medium (cannibalisation) |

### Not problems (checked)
- `robots.txt` is correct (`Allow: /` plus a Sitemap line). Unchanged.
- All 60 Google Play package IDs linked from the site resolve to live listings (checked 2026-11-12).
- Images already have `alt` text; below-the-fold images already use `loading="lazy"`.
- Privacy pages are **not** blocked and should stay indexable. Google Play requires a reachable policy URL, and a policy page is legitimate content. They are left out of the sitemap (low search value) but not noindexed.

---

## C. Implemented changes (branch `seo/production-sync-and-technical-seo`)

All edits are made by `tools/apply_seo.py` (re-runnable, standard library only) and validated by `tools/seo_check.py`.

| File(s) | What changed | Why | Validation |
|---|---|---|---|
| repo root | Replaced old repo contents with the exact production site; old site moved to `legacy-monty-site/` | Make the repo the source of truth | `diff -r` against the live mirror: identical; 94 files SHA-1-verified against Vercel deploy hashes |
| `.vercelignore` | Excludes `legacy-monty-site`, `tools`, `*.md` | Keep non-site files out of deploys | n/a |
| `sitemap.xml` | 58 indexable canonical URLs (was 42). Adds the hubs, `obe`, `oracle`, `neuro`, `entrainment`, `google-play`, `catalog`, `apps`, the 8 collection app pages and the new guide. Excludes privacy pages, 404 and `app/obe-induction.html` (canonicalised to `/obe.html`) | Discovery of commercially useful pages | Checker: every `<loc>` exists, is self-canonical and not noindex |
| 23 hub/landing pages (`angels`, `archive`, `apps`, `library`, `catalog`, `new`, `entrainment`, `neuro`, `obe`, `oracle`, `seven-angels`, `almanac`, `planetary-attunement` and others) | Unique, keyword-led titles; tightened descriptions where weak or overlong; self-canonical; `og:url`/`og:type`/`og:site_name`/`twitter:card` | Fix duplicates (#4) and missing canonicals (#3); better SERP snippets | 0 duplicate titles; 0 checker errors |
| `catalog.html` | First heading promoted from `h2` to `h1` (computed styles identical); `og:url` fixed | #5 | Playwright: computed margin, size and line-height identical to before |
| `index.html` | `Organization` + `WebSite` JSON-LD (only verifiable facts: name, URL, email, existing social/Play profiles); footer link to the new guide | Entity understanding | JSON-LD parses |
| 35 × `app/*.html` | `BreadcrumbList` JSON-LD; Archive in nav and footer; new "The history behind it" block linking each app to the Archive chapter that already links to it (mapping taken from the archive's own links) and to the planetary-hours guide where relevant | Two-way links between educational and commercial pages | Visual check: block reuses the page's own `.rel` style |
| `app/obe-induction.html` | Canonical points to `/obe.html` (the 2,200-word flagship page for the same app, `com.discoveryscience.ritual`) | Consolidate two pages targeting the same app | Checker reports the intentional cross-canonical |
| 37 pages | `href="/#state"`, `/#eeg-editions`, `/#gods` etc. repointed to `/catalog.html#…`; "Coming Soon" now goes to `/new.html`. Labels unchanged | #6 | Fragment checker: all target IDs exist |
| 23 privacy pages | Self-canonical; meta description where missing; one line at the end: "About {App} and the other Discovery Science apps →". **Policy text untouched; no scripts added** | #9; turns the top entry page into a path to the app | Visual diff: only the added line |
| `404.html` | `noindex` | #11 | n/a |
| `archive.html` | Link from the planetary-hours chapter to the new guide | Internal linking | n/a |
| `vercel.json` (new, ds-03) | 301s: `/about.html`, `/contact.html`, `/how-it-works.html` → `/`; `/publications.html`, `/resources.html` → `/library.html` | Recover legacy visits (#7) | **Needs verification after deploy** |
| `planetary-hours.html` + `assets/planetary-hours.js` (new) | Study guide (see D) with a no-dependency calculator. Manual sunrise/sunset entry, or opt-in device location with on-device NOAA sunrise math; nothing is transmitted. Article, BreadcrumbList and FAQPage JSON-LD | Organic content tied to six apps | Calculator matches hand computation; sunrise matches almanac values for London, New York and Sydney within ~1 min; polar and invalid input handled |
| `assets/track.js` (new), included on all non-privacy pages | See E | Conversion measurement | Playwright: correct events and URL tagging; analytics script loaded exactly once |

**Regression testing (Playwright, desktop 1366px and phone 390px, 22 pages, old vs new):** pages with head-only edits render **pixel-identical**. The differences that exist are the intended additions. No new JavaScript errors, and no horizontal scroll at 390px.

**Not changed:** pricing, Play links and package IDs, app functionality, design system, policy wording, `robots.txt`, the `ds-home` serverless functions (their full source cannot be downloaded through the Vercel API; see F).

---

## D. Content and keyword strategy

Principle: improve and connect existing material first. The 93 KB Archive is strong, well-sourced content, but it is one omnibus URL and cannot rank for many distinct queries. Spin focused guides out of it only where an app matches the search intent.

| Target page | Primary search intent | Keyword theme | Related app(s) | Recommended internal links | Status |
|---|---|---|---|---|---|
| `/planetary-hours.html` **(new)** | Informational + tool ("what are planetary hours", "how to calculate planetary hours", "planetary hours calculator", "planetary hours today") | planetary hours, Chaldean order, unequal hours, planetary day rulers | Ars Astrorum, Celestial Above, Celestial Veil, Planetary Attunement, Angelarium, Ars Paulina, Seven Angels | From Archive §V/§VI, the six app pages, homepage footer; out to the apps, `/seven-angels.html`, the Archive | **Done**. Evidence, tradition and modern practice are labelled throughout; sources cited (Cassius Dio 37.18–19; Picatrix eds. Pingree and Attrell–Porreca; Peterson's Lemegeton; Agrippa ed. Perrone Compagni; Zerubavel; Dohrn-van Rossum) |
| `/seven-angels.html` | "seven planetary angels", "angels of the days" | Michael, Gabriel, Samael, Raphael, Sachiel, Anael, Cassiel; Heptameron | 7 angel apps | ↔ planetary-hours guide; Archive §VI | Title/meta improved. **Next:** add a short Heptameron history section above the app grid |
| Ars Paulina guide (proposed `/ars-paulina.html`) | "Ars Paulina", "Lemegeton book III", "angels of the hours" | Lemegeton, hour angels | Ars Paulina: A Book of Hours (`com.discoveryscience.arspaulina`, currently has no landing page) | Archive §VI, §XVI; planetary hours | Proposed. Also the most obvious missing app landing page |
| Picatrix guide (proposed) | "Picatrix", "Ghayat al-Hakim", "planetary talismans" | astral magic, Picatrix | Rites of Magic, Celestial Above | Archive §V | Proposed. Archive §V already holds the core text |
| `/app/apkallu.html` + Archive §IX | "apkallu", "seven sages Mesopotamia", "KAR 298" | apkallu, Mesopotamian protective spirits | APKALLU | apkallu-privacy → app page (done); Archive §IX ↔ app | Linked. **Next:** expand the app page with the Nimrud and KAR 298 context already written in `assets/site.js` |
| `/app/enochian-calls.html` + Archive §III | "Enochian angels", "John Dee Enochian calls" | Dee, Kelley, 48 Calls, Aethyrs | Enochian Calls | Archive §III ↔ app (done) | Linked |
| `/app/hekhalot-the-seven-palaces.html`, `/app/merkavah-ezekiels-chariot.html` + Archive §II | "Hekhalot literature", "Merkavah mysticism" | Hekhalot Rabbati, 3 Enoch, Ezekiel 1 | Hekhalot, Merkavah | Archive §II ↔ apps (done) | Linked |
| Heptameron | "Heptameron Peter of Abano" | Heptameron correspondences | Angelarium, Celestial Veil, Seven Angels | Covered inside the planetary-hours guide for now | Fold in; avoid a thin duplicate page |
| Ancient ritual calendars / historical planetary timing | broad, low intent | calendars, hemerologies | weak app match | — | **Deprioritised**: overlaps the planetary-hours guide; would produce a thin, duplicative page |

Every new page must keep the Archive's standard: name the source, label tradition versus evidence, and never claim efficacy.

---

## E. Conversion tracking

**Implemented:** `assets/track.js` (2 KB, no dependencies, no cookies, no personal data), loaded on all non-privacy pages.

| Event (Vercel Web Analytics custom event) | Fired when | Data |
|---|---|---|
| `Play Click` | Click on a `play.google.com/store/apps/details` link | `page` (path), `app` (package ID) |
| `Play Developer Click` | Click on the Play developer page | `page` |
| `App Store Click` | Click on an `apps.apple.com` link | `page`, `app` (Apple ID) |
| `Outbound Click` | Any other external link (Etsy, Gumroad, AppSumo, YouTube…) | `page`, `host` |

**Google Play install-referrer tagging:** at click time, Play listing links get `&referrer=utm_source=discovery-science.com&utm_medium=website&utm_campaign=<page-slug>`. Example: `campaign=app-apkallu` or `planetary-hours`. Play Console's store-listing acquisition reports can then attribute listing visits, and installs where Play reports them, to the referring page. This is free and independent of the Vercel plan.

**How to answer the four questions:**
1. *Which landing pages attract visitors:* Vercel Analytics → Pages. This now includes the homepage and app pages for the first time.
2. *Which apps generate download-link clicks:* Vercel → Events → `Play Click`, broken down by `app`.
3. *Which content pages lead toward apps:* `Play Click` broken down by `page`, plus Play Console acquisition by `utm_campaign`.
4. *Which traffic sources engage most:* Vercel events can be filtered by `referrerHostname` and `utm_*`.

**An outbound click is not an install or a purchase.** Only Play Console data speaks to installs.

**Requires verification:**
- **Vercel custom events need a Pro (or Enterprise) plan.** I could not read this team's plan through the API. On Hobby, `va('event')` calls are ignored without error; pageviews and the Play referrer tagging still work.
- **Baseline break:** once deployed, pageviews from the homepage and 35 app pages start being counted for the first time. Visitor numbers will jump for measurement reasons, not traffic reasons. Compare like-for-like paths only.
- Confirm in Play Console (Statistics / Store performance → traffic sources → UTM campaigns) that tagged visits appear. Allow 1–2 days.
- Privacy pages deliberately get no analytics (several policies state "no analytics"). Their visits are still seen if Vercel counts them as it does today.

---

## F. Deployment

| Item | Status |
|---|---|
| Git branch | `seo/production-sync-and-technical-seo`, commits `d0bebcd` (production snapshot) and the SEO-changes commit on top of it |
| Pull request | **Not created. Push refused (HTTP 403)**: the Claude GitHub App is not installed on `ostrander949-ops/DS03`. The branch is saved as a git bundle, `seo-branch.bundle`, next to this report |
| Build/test | No build step (static). `python3 tools/seo_check.py` → **0 errors** (baseline: **66 errors**); remaining warnings are long titles/descriptions on pages I did not rewrite. Playwright visual-regression and functional tests passed as described in C and E |
| Deployment | **Not deployed** (by design: needs owner approval and the routing change below) |

### Unresolved blocker: the two-project routing
Today `/`, `/sitemap.xml`, `/app/*.html`, `/archive.html` and the other rewritten paths are served by `ds-home`. Recommended path, once the branch is reviewed:

1. `vercel deploy` (preview) from the repo root, linked to project `ds-03`. Check pages on the preview URL; project routes may also apply to previews, so verify `/` and `/app/apkallu.html` show the new footer and history block.
2. `vercel deploy --prod`.
3. In Vercel → ds-03 → Routes, **disable** the nine `ds-home` rewrites (IDs `d2f57bd5…`, `2646ef00…`, `8abc69ea…`, `f428ffb1…`, `14d7d26b…`, `a72766d2…`, `f1959ac1…`, `3f1cde4c…`, `5db6761d…`). Because ds-03's files equal what ds-home serves today, plus these edits, this changes nothing except the intended improvements, and it removes the dependency on `ds-home`.
4. Verify on the live domain: `/sitemap.xml` has 58 URLs; `/planetary-hours.html` returns 200; `/about.html` returns 308 → `/`; Vercel → Events shows `Play Click` after a test click.
5. Submit `https://www.discovery-science.com/sitemap.xml` in Search Console and request indexing for `/planetary-hours.html`, `/angels.html` and `/obe.html`.
6. Rollback: re-enable the routes, or promote the previous deployment `dpl_GBzT2mpnucoV2fvdwLgPZSpTWwme`.

Alternative, if `ds-home` must stay: copy the changed static files (`index.html`, `sitemap.xml`, `library.html`, `catalog.html`, `seven-angels.html`, `shop.html`, `almanac.html`, `asclepion.html`) into the local `ds-home` folder and redeploy it. The function-rendered pages (`/app/*`, `/new.html`, `/archive.html`) would still need `api/app.js`, `api/apps.js` and `api/archive.js` edited by hand.

Also recommended: Vercel → Domains → `discovery-science.com` → change the redirect from **307 to 308**.

---

## G. Next steps (highest impact first)

1. **Ship it:** install the Claude GitHub App or push the bundle, merge, deploy, retire the `ds-home` rewrites, then submit the sitemap in Search Console. Nothing above helps until it is live, and the site needs a single source of truth.
2. **Connect `ds-03` to the GitHub repo** (Vercel → Settings → Git) so every deploy is versioned and gets a preview URL, ending the CLI-only, two-folder workflow.
3. **Fix the Google Play → website loop.** The top entry page is a privacy policy reached from Play. In each Play listing, set the website field to the app's landing page (e.g. `/app/apkallu.html`), not just the policy, and make sure every Play listing has its matching page. Ars Paulina, the 72 Names, Angel Number Widget and others have none yet.
4. **Consolidate the app hubs** (`new.html`, `apps.html`, `catalog.html`, `google-play.html`) into one canonical "all apps" page with 301s from the rest, and **decide on `/papers/*`**: either restore those papers (they still earn Google Scholar referrals) or 301 them deliberately.
5. **Publish two more source-led guides** that match apps without existing landing pages, the **Ars Paulina** (with a real landing page for the paid app) and the **Picatrix**, built from Archive §V/§VI the same way as the planetary-hours guide, then add a Heptameron history section to `/seven-angels.html`.

### Notes for the reviewer
- Realistic expectation: 125 → 1,250 monthly visitors is a growth target. Organic search currently delivers almost none of the traffic, so the gains depend on indexing the 16 previously unlisted pages, on new guide content ranking, and on Play listings linking to landing pages.
- I did not invent ratings, prices, testimonials or features. JSON-LD uses only data already on the pages. `MobileApplication` markup without `offers` or `aggregateRating` is valid but will not produce app rich results. Adding real Play ratings is a possible future step if kept current.
- Two Play apps share the "Oracle" name (`com.discoveryscience.oracle` "Consult the Angels" and `com.discoveryscience.oracle.tarot`). `oracle.html` links the former and `app/oracle.html` the latter. This looks intentional but is worth a human check.
