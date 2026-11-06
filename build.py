from pathlib import Path
import html,json,re
from markdown_it import MarkdownIt
ROOT=Path(__file__).parent
LESSONS=[
('01','problem','何を商品にするか決める','知識より先に、誰の何を解決するのか','経験を棚卸しし、購入者の困りごとと結びつける。',[
('困りごとを先に決める','「自分が何を知っているか」だけでは商品は決まりません。買い手の状況、困りごと、解決後の状態の三つを具体的に置くところから始めます。経験や専門性は、その問題を解決できる理由になります。'),
('課題の粒度を下げる','「勉強に困っている」は範囲が広すぎます。いつ、何と比べて、何ができないのか。たとえば「資格試験の対策資料が見つからず、勉強の順番を決められない」のように、実際の行動が見える形まで狭めます。'),
('材料を探す場所','自分の現場で繰り返し説明してきたこと、読者の質問やレビュー、検索時に使われる言葉。これらは課題候補の手掛かりです。ただし、検索候補があるだけで購入需要があるとは断定できません。'),
('ここで作る成果物','「誰が・何に困り・何ができるようになるか」の一文と、それを支える本人の経験を一つ記録します。次のテーマでは、この成果物を教材や商品の目次に変えます。')],
['想定読者を「全員」にしない','経験のない実績を足さない','買い手の言葉と自分の思い込みを分ける']),
('02','design','知識を商品に組み立てる','教材やnoteの価値は、情報量ではなく到達できる順番','ゴールから逆算して目次・章・演習を設計する。',[
('目次を「できること」で作る','購入者が商品を使い終わったとき、何ができる状態になっているかを一文にします。そこから中間地点を分解し、前提関係の順番で並べていきます。'),
('知識を棚卸しする','既存記事、画像、記録、手順、よく受ける質問を一覧化します。「収録する内容」「重複している内容」「足りない内容」「入れない内容」を区別すると、制作量を過大に見積もらずに済みます。'),
('読んで終わりにしない','一章ごとに問題、チェック項目、実践課題のいずれかを置きます。「学んだ」ではなく「実行できた」を判断できる形式です。'),
('ここで作る成果物','商品の目次、各章でできるようになること、足りない素材の一覧を作ります。単品記事を束ねる場合も、「寄せ集め」ではなく目的までの道筋が必要です。')],
['目次と実際の中身を一致させる','先に100本の記事を作ろうとしない','既存の素材を無理に全て入れない']),
('03','offer','オファーと価格を決める','価格を決める前に、何をどんな条件で届けるか','中身・束ね方・条件を分けて商品の提示方法を設計する。',[
('オファーは商品名ではない','商品に何が含まれ、どこまで支援し、購入後に何を受け取れるのか。それらを買い手へ示す全体がオファーです。'),
('先に商品構成を確定する','単品かセットか、更新はあるか、対象外は誰か。こうした条件によって購入の判断材料が変わります。価格だけ先に決めると、理由が後付けになりやすくなります。'),
('比較材料を用意する','類似商品の価格、個別購入した場合の費用、セット固有の価値などを正確に比較します。根拠のない定価や実態のない期限表示は採用しません。'),
('ここで作る成果物','収録範囲、提供形態、対象・対象外、価格候補、比較に使った根拠と確認日を一つのシートにします。')],
['売上試算を実績として書かない','架空の割引前価格を表示しない','対象外の人も明示する']),
('04','sales','販売ページを設計する','買い手が判断できる情報を、必要な順番で提示する','販売ページを不安解消と購入判断の資料にする。',[
('読者が知りたい順番','困りごと、解決策、収録内容、根拠、向いていない人、よくある疑問、価格と購入方法。これは出発点となる構成例であり、すべての商品で順番を固定する必要はありません。'),
('「中身」を見せる','具体的な目次、教材サンプル、使用方法、更新条件があると、買い手は自分に必要かどうか判断できます。「充実しています」だけでは判断材料になりません。'),
('信用の根拠','本人が実際に経験したこと、公開可能な制作過程、確認できる数字を扱います。他人の成功事例を自分の成果のように見せたり、保証できない結果を約束したりしません。'),
('ここで作る成果物','販売ページの見出し、サンプル掲載位置、FAQ、価格・条件の掲載位置を一つの設計図にします。')],
['販売ページだけで中身を大きく見せない','誇張や「誰でも」を避ける','購入後の受け取り方法まで説明する']),
('05','reach','商品を知ってもらう','検索・SNS・販売ページを別々に作らない','検索とSNSから、商品を必要とする読者へ届く経路を設計する。',[
('集客より先に「入口となる質問」を決める','テーマ1で言語化した困りごとをそのまま起点にします。「電子商材を作る」と検索する人、「noteで目次をどう作るか」と検索する人では、今すぐ欲しい答えが違います。商品名を広める前に、読者がどの段階の何を知りたいかを整理します。無料記事はその質問に実際に答え、記事を読んだだけでも一つの行動ができる内容にします。'),
('検索記事・SNS・販売ページに違う役割を与える','検索記事は特定の困りごとに対する詳しい答え、SNSは作品・工程・疑問の切り口を伝える短い入口、販売ページは商品の目次・サンプル・価格・条件を確かめる場所です。三つとも同じ売り文句にすると重複します。SNSで疑問を示し、無料記事で手順を説明し、必要な人だけ商品へ進める流れを作ります。'),
('一つのテーマから三つのコンテンツを考える','例えば「資格教材の目次が決められない」が入口なら、検索記事は「目次をゴールから逆算する5手順」、SNSは「情報量が多いだけでは教材にならない」という論点、販売ページは「実際の目次とサンプル」です。どの媒体も同じ想定読者と解決後の状態を共有します。媒体ごとに無関係なテーマを量産しません。'),
('無料記事から次に進む理由を示す','記事末尾に機械的に購入リンクを置くのではなく、本文で解説した手順と、商品で提供する補助を明確に分けます。例：「目次の考え方はこの記事で確認できます。自分の商品を整理したい場合は設計ボードへ」。記事そのものの答えを不自然に隠し、有料部分でしか結論が分からない構成を標準にはしません。'),
('検索順位・閲覧数・購入を同じ数字にしない','検索結果で表示された回数、クリックされた回数、記事内で関連ページに進んだ数、販売ページの閲覧、売上は別々の段階です。Search Consoleでは検索パフォーマンスの指標を確認できますが、購入までは自動的には把握できません。利用するサービスで測定できるものだけを記録し、分からない数字は空欄にします。'),
('発信前に確認する三つのこと','（1）無料記事は読者の質問に具体的に答えているか。（2）関連する学習記事・設計ツール・販売ページへのリンクは文脈上自然か。（3）購入前に商品の中身と条件を見られるか。ここまで揃えてから発信を増やします。複数の媒体を毎日運用する必要はありません。')],
['検索・SNS・販売ページの役割を分ける','記事の答えを途中で隠して誘導しない','計測できる指標とできない指標を分ける']),
('06','improve','売った後に改善する','数字は眺めるためでなく、次の修正箇所を決めるため','記事から販売までの流れを分けて振り返る。',[
('まず見る指標を決める','記事ごとの閲覧、反応、販売ページへの到達、販売の内訳、継続利用。確認できる範囲だけを記録し、取得できない数字は空欄にします。'),
('どこで止まったかを見る','記事が読まれない、記事は読まれるが販売ページへ進まない、販売ページまで来るが購入されない。位置によって疑うべき原因は違います。'),
('修正対象を一つに絞る','記録した数値と観察から一つ仮説を立て、次の確認日を決めます。複数を同時に変えると、改善の原因を判別しにくくなります。'),
('ここで作る成果物','変更前の数字、考えた仮説、実施した修正、次に見る指標を月次の実践記録にします。振り返りを次の商品や記事に再利用します。')],
['見られた数と買われた数を混同しない','測定できない数字は推測で補わない','数日間の変動だけで結論を出さない'])]

SITE_ORIGIN='https://knowledge-product-studio.vercel.app'
SUPPLEMENTS={
'problem':('課題を一文にする演習','まず「誰が・いつ・どんな状況で・何をできずに困っているか」を決めます。自分の想像だけで書いた箇所は、あとで確かめたい仮説として残します。',[
'想定する人を「初めて受験する人」などの状況まで具体化する',
'その人が検索しそうな質問を一文にし、実際に耳にした質問と区別する',
'この記事や商品を使った後にできることを動詞で書く'],
'例：「コーヒーに詳しくなりたい」より「初めて試験対策を始め、学習順が決められない人が、勉強の目次を作れる」とした方が、商品の範囲を決めやすくなります。'),
'design':('教材の目次を仮組みする演習','テーマ1の「解決後にできること」を、一つの教材で到達できるゴールに変えます。',[
'完成後の状態を一文で書く',
'そこへ進むために必要な知識を三〜五章に分け、前提の順に並べる',
'各章に確認課題を一つ付け、不足している素材を見つける'],
'例：資格教材なら「範囲の整理→分野別の理解→演習→復習」という案を作れます。ただし、実際の試験内容と照合して章立てを確定します。'),
'offer':('価格を数字だけで決めない演習','何を渡すかがまだ曖昧なら、値付けより商品の範囲と条件を優先します。',[
'単品・セット・定期更新など、受け取る内容を列挙する',
'購入者が比較する別の方法と、自分の商品にだけある価値を明記する',
'価格案・更新条件・対象外の人を同じシートに記録する'],
'例：「記事3本のセット」ではなく、何を順番に解決できるのかを説明します。価格は未検証なら仮の案として扱います。'),
'sales':('販売ページの下書きを作る演習','商品名を強調する前に、読者の判断に必要な材料があるかを調べます。',[
'困りごと→解決策→内容→根拠→対象外→FAQ→価格と受取方法を並べる',
'目次と実際に見られるサンプルを確保する',
'「向かない人」「更新範囲」「受取手順」を読み手の言葉で記載する'],
'例：「充実の教材」と書くより、実際の章見出し・問題サンプル・更新の扱いを並べた方が購入判断に役立ちます。'),
'reach':('無料記事と商品を一本の導線にする演習','SNS発信や検索記事を増やす前に、一つの困りごとについて「入口→答え→次の行動」を設計します。',[
'読者の検索する質問を一つ書き、無料記事で答える手順を決める',
'SNSで示す一つの論点と、記事で補う詳細を分ける',
'商品への導線は内容の違いと判断材料を明示し、無理な誘導を避ける'],
'例：無料記事では教材の目次の作り方を説明し、実際のテンプレートが必要な人にのみ設計ツールや教材を案内します。'),
'improve':('月に一度の改善記録を作る演習','数字は現在取得できる範囲から始めます。計測できない項目を想像で埋めないでください。',[
'記事の閲覧、販売ページの閲覧、販売件数など取得可能な項目と期間を記録する',
'読者が止まる箇所について仮説を一つ作る',
'次回までに一か所だけ直し、確認する指標を決める'],
'例：記事は読まれるのに商品説明へ進まないなら、価格変更より先に内部リンクの意味や置き場所を確認するという順序です。')}

CSS='/assets/site.css?v=3'
JS='/assets/studio.js?v=2'

def header(active=''):
 return f'''<header class="site-header"><div class="nav-wrap"><a class="brand" href="/"><span class="brand-mark">k.</span><span>経験をカタチにするLab <small>Knowledge Product Studio</small></span></a><nav aria-label="メインナビ"><a href="/academy/">学習カリキュラム</a><a class="{'active' if active=='learn' else ''}" href="/learn/">学ぶ</a><a class="{'active' if active=='studio' else ''}" href="/studio/">商品設計ボード</a><a class="{'active' if active=='thinking' else ''}" href="/thinking/">考える</a><a href="/diagram/">図解</a><a href="/guides/">読みもの</a><a href="/about/">このサイトについて</a></nav></div></header>'''

def layout(title, desc, body, active='',noindex=True, extra_script='', canonical_path='/'):
 metarobots='<meta name="robots" content="noindex,nofollow">' if noindex else ''
 canonical=SITE_ORIGIN+canonical_path
 return f'''<!doctype html><html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(title)} | 経験をカタチにするLab</title><meta name="description" content="{html.escape(desc)}">{metarobots}<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{html.escape(canonical)}"><meta name="twitter:card" content="summary"><link rel="canonical" href="{html.escape(canonical)}"><link rel="stylesheet" href="{CSS}"></head><body>{header(active)}{body}<footer class="footer"><div class="container footer-inner"><span>経験をカタチにするLab <span class="muted">— 商品の作り方を、考えるところから。</span></span><a href="/about/">運営・データについて</a><span class="muted">© 2026 Knowledge Product Studio</span></div></footer>{extra_script}</body></html>'''

def card(n,slug,title,desc):
 return f'<a class="lesson-card" href="/learn/{slug}/"><span class="chapter">LESSON {n}</span><span class="lesson-title">{html.escape(title)}</span><span class="lesson-desc">{html.escape(desc)}</span><span class="lesson-next">記事を読む <span aria-hidden="true">↗</span></span></a>'

home='''<main><div class="hero container"><div><span class="eyebrow"><span class="status-dot"></span> 自分の経験や知識を、役立つ形にする</span><h1>自分の経験を、<br><em>誰かに役立つ形に。</em><br>考えるところから始める。</h1><p class="lead">経験や知識はある。でも、何を誰に届ければよいか分からない。このLabでは、有料noteやPDF教材など、自分の経験を人の役に立つ商品へ変える考え方を学び、実際の企画まで整理できます。</p><div class="hero-actions"><a class="button primary" href="/academy/">カリキュラムから学ぶ <span>→</span></a><a class="button secondary" href="/learn/">6つのテーマから学ぶ</a><a class="button secondary" href="/thinking/">考えを深く整理する</a><a class="button secondary" href="/diagram/">図解を作る</a></div><div class="hero-foot">経験の整理 / 有料note / SEO / Webマーケティング / 教材づくり · 無料の学習から始める</div></div><div class="hero-illustration"><div class="sketch-head"><span>PRODUCT MAP</span><span>01 — 04</span></div><div class="sketch-center">あなたの<br><b>知識・経験</b></div><div class="sketch-branch">誰の悩み？ <span>→</span></div><div class="sketch-branch b2">何が変わる？ <span>→</span></div><div class="sketch-branch b3">どんな商品？ <span>→</span></div><div class="sketch-bottom">アイデア → 設計 → 販売 → 改善</div></div></div><section class="container section"><div class="section-heading"><div><div class="eyebrow">LEARNING ROADMAP</div><h2>作り方を、順序立てて学ぶ。</h2><p>一つずつ理解し、設計ボードに書き戻す。知識だけで終わらない構成です。</p></div><a class="simple-link" href="/learn/">学習テーマ一覧を見る ↗</a></div><div class="lesson-grid">'''+''.join(card(n,slug,title,desc) for n,slug,title,sub,desc,body,checks in LESSONS)+'''</div></section><section class="muted-section"><div class="container split"><div><div class="eyebrow">BUILD YOUR PRODUCT</div><h2>考えたことを、<br>そのまま設計に残す。</h2><p>記事で学んだ「誰に、何を、どんな形で届けるか」をボードに保存。企画の要点を編集しながら、最後にJSONで持ち出せます。</p><a class="button dark" href="/studio/">設計ボードを開く →</a></div><div class="feature-stack"><div class="feature"><strong>01</strong><div><b>課題と相手を整理</b><span>経験の棚卸しを商品アイデアに変える</span></div></div><div class="feature"><strong>02</strong><div><b>目次と価格を設計</b><span>中身と条件を決め、無理のない提供形態を選ぶ</span></div></div><div class="feature"><strong>03</strong><div><b>検証を続ける</b><span>売上の予測と実績を混同せず、改善を記録する</span></div></div></div></div></section><section class="container lab-course-cta"><div><span class="eyebrow">LEARN / PRACTICE / REVIEW</span><h2>経験の商品化からSEO・Webマーケティングまで。</h2><p>8つの学習領域を実例と演習で学び、非公式の理解度チェックで判断の練習ができます。売り方だけでなく、読者の課題を解く順番を学びます。</p></div><div class="hero-actions"><a class="button primary" href="/academy/">8領域のカリキュラムを見る →</a><a class="button secondary" href="/academy/cases/">実際のサイトを分析する →</a></div></section><section class="container section small-cta"><div><div class="eyebrow">OUR APPROACH</div><h2>売れると断定しない。<br>買う理由を、説明できるようにする。</h2><p>学習記事で考え方を確かめ、商品設計ボードに自分の判断を残す。売上を保証する仕組みではなく、誰に何を届けるかを自分の言葉で説明できる状態を目指します。</p></div></section></main>'''
(ROOT/'index.html').write_text(layout('経験や知識を商品にする方法｜有料note・PDF教材の作り方','仕事・趣味・勉強の経験を有料noteやPDF教材にするための学習サイト。経験の棚卸しから読者の課題、構成・価格・発信まで、記事と無料ツールで考えられます。',home,canonical_path='/'),encoding='utf-8')

learning='''<main class="container page-main"><div class="eyebrow">LEARN</div><h1>経験や知識を商品にする6つの学習テーマ</h1><p class="lead narrow">有料noteやPDF教材を作る前に、読者の困りごと、構成、価格、伝え方、改善までを順に考えます。最初のテーマが決まらない方は、経験の整理から始められます。</p><div class="notice"><strong>何を作るか決められない場合は</strong>、まず <a href="/guides/">経験と知識から考える読みもの</a> をご覧ください。</div><p class="academy-inline-link">SEOやWebマーケティングを含む学習経路は <a href="/academy/">8領域のカリキュラム</a> から確認できます。</p><div class="lesson-grid roomy">'''+''.join(card(n,slug,title,desc) for n,slug,title,sub,desc,body,checks in LESSONS)+'''</div><div class="bottom-panel"><h2>読みながら、あなたの商品の設計も進める</h2><p>入力した内容は現在の端末のブラウザに保存されます。アカウント登録やサーバーへの送信は行いません。</p><a class="button primary" href="/studio/">商品設計ボードへ →</a></div></main>'''
(ROOT/'learn'/'index.html').write_text(layout('経験や知識を商品にする学習テーマ一覧','有料noteやPDF教材を作りたい人へ。経験の棚卸し、構成、価格、販売ページ、発信、改善を6つの学習テーマで説明。',learning,active='learn',canonical_path='/learn/'),encoding='utf-8')

MD = MarkdownIt('commonmark', {'html': False}).enable('table')

def render_lesson_markdown(slug):
    path=ROOT/'content'/'lessons'/f'{slug}.md'
    text=path.read_text(encoding='utf-8')
    tokens=MD.parse(text)
    toc=[]
    chapter=0
    for i, token in enumerate(tokens):
        if token.type == 'heading_open' and token.tag in ('h2','h3'):
            title=tokens[i+1].content
            if token.tag=='h2':
                chapter+=1
                anchor=f'chapter-{chapter}'
                toc.append((title,anchor))
            else:
                anchor=f'chapter-{chapter}-detail-{i}'
            token.attrSet('id',anchor)
    html_body=MD.renderer.render(tokens, MD.options, {})
    html_body=re.sub(r'(<table>.*?</table>)', r'<div class="table-scroll">\1</div>', html_body, flags=re.S)
    nav='<nav class="article-toc" aria-label="この記事の目次"><strong>この記事の目次</strong><ol>'+''.join(f'<li><a href="#{html.escape(a)}">{html.escape(t)}</a></li>' for t,a in toc)+'</ol></nav>'
    return nav + '<div class="article-markdown">'+html_body+'</div>'

for idx,(n,slug,title,sub,desc,topics,checks) in enumerate(LESSONS):
  siblings=''.join(f'<a class="side-item {"selected" if slug==s else ""}" href="/learn/{s}/"><span>{n2}</span>{html.escape(t)}</a>' for n2,s,t,_,_,_,_ in LESSONS)
  sections=render_lesson_markdown(slug) if (ROOT/'content'/'lessons'/f'{slug}.md').exists() else ''.join(f'<section id="part-{i+1}" class="article-section"><h2>{html.escape(t)}</h2><p>{html.escape(txt)}</p></section>' for i,(t,txt) in enumerate(topics))
  checklist=''.join(f'<li>{html.escape(c)}</li>' for c in checks)
  x_title,x_intro,x_steps,x_example=SUPPLEMENTS[slug]
  exercise='' if (ROOT/'content'/'lessons'/f'{slug}.md').exists() else f'<section class="article-exercise"><span class="eyebrow">WORKSHEET / LESSON {n}</span><h2>{html.escape(x_title)}</h2><p>{html.escape(x_intro)}</p><ol>'+''.join(f'<li>{html.escape(step)}</li>' for step in x_steps)+f'</ol><p class="example">{html.escape(x_example)}</p></section>'
  sources='<div class="article-references"><strong>参照資料</strong><p><a href="https://developers.google.com/search/docs/fundamentals/creating-helpful-content?hl=ja" rel="noopener noreferrer" target="_blank">Google検索セントラル：ユーザーを第一に考えたコンテンツ</a></p><p><a href="https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap" rel="noopener noreferrer" target="_blank">Google検索セントラル：サイトマップ</a></p></div>' if slug=='reach' else ''
  nxt=LESSONS[idx+1] if idx+1<len(LESSONS) else None
  nextlink=f'<a class="next-lesson" href="/learn/{nxt[1]}/"><span>次のテーマ</span><strong>{html.escape(nxt[2])} →</strong></a>' if nxt else '<a class="next-lesson" href="/learn/"><span>学習を終えたら</span><strong>もう一度、自分の商品の課題を見直す →</strong></a>'
  notice='' 
  if slug=='reach':notice='' 
  body=f'''<main class="container article-layout"><article class="article"><div class="bread"><a href="/">ホーム</a> / <a href="/learn/">学ぶ</a> / テーマ{n}</div><div class="eyebrow">LESSON {n} / PRODUCT DESIGN</div><h1>{html.escape(title)}</h1><p class="article-lead">{html.escape(sub)}。</p>{notice}<div class="article-summary"><b>このテーマの到達点</b><p>{html.escape(desc)}</p></div>{sections}{exercise}{sources}<section class="article-section check-panel"><h2>制作時の確認ポイント</h2><ul>{checklist}</ul></section><section class="work-callout"><div class="eyebrow">APPLY WHAT YOU LEARN</div><h2>自分の商品で考えてみる</h2><p>このテーマで考えた項目を、商品設計ボードで直接開きます。入力中の企画は同じ端末に保存され、次のテーマにも引き継げます。</p><a class="button primary" href="/studio/?lesson={slug}">商品設計ボードを開く →</a></section>{nextlink}</article><aside class="article-sidebar"><div class="side-title">学習の目次</div>{siblings}<div class="side-note">作業中の企画は商品設計ボードへ。ページを移動しても入力内容は同じ端末に保存されます。</div><a class="button secondary small" href="/studio/">商品設計ボード ↗</a></aside></main>'''
  target=ROOT/'learn'/slug;target.mkdir(exist_ok=True)
  (target/'index.html').write_text(layout(f'{title}｜電子商材の作り方',f'{desc} 電子商材や有料noteの作り方を学ぶテーマ{n}。',body,active='learn',canonical_path=f'/learn/{slug}/'),encoding='utf-8')

studio='''<main class="container studio-main"><div class="bread"><a href="/">ホーム</a> / 商品設計ボード</div><div class="studio-heading"><div><div class="eyebrow">YOUR PRODUCT WORKSPACE</div><h1>商品設計ボード</h1><p>自分の知識と買い手の困りごとをつなぎ、一つの電子商材の設計を進めます。</p></div><div class="studio-actions"><span id="saveStatus" class="save-status" role="status" aria-live="polite">この端末に保存</span><button id="exportBtn" class="button secondary" type="button">JSONを書き出す</button><label for="importInput" class="button secondary file-label">JSONを読み込む</label><input id="importInput" type="file" accept="application/json,.json" hidden></div></div><div class="notice storage-note">この試作版では入力データはこのブラウザ内のみ（localStorage）に保存されます。別端末との同期、会員登録、バックアップはありません。消去に備え、JSONを書き出して保管してください。</div><div class="notice"><strong>商品を決める前に考えを整理したい場合：</strong> <a href="/thinking/">思考の整理室を開く →</a>。ここの記録と商品設計ボードは別々に保存されます。</div><div class="lesson-guide" id="lessonGuide" role="region" aria-live="polite" hidden></div><div class="studio-tabs" role="tablist" aria-label="設計画面の切り替え"><button class="tab active" data-panel="map" role="tab" aria-selected="true">商品マップ</button><button class="tab" data-panel="sheet" role="tab" aria-selected="false">商品設計シート</button><button class="tab" data-panel="review" role="tab" aria-selected="false">完成チェック</button></div><section id="panel-map" class="panel active"><div class="map-intro"><div><h2>商品アイデアの関係図</h2><p>下のカードを編集すると、このマップにも反映されます。まずは誰のどんな困りごとを扱うか考えます。</p></div><button class="simple-btn" type="button" id="resetSample">入力例に戻す</button></div><div class="product-map" id="productMap"><div class="map-layer"><div class="map-node top" id="node-experience"><span>持っている経験</span><strong data-field="experience"></strong></div><div class="map-node left" id="node-audience"><span>届けたい相手</span><strong data-field="audience"></strong></div><div class="map-node middle main-node" id="node-product"><span>作りたい商品</span><strong data-field="productName"></strong></div><div class="map-node right" id="node-problem"><span>相手の困りごと</span><strong data-field="problem"></strong></div><div class="map-node bottom" id="node-outcome"><span>購入後の変化</span><strong data-field="outcome"></strong></div></div></div><div class="quick-edit"><h3>まず、この5つを書き換える</h3><div class="field-grid"><label>自分の経験・知識<textarea name="experience" rows="2"></textarea></label><label>想定する読者・買い手<textarea name="audience" rows="2"></textarea></label><label>相手の困りごと<textarea name="problem" rows="2"></textarea></label><label>解決後にできること<textarea name="outcome" rows="2"></textarea></label><label class="wide">仮の商品名<input name="productName" type="text"></label></div></div></section><section id="panel-sheet" class="panel" hidden><div class="panel-head"><h2>商品設計シート</h2><p>各テーマで考えた内容を一枚にまとめます。途中でも保存できます。</p></div><div class="field-grid sheet-fields"><label>商品形式<select name="format"><option value="note記事">note有料記事</option><option value="PDF教材">PDF教材</option><option value="有料マガジン">有料マガジン</option><option value="Webアプリ">Webアプリ</option><option value="オンライン講座">オンライン講座</option><option value="その他">その他</option></select></label><label>価格案（円）<input type="number" name="price" min="0" step="1" placeholder="未定なら空欄"></label><label class="wide">販売する内容・目次<textarea name="outline" rows="5" placeholder="例：第1章… / 第2章…"></textarea></label><label class="wide">他の方法と比べた価値・根拠<textarea name="value" rows="3"></textarea></label><label class="wide">向いていない人・含まない内容<textarea name="exclusions" rows="3"></textarea></label><label class="wide">販売ページで証明できる材料<textarea name="evidence" rows="3" placeholder="目次、サンプル、制作経緯、確認できる実績"></textarea></label><label class="wide">販売先や届け方<textarea name="channel" rows="2" placeholder="例：note / ダウンロードリンク / その他"></textarea></label></div></section><section id="panel-review" class="panel" hidden><div class="panel-head"><h2>商品として説明できるか</h2><p>AIによる需要予測ではなく、入力済み項目と設計上の確認です。販売や売上を保証するものではありません。</p></div><div id="reviewList" class="review-list"></div><div class="review-hint">空欄や未確認を整理した後、商品の本文・目次・サンプルを制作してください。現時点で外部サービスへの自動投稿は行いません。</div></section><div class="studio-bottom"><a href="/learn/">← 6テーマの教材へ戻る</a><button id="clearBtn" class="text-danger" type="button">この端末の入力を初期化</button></div></main>'''
(ROOT/'studio'/'index.html').write_text(layout('商品設計ボード｜電子商材の企画を整理する','経験・課題・商品構成・価格・販売条件を一か所に整理。電子商材の企画を端末内に保存・JSON出力できます。',studio,active='studio',extra_script=f'<script defer src="{JS}"></script>',canonical_path='/studio/'),encoding='utf-8')
about='''<main class="container page-main prose"><div class="eyebrow">ABOUT</div><h1>このサイトについて</h1><p>経験をカタチにするLab（KPS）は、自分の仕事・勉強・創作経験を、有料noteやPDF教材など役立つ形にしたい人のための学習・設計サイトです。商品化を急がず、読者の困りごとと自分の経験を結ぶ考え方から扱います。収益や販売結果を保証するものではありません。</p><h2>教材について</h2><p>個人の教材制作、note運営、Webアプリ開発の経験と、商品設計に関する調査をもとに構成しています。教材では、課題の切り取りから改善までの設計を扱っています。試験対策教材などのケースは方法を説明するための企画例です。未確認の販売実績や制度情報を事実として表示しません。</p><h2>運営と制作経験について</h2><p>このサイトでは、運営者自身のnote記事制作、コーヒーの学習教材づくり、Webツール制作の試行錯誤から得た判断も素材にしています。制作経験と一般的な助言は区別し、売上などの未確認実績を成果として示しません。関連する発信は <a href="https://note.com/kakeruxkakeru" rel="noopener noreferrer" target="_blank">運営者のnote</a> でも確認できます。</p><h2>保存・プライバシーについて</h2><p>思考ノート・商品設計ボード・図解の下書きは、基本的に利用端末のブラウザ内へ保存します。端末を変えたりブラウザのデータを削除すると、記録が失われる可能性があります。必要なデータはJSON形式で書き出して保管してください。図解エディターの編集・PNG書き出し・JSON保存・色の保存はログインなしで無料利用できます。色はこの端末に保存され、既存アカウントの利用者に限って従来の色データを追加で読み込む場合があります。思考ノートや商品設計ボードの本文は自動的にアカウントへ同期されません。</p><h2>サービスの状態</h2><p>本サイトは「経験をカタチにするLab」です。商品企画、SEO、Webマーケティングを段階的に学べる構成へ拡張中です。独自の理解度チェックは非公式で、公的な資格や認定ではありません。現状は公開前の試作版です。図解エディターの有料制限は解除し、PNG書き出しと色の保存を含む基本機能を無料公開しています。アカウントへのログインは任意です。外部AIとのJSON受け渡しは可能ですが、AI APIによる自動生成やnoteへの自動投稿、Museとの直接連携は実装していません。正式公開前に機能や表記を見直します。</p><a class="button secondary" href="/">ホームに戻る →</a></main>'''
(ROOT/'about').mkdir(exist_ok=True)
(ROOT/'about'/'index.html').write_text(layout('運営とデータ保存について','経験をカタチにするLabの目的、教材の状態、商品設計ボードの保存・プライバシー方針を案内します。',about,canonical_path='/about/'),encoding='utf-8')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://knowledge-product-studio.vercel.app/sitemap.xml\n',encoding='utf-8')
from xml.sax.saxutils import escape as xml_escape
paths=['/','/learn/']+[f'/learn/{slug}/' for _,slug,*_ in LESSONS]+['/studio/','/thinking/','/diagram/','/guides/','/guides/experience-to-product/','/guides/paid-note-theme/','/guides/note-vs-pdf/','/academy/','/academy/seo/','/academy/cases/','/academy/check/','/about/']
xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{xml_escape(SITE_ORIGIN+path)}</loc></url>\n' for path in paths)+'</urlset>\n'
(ROOT/'sitemap.xml').write_text(xml,encoding='utf-8')
(ROOT/'vercel.json').write_text(json.dumps({'cleanUrls':True,'trailingSlash':True,'headers':[{'source':'/(.*)','headers':[{'key':'X-Robots-Tag','value':'noindex, nofollow'},{'key':'X-Content-Type-Options','value':'nosniff'},{'key':'Referrer-Policy','value':'strict-origin-when-cross-origin'}]}]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if not (ROOT/'README.md').exists():
    (ROOT/'README.md').write_text('''# 経験をカタチにするLab / Knowledge Product Studio\n\n電子商材の作り方を学びながら、自分の商品企画を形にするWebサイトの初期版です。\n\n## 現状\n\n- 学ぶ：テーマ1,2,3,4,6の教材プレビュー、テーマ5の新規執筆レビュー版\n- 考える：思考の整理室（問い、経験、理由、価値基準、選択肢、判断履歴）\n- 作る：商品マップ、商品設計シート、完成チェック\n- 保存：localStorage、JSONエクスポート・インポート（ユーザーデータはサーバー非送信）\n- SEO：静的記事別URL、固有title/description、内部リンクを実装。ただし公開前レビューのため全ページnoindex\n- 未実装：ユーザー認証、同期、決済、Muse連携、note投稿、Analytics/SC連携\n\n思考ノートは別キー `kps-thought-v1`。JSONエクスポート・インポートは商品設計ボードと互換性を持たせず、勝手に移植しない。非公開COS Brainは公開KPSへ複製しない。\n\n## 手元で起動\n\n`python3 -m http.server 8000` をこのディレクトリで実行して `http://localhost:8000` へアクセス。静的ファイルのみで動作します。\n\n## 記事の出典と編集状態\n\n2026-11-01に提供された学習ハブのテーマ1,2,3,4,6のMarkdown原稿を資料に、新サイト向けに要点を再構成。原稿は本人による公開前レビュー前提。テーマ5は原稿未提供のため、Google公式資料を確認して独立執筆した教材です。運営者の確認前です。\n\n## 運営構成\n\n- COS（既存の private repo）：運営者Brain、Knowledge、監査、記事企画の正本。**内容を直接公開しない**。\n- 本リポジトリ：公開予定の教材と利用者向けアプリのソース。\n- Vercel：静的ホスティング（Production READY）。\n- 将来のユーザーデータ保管：独立したDB/認証基盤へ。GitHub commitをユーザー操作の保存先にしない。\n\n## 公開前チェック\n\n1. ブランド名・サイトURLの確定・運営者連絡先・プライバシーポリシーを確定\n2. テーマ5の新規原稿およびテーマ1〜6を全て運営者が編集確認\n3. すでに準備済みのsitemap.xml・canonicalを監査し、OG画像や運営者情報を整備した後、noindexを解除\n4. 記事・スマホUI・保存/復元・各リンクを実機点検\n5. 本番公開後にGoogle Search Consoleなどを接続\n
## 2026-11-01 第2工程

- 各テーマに具体的演習と商品設計ボードへのテーマ別誘導を追加。既存の保存キー `kps-product-v1` とJSON形式は変更しない。
- テーマ5は外部一次資料を参照した別原稿。ユーザー提供の原稿ではないことを記録。
- `sitemap.xml`、canonical、OG URLを生成。`robots.txt` はクロールを許可し、ページおよびレスポンスヘッダーの `noindex` で索引登録を保留。
- Chromeの実ブラウザーQAおよび運営者による文章確認が済むまで、Google索引登録は開始しない。

`python tests/smoke.py` と `node --check assets/studio.js` により基本チェック。
''',encoding='utf-8')
print('Generated pages:',len(list(ROOT.rglob('*.html'))))
