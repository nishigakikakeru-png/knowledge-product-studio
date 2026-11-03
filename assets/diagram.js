(()=>{'use strict';
const SCHEMA='kps-diagram-v1',KEY='kps-diagram-draft-v1', W=1100,H=660, MAX=100, COLORS=['#ffffff','#202a38','#dfeaf1','#e5c0a0','#8dbcc4','#f4deaf','#7291b5','#cee1cc'];
const SUPABASE_URL='https://kknhlihfrkyebebkockh.supabase.co', PUBLISHABLE='sb_publishable_zaCpsdP0HCh3C4vBmCBdeg_qnns3oar',AUTH_RETURN='https://knowledge-product-studio.vercel.app/diagram/';
const $=id=>document.getElementById(id),stage=$('stage'),space=$('stageSpace'),viewport=$('viewport'),inspector=$('inspector');
const fonts={sans:'"Noto Sans JP","Yu Gothic",sans-serif',serif:'"Noto Serif JP","Yu Mincho",serif',mono:'ui-monospace,monospace'};
let db=null,user=null,licensed=false,selected=null,scale=1,drag=null,saveTimer=null,history=[],future=[];
const uid=()=>typeof crypto!=='undefined'&&crypto.randomUUID?crypto.randomUUID():'d'+Date.now()+Math.random().toString(36).slice(2);
function defaultScene(){return{schema:SCHEMA,width:W,height:H,background:'#ffffff',elements:[
{id:uid(),type:'box',x:100,y:110,w:900,h:170,text:'選択肢を増やしたい',fill:'#e8f1f4',stroke:'#8da7b8',color:'#183445',size:43,radius:24,angle:0,opacity:100,font:'sans',align:'center',z:1},
{id:uid(),type:'arrow',x:535,y:310,w:35,h:40,text:'',fill:'#ffffff',stroke:'#738a97',color:'#738a97',size:25,radius:0,angle:90,opacity:100,font:'sans',align:'center',z:2},
{id:uid(),type:'box',x:185,y:385,w:730,h:128,text:'自分で収益を生む仕組みを作る',fill:'#ffffff',stroke:'#95a8b5',color:'#20384a',size:34,radius:15,angle:0,opacity:100,font:'sans',align:'center',z:3}
]};}
let scene=defaultScene();
const number=(x,lo,hi,d)=>Number.isFinite(+x)?Math.min(hi,Math.max(lo,+x)):d;
const hex=x=>typeof x==='string'&&/^#[0-9a-fA-F]{6}$/.test(x)?x:'#ffffff';
function normalize(src){
 if(!src||typeof src!=='object'||src.schema!==SCHEMA||!Array.isArray(src.elements)||src.elements.length>MAX)throw Error('KPS図解JSON形式ではありません');
 const els=src.elements.map((v,i)=>{if(!v||typeof v!=='object'||!['box','text','arrow','symbol'].includes(v.type))throw Error('不正なアイテム形式');
 return{id:uid(),type:v.type,x:number(v.x,-300,1300,100),y:number(v.y,-300,900,100),w:number(v.w,30,1050,220),h:number(v.h,24,650,90),text:String(v.text||'').slice(0,2500),fill:hex(v.fill),stroke:hex(v.stroke),color:hex(v.color),size:number(v.size,12,84,28),radius:number(v.radius,0,80,14),angle:number(v.angle,-180,180,0),opacity:number(v.opacity,10,100,100),font:fonts[v.font]?v.font:'sans',align:['left','center','right'].includes(v.align)?v.align:'center',z:i+1};});
 return{schema:SCHEMA,width:W,height:H,background:hex(src.background),elements:els};}
function setStatus(v){$('saveStatus').textContent=v}
function persist(){try{localStorage.setItem(KEY,JSON.stringify({savedAt:Date.now(),scene}));setStatus('この端末に保存済み');}catch(e){setStatus('保存に失敗。JSONで保存してください')}}
function schedule(){setStatus('保存中…');clearTimeout(saveTimer);saveTimer=setTimeout(persist,350)}
function snapshot(){history.push(JSON.stringify(scene));if(history.length>35)history.shift();future.length=0;}
function resetFrom(str){const prev=JSON.stringify(scene);try{scene=normalize(JSON.parse(str));selected=null;history.push(prev);if(history.length>35)history.shift();future=[];render();schedule()}catch(e){alert('読み込みできません：'+e.message)}}
function load(){try{const data=JSON.parse(localStorage.getItem(KEY)||'null');if(data?.scene){scene=normalize(data.scene);if(Date.now()-data.savedAt>7*86400000)setStatus('7日以上前の下書きを復元しました。JSON保存を推奨');}}catch(e){setStatus('下書きの復元に失敗しました。原本は保持しています')}}
function fit(){const avail=Math.max(280,viewport.clientWidth-40);setScale(Math.min(1.2,avail/W),false)}
function setScale(v,update=true){scale=number(v,.25,2,1);stage.style.width=W+'px';stage.style.height=H+'px';stage.style.transform='scale('+scale+')';space.style.width=(W*scale)+'px';space.style.height=(H*scale)+'px';if(update){$('zoom').value=Math.round(scale*100)}$('zoomLabel').textContent=Math.round(scale*100)+'%'}
const current=()=>scene.elements.find(e=>e.id===selected);
function ensureSelect(){const e=current();inspector.classList.toggle('collapsed',!e);$('selectedLabel').textContent=e?{box:'ボックス',text:'文字',arrow:'矢印',symbol:'記号'}[e.type]+'を編集中':'要素を選択してください';return e}
function select(id,raise=true){selected=id;const e=current();if(e&&raise){e.z=Math.max(0,...scene.elements.map(v=>v.z))+1;normalizeZ();schedule()}render();}
function normalizeZ(){if(Math.max(0,...scene.elements.map(e=>e.z))>10000){scene.elements.sort((a,b)=>a.z-b.z).forEach((e,i)=>e.z=i+1)}}
function drawElement(v){
 const el=document.createElement('div');el.className='d-element'+(v.type==='arrow'?' d-arrow':'')+(v.id===selected?' selected':'');el.dataset.id=v.id;el.style.left=v.x+'px';el.style.top=v.y+'px';el.style.width=v.w+'px';el.style.height=v.h+'px';el.style.zIndex=v.z;el.style.transform='rotate('+v.angle+'deg)';el.style.opacity=v.opacity/100;el.style.color=v.color;
 if(v.type==='arrow'){el.style.borderTop='0';el.style.setProperty('--arrow-color',v.stroke);el.style.setProperty('--arrow-width',Math.max(2,Math.min(12,v.size/6))+'px');}else{
 el.style.background=v.type==='box'?v.fill:'transparent';el.style.border=v.type==='box'?'2px solid '+v.stroke:'0';el.style.borderRadius=v.radius+'px';}
 const content=document.createElement('div');content.className='d-contents';content.textContent=v.text;content.style.fontFamily=fonts[v.font];content.style.fontSize=v.size+'px';content.style.fontWeight=v.type==='box'?'700':'500';content.style.textAlign=v.align;content.style.padding=v.type==='box'?'10px 16px':'2px';content.style.alignContent='center';
 if(v.type!=='arrow')el.append(content);
 if(v.id===selected){const grip=document.createElement('div');grip.className='d-resize';grip.title='サイズ変更';el.append(grip)}
 stage.append(el);
}
function render(){stage.style.background=scene.background;stage.replaceChildren();scene.elements.slice().sort((a,b)=>a.z-b.z).forEach(drawElement);const e=ensureSelect();$('bgColor').value=scene.background;if(e){
 const f={elText:'text',fontSize:'size',radius:'radius',rotation:'angle',opacity:'opacity',elWidth:'w',elHeight:'h',textColor:'color',fillColor:'fill',strokeColor:'stroke',fontFamily:'font',textAlign:'align'};
 for(const [id,key]of Object.entries(f)){if(document.activeElement!==$(id))$(id).value=e[key]}
 $('fontVal').textContent=e.size;$('radiusVal').textContent=e.radius;$('rotateVal').textContent=e.angle+'°';$('alphaVal').textContent=e.opacity+'%';$('widthVal').textContent=Math.round(e.w);$('heightVal').textContent=Math.round(e.h);
 }renderPalette();}
function add(type){if(scene.elements.length>=MAX){alert('この図解は100アイテムまでです');return;}snapshot();const props={box:{text:'新しいボックス',w:330,h:115,fill:'#eaf1f6'},text:{text:'新しいテキスト',w:300,h:95,fill:'#ffffff'},arrow:{text:'',w:180,h:36,fill:'#ffffff'},symbol:{text:'★',w:100,h:100,fill:'#ffffff'}}[type];const e={id:uid(),type,x:Math.max(10,Math.round(W*.4+Math.random()*35)),y:Math.max(10,Math.round(H*.25+Math.random()*35)),w:props.w,h:props.h,text:props.text,fill:props.fill,stroke:'#718d9e',color:'#1f3548',size:type==='text'?31:26,radius:15,angle:0,opacity:100,font:'sans',align:'center',z:Math.max(0,...scene.elements.map(x=>x.z))+1};scene.elements.push(e);select(e.id);schedule();}
function remove(){if(!current())return;snapshot();scene.elements=scene.elements.filter(x=>x.id!==selected);selected=null;render();schedule()}
function duplicate(){const e=current();if(!e)return;if(scene.elements.length>=MAX)return alert('100アイテムまでです');snapshot();const next={...e,id:uid(),x:e.x+24,y:e.y+24,z:Math.max(...scene.elements.map(v=>v.z))+1};scene.elements.push(next);select(next.id);}
for(const b of document.querySelectorAll('[data-add]'))b.addEventListener('click',()=>add(b.dataset.add));
$('duplicate').addEventListener('click',duplicate);$('remove').addEventListener('click',remove);
$('undo').addEventListener('click',()=>{if(!history.length)return;future.push(JSON.stringify(scene));scene=normalize(JSON.parse(history.pop()));selected=null;render();schedule()});
$('redo').addEventListener('click',()=>{if(!future.length)return;history.push(JSON.stringify(scene));scene=normalize(JSON.parse(future.pop()));selected=null;render();schedule()});
$('fit').addEventListener('click',fit);
$('zoom').addEventListener('input',e=>setScale(e.target.value/100));
$('bgColor').addEventListener('input',e=>{scene.background=e.target.value;stage.style.background=scene.background;schedule()});
$('bgColor').addEventListener('pointerdown',snapshot);
const properties={elText:'text',fontSize:'size',radius:'radius',rotation:'angle',opacity:'opacity',elWidth:'w',elHeight:'h',textColor:'color',fillColor:'fill',strokeColor:'stroke',fontFamily:'font',textAlign:'align'};
for(const [id,key]of Object.entries(properties)){
 const input=$(id);input.addEventListener('focus',()=>{if(current())snapshot()});
 input.addEventListener('pointerdown',()=>{if(input.type==='range'&&current())snapshot()});
 input.addEventListener('input',()=>{const e=current();if(!e)return;e[key]=input.value;e[key]=['size','radius','angle','opacity','w','h'].includes(key)?Number(e[key]):e[key];render();schedule();});
}
$('closeInspector').addEventListener('click',()=>inspector.classList.toggle('collapsed'));
let dragMode='';
stage.addEventListener('pointerdown',ev=>{
 const el=ev.target.closest('.d-element');if(!el||!stage.contains(el)){selected=null;render();return;}
 if(el.dataset.id!==selected)select(el.dataset.id);const e=current();if(!e)return;snapshot();dragMode=ev.target.classList.contains('d-resize')?'resize':'move';
 drag={id:e.id,mode:dragMode,startX:ev.clientX,startY:ev.clientY,x:e.x,y:e.y,w:e.w,h:e.h};stage.setPointerCapture(ev.pointerId);ev.preventDefault();
});
stage.addEventListener('pointermove',ev=>{if(!drag)return;const e=current();if(!e||e.id!==drag.id)return;const dx=(ev.clientX-drag.startX)/scale,dy=(ev.clientY-drag.startY)/scale;if(drag.mode==='move'){e.x=Math.round(number(drag.x+dx,-300,W+100,0));e.y=Math.round(number(drag.y+dy,-300,H+100,0));}else{e.w=Math.round(number(drag.w+dx,30,1050,250));e.h=Math.round(number(drag.h+dy,24,650,80));}render();ev.preventDefault()});
const endDrag=()=>{if(drag){drag=null;schedule()}};
stage.addEventListener('pointerup',endDrag);stage.addEventListener('pointercancel',endDrag);
function download(content,name,mime){const b=new Blob([content],{type:mime});const url=URL.createObjectURL(b),a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),10000)}
const today=()=>new Date().toISOString().slice(0,10);

function jsonText(){return JSON.stringify(scene,null,2);}
function showJsonText(){
 const panel=$('codePanel');
 panel.hidden=false;
 $('jsonEditor').value=jsonText();
 panel.scrollIntoView({behavior:'smooth',block:'start'});
}
function saveJsonFile(){
 try{
  download(jsonText(),'KPS-図解-'+today()+'.json','application/json;charset=utf-8');
  setStatus('JSONのダウンロードを開始しました。保存されない場合は「スマホで共有」か「JSONコピー」を使ってください。');
 }catch(e){
  showJsonText();
  setStatus('このブラウザではダウンロードできません。JSONをコピーして保存してください。');
 }
}
$('saveJson').addEventListener('click',saveJsonFile);
$('saveJsonTop')?.addEventListener('click',saveJsonFile);
$('showJson').addEventListener('click',showJsonText);
$('copyJson').addEventListener('click',async()=>{
 try{
  if(!navigator.clipboard?.writeText)throw Error('clipboard unavailable');
  await navigator.clipboard.writeText(jsonText());
  setStatus('JSONをコピーしました。メモアプリなどに貼り付けて保管できます。');
 }catch(e){
  showJsonText();
  $('jsonEditor').focus();$('jsonEditor').select();
  setStatus('JSONを表示しました。範囲選択してコピーしてください。');
 }
});
$('shareJson').addEventListener('click',async()=>{
 try{
  const file=new File([jsonText()],'KPS-図解-'+today()+'.json',{type:'application/json'});
  if(!navigator.canShare?.({files:[file]})||!navigator.share)throw Error('share unavailable');
  await navigator.share({files:[file],title:'KPS 図解JSON'});
  setStatus('共有先にJSONを渡しました。保存は共有先で確認してください。');
 }catch(e){
  if(e.name==='AbortError')return;
  showJsonText();
  setStatus('ファイル共有に対応していません。JSONコピーを利用してください。');
 }
});
$('loadSample').addEventListener('click',async()=>{
 try{
  const response=await fetch('/diagram/example.json',{cache:'no-store'});
  if(!response.ok)throw Error('HTTP '+response.status);
  const content=await response.text();
  if(!confirm('現在の図解をサンプルで置き換えますか？ 必要なら先にJSONを保存してください。'))return;
  resetFrom(content);
  setStatus('サンプル図解を読み込みました。編集・JSON保存を試せます。');
 }catch(e){setStatus('サンプルを読み込めませんでした。ファイルを直接保存してJSON読込をお試しください。');}
});

$('openJson').addEventListener('change',async e=>{const file=e.target.files?.[0];e.target.value='';if(!file)return;if(file.size>600000)return alert('600KB以下のJSONを使ってください');if(!confirm('現在の図解を新しいファイルに置き換えますか？'))return;resetFrom(await file.text())});
$('codeToggle').addEventListener('click',()=>{const p=$('codePanel');p.hidden=!p.hidden;if(!p.hidden){$('jsonEditor').value=JSON.stringify(scene,null,2);p.scrollIntoView({behavior:'smooth',block:'nearest'})}});
$('refreshJson').addEventListener('click',()=>$('jsonEditor').value=JSON.stringify(scene,null,2));
$('applyJson').addEventListener('click',()=>{if(!confirm('現在の図解を入力したJSONで置き換えますか？'))return;resetFrom($('jsonEditor').value)});
$('copyPrompt').addEventListener('click',async()=>{const prompt='次の文章からnote用の見やすいフローチャートを作成してください。出力は説明文なしのJSONのみ。スキーマは '+SCHEMA+'、width:1100、height:660、background:#ffffff、elements配列（最大30要素）。各要素は type:box|text|arrow|symbol, x,y,w,h,text,fill,stroke,color,size,radius,angle,opacity,font:sans|serif|mono,align:left|center|right,z を必須としてください。要素はキャンバス内に収め、文字が重ならないようにしてください。ユーザーの文章: 【ここに文章を貼る】';try{await navigator.clipboard.writeText(prompt);setStatus('外部AI用指示文をコピーしました')}catch(e){alert(prompt)}});
function wrapLines(ctx,str,maxw){const lines=[];for(const par of String(str).split('\n')){let line='';for(const ch of [...par]){if(ctx.measureText(line+ch).width>maxw&&line){lines.push(line);line=ch}else line+=ch;}lines.push(line);}return lines;}
function drawPng(){
 const canvas=document.createElement('canvas'),mul=2;canvas.width=W*mul;canvas.height=H*mul;const c=canvas.getContext('2d');if(!c)throw Error('canvas not available');c.scale(mul,mul);c.fillStyle=scene.background;c.fillRect(0,0,W,H);
 for(const v of scene.elements.slice().sort((a,b)=>a.z-b.z)){c.save();c.translate(v.x+v.w/2,v.y+v.h/2);c.rotate(v.angle*Math.PI/180);c.globalAlpha=v.opacity/100;
 if(v.type==='arrow'){c.strokeStyle=v.stroke;c.fillStyle=v.stroke;c.lineWidth=Math.max(2,v.size/6);c.lineCap='round';c.beginPath();c.moveTo(-v.w/2+4,0);c.lineTo(v.w/2-15,0);c.stroke();c.beginPath();c.moveTo(v.w/2-15,-9);c.lineTo(v.w/2-1,0);c.lineTo(v.w/2-15,9);c.closePath();c.fill();}
 else{if(v.type==='box'){const r=Math.min(v.radius,v.h/2,v.w/2);c.beginPath();c.roundRect(-v.w/2,-v.h/2,v.w,v.h,r);c.fillStyle=v.fill;c.fill();c.lineWidth=2;c.strokeStyle=v.stroke;c.stroke();}
 c.fillStyle=v.color;c.font=(v.type==='box'?'700 ':'500 ')+v.size+'px '+fonts[v.font];c.textAlign=v.align;c.textBaseline='middle';const lines=wrapLines(c,v.text,v.w-(v.type==='box'?32:4));const max=Math.max(1,Math.floor((v.h-12)/(v.size*1.35))),shown=lines.slice(0,max),lh=v.size*1.35;const x=v.align==='left'?-v.w/2+15:v.align==='right'?v.w/2-15:0;shown.forEach((line,i)=>c.fillText(line,x,(i-(shown.length-1)/2)*lh));}
 c.restore();}
 return canvas;
}
$('exportPng').addEventListener('click',()=>{if(!licensed){$('licenseDialog').hidden=false;return;}try{drawPng().toBlob(blob=>{if(!blob)return alert('PNG変換に失敗しました');const u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download='KPS-図解-'+today()+'.png';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),20000)},'image/png')}catch(e){alert('画像を書き出せませんでした：'+e.message)}});
function renderPalette(){const box=$('palette');box.replaceChildren();for(const color of COLORS){const b=document.createElement('button');b.type='button';b.title=color;b.style.background=color;b.addEventListener('click',()=>{const e=current();if(!e)return;snapshot();e.fill=color;render();schedule();});box.append(b)}}
$('savePalette').addEventListener('click',async()=>{if(!licensed||!db||!user){$('licenseDialog').hidden=false;return;}const e=current();if(!e)return;const color=e.fill;if(!COLORS.includes(color))COLORS.push(color);const {error}=await db.from('kps_diagram_palettes').upsert({user_id:user.id,colors:COLORS});if(error)setStatus('色の保存は現在準備中です');else{renderPalette();setStatus('色をアカウントに保存しました')}});
// KPS uses the existing Supabase identity but a separate browser session.
// No link-click redirect or CMS-side login is required for the six-digit code flow.
let otpEmail='',otpCooldownUntil=0,otpTimer=null,authBusy=false;
function authStatus(message){$('authMessage').textContent=message;}
function renderAuthDialog(){
 const signed=Boolean(user);
 $('authSignedIn').hidden=!signed;
 $('authRequestForm').hidden=signed||Boolean(otpEmail);
 $('authVerifyForm').hidden=signed||!otpEmail;
 $('signOut').hidden=!signed;
 $('authSessionEmail').textContent=signed?'ログイン中：'+(user.email||'KPSアカウント'):'';
 $('otpRecipient').textContent=otpEmail?'送信先：'+otpEmail:'';
 $('authCode').disabled=signed;
 updateOtpCooldown();
}
function updateOtpCooldown(){
 const remaining=Math.max(0,Math.ceil((otpCooldownUntil-Date.now())/1000));
 $('resendOtp').disabled=authBusy||!otpEmail||remaining>0;
 $('resendOtp').textContent=remaining>0?'再送信まで '+remaining+'秒':'コードを再送信';
 if(!remaining&&otpTimer){clearInterval(otpTimer);otpTimer=null;}
}
function startOtpCooldown(){
 otpCooldownUntil=Date.now()+60000;
 if(otpTimer)clearInterval(otpTimer);
 otpTimer=setInterval(updateOtpCooldown,1000);
 updateOtpCooldown();
}
function setAuthBusy(busy){
 authBusy=busy;
 $('sendLink').disabled=busy;
 $('verifyCode').disabled=busy;
 $('changeEmail').disabled=busy;
 updateOtpCooldown();
}
async function initSupabase(){
 if(db)return db;
 try{
  if(!window.supabase){
   await new Promise((resolve,reject)=>{const script=document.createElement('script');script.src='https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.116.0/dist/umd/supabase.min.js';script.onload=resolve;script.onerror=reject;document.head.append(script)});
  }
  // A unique storage key keeps KPS login tokens distinct from other apps.
  // Code-based verification creates the session here, not via an email redirect.
  db=window.supabase.createClient(SUPABASE_URL,PUBLISHABLE,{auth:{
   storageKey:'kps-diagram-auth',persistSession:true,autoRefreshToken:true,detectSessionInUrl:false
  }});
  db.auth.onAuthStateChange((_event,session)=>{
   user=session?.user||null;
   if(!user){licensed=false;updateAccount();}
   else setTimeout(()=>refreshLicense(),0);
  });
  const {data,error}=await db.auth.getSession();
  if(error)throw error;
  if(data?.session){
   const account=await db.auth.getUser();
   if(!account.error&&account.data?.user){user=account.data.user;await refreshLicense();}
   else {user=null;licensed=false;updateAccount();}
  }else{user=null;licensed=false;updateAccount();}
  return db;
 }catch(e){authStatus('KPS認証の接続に失敗しました。時間をおいて再度お試しください。');throw e;}
}
async function refreshLicense(){
 licensed=false;
 if(!db||!user){updateAccount();return;}
 const id=user.id;
 try{
  const {data,error}=await db.from('kps_diagram_entitlements')
   .select('active').eq('user_id',id).eq('active',true).maybeSingle();
  if(!error&&data?.active)licensed=true;
  if(!licensed){
   const owner=await db.from('app_admins').select('role').eq('user_id',id).eq('role','owner').maybeSingle();
   if(!owner.error&&owner.data?.role==='owner')licensed=true;
  }
  if(licensed){
   const p=await db.from('kps_diagram_palettes').select('colors').eq('user_id',id).maybeSingle();
   if(!p.error&&Array.isArray(p.data?.colors)){
    COLORS.splice(0,COLORS.length,...p.data.colors.filter(hex=>/^#[0-9a-fA-F]{6}$/.test(hex)).slice(0,64));
    renderPalette();
   }
  }
 }catch(e){licensed=false;}
 if(!user||user.id!==id){licensed=false;return;}
 updateAccount();
}
function updateAccount(){
 $('accountBtn').textContent=user?(licensed?'ライセンス有効':'KPSログイン済み'):'KPSログイン';
 $('licenseMessage').textContent=user?(licensed?'KPSの利用権限を確認できました。':'ログイン済みです。書き出し購入は現在準備中です。'):'買い切り決済は準備中です。KPSにログインすると既存の利用権限を確認できます。';
 if(licensed)$('licenseDialog').hidden=true;
 renderAuthDialog();
}
$('accountBtn').addEventListener('click',async()=>{
 $('authDialog').hidden=false;
 authStatus('KPSのログイン状態を確認しています。');
 renderAuthDialog();
 try{await initSupabase();authStatus(user?'KPSにログインしています。':'メールアドレスを入力して6桁コードを受け取ってください。');}catch(e){}
});
async function sendOtp(email){
 if(authBusy)return;
 if(Date.now()<otpCooldownUntil){updateOtpCooldown();authStatus('再送信は表示された秒数が経過してから行ってください。');return;}
 if(!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(email)){authStatus('メールアドレスを確認してください。');return;}
 setAuthBusy(true);
 authStatus('認証コードを送信しています。');
 try{
  await initSupabase();
  const {error}=await db.auth.signInWithOtp({
   email,options:{shouldCreateUser:true,emailRedirectTo:AUTH_RETURN}
  });
  if(error)throw error;
  otpEmail=email;
  $('authCode').value='';
  startOtpCooldown();
  renderAuthDialog();
  $('authCode').focus();
  authStatus('メール内の6桁コードを、この画面へ入力してください。メールのリンクは開かないでください。数字がない場合はメールテンプレートの設定が必要です。');
 }catch(e){
  authStatus('送信できませんでした。メールアドレス、通信状態、送信回数制限を確認してください。');
 }finally{setAuthBusy(false);}
}
$('authRequestForm').addEventListener('submit',event=>{
 event.preventDefault();
 void sendOtp($('authEmail').value.trim().toLowerCase());
});
$('authCode').addEventListener('input',()=>{
 const clean=$('authCode').value.replace(/\\D/g,'').slice(0,6);
 if($('authCode').value!==clean)$('authCode').value=clean;
});
$('authVerifyForm').addEventListener('submit',async event=>{
 event.preventDefault();
 if(authBusy)return;
 const token=$('authCode').value.replace(/\\D/g,'');
 if(!otpEmail||!/^[0-9]{6}$/.test(token)){authStatus('6桁の数字を入力してください。');return;}
 setAuthBusy(true);
 authStatus('認証コードを確認しています。');
 try{
  await initSupabase();
  const {data,error}=await db.auth.verifyOtp({email:otpEmail,token,type:'email'});
  if(error||!data?.session?.user)throw error||new Error('No session');
  user=data.session.user;
  otpEmail='';
  $('authCode').value='';
  await refreshLicense();
  renderAuthDialog();
  authStatus(licensed?'KPSにログインしました。永久利用権限を確認しました。':'KPSにログインしました。無料の編集機能を利用できます。');
  $('authDialog').hidden=true;
  setStatus(licensed?'KPSの利用権限を確認しました':'KPSにログインしました');
 }catch(e){
  authStatus('認証コードが一致しないか期限切れです。最新の6桁コードを確認してください。');
  $('authCode').select();
 }finally{setAuthBusy(false);}
});
$('resendOtp').addEventListener('click',()=>{
 if(otpEmail)void sendOtp(otpEmail);
});
$('changeEmail').addEventListener('click',()=>{
 otpEmail='';
 $('authCode').value='';
 renderAuthDialog();
 $('authEmail').focus();
 authStatus('新しい送信先のメールアドレスを入力してください。');
});
$('signOut').addEventListener('click',async()=>{
 if(!db){authStatus('KPSへ接続できません。');return;}
 setAuthBusy(true);
 try{
  // Supabase's default global sign-out would invalidate CMS sessions too.
  const {error}=await db.auth.signOut({scope:'local'});
  if(error)throw error;
  user=null;licensed=false;otpEmail='';
  updateAccount();
  authStatus('KPSからのみログアウトしました。他のアプリのログインは維持されます。');
 }catch(e){authStatus('ログアウトに失敗しました。再度お試しください。');}
 finally{setAuthBusy(false);}
});
$('closeAuth').addEventListener('click',()=>$('authDialog').hidden=true);
$('closeLicense').addEventListener('click',()=>$('licenseDialog').hidden=true);
$('loginFromDialog').addEventListener('click',()=>{$('licenseDialog').hidden=true;$('accountBtn').click()});
for(const node of [$('licenseDialog'),$('authDialog')]){
 node.addEventListener('pointerdown',e=>{if(e.target===node)node.hidden=true});
}
window.addEventListener('pagehide',()=>{clearTimeout(saveTimer);persist()});
load();render();requestAnimationFrame(fit);window.addEventListener('resize',()=>{if(scale<1)fit()});initSupabase().catch(()=>{});
})();