# KPS 図解エディター：メール6桁コード認証の運用

更新：2026-11-03
対象：`https://knowledge-product-studio.vercel.app/diagram/`
認証プロジェクト：既存Supabase（Character Motion Studioと共通ユーザーID）。**CMSのリポジトリ、ユーザー情報、課金情報は変更しない。**

## 独立性の定義

- KPS内のメール＋6桁コード入力で認証完結。メール内のリンクはクリック不要。
- KPSのブラウザ認証情報は `storageKey:'kps-diagram-auth'` で他アプリと区別する。
- KPSからのログアウトは `auth.signOut({scope:'local'})` で当該セッションのみ終了。CMSや他端末のセッションをグローバルに失効させない。
- 同じメールを使うと、Supabase内部のユーザーIDは同一。ユーザー情報とアプリ単位の購入／永続利用権限は別概念。
- KPSの買い切り権限は `public.kps_diagram_entitlements`、パレットは `public.kps_diagram_palettes`。アプリの登録メールやlocalStorageフラグを元に権限を昇格させない。
- 既存のowner登録は恒久無料権限を継続する。新しいKPS利用者は無料編集が可能で、書き出し購入はまだ未開通。

## 重要：Supabase共通メールテンプレートの設定が必要（運営者側1回）

Supabaseダッシュボードの `Authentication → Email Templates → Magic Link` を開く。
現在のCMS用リンクやメール本文を**削除・置換せず**、本文に次の1行を追加する：

```html
<p>ログイン用の6桁コード：<strong>{{ .Token }}</strong></p>
```

既に `{{ .Token }}` がある場合は変更不要。
Supabaseの `signInWithOtp` はメールテンプレートに `{{ .Token }}` がないと、原則リンク型のメールしか届かず、KPS内でコード認証できない。
KPSでは未登録メールからの新規利用も可能にしているため、新規登録時のメールにコードがない場合は `Confirm signup` テンプレートも同じ原則で確認し、既存内容を壊さず `{{ .Token }}` 表示を追加する。

既存CMSの `{{ .ConfirmationURL }}` や独自ログインリンクはそのまま残してよい。共通テンプレートにコードが追加されるのでCMS側メールにも数字が表示されるが、CMSのログイン方法は変更されない。

安全のため、テンプレートを保存する前に現状を控え、差分が `{{ .Token }}` の表示追加だけであることを確認する。

## URL設定

`Authentication → URL Configuration → Redirect URLs` に必要なら以下を追加：
`https://knowledge-product-studio.vercel.app/diagram/`

**Site URLをCMSからKPSへ書き換えない。** KPSの6桁コード入力はメール内リンクでのリダイレクトに依存しない。
既存CMSの許可URLも削除しない。

## 実際のログイン検証

1. KPS図解エディターへ移動し、「KPSログイン」を開く。
2. CMSと同じ所有者メールを入力して「6桁コードをメールで受け取る」を押す。
3. 届いた最新メールに6桁の数字があることを確認する。**メール内のリンクを押さず**、KPSの画面に戻って数字を入力する。
4. KPSのログイン完了・ライセンス有効を確認する（所有者は `kps_diagram_entitlements` のレコードを元に自動判定）。
5. PNG出力が利用可能であること、無料JSON保存も継続することを確認する。
6. KPSからログアウトした後も、CMSのブラウザセッションが維持されることを確認する。CMSを意図的にログアウトさせない。

メールは一般に1分未満の連続送信が制限され、認証コードには有効期限がある。最新のメールを使用し、コードを共有しない。

## 切り分け

- メールに数字がない：共通メールテンプレートに `{{ .Token }}` がない可能性。
- メールリンクをクリックするとCMSへ飛ぶ：旧メールリンクの挙動。KPSではリンクは不要。
- KPSでコードがエラー：送信先メール・6桁の数字・コード期限・送信頻度を確認。
- ログイン成功でもPNGが購入画面：所有者の同一ユーザーIDが `kps_diagram_entitlements` の有効行に存在するか管理側で調査。表示だけを有料状態に書き換えない。
- JSON保存：ログイン・購入不要。JSONは画像ではなく再編集用データ。

参考： https://supabase.com/docs/guides/auth/auth-email-passwordless
参考： https://supabase.com/docs/guides/auth/signout
