"""Dependency-light route/SEO/static data checks; optional Playwright browser smoke."""
from html.parser import HTMLParser
import http.server
import socketserver
import threading
from pathlib import Path
from urllib.parse import urlparse, quote
import xml.etree.ElementTree as ET
import json

ROOT = Path(__file__).resolve().parents[1]
LESSONS=('problem','design','offer','sales','reach','improve')
PAGES=['/','/learn/',*[f'/learn/{x}/' for x in LESSONS],'/studio/','/thinking/','/diagram/','/guides/','/guides/experience-to-product/','/guides/paid-note-theme/','/guides/note-vs-pdf/','/academy/','/academy/seo/','/academy/cases/','/academy/check/','/about/']
ORIGIN='https://knowledge-product-studio.vercel.app'
class AuditParser(HTMLParser):
    def __init__(self): super().__init__();self.links=[];self.canon=[];self.robots=[];self.h1=0;self.description=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='a' and a.get('href'):self.links.append(a['href'])
        if tag=='link' and a.get('rel')=='canonical':self.canon.append(a.get('href'))
        if tag=='meta' and a.get('name')=='robots':self.robots.append(a.get('content'))
        if tag=='meta' and a.get('name')=='description':self.description.append(a.get('content'))
        if tag=='h1':self.h1+=1

def static():
    for route in PAGES:
        f=ROOT/route.lstrip('/')/'index.html'
        p=AuditParser();p.feed(f.read_text('utf-8'))
        assert p.canon==[ORIGIN+route],(route,'canonical',p.canon)
        assert p.robots==['noindex,nofollow'],(route,'robots',p.robots)
        assert p.h1==1,(route,'h1',p.h1)
        assert len(p.description)==1 and len(p.description[0])>20,route
        for href in p.links:
            if href.startswith('/'):
                u=urlparse(href).path
                q=ROOT/u.lstrip('/')/'index.html' if u.endswith('/') else ROOT/u.lstrip('/')
                assert q.exists(),(route,href)
    xml=ET.parse(ROOT/'sitemap.xml')
    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    locs=[e.text for e in xml.findall('.//s:loc',ns)]
    assert len(locs)==len(PAGES) and set(locs)==set(ORIGIN+p for p in PAGES)
    assert 'Allow: /' in (ROOT/'robots.txt').read_text()
    conf=json.loads((ROOT/'vercel.json').read_text())
    assert 'noindex' in json.dumps(conf)
    # SEO content intentionally remains noindex until editorial release; entry cluster is distinct.
    guide_pages=['experience-to-product','paid-note-theme','note-vs-pdf']
    for slug in guide_pages:
        doc=(ROOT/'guides'/slug/'index.html').read_text('utf-8')
        assert '<h1>' in doc and 'noindex,nofollow' in doc
        assert 'href="/guides/"' in doc and 'href="/learn/' in doc
    assert 'href="/guides/"' in (ROOT/'index.html').read_text('utf-8')
    assert '経験をカタチにするLab' in (ROOT/'index.html').read_text('utf-8')
    for section in ['','seo/','cases/','check/']:
        article=(ROOT/'academy'/section/'index.html').read_text('utf-8')
        assert '経験をカタチにするLab' in article
        assert 'noindex,nofollow' in article
    assert '非公式' in (ROOT/'academy'/'check'/'index.html').read_text('utf-8')
    assert (ROOT/'assets'/'academy-check.js').is_file()


    # Diagram editing and JSON export must work without authentication.
    diagram_js = (ROOT/'assets'/'diagram.js').read_text('utf-8')
    assert "const URL=" not in diagram_js, 'URL shadowing breaks URL.createObjectURL download'
    assert 'URL.createObjectURL' in diagram_js
    assert "const SUPABASE_URL=" in diagram_js
    assert 'saveJsonFile' in diagram_js
    assert 'AUTH_RETURN' in diagram_js
    # Separate KPS OTP flow: same Supabase identity, independent session and logout.
    assert "storageKey:'kps-diagram-auth'" in diagram_js
    assert "detectSessionInUrl:false" in diagram_js
    assert "shouldCreateUser:true" in diagram_js
    assert "verifyOtp({email:otpEmail,token,type:'email'})" in diagram_js
    assert "signOut({scope:'local'})" in diagram_js
    assert "auth.signOut()" not in diagram_js
    diagram_html=(ROOT/'diagram'/'index.html').read_text('utf-8')
    assert 'id="authCode"' in diagram_html and 'id="authVerifyForm"' in diagram_html
    assert 'id="authRequestForm"' in diagram_html
    assert '¥2,980' not in diagram_html and 'licenseDialog' not in diagram_html
    assert 'PNGを無料保存' in diagram_html
    assert 'すべて無料で利用できます' in diagram_html
    assert "PALETTE_KEY='kps-diagram-colors-v1'" in diagram_js
    assert "if(!licensed){$('licenseDialog')" not in diagram_js
    assert "setItem(PALETTE_KEY" in diagram_js
    assert "width:w,height:h" in diagram_js, 'import must preserve custom canvas dimensions'
    assert "if(!confirm('現在の図解を入力したJSONで置き換えますか？'))" not in diagram_js, 'no blocking dialog for JSON paste'
    assert "if(!confirm('現在の図解を新しいファイルに置き換えますか？'))" not in diagram_js, 'no blocking dialog for file import'
    assert "scene.width*mul" in diagram_js and "scene.height*mul" in diagram_js, 'PNG uses loaded canvas dimensions'
    assert 'id="canvasSizeLabel"' in diagram_html and 'id="jsonImportStatus"' in diagram_html, 'visible size and import result'
    assert 'id="copyImportUrl"' in diagram_html and 'id="importUrlFallback"' in diagram_html, 'URL import link UI'
    assert "window.addEventListener('hashchange',importFromLocationHash)" in diagram_js, 'URL import must work without typing'
    assert "window.history.replaceState" in diagram_js, 'successful import must clear sensitive hash'
    assert "resetFrom(data,'URL')" in diagram_js, 'URL import uses same validated path as file import'
    assert "window.location.hash" in diagram_js, 'fragment-based import, never URL query sent to server'
    assert "MAX_IMPORT_URL_CHARS=32000" in diagram_js, 'URL length cap'
    sample = json.loads((ROOT/'diagram'/'example.json').read_text('utf-8'))
    assert sample['schema']=='kps-diagram-v1' and len(sample['elements'])>=3
    assert 'v=7' in (ROOT/'diagram'/'index.html').read_text('utf-8')
    assert "const KEY='kps-thought-v1'" in (ROOT/'assets'/'thinking.js').read_text()
    assert "const KEY='kps-product-v1'" in (ROOT/'assets'/'studio.js').read_text()
    for slug in LESSONS:
        assert f'lesson={slug}' in (ROOT/'learn'/slug/'index.html').read_text()
    # User-supplied original five lessons must remain full-length editorial articles.
    from html.parser import HTMLParser
    class LessonContentParser(HTMLParser):
        def __init__(self): super().__init__();self.h2=0;self.h3=0;self.toc=0;self.scroll=0
        def handle_starttag(self,tag,attrs):
            a=dict(attrs)
            if tag=='h2':self.h2+=1
            if tag=='h3':self.h3+=1
            if tag=='a' and (a.get('href') or '').startswith('#chapter-'):self.toc+=1
            if tag=='div' and 'table-scroll' in a.get('class','').split():self.scroll+=1
    for slug in ('problem','design','offer','sales','improve'):
        article= (ROOT/'learn'/slug/'index.html').read_text('utf-8')
        parsed=LessonContentParser();parsed.feed(article)
        assert len(article)>6500,(slug,'summary page rather than full article')
        assert parsed.h2>=6 and parsed.h3>=4 and parsed.toc==5,(slug,parsed.h2,parsed.h3,parsed.toc)
        assert '公開前に本人が' not in article,(slug,'editorial note leaked into reader view')
        if slug in ('sales','improve'):assert parsed.scroll>=1,(slug,'table overflow')
    print(f'Static checks OK: {len(PAGES)} HTML pages, all internal links, canonical, sitemap, robots, article/studio links')

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
    def log_message(self,*a):pass

def browser():
    try:from playwright.sync_api import sync_playwright, Error as PlaywrightError
    except ImportError:
        print('Playwright unavailable: browser tests skipped');return
    with socketserver.ThreadingTCPServer(('127.0.0.1',0),Handler) as server:
        t=threading.Thread(target=server.serve_forever,daemon=True);t.start()
        base='http://127.0.0.1:'+str(server.server_address[1])
        try:
            with sync_playwright() as playwright:
                import shutil
                chromium_path=shutil.which('chromium') or shutil.which('chromium-browser')
                launch_args={'headless':True,'args':['--no-sandbox']}
                if chromium_path:launch_args['executable_path']=chromium_path
                browser=playwright.chromium.launch(**launch_args)
                for width in [390,1280]:
                    ctx=browser.new_context(viewport={'width':width,'height':850},accept_downloads=True)
                    page=ctx.new_page();errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
                    for route in PAGES:
                        try:response=page.goto(base+route)
                        except PlaywrightError as e:
                            if 'ERR_BLOCKED_BY_ADMINISTRATOR' in str(e):
                                print('Browser QA skipped: Chromium navigation is blocked by container policy')
                                browser.close()
                                return
                            raise
                        assert response.status==200,(route,response.status)
                        assert page.locator('h1').count()==1
                    # Set existing saved user data, and verify context navigation doesn't overwrite it
                    page.goto(base+'/studio/')
                    page.locator('[name="audience"]').fill('保存済みの読者')
                    page.locator('[name="problem"]').fill('保存済みの課題')
                    page.wait_for_timeout(600)
                    page.goto(base+'/learn/design/')
                    page.locator('.work-callout a').click()
                    assert 'lesson=design' in page.url
                    assert page.locator('#lessonGuide').is_visible()
                    assert page.locator('#panel-sheet').is_visible()
                    page.locator('#lessonGuide button').click()
                    assert page.locator('[name="outline"]').evaluate('(x)=>x===document.activeElement')
                    page.goto(base+'/studio/?lesson=problem')
                    assert page.locator('[name="audience"]').input_value()=='保存済みの読者'
                    assert page.locator('[name="problem"]').input_value()=='保存済みの課題'
                    # Thought notes must persist without changing product-board storage.
                    page.goto(base+'/thinking/')
                    page.locator('#thinkTitle').fill('なぜ仕組みを作るのか')
                    page.locator('[data-thought="principle"]').fill('選べる範囲を増やしたい')
                    page.locator('#saveSnapshot').click()
                    page.wait_for_timeout(550)
                    page.reload()
                    assert page.locator('#thinkTitle').input_value()=='なぜ仕組みを作るのか'
                    assert page.locator('.snapshot').count()==1
                    page.goto(base+'/studio/')
                    assert page.locator('[name="audience"]').input_value()=='保存済みの読者'
                    # export still contains original schema and saved data
                    with page.expect_download() as d:page.locator('#exportBtn').click()
                    dl=d.value
                    file=Path('/tmp/kps-smoke-export.json');dl.save_as(file)
                    data=json.loads(file.read_text())
                    assert data['schema']=='knowledge-product-studio/product-v1'
                    assert data['product']['audience']=='保存済みの読者'
                    # responsive horizontal overflow should not make entire site scroll sideways
                    for route in ['/', '/learn/reach/','/studio/?lesson=offer','/thinking/']:
                        page.goto(base+route)
                        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 2'),(route,width,page.evaluate('document.documentElement.scrollWidth'))
                    assert not errs,(width,errs)
                    # Mock only the network Auth SDK: never send a real email in tests.
                    auth_ctx=browser.new_context(viewport={'width':width,'height':850},accept_downloads=True)
                    auth_ctx.add_init_script("""
                        window.__kpsMockCalls=[];
                        window.supabase={createClient:function(url,key,options){
                          window.__kpsMockCalls.push({op:'init',storageKey:options.auth.storageKey,detectSessionInUrl:options.auth.detectSessionInUrl});
                          const listeners=[];
                          const user={id:'00000000-0000-4000-8000-000000000001',email:'sample-owner@example.com'};
                          const auth={
                            getSession:async()=>({data:{session:null},error:null}),
                            getUser:async()=>({data:{user},error:null}),
                            onAuthStateChange:callback=>{listeners.push(callback);return{data:{subscription:{unsubscribe:()=>{}}}};},
                            signInWithOtp:async args=>{window.__kpsMockCalls.push({op:'send',email:args.email,options:args.options});return{data:{session:null},error:null};},
                            verifyOtp:async args=>{window.__kpsMockCalls.push({op:'verify',token:args.token,type:args.type});
                              if(args.token!=='123456')return{error:{message:'Invalid code'},data:null};
                              const session={user};listeners.forEach(cb=>cb('SIGNED_IN',session));
                              return{data:{session,user},error:null};},
                            signOut:async args=>{window.__kpsMockCalls.push({op:'signout',scope:args.scope});listeners.forEach(cb=>cb('SIGNED_OUT',null));return{error:null};}
                          };
                          return{auth,from:table=>({select(){return this},eq(){return this},maybeSingle:async()=>{
                            return{data:table==='kps_diagram_entitlements'?{active:true}:null,error:null};}})};
                        }};
                    """)
                    auth_page=auth_ctx.new_page()
                    assert auth_page.goto(base+'/diagram/',wait_until='domcontentloaded').status==200
                    # JSON and PNG downloads require no login and no purchase.
                    with auth_page.expect_download() as d:auth_page.locator('#saveJsonTop').click()
                    assert d.value.suggested_filename.endswith('.json')
                    with auth_page.expect_download() as png:auth_page.locator('#exportPng').click()
                    assert png.value.suggested_filename.endswith('.png')
                    # Regression from Muse handoff (2026-11-07): imports must work even
                    # when the browser automatically dismisses JavaScript confirm dialogs.
                    # Import never needs a blocking prompt; previous data is kept in Undo.
                    auth_page.on('dialog', lambda dlg: dlg.dismiss())
                    import struct
                    one_box={'schema':'kps-diagram-v1','width':1100,'height':400,'background':'#FAF5EE',
                       'elements':[{'id':'el-1','type':'box','x':100,'y':100,'w':600,'h':120,
                         'text':'テスト確認','fill':'#F1E6D2','stroke':'#B08D5F',
                         'color':'#3B2A1E','size':28,'radius':14,'angle':0,'opacity':100,
                         'font':'sans','align':'center','z':1}]}
                    auth_page.locator('#codeToggle').click()
                    auth_page.locator('#jsonEditor').fill(json.dumps(one_box,ensure_ascii=False))
                    auth_page.locator('#applyJson').click()
                    assert auth_page.locator('#stage .d-element').count()==1
                    assert auth_page.locator('#stage').inner_text().strip()=='テスト確認'
                    assert auth_page.locator('#canvasSizeLabel').inner_text()=='1100 × 400px'
                    assert auth_page.locator('#stage').evaluate("(el)=>el.style.height")=='400px'
                    assert '1要素' in auth_page.locator('#jsonImportStatus').inner_text()
                    assert json.loads(auth_page.evaluate("localStorage.getItem('kps-diagram-draft-v1')"))['scene']['height']==400
                    assert '選択肢を増やしたい' in auth_page.evaluate("localStorage.getItem('kps-diagram-previous-before-import-v1')")
                    with auth_page.expect_download() as exported:
                        auth_page.locator('#exportPng').click()
                    png_file=Path('/tmp/kps-import-custom-canvas.png')
                    exported.value.save_as(png_file)
                    png_bytes=png_file.read_bytes()
                    assert png_bytes[:8]==b'\x89PNG\r\n\x1a\n'
                    assert struct.unpack('>II',png_bytes[16:24])==(2200,800)
                    # Failed imports must preserve the visible diagram and show why.
                    auth_page.locator('#jsonEditor').fill('{"schema":"wrong","elements":[]}')
                    auth_page.locator('#applyJson').click()
                    assert auth_page.locator('#stage').inner_text().strip()=='テスト確認'
                    assert '読み込めません' in auth_page.locator('#jsonImportStatus').inner_text()
                    # Original 1100x660 sample and the custom-size diagram remain undoable.
                    auth_page.locator('#undo').click()
                    assert auth_page.locator('#stage .d-element').count()==3
                    assert auth_page.locator('#canvasSizeLabel').inner_text()=='1100 × 660px'
                    auth_page.locator('#redo').click()
                    assert auth_page.locator('#stage').inner_text().strip()=='テスト確認'
                    assert auth_page.locator('#canvasSizeLabel').inner_text()=='1100 × 400px'
                    # Simulate the user's 15-element diagram; test actual file input.
                    many={'schema':'kps-diagram-v1','width':1100,'height':880,'background':'#FAF5EE',
                          'elements':[{**one_box['elements'][0],'id':f'row-{i}','type':'box',
                            'text':f'産地一覧 {i+1}','x':25+(i%3)*360,'y':30+(i//3)*160,
                            'w':325,'h':140} for i in range(15)]}
                    auth_page.locator('#openJson').set_input_files({
                       'name':'15-origin-regions.json','mimeType':'application/json',
                       'buffer':json.dumps(many,ensure_ascii=False).encode('utf-8')})
                    # The file input handler reads File.text() asynchronously.
                    # Wait for the import rather than checking the old DOM immediately.
                    auth_page.wait_for_function("document.querySelectorAll('#stage .d-element').length===15",timeout=12000)
                    assert auth_page.locator('#stage .d-element').count()==15
                    assert auth_page.locator('#canvasSizeLabel').inner_text()=='1100 × 880px'
                    assert '15要素' in auth_page.locator('#saveStatus').inner_text()
                    auth_page.reload(wait_until='domcontentloaded')
                    assert auth_page.locator('#stage .d-element').count()==15
                    assert auth_page.locator('#canvasSizeLabel').inner_text()=='1100 × 880px'
                    with auth_page.expect_download() as many_png:
                        auth_page.locator('#exportPng').click()
                    many_file=Path('/tmp/kps-import-15-elements.png')
                    many_png.value.save_as(many_file)
                    assert struct.unpack('>II',many_file.read_bytes()[16:24])==(2200,1760)

                    # Muse handoff (2026-11-07): AI opens a URL; it must import
                    # without typing in a textarea or relying on synthetic input events.
                    auth_page.locator('#codeToggle').click()
                    auth_page.evaluate("""() => {
                      Object.defineProperty(navigator,'clipboard',{
                        configurable:true,
                        value:{writeText:async text=>{window.__diagramUrlCopied=text}}
                      });
                    }""")
                    auth_page.locator('#copyImportUrl').click()
                    auth_page.wait_for_function("typeof window.__diagramUrlCopied==='string'")
                    generated_link=auth_page.evaluate('window.__diagramUrlCopied')
                    assert generated_link.startswith(base+'/diagram/#import=b64.')
                    assert len(generated_link)<32000
                    assert 'URLをコピー' in auth_page.locator('#jsonImportStatus').inner_text()
                    # A second page in the same browser starts from the 15-element
                    # saved draft. A link import must auto-run, confirm success, then
                    # remove the JSON fragment from the address bar.
                    linked_page=auth_ctx.new_page()
                    assert linked_page.goto(generated_link,wait_until='domcontentloaded').status==200
                    linked_page.wait_for_function(
                        "document.querySelectorAll('#stage .d-element').length===15 && window.location.hash===''")
                    assert linked_page.locator('#canvasSizeLabel').inner_text()=='1100 × 880px'
                    assert 'URLを反映しました' in linked_page.locator('#saveStatus').inner_text()
                    # Percent-encoded JSON is accepted as well as compact base64url.
                    # This URL differs from the saved 15-element scene.
                    from_url={**one_box,'height':760,'elements':[
                        {**one_box['elements'][0],'text':'URL入力確認'}]}
                    plain_link=base+'/diagram/#import='+quote(
                        json.dumps(from_url,ensure_ascii=False,separators=(',',':')),safe='')
                    assert linked_page.goto(plain_link,wait_until='domcontentloaded').status==200
                    linked_page.wait_for_function(
                        "document.querySelectorAll('#stage .d-element').length===1 && document.querySelector('#canvasSizeLabel').textContent==='1100 × 760px' && window.location.hash===''")
                    assert linked_page.locator('#stage').inner_text().strip()=='URL入力確認'
                    assert '産地一覧 1' in linked_page.evaluate(
                        "localStorage.getItem('kps-diagram-previous-before-import-v1')")
                    with linked_page.expect_download() as url_png:
                        linked_page.locator('#exportPng').click()
                    url_file=Path('/tmp/kps-import-from-url.png')
                    url_png.value.save_as(url_file)
                    assert struct.unpack('>II',url_file.read_bytes()[16:24])==(2200,1520)
                    # An invalid link reports an error, without touching the drawing.
                    assert linked_page.goto(base+'/diagram/#import=b64.bad!data',
                        wait_until='domcontentloaded').status==200
                    linked_page.wait_for_function(
                        "document.querySelector('#jsonImportStatus').textContent.includes('読み込めません')")
                    assert linked_page.locator('#stage').inner_text().strip()=='URL入力確認'
                    linked_page.locator('#undo').click()
                    assert linked_page.locator('#stage .d-element').count()==15
                    assert linked_page.locator('#canvasSizeLabel').inner_text()=='1100 × 880px'
                    linked_page.close()
                    # If clipboard access is blocked, a selectable link must appear.
                    auth_page.evaluate("""() => {
                      Object.defineProperty(navigator,'clipboard',{
                        configurable:true,value:{writeText:async()=>{throw Error('blocked')}}
                      });
                    }""")
                    auth_page.locator('#copyImportUrl').click()
                    assert auth_page.locator('#importUrlFallback').is_visible()
                    assert '#import=b64.' in auth_page.locator('#importUrlFallback').input_value()

                    # Saving a color uses localStorage, including after a page reload.
                    auth_page.locator('.d-element').first.click()
                    auth_page.locator('#fillColor').evaluate("(el)=>{el.value='#a1b2c3';el.dispatchEvent(new Event('input',{bubbles:true}))}")
                    auth_page.locator('#savePalette').click()
                    assert auth_page.evaluate("JSON.parse(localStorage.getItem('kps-diagram-colors-v1')).includes('#a1b2c3')")
                    auth_page.reload()
                    assert auth_page.evaluate("JSON.parse(localStorage.getItem('kps-diagram-colors-v1')).includes('#a1b2c3')")
                    auth_page.locator('#accountBtn').click()
                    auth_page.locator('#authEmail').fill('sample-owner@example.com')
                    auth_page.locator('#sendLink').click()
                    auth_page.wait_for_selector('#authVerifyForm:not([hidden])')
                    auth_page.locator('#authCode').fill('123456')
                    auth_page.locator('#verifyCode').click()
                    auth_page.wait_for_function("document.getElementById('accountBtn').textContent.includes('KPSログイン済み')")
                    assert auth_page.url.endswith('/diagram/')
                    auth_page.locator('#accountBtn').click()
                    auth_page.locator('#signOut').click()
                    actions=auth_page.evaluate('window.__kpsMockCalls')
                    assert actions[0]['storageKey']=='kps-diagram-auth'
                    assert actions[0]['detectSessionInUrl'] is False
                    assert any(x.get('op')=='send' and x['options'].get('shouldCreateUser') is True for x in actions)
                    assert any(x.get('op')=='verify' and x['type']=='email' for x in actions)
                    assert any(x.get('op')=='signout' and x['scope']=='local' for x in actions)
                    auth_ctx.close()
                    ctx.close()
                browser.close()
            print('Chromium smoke OK: mobile 390 and desktop 1280, route loading, links, lesson context, autosave and JSON export')
        finally:
            server.shutdown();t.join(timeout=3)

if __name__=='__main__':
    static();browser()
