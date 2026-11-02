(() => {
'use strict';
const KEY='kps-thought-v1', SCHEMA='knowledge-product-studio/thought-v1';
const FIELDS=['title','spark','fact','feeling','why1','why2','principle','options','costs','alternative','decision','reader'];
const MAX_NOTES=60, MAX_VERSIONS=30;
const $=id=>document.getElementById(id);
const empty=()=>Object.fromEntries(FIELDS.map(x=>[x,'']));
const create=()=>({id:(typeof crypto!=='undefined'&&crypto.randomUUID?crypto.randomUUID():Date.now()+'-'+Math.random().toString(36).slice(2)),updatedAt:new Date().toISOString(),...empty(),snapshots:[]});
let state={activeId:null,notes:[]},saveTimer=null;
function notice(t){$('thinkStatus').textContent=t;}
function cleanNote(raw){if(!raw||typeof raw!=='object'||Array.isArray(raw))throw new Error('invalid note');const x={id:String(raw.id||'').slice(0,100),updatedAt:String(raw.updatedAt||'').slice(0,60),snapshots:[]};for(const f of FIELDS){if(raw[f]!==undefined&&typeof raw[f]!=='string')throw new Error('invalid field');x[f]=(raw[f]||'').slice(0,20000);}if(!x.id)throw new Error('missing id');if(Array.isArray(raw.snapshots))x.snapshots=raw.snapshots.slice(-MAX_VERSIONS).map(s=>({date:String(s.date||'').slice(0,60),text:String(s.text||'').slice(0,60000)}));return x;}
function load(){try{const raw=localStorage.getItem(KEY);if(raw){const o=JSON.parse(raw);if(!o||o.schema!==SCHEMA||!Array.isArray(o.notes)||o.notes.length>MAX_NOTES)throw new Error('schema');state={activeId:o.activeId,notes:o.notes.map(cleanNote)};}}catch(e){notice('保存内容を読み込めません。元データは変更していません。');}if(!state.notes.length){const n=create();state.notes=[n];state.activeId=n.id;}if(!state.notes.some(x=>x.id===state.activeId))state.activeId=state.notes[0].id;}
function active(){return state.notes.find(x=>x.id===state.activeId);}
function save(){try{localStorage.setItem(KEY,JSON.stringify({schema:SCHEMA,activeId:state.activeId,notes:state.notes}));notice('この端末に保存済み');}catch(e){notice('保存できません。JSONを書き出してください');}}
function schedule(){notice('保存中…');clearTimeout(saveTimer);saveTimer=setTimeout(save,450);}
function formatted(n){return [
['今の問い',n.title],['きっかけ・違和感',n.spark],['確認できている事実',n.fact],['最初の気持ち',n.feeling],['その理由',n.why1],['さらに奥の理由',n.why2],['大切な価値基準',n.principle],['増える選択肢',n.options],['失う選択肢・負担',n.costs],['反対の見方',n.alternative],['今の判断',n.decision],['誰に役立つか（任意）',n.reader]
].filter(([,v])=>v.trim()).map(([k,v])=>k+'\n'+v.trim()).join('\n\n')||'まだ記録がありません。';}
function drawList(){const list=$('thoughtList');list.replaceChildren();for(const n of [...state.notes].sort((a,b)=>(b.updatedAt||'').localeCompare(a.updatedAt||''))){const b=document.createElement('button');b.type='button';b.setAttribute('aria-current',String(n.id===state.activeId));const title=document.createElement('strong');title.textContent=n.title.trim()||'名前のない問い';const date=document.createElement('small');const dt=new Date(n.updatedAt);date.textContent=Number.isNaN(dt.getTime())?'記録日なし':dt.toLocaleDateString('ja-JP');b.append(title,date);b.addEventListener('click',()=>{state.activeId=n.id;render();showNextPrompt();save();});list.append(b);}}
function drawMap(n){const view={mapTitle:n.title,mapRoot:n.why2||n.why1,mapPrinciple:n.principle,mapOptions:[n.options&&'増える：'+n.options,n.costs&&'失う：'+n.costs].filter(Boolean).join('\n'),mapDecision:n.decision};for(const [id,val] of Object.entries(view))$(id).textContent=val.trim()||'未入力';$('thoughtSummary').textContent=formatted(n);}
function drawSnapshots(n){const box=$('snapshotList');box.replaceChildren();if(!n.snapshots.length){const p=document.createElement('p');p.className='empty-hint';p.textContent='判断を記録すると、過去の時点の考えを比較できます。';box.append(p);}for(const s of [...n.snapshots].reverse()){const details=document.createElement('details');details.className='snapshot';const summary=document.createElement('summary');const date=new Date(s.date);summary.textContent='記録：'+(Number.isNaN(date.getTime())?s.date:date.toLocaleString('ja-JP'));const pre=document.createElement('pre');pre.textContent=s.text;details.append(summary,pre);box.append(details);}}
const PROMPTS=[
{field:'spark',texts:['いま引っかかっている出来事は何ですか？','その出来事のどこが、普段と違って感じられましたか？']},
{field:'fact',texts:['誰が見ても確認できる事実は何ですか？','推測していることを除くと、何が残りますか？']},
{field:'feeling',texts:['最初に浮かんだ気持ちを、整えずに書くと？','その出来事が嬉しかった／嫌だったのはなぜでしょう？']},
{field:'why1',texts:['それを大切だと思った理由は何ですか？','もしそれが叶わなくても構わないとしたら、何が変わりますか？']},
{field:'why2',texts:['その考えは、いつ頃から変わらず持っていますか？','別の経験でも同じ判断をしてきましたか？']},
{field:'principle',texts:['どんな条件なら、手段が変わっても守りたいことは何ですか？','自分の判断を一文の原則にすると？']},
{field:'options',texts:['今の選択によって、何が新しく選べるようになりますか？','最終的に何を選べる状態でいたいのでしょう？']},
{field:'costs',texts:['その選択の維持に必要な時間や費用は何ですか？','何を始めないことで、別の可能性を残せますか？']},
{field:'alternative',texts:['反対の意見を持つ人には、どんな理由がありますか？','見えていない前提条件はありませんか？']},
{field:'decision',texts:['今は続ける・保留する・やめるのどれを選びますか？','どんな事実が分かれば、判断を変えますか？']}
];let promptIndex=0,focusField='spark';
function showNextPrompt(advance=false){const n=active();const target=PROMPTS.find(x=>!n[x.field].trim())||PROMPTS[PROMPTS.length-1];if(advance)promptIndex++;else promptIndex=0;focusField=target.field;$('nextPrompt').textContent=target.texts[promptIndex%target.texts.length];}
function render(){const n=active();for(const el of document.querySelectorAll('[data-thought]'))el.value=n[el.dataset.thought]||'';drawList();drawMap(n);drawSnapshots(n);}
load();render();showNextPrompt();
for(const el of document.querySelectorAll('[data-thought]')){el.addEventListener('input',()=>{const n=active();n[el.dataset.thought]=el.value.slice(0,20000);n.updatedAt=new Date().toISOString();drawMap(n);showNextPrompt();schedule();if(el.dataset.thought==='title')drawList();});}
$('newThought').addEventListener('click',()=>{if(state.notes.length>=MAX_NOTES){notice('問いは最大60件です。JSONで保存し、整理してください。');return;}const n=create();state.notes.unshift(n);state.activeId=n.id;render();showNextPrompt();schedule();$('thinkTitle').focus();});
$('removeThought').addEventListener('click',()=>{if(!confirm('この問いと判断履歴を削除しますか？ 取り消せません。'))return;state.notes=state.notes.filter(n=>n.id!==state.activeId);if(!state.notes.length)state.notes.push(create());state.activeId=state.notes[0].id;render();showNextPrompt();save();});
$('saveSnapshot').addEventListener('click',()=>{const n=active();if(!FIELDS.some(f=>n[f].trim())){notice('先に考えを一つ書いてください');return;}if(n.snapshots.length>=MAX_VERSIONS){notice('履歴は最大30件です。JSONで書き出してから整理してください。');return;}n.snapshots.push({date:new Date().toISOString(),text:formatted(n)});n.updatedAt=new Date().toISOString();drawSnapshots(n);save();});
$('copyThought').addEventListener('click',async()=>{try{await navigator.clipboard.writeText(formatted(active()));notice('現在の内容をコピーしました');}catch(e){notice('コピーできません。下の「文章としてまとめる」から選択してください');}});
$('thinkExport').addEventListener('click',()=>{clearTimeout(saveTimer);save();const b=new Blob([JSON.stringify({schema:SCHEMA,exportedAt:new Date().toISOString(),notes:state.notes,activeId:state.activeId},null,2)],{type:'application/json;charset=utf-8'});const u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download='KPS-思考ノート-'+new Date().toISOString().slice(0,10)+'.json';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1500);});
$('thinkImport').addEventListener('change',async e=>{const f=e.target.files?.[0];e.target.value='';if(!f)return;if(f.size>1500000){notice('1.5MB以下のJSONのみ読み込めます');return;}try{const x=JSON.parse(await f.text());if(x.schema!==SCHEMA||!Array.isArray(x.notes)||!x.notes.length||x.notes.length>MAX_NOTES)throw new Error('schema');const notes=x.notes.map(cleanNote);if(new Set(notes.map(n=>n.id)).size!==notes.length)throw new Error('duplicate');if(!confirm('現在の思考ノートを読み込んだ内容で置き換えますか？ 先にJSONを書き出して保管してください。'))return;state={notes,activeId:notes.some(n=>n.id===x.activeId)?x.activeId:notes[0].id};render();showNextPrompt();save();}catch(e){notice('読み込めない思考ノート形式です');}});
$('nextPromptBtn').addEventListener('click',()=>showNextPrompt(true));
$('focusPromptBtn').addEventListener('click',()=>{const el=document.querySelector('[data-thought="'+focusField+'"]');if(el){el.scrollIntoView({behavior:'smooth',block:'center'});el.focus({preventScroll:true});}});
window.addEventListener('pagehide',()=>{clearTimeout(saveTimer);save();});
})();
