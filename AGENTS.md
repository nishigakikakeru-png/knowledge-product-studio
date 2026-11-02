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
