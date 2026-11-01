# Editorial provenance — 2026-11-01

Original user-supplied Markdown drafts are the editorial basis for five learning articles:

| Lesson | Original user file | Publish-safe source |
| --- | --- | --- |
| 01 課題の切り取り | 学習ハブ_テーマ1_課題の切り取り.md | content/lessons/problem.md |
| 02 商品化・カリキュラム設計 | 学習ハブ_テーマ2_商品化とカリキュラム設計.md | content/lessons/design.md |
| 03 オファーと価格 | 学習ハブ_テーマ3_オファーと価格.md | content/lessons/offer.md |
| 04 販売ページ | 学習ハブ_テーマ4_販売ページ.md | content/lessons/sales.md |
| 06 分析と改善 | 学習ハブ_テーマ6_分析と改善.md | content/lessons/improve.md |

The original private files were NOT committed to this public repository. Their core structure (chapters 1-5, detailed technical sections, mistakes, summaries) was preserved in publish-facing adapted Markdown. The original "珈琲読書でどう使うか" sections were turned into openly framed *design examples* because actual published inventories, current exam details, sales outcomes and pricing require separate verification. Absolute claims like "every successful product" and the inference that search autocomplete alone proves purchase demand were narrowed. The articles are not original source document replicas and should not be represented as such.

Theme 05 was not in the original user attachments. It remains a separately authored draft in the build.py lesson data, supported by the linked Google Search documentation. Do not misattribute it to the user.

The source-of-truth for public article text is content/lessons/*.md, rendered via `python build.py` (mistune is NOT used; install `markdown-it-py` for Markdown rendering). Generated learn/*/index.html must never be manually treated as the only source.

Original user material may contain private roadmaps. Do not upload it verbatim to public GitHub. Verify prices, exam criteria and third-party facts with primary sources before removing noindex.
