"""Dependency-light route/SEO/static data checks; optional Playwright browser smoke."""
from html.parser import HTMLParser
import http.server
import socketserver
import threading
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
import json

ROOT = Path(__file__).resolve().parents[1]
LESSONS=('problem','design','offer','sales','reach','improve')
PAGES=['/','/learn/',*[f'/learn/{x}/' for x in LESSONS],'/studio/','/about/']
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
    with socketserver.TCPServer(('127.0.0.1',0),Handler) as server:
        t=threading.Thread(target=server.serve_forever,daemon=True);t.start()
        base='http://127.0.0.1:'+str(server.server_address[1])
        try:
            with sync_playwright() as playwright:
                browser=playwright.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
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
                    # export still contains original schema and saved data
                    with page.expect_download() as d:page.locator('#exportBtn').click()
                    dl=d.value
                    file=Path('/tmp/kps-smoke-export.json');dl.save_as(file)
                    data=json.loads(file.read_text())
                    assert data['schema']=='knowledge-product-studio/product-v1'
                    assert data['product']['audience']=='保存済みの読者'
                    # responsive horizontal overflow should not make entire site scroll sideways
                    for route in ['/', '/learn/reach/','/studio/?lesson=offer']:
                        page.goto(base+route)
                        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 2'),(route,width,page.evaluate('document.documentElement.scrollWidth'))
                    assert not errs,(width,errs)
                    ctx.close()
                browser.close()
            print('Chromium smoke OK: mobile 390 and desktop 1280, route loading, links, lesson context, autosave and JSON export')
        finally:
            server.shutdown();t.join(timeout=3)

if __name__=='__main__':
    static();browser()
