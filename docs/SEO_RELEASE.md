# SEO implementation and release gates

## Canonical host
`https://knowledge-product-studio.vercel.app` is the current verified production alias. The generator `SITE_ORIGIN` controls canonical and sitemap. Do not change domains without also updating every generated canonical, `robots.txt`, sitemap and redirects.

## Staging vs indexing
- The site is accessible publicly for owner review.
- Each HTML page currently has `meta name=robots content=noindex,nofollow`.
- The Vercel config sends `X-Robots-Tag: noindex, nofollow` for all routes.
- `robots.txt` allows crawling; this is intentional because Google must be allowed to access a page to see `noindex`. Blocking crawling with `Disallow: /` at the same time as `noindex` risks Google not observing the rule.
- The sitemap contains only public navigable HTML routes, not API/source/assets. It is staged for release and is **not** proof that pages are indexable.

## Release plan
1. Owner approves complete article text, independent Theme 5, sample claims, author/contact information.
2. Test all URLs in browser, localStorage/JSON import/export, responsive layouts and errors.
3. Remove noindex from *both* generator and Vercel headers; rebuild; verify responses on production, then submit sitemap in Search Console.
4. Measure queries and internal progression. Keep conversion assumptions separate from actual sales.

Official references:
- https://developers.google.com/search/docs/fundamentals/creating-helpful-content?hl=ja
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- https://developers.google.com/search/docs/crawling-indexing/block-indexing?hl=ja
