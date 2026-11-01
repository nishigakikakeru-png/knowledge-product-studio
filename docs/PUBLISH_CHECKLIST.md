# Release gate — Knowledge Product Studio

## Implemented and verified
- [x] Separate public repo `nishigakikakeru-png/knowledge-product-studio` and Vercel production deployment
- [x] 10 static page URLs including all six lessons, product board, about
- [x] Theme 5 independently drafted from public references; provenance documented
- [x] Six lessons include a practical exercise and contextual links to planner fields
- [x] Planner's `kps-product-v1` key and JSON schema unchanged (existing saved work must be preserved)
- [x] Page-specific title/description, canonical, sitemap.xml, robots.txt (Allow), and noindex controls in HTML and Vercel response headers
- [x] Automated static link/metadata test and JavaScript syntax check

## Before Google indexing (not yet done)
- [ ] Owner confirms all article wording, original examples, and factual statements (especially independently written lesson 5)
- [ ] Confirm public-facing owner identity, contact route, privacy notices and terms
- [ ] Recheck site under actual browser on both phone and desktop (automated Chromium in chat environment may be restricted)
- [ ] Check all functional paths including JSON export/import, persistence and reset on production
- [ ] Finalize brand and canonical domain; update SITE_ORIGIN and sitemap if different
- [ ] Add Open Graph image and verify social previews
- [ ] Remove HTML meta `noindex` and Vercel `X-Robots-Tag`, not just robots.txt
- [ ] Resubmit sitemap in Google Search Console; indexing is not guaranteed

## Boundaries
No account auth, cloud sync, payments, Muse or note publication integration in v1. Do not sync internal/private COS Brain or user product data into this public repository.
