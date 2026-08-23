# SEO baseline — 2026-08-17 (pre city-page consolidation)

Captured before the removal of 15 city pages, /kentucky/ regional hub, and
/air-duct-cleaning/. Purpose: measure whether the consolidation improves indexation.
Compare to a re-run of the same crawl 4-6 weeks after deploy.

## Summary counters
- Crawled URLs (200 status, HTML content pages): **59**
- Sitemap URLs: **58**
- GSC indexed count (reported by Christian): **38**
- GSC "Crawled - currently not indexed" (reported by Christian): **28**
- GSC "Discovered - currently not indexed" (reported by Christian): **12**

Crawl method: BFS from `/` following every internal href, browser UA,
depth-unlimited. Excluded prefixes: `/api/`, `/portal/`, `/admin/`, `/static/`,
`/media/`, `/gift-card/webhook/`. Static asset extensions excluded.

## Inbound link table — every crawled URL, most-linked first

| inbound | depth | in_sitemap | path |
|---:|---:|:-:|---|
| 59 | 0 | yes | `/` |
| 59 | 1 | yes | `/air-bnb-cleaning/` |
| 59 | 1 | yes | `/areas-we-serve/` |
| 59 | 1 | yes | `/blog/` |
| 59 | 1 | yes | `/bulk-cardboard-removal/` |
| 59 | 1 | yes | `/contact/` |
| 59 | 1 | yes | `/dump-trailer-rental/` |
| 59 | 1 | yes | `/estate-clean-out/` |
| 59 | 1 | yes | `/estate-hoarder-cleanout/` |
| 59 | 1 | yes | `/eviction-clean-out/` |
| 59 | 1 | yes | `/faq/` |
| 59 | 1 | yes | `/fence-removal/` |
| 59 | 1 | yes | `/foreclosure-clean-out/` |
| 59 | 1 | yes | `/gallery/` |
| 59 | 1 | yes | `/garage-clean-out/` |
| 59 | 1 | yes | `/gift-card/` |
| 59 | 1 | — | `/gift-card/check/` |
| 59 | 1 | yes | `/hot-tub-removal/` |
| 59 | 1 | yes | `/junk-removal-bowling-green/` |
| 59 | 1 | yes | `/junk-removal-clarksville/` |
| 59 | 1 | yes | `/junk-removal/` |
| 59 | 1 | yes | `/kentucky/` |
| 59 | 1 | yes | `/light-demolition/` |
| 59 | 1 | yes | `/loyalty/` |
| 59 | 1 | yes | `/move-in-move-out-cleaning/` |
| 59 | 1 | yes | `/move-out-deep-cleaning/` |
| 59 | 1 | yes | `/pricing/` |
| 59 | 1 | yes | `/property-manager-hub/` |
| 59 | 1 | yes | `/quote/` |
| 59 | 1 | yes | `/recurring-maid-services/` |
| 59 | 1 | yes | `/referral/` |
| 59 | 1 | yes | `/residential-cleaning/` |
| 59 | 1 | yes | `/scrap-metal-pickup/` |
| 59 | 1 | yes | `/services/` |
| 59 | 1 | yes | `/short-term-rental-turnover/` |
| 59 | 1 | yes | `/storage-unit-clean-out/` |
| 59 | 1 | — | `/track/` |
| 32 | 2 | yes | `/junk-removal-nashville/` |
| 27 | 1 | yes | `/book/` |
| 23 | 2 | yes | `/junk-removal-hendersonville-tn/` |
| 22 | 2 | yes | `/junk-removal-gallatin-tn/` |
| 21 | 2 | yes | `/junk-removal-franklin-ky/` |
| 18 | 2 | yes | `/junk-removal-springfield-tn/` |
| 18 | 2 | yes | `/junk-removal-white-house-tn/` |
| 15 | 2 | yes | `/junk-removal-goodlettsville-tn/` |
| 15 | 2 | yes | `/junk-removal-spring-hill-tn/` |
| 12 | 2 | yes | `/junk-removal-brentwood-tn/` |
| 12 | 2 | yes | `/junk-removal-franklin-tn/` |
| 12 | 2 | yes | `/junk-removal-lavergne-tn/` |
| 12 | 2 | yes | `/junk-removal-portland-tn/` |
| 11 | 2 | yes | `/junk-removal-lebanon-tn/` |
| 11 | 2 | yes | `/junk-removal-smyrna-tn/` |
| 9 | 2 | yes | `/junk-removal-russellville-ky/` |
| 7 | 2 | yes | `/junk-removal-nolensville-tn/` |
| 6 | 2 | yes | `/junk-removal-mt-juliet-tn/` |
| 6 | 2 | yes | `/junk-removal-scottsville-ky/` |
| 5 | 2 | yes | `/junk-removal-murfreesboro-tn/` |
| 4 | 2 | yes | `/junk-removal-ashland-city-tn/` |
| 2 | 2 | yes | `/blog/nashville-waste-crisis-junk-removal-costs/` |

## Orphans (sitemap URLs with 0 inbound internal links)
- `/air-duct-cleaning/`

## Sitemap-vs-crawl delta
- URLs in sitemap but not reachable via BFS from /: 1
  - `/air-duct-cleaning/`
- URLs discovered by BFS but not in sitemap: 2
  - `/gift-card/check/`
  - `/track/`

## Pages slated for removal in the consolidation
All 301 to `/areas-we-serve/`.

| path | current inbound | current depth |
|---|---:|---:|
| `/junk-removal-clarksville/` | 59 | 1 |
| `/junk-removal-bowling-green/` | 59 | 1 |
| `/junk-removal-russellville-ky/` | 9 | 2 |
| `/junk-removal-scottsville-ky/` | 6 | 2 |
| `/junk-removal-lebanon-tn/` | 11 | 2 |
| `/junk-removal-ashland-city-tn/` | 4 | 2 |
| `/junk-removal-mt-juliet-tn/` | 6 | 2 |
| `/junk-removal-brentwood-tn/` | 12 | 2 |
| `/junk-removal-franklin-tn/` | 12 | 2 |
| `/junk-removal-spring-hill-tn/` | 15 | 2 |
| `/junk-removal-murfreesboro-tn/` | 5 | 2 |
| `/junk-removal-smyrna-tn/` | 11 | 2 |
| `/junk-removal-lavergne-tn/` | 12 | 2 |
| `/junk-removal-nolensville-tn/` | 7 | 2 |
| `/kentucky/` | 59 | 1 |
| `/air-duct-cleaning/` | 0 | ? |

## Pages kept as canonical city landings

| path | current inbound | current depth |
|---|---:|---:|
| `/junk-removal-nashville/` | 32 | 2 |
| `/junk-removal-franklin-ky/` | 21 | 2 |
| `/junk-removal-springfield-tn/` | 18 | 2 |
| `/junk-removal-white-house-tn/` | 18 | 2 |
| `/junk-removal-portland-tn/` | 12 | 2 |
| `/junk-removal-gallatin-tn/` | 22 | 2 |
| `/junk-removal-hendersonville-tn/` | 23 | 2 |
| `/junk-removal-goodlettsville-tn/` | 15 | 2 |

## Reproduction
- Full crawl JSON (edges + depth + status) is stored outside the repo at
  `c:/Users/thomp/Desktop/jb_link_graph_2026-08-17.json` on the workstation that
  produced this baseline. It is the exact data behind the tables above.
- Reference map for the 16 removed slugs is at
  `c:/Users/thomp/Desktop/jb_removal_refs.json`.
- Re-run script: BFS crawler used for this baseline lives in the session
  transcript; can be regenerated verbatim.
