# Knowledge Product Studio — ChatGPT / coding agent guidance

## Mission

Build a Japanese learning + product planning website for people who do not know **what knowledge to sell or how to sell it**. SEO is a distribution method for useful learning articles, **not the product itself**.

## Architecture rules

- This is the **public-facing** site, separate from `nishigakikakeru-png/content-operations-studio` (COS) and `character-motion-studio2`.
- COS contains private editorial Brain, Knowledge and plans. **Never copy private COS runtime data into this public repository.** Borrow reviewed principles and purpose-built components only.
- Do not expose GitHub/Vercel/ChatGPT operational complexity to customers.
- Customer-side scope: learning pages, optional local-only thinking workspace, product concept map, product outline, pricing/offer, selling page, improvement workflow.
- Thinking workspace is intentionally independent of product editor: localStorage key `kps-thought-v1` and separate JSON schema; preserve `kps-product-v1` exactly. No autosending personal notes to COS, GitHub or publishing channels.
- Owner-side scope: ChatGPT-assisted editorial research, source verification, internal links, SEO audits, GitHub commits and Vercel deploys.
- Muse/AI and note publishing integrations are future interfaces, **not v1 features**.
- User data must not be checked into GitHub or drive redeploys. The initial product form uses device-local localStorage. Mark its limits plainly; later use isolated per-user authenticated storage.

## Editorial status

- The 2026-11-01 provided files were drafts for themes 1,2,3,4,6; they explicitly requested owner editing before publication.
- Theme 5 source material was not provided. Only a placeholder overview exists; do not claim it is fully researched.
- Noindex is intentionally enabled until the site and every article are reviewed and approved for public indexing.
- Do not invent conversion rates, visitor counts, sales history, customer quotes or endorsements.
- Distinguish verified fact, firsthand experience, hypothesis, and editorial suggestion.

## Before updating content

1. Check `docs/EDITORIAL_SOURCES.md` and existing pages.
2. Preserve the six-theme curriculum and the connection between lessons and the product board.
3. Verify any fresh legal/platform requirements with up-to-date primary sources.
4. Maintain meaningful unique titles, descriptions, logical H1/H2, accurate internal links and mobile functionality.
5. Run `python build.py` only if regeneration of page contents is intentional; the generator overwrites generated HTML pages.
6. Test `node --check assets/studio.js`, link integrity, autosave, JSON import/export, mobile behavior.
7. Only after editorial and production review: configure canonical domain, sitemap, real privacy/contact disclosures, then remove preview noindex.

## Deployment

Static HTML/CSS/JS; Vercel framework Other. No npm dependencies. Do not deploy to COS or CMS Vercel projects. New project must have its own GitHub repository and Vercel project. Prefer staged preview review before production. Never claim deployment success without verifying the returned URL and READY state.

## Diagram Editor (2026-11-03)
- Route `/diagram/` is a static local-first visual editor; its draft key is `kps-diagram-draft-v1`, separate from existing user workspace keys. Do not commit user project JSON to GitHub.
- **2026-11-07 policy update**: The diagram editor is **free**, including PNG download, JSON export/import and local saved-color palette. Remove purchase/¥2,980/license-dialog UI; do not reintroduce purchase checks in PNG or palette saving. Keep the local draft key and schema unchanged.
- Existing Supabase 6-digit OTP stays **optional**, only to preserve users' old account sessions and eligible cloud palettes; never block a free action on authentication, entitlement lookup or network. Local palette key: `kps-diagram-colors-v1`. Only synchronize to existing cloud records for already-entitled accounts, respecting RLS; do not change CMS billing/auth or shared database.
- KPS only embeds a link to Piggy Mix; no cross-origin access to its user palettes is implemented. External AI integration uses explicit JSON exchange, without automatic API requests.

## KPS authentication implementation (2026-11-03)
- KPS uses independent six-digit email OTP UI (`auth.signInWithOtp` + `verifyOtp({ type:'email' })`), not email-link navigation to CMS. A KPS-specific session key `kps-diagram-auth` stores the browser session. Supabase identity by email is shared; license and UI are application-specific.
- Sign out KPS with `auth.signOut({scope:'local'})` only. Do not use Supabase's default global signout because it may invalidate CMS/other sessions.
- Existing CMS code, authentication logic and billing state must remain unchanged. Never repoint the Supabase Site URL from CMS to KPS.
- Operator setup prerequisite: append `{{ .Token }}` to the shared Supabase Magic Link email template **without removing the existing CMS link**. The connector currently cannot edit Auth email templates. See `docs/KPS_EMAIL_OTP_SETUP.md`; do not claim end-to-end OTP delivery was verified before that change.
- Keep test assertions for both mobile and desktop OTP inputs, independent local logout, free JSON export, and owner entitlement lookup.

## Brand and learning design (2026-11-03)
- Official public name is exactly `経験をカタチにするLab`; repository name and KPS as internal acronym remain unchanged. Do not show `商材設計ラボ` as the current site name.
- The site teaches the skills behind ethical product design and web marketing: identifying useful experiences, search intent, SEO, article architecture, product format, pricing, conversion pathways, analytics and iteration.
- The `商材屋の合格ライン` is a hypothetical competency metaphor, NOT a real examination, certification, government qualification or the official SEO検定. The self-check is an original, non-accredited study aid, with no issued credentials.
- `/academy/` is the learning map; `/academy/seo/` a first SEO study module; `/academy/cases/` original examples grounded in current CMS code and prior work; `/academy/check/` a local-only knowledge check. Do not duplicate private COS Brain or user work.
- Preserve all existing KPS storage keys, authentication/session separation and separate CMS code. Keep whole site noindex until editorial, legal and UX review; do not claim unmeasured search ranking or income results.
