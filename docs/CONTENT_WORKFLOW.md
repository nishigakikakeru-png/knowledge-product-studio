# Editorial workflow

1. Edit `content/lessons/problem.md`, `design.md`, `offer.md`, `sales.md`, `improve.md` for lessons 1,2,3,4,6. Keep their five-section instructional organization.
2. `reach` (lesson 5) is independently authored inside `LESSONS` in `build.py` until a user-supplied original is available. Do not pretend it is original user text.
3. Run `python -m pip install -r requirements-build.txt` once, then `python build.py` to regenerate the static site.
4. Run `python tests/smoke.py` and `node --check assets/studio.js`. Explicitly log skipped browser tests.
5. For facts that can change (exam fees, scope, competing prices), verify current primary sources and mark checked date, or keep the example clearly illustrative.
6. Keep editorial status out of public article prose. Keep `noindex` until the publication checklist and editor approval are complete.
7. Never edit user workspace save schema or localStorage key as a side effect of writing articles.

## 思考の整理室（2026-11-02）
- `thinking/index.html` と `assets/thinking.js` / `assets/thinking.css` は商品設計と独立。個人の生データをリポジトリへ保存しない。
- 既存 `kps-product-v1` の読み書きやJSONスキーマを変更しない。`kps-thought-v1` は独立キー。
- `build.py` は thinking ページ自体を再生成しないが、ナビゲーションとsitemapには `/thinking/` を含める。
- UIの文言は誰でも使える問いにし、COS非公開Brainを公開サイトへ転載しない。
