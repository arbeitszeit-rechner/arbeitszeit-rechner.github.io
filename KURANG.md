**# TODO.md — Open Tasks, Known Issues, Follow-up Work**



As of: 2026-10-13, after **\*\*Phase 3\*\*** (glossary entries; Phase 1 = Hugo project structure, Phase 2 = glossary hub). `[x]` means: the file or feature exists. It does **\*\*not\*\*** mean it has been built with Hugo or tested in a browser (see “Not verified”).



**## Phase Status**



\| Phase | Status |

\|---|---|

\| 1 — Hugo project structure | Files created, **\*\*build not run\*\*** |

\| 2 — Glossary hub (content, categories) | Files created, **\*\*build not run\*\*** |

\| 3 — Glossary entries (research, front matter, answer, source, link) | 31 entries created, content **\*\*not legally reviewed\*\***, **\*\*build not run\*\*** |



**## Not Verified (Highest Priority)**



\- [ ] **\*\*Hugo build missing.\*\*** Hugo was not installed in the working environment, and the download (npm/GitHub) was blocked by the network policy (HTTP 403). Only the following were checked: TOML parses, front matter validates (`scripts/validate.py content`: 0 errors), `{{ }}` blocks are balanced in all templates, and calculator logic was tested with Node (8 cases). Templates, partials using `return`, JSON-LD output, and menu logic have **\*\*not\*\*** been tested against Hugo.

  - Next step locally: run `hugo --minify`, then `python3 scripts/validate.py public`; fix `SEO: Meta-Description …` warnings and template errors.

  - Hugo ≥ 0.128 (the standard version is sufficient). Pin a fixed version in CI.

\- [ ] **\*\*Lighthouse has not been measured.\*\*** No claims can be made about performance, accessibility, best practices, SEO, or Core Web Vitals. Measure with Chrome DevTools/Lighthouse (mobile, incognito) and PageSpeed Insights after deployment; field data (CrUX) will only be available after launch.

\- [ ] **\*\*Structured data has not been externally validated.\*\*** Check with Rich Results Test and validator.schema.org.

\- [ ] **\*\*Fallback font metrics\*\*** (`size-adjust`, `ascent-override`, etc.) are approximations; check CLS in the Lighthouse report.

\- [ ] For `sitemap: disable: true` in the front matter of legal pages, verify that those pages are absent from `public/sitemap.xml`.

\- [ ] Manually test contrast, keyboard navigation, and screen reader behavior (menu, calculator, `aria-live`).



**## Phase 1 — Completed (Files Exist)**



\- [x] `hugo.toml` (de-DE, base URL, menus, sitemap, minification, advertising parameters, no RSS/taxonomies)

\- [x] Layouts: `baseof`, homepage (`index.html`), `single`, `list`, `404`, glossary hub and entry (`layouts/glossar/`)

\- [x] Partials: `head`, `seo`, `schema` (JSON-LD graph), `breadcrumbs` (+ BreadcrumbList in the graph), `navbar`, `footer`, `scripts`, `calculator`, `byline`, `author-profile`, `glossary-links`, `ads/slot`, helpers `crumbs`, `first-paragraph`

\- [x] `layouts/robots.txt` (production: allow + sitemap; development: block); sitemap via Hugo defaults

\- [x] Shortcodes `ad` (ad placement in an article), `kontaktdaten`

\- [x] CSS design system (`assets/css/main.css`, embedded inline), JS (`assets/js/main.js`: menu + calculator, deferred)

\- [x] Inter self-hosted: `static/fonts/` (WOFF, reduced to Latin characters, license `LICENSE-Inter.txt`), favicon `static/favicon.svg`

\- [x] Functional calculator (start, end, break, target → net, decimal, gross, overtime/undertime, night shift, § 4 ArbZG notice)

\- [x] `data/author.yaml` (reusable author profile, intentionally empty)

\- [x] Content templates: homepage, glossary hub, About Us, Contact, Privacy Policy, Terms of Use (descriptions 150–155 characters, titles without suffixes)

\- [x] Archetypes (`default`, `glossar`), `.gitignore`, `scripts/validate.py`, `README.md`

\- [x] No GitHub repository created (as specified)



**## Phase 1 — Open / Known Issues**



**### Information Needed From You (Nothing Has Been Invented)**

\- [ ] **\*\*Author profile\*\***: name, role if applicable, a short verified description, and optional profile URLs in `data/author.yaml`. Until then, “Arbeitszeit Rechner Editorial Team” will appear, and the organization will be listed as the author in JSON-LD.

\- [ ] **\*\*Operator details and contact\*\***: `params.contact.email` in `hugo.toml` and details for the legal notice/privacy policy. Until then, the Contact page only displays a notice.

\- [ ] Confirm that the “Editorial Principles” and “Funding and Advertising” section on the “About Us” page reflect your actual practices.



**### Legal (Before Publication)**

\- [ ] **\*\*Legal notice missing\*\*** and was not included in the page list. Generally required for a website with advertising in Germany (§ 5 DDG). Create the page, link it in `[[menus.footer]]`, and have it legally reviewed.

\- [ ] **\*\*Privacy Policy and Terms of Use\*\*** are templates containing `[INFORMATION REQUIRED]`/`[REVIEW]` markers. Have them fully reviewed for compliance with German and EU law. Then remove `template_notice`, `noindex`, and `sitemap.disable` from the front matter. (Decision: until then, both pages remain `noindex` and excluded from the sitemap.)

\- [ ] **\*\*Consent management (CMP)\*\*** for AdSense/EEA before enabling advertising (TDDDG, Google requirements). `scripts.html` loads AdSense only when `ads.mode = "live"`.

\- [ ] Create `ads.txt` (an AdSense publisher ID is required).



**### Content and SEO**

\- [ ] **\*\*Homepage article missing\*\*** (`content/_index.md` contains only front matter). Afterward, check the Article JSON-LD against the visible content (author, date, headline).

\- [x] Topic map and cluster prioritization: see `TOPICAL_MAP.md`

\- [ ] `og:image` and the organization logo are missing (no image assets available); then add `og:image`, `twitter:card=summary_large_image`, and Article `image`.

\- [x] Glossary entries exist; `featured: true` (12 entries) controls the chips on the homepage (check their display after the build).

\- [ ] Add internal links from the homepage article to glossary entries.

\- [ ] Calculator features intentionally omitted: weekly/monthly calculations, multiple breaks, consideration of collective agreement/contract rules, copying/sharing the result.



**### Technical**

\- [ ] WOFF instead of WOFF2: no Brotli module was available. Regenerate Inter as WOFF2 (e.g., from rsms.me/inter or `@fontsource/inter`) and adjust `@font-face`/preload. Font source: locally installed Debian package `fonts-inter`; verify the version.

\- [ ] Deployment: GitHub repository (does not exist yet), Actions workflow with a fixed Hugo version, Pages settings. The domain `arbeitszeit-rechner.github.io` assumes that the GitHub account or organization is named `arbeitszeit-rechner` and the repository is `arbeitszeit-rechner.github.io`.

\- [ ] CSS is embedded inline (no render-blocking, but not cacheable). If the CSS grows, switch to an external, fingerprinted file.

\- [ ] Ad placements are in `placeholder` mode (visible placeholders for layout testing). Set to `off` or `live` before launch. Ads on glossary pages are disabled via `cascade` until the entries become full articles (to avoid thin pages with ads).

\- [ ] The breadcrumb separator uses `content` with alternative-text syntax; visually check it in Safari/Firefox.



**## Phase 2 — Glossary Hub (Completed, Files Exist)**



\- [x] `content/glossar/_index.md`: hub text (purpose, reference to the calculator and homepage article, link to “About Us”) and 6 categories with short descriptions: Working Time Fundamentals, Breaks and Rest Periods, Overtime and Additional Work, Working Time Models, Laws and Regulations, Calculation and Conversion

\- [x] `layouts/glossar/list.html`: jump navigation to categories, grouped entry lists (alphabetical, with questions), link back to the calculator; categories without entries are hidden, and a notice appears if there are no entries

\- [x] `scripts/validate.py content` additionally checks that category names are unique, descriptions are present, and every entry references a defined category

\- [ ] Check the hub display after the Hugo build (grouping, `#kat-…` anchors, JSON-LD `DefinedTermSet`). With the 31 entries from Phase 3, all six categories should appear (4–6 entries per category).

\- [ ] The `/#rechner` and `/#artikel` links in the hub text will work once the homepage article exists (`#artikel` is already present in the template).

\- [ ] Adjust categories if necessary after the term research in Phase 3 (assign each term to only one category).



**## Phase 3 — Glossary Entries (Created, Review Pending)**



\- [x] 31 entries in `content/glossar/` (distribution: Fundamentals 6, Breaks and Rest Periods 4, Overtime and Additional Work 5, Working Time Models 6, Laws and Regulations 6, Calculation and Conversion 4); topic map in `TOPICAL_MAP.md`

\- [x] For each entry: front matter, direct answer (≤ 50 words), exactly one external link, one link to the homepage, description of 150–155 characters, title without suffix, unique slug

\- [x] `python3 scripts/validate.py content`: 0 errors (lengths, uniqueness, answer length, link count, categories)

\- [ ] **\*\*Content and legal review before publication.\*\*** The legal references were checked against a copy of the ArbZG (file version: 2019) (§§ 2, 3, 5, 6, 9, 16). They were not compared with the current version because gesetze-im-internet.de was inaccessible. Check that all links to legislation are accessible and that the wording is up to date.

\- [ ] **\*\*Claims not explicitly supported by the linked source\*\*** (have a specialist review them or link a better source):

  - `bereitschaftsdienst`: “counts as working time” is based on ECJ/Federal Labour Court (BAG) case law; only § 7 ArbZG is linked

  - `rufbereitschaft`: “only actual call-outs count” (BAG case law); § 5 ArbZG is linked

  - `ruhepause`: the definition “neither working nor being required to remain available” comes from case law

  - `minusstunden`: statement concerning § 615 BGB (operational risk) and entitlement to wages

  - `ueberstundenverguetung`: requirements “ordered, approved, or tolerated” and burden of proof (BAG press release not checked in full text)

  - `mehrarbeit`: the term is not uniformly defined by law; the distinction from overtime is deliberately phrased cautiously

  - `arbeitszeiterfassung`: check for changes in the law following the 2022 BAG ruling before publication

  - `vollzeit`: “often 35 to 40 hours” is a general statement without a source

  - `arbeit-auf-abruf`, `teilzeit`, `arbeitszeit-jugendliche`: verify the figures from memory against § 12 and § 8 TzBfG and §§ 8, 11 JArbSchG

\- [ ] **\*\*Weak source:\*\*** `dezimalstunden` links to the Wikipedia article “Industrieminute” because no official source was found. Replace it with a better source (e.g., REFA or an official body).

\- [ ] Entries are intentionally brief (answer, note, source only). Full articles will follow later; only then enable advertising (remove `cascade: ads: false` from the hub) and check author/date information.

\- [ ] Calculator references: statements such as “The calculator points out the minimum break” match the calculator logic, but should be maintained when functionality changes.

\- [ ] Possible additional terms (not implemented; see `TOPICAL_MAP.md`): work readiness, travel time/business trips, time off in lieu, overtime premium, minimum wage and working time, vacation and working time, monthly working hours.
