# KPS 図解エディター：JSON読込・キャンバスサイズの修正（2026-11-07）

## 依頼と再現条件

Museからの引継ぎ：`/diagram/`でKPS図解JSONを「ファイル読込」または「図解JSON」へ貼り付けても初期サンプルのまま。次の最小JSONで、キャンバスが図形1つ・1100×400pxに変わる必要がある。

```json
{"schema": "kps-diagram-v1", "width": 1100, "height": 400, "background": "#FAF5EE", "elements": [{"id": "el-1", "type": "box", "x": 100, "y": 100, "w": 600, "h": 120, "text": "テスト確認", "fill": "#F1E6D2", "stroke": "#B08D5F", "color": "#3B2A1E", "size": 28, "radius": 14, "angle": 0, "opacity": 100, "font": "sans", "align": "center", "z": 1}]}
```

## 監査で判明した問題

1. ファイル読込と貼り付け反映のどちらも、`confirm()`が承認されなければ`resetFrom()`を実行しない。ブラウザ自動化・AIブラウザ・確認表示状態によって更新されない問題を生む。
2. `normalize()`が常に`width:1100,height:660`を返し、入力JSONのサイズを捨てていた。
3. キャンバス表示`1100 × 660px`、拡大表示、PNG出力の幅と高さにも固定値を使用していた。
4. JSONの不正入力時の通知がalertに依存していたため、実際の編集画面にはエラー理由を表示できなかった。
5. 前回の無料化テストはPNG保存とローカル色保存を確認していたが、**JSON貼り付け／実ファイル読込からPNGまでの一連の作業を確認していなかった**。

## 対策と仕様

- ファイル読込・貼り付け反映の`confirm()`を撤廃し、ボタン／ファイル選択から直ちに検証と反映を行う。
- 読込前の図解は従来の「戻す」履歴に残し、加えて`kps-diagram-previous-before-import-v1`へバックアップする。既存の`kps-diagram-draft-v1`／`kps-diagram-v1`は保持。
- `width`と`height`は幅320〜4096px・高さ200〜4096pxの整数で検証。古いJSONで未指定の場合は1100×660pxとする。
- 読込後、キャンバス表示・自動ズーム・描画領域・PNG出力解像度（各2倍）を同じ寸法に更新。
- 成功・失敗理由を`#jsonImportStatus`および上部のステータスで明示。不正JSONはキャンバスを変更しない。
- 「戻す」「進む」でも図解サイズと表示領域を更新。
- JSONで指定された図解の背景や要素は上書きされるが、過去の保存データや他アプリのログイン情報は変更しない。
- PNG保存・色保存の無料提供は維持。SupabaseとCMSの設定は変更しない。

## 自動回帰テスト

`tests/smoke.py`のChromiumテスト（390px、1280px）で以下を確認する。

- 引継ぎの1要素JSONを貼り付けて即時反映できること（`confirm()`自動キャンセル環境でも動作）。
- 1要素とサイズ1100×400pxが画面に現れ、PNGが2200×800pxで保存されること。
- 不正JSONは元データを保持し、エラー理由を表示すること。
- 「戻す」で以前の3要素・1100×660pxに復元し、「進む」で再反映できること。
- サンプルとして用意した15要素の図を実ファイルから読込、1100×880pxで表示、再読み込み後も保持されること。
- 15要素のPNGは2200×1760pxで保存されること。
- 無料PNG、端末内色保存、既存の任意6桁コード認証テストが引き続き成功すること。

※ユーザー固有の15要素の本番JSONや3つのMuseデータは引継ぎ文に含まれないため、テスト用に生成した15要素のJSONで確認する。実際の3点は利用者側で読み込んで最終確認する。

## 追記：URLで直接図解を読み込む（2026-11-07）

### 背景
Museの追記引継ぎでは、**本人の手入力では図解が描画された一方、AIブラウザの画面入力では反映されなかった**との検証結果が報告された。入力イベントの欠落という原因仮説は、KPSの現行実装が`textarea.value`を直接読んでいるため、現時点では確定とはいえない。ただし、**入力欄への自動操作を回避する**という改善方針は合理的。

### URL仕様
正式URL：`https://knowledge-product-studio.vercel.app/diagram/`
推奨フォーマット：
```text
https://knowledge-product-studio.vercel.app/diagram/#import=b64.<UTF-8 JSONをbase64url化した文字列>
```
簡易フォーマット：
```text
https://knowledge-product-studio.vercel.app/diagram/#import=<encodeURIComponent(JSON.stringify(diagram))>
```

- ユーザーまたはAI側がURLを開くと、ページ起動時に`location.hash`からJSONを取り出し、既存のファイル読込と**同じ検証処理**で直接描画する。
- 同じページを開いたまま新しい`#import=`へ移動した場合も読み込み可能。
- 操作前の図解は`kps-diagram-previous-before-import-v1`へ退避し、「戻す」で復旧可能。従来の下書きキー`kps-diagram-draft-v1`はそのまま。
- 読み込み成功時はハッシュをブラウザのURLから削除して、更新時に再読み込みされることを防ぐ。失敗時は編集内容を変更せず、上部ステータスとコード欄にエラー表示。
- URLに埋め込む文字列は最大32,000文字。大きな図解はファイル読込へ切り替える。
- ハッシュ部分は通常のHTTPリクエストのURLとしてサーバーに送られない。ただし、**URLを共有すると図解の内容も渡る**。機密データや未公開個人情報を含む図解はリンクとして配布しないこと。
- 「コード / AI」欄の**「図解を開くURLをコピー」**で、現在の図解の共有リンクを生成できる。クリップボードが使えない場合は、コピー可能なテキスト欄を表示する。
- URL読込にはログイン、決済、APIキーは不要。PNG無料化・Supabase任意認証・CMSログイン情報には変更なし。
- 元のHTMLを埋め込むiframeや外部AIからの画面入力を必要とせず、`kps-diagram-v1`形式のJSONがあれば外部側でURLを生成できる。

### AI側のURL生成例（JavaScript）
```js
const bytes = new TextEncoder().encode(JSON.stringify(diagram));
const binary = Array.from(bytes, (byte) => String.fromCharCode(byte)).join('');
const code = btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const url = 'https://knowledge-product-studio.vercel.app/diagram/#import=b64.' + code;
// このURLをブラウザで開く。図解のJSONをtextareaに自動入力する必要はない。
```

### 回帰テスト
- 現在の15要素図解からコピーした`b64.` URLを新しいタブで開き、15要素が描画されること。
- `encodeURIComponent`と同等のパーセントエンコードURLから、日本語テキストを含む1要素・1100×760pxの図解が表示されること。
- URL読み込み結果がPNGで2200×1520pxになること。
- 不正なハッシュで元の図解が消えず、エラーが表示されること。
- 「戻す」でURL読み込み前の図解に戻れること。
- クリップボードが使えない場合の手動コピー欄。
