(() => {
'use strict';
const KEY='kps-product-v1';
const DEFAULT={experience:'例：資格試験の勉強で試行錯誤した',audience:'例：初めてその資格を受験する人',problem:'例：勉強する順番がわからない',outcome:'例：試験日までの計画を立てられる',productName:'例：試験対策の学習ガイド',format:'note記事',price:'',outline:'',value:'',exclusions:'',evidence:'',channel:''};
const fields=Object.keys(DEFAULT);
const filled=v=>typeof v==='string'&&v.trim().length>0&&!/^例\s*[：:]/.test(v.trim());
const byName=name=>document.querySelector(`[name="${name}"]`);
const $=id=>document.getElementById(id);
let state={...DEFAULT};let saveTimer=null;let dirty=false;
const saveStatus=$('saveStatus');
function status(message){if(saveStatus)saveStatus.textContent=message;}
function load(){try{const raw=localStorage.getItem(KEY);if(!raw)return;let data=JSON.parse(raw);if(!data||typeof data!=='object'||Array.isArray(data))throw new Error('bad data');for(const f of fields){if(typeof data[f]==='string')state[f]=data[f].slice(0,20000);}}catch(e){status('保存データを読めません。JSONで保護してください');}}
function render(){for(const f of fields){let el=byName(f);if(el && el.value!==state[f])el.value=state[f];}document.querySelectorAll('[data-field]').forEach(el=>{let txt=state[el.dataset.field]?.trim();el.textContent=txt||'未入力';});const list=$('reviewList');if(list){const tests=[['誰に届けるかが決まっている',filled(state.audience),'想定読者を具体的に記述'],['解決する困りごとが決まっている',filled(state.problem),'状況まで含めて整理'],['解決後の変化が説明できる',filled(state.outcome),'購入者が何をできるようになるか'],['商品名と形が決まっている',filled(state.productName)&&filled(state.format),'note・PDFなどの形式も確認'],['収録内容・目次がある',filled(state.outline),'実物と一致する内容を記載'],['比較できる価値の根拠がある',filled(state.value),'価格の前に内容の根拠を用意'],['対象外や限界を明示した',filled(state.exclusions),'向いていない人も分かる'],['サンプル・実績などの資料がある',filled(state.evidence),'架空の実績を使わない'],['届ける場所が決まっている',filled(state.channel),'販売先と受け取り方'],['価格に根拠がある',filled(state.price)&&filled(state.value),'未定なら無理に決めない']];list.replaceChildren(...tests.map(([title,check,desc])=>{let div=document.createElement('div');div.className='review-item'+(check&&String(check).trim()?' done':'');let icon=document.createElement('span');icon.className='review-check';icon.textContent=check&&String(check).trim()?'✓':'○';let col=document.createElement('div');let b=document.createElement('b');b.textContent=title;let sm=document.createElement('small');sm.textContent=desc;col.append(b,sm);div.append(icon,col);return div;}));}}
function save(){try{localStorage.setItem(KEY,JSON.stringify(state));dirty=false;status('この端末に保存済み');}catch(e){status('保存できません。JSONで書き出してください');}}
function scheduleSave(){dirty=true;status('保存中…');clearTimeout(saveTimer);saveTimer=setTimeout(save,450);}
function setState(obj){state={...DEFAULT,...obj};render();scheduleSave();}
load();render();
for(const f of fields){let el=byName(f);if(!el)continue;el.addEventListener('input',()=>{state[f]=el.value;render();scheduleSave();});el.addEventListener('change',()=>{state[f]=el.value;render();scheduleSave();});}
for(const button of document.querySelectorAll('.tab')){button.addEventListener('click',()=>{const id=button.dataset.panel;document.querySelectorAll('.tab').forEach(b=>{const selected=b===button;b.classList.toggle('active',selected);b.setAttribute('aria-selected',String(selected));});document.querySelectorAll('.panel').forEach(p=>{const active=p.id==='panel-'+id;p.hidden=!active;p.classList.toggle('active',active);});});}
$('exportBtn')?.addEventListener('click',()=>{clearTimeout(saveTimer);save();const payload={schema:'knowledge-product-studio/product-v1',exportedAt:new Date().toISOString(),product:state};const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json;charset=utf-8'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='商品設計ボード-'+new Date().toISOString().slice(0,10)+'.json';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1500);});
$('importInput')?.addEventListener('change',async ev=>{const file=ev.target.files?.[0];ev.target.value='';if(!file)return;if(file.size>200000){status('200KB以下のJSONのみ読み込めます');return;}try{let parsed=JSON.parse(await file.text());if(parsed.schema!=='knowledge-product-studio/product-v1'||!parsed.product||typeof parsed.product!=='object'||Array.isArray(parsed.product))throw new Error('schema');let data={};for(const f of fields){let x=parsed.product[f];if(x!==undefined&&typeof x!=='string')throw new Error(f);data[f]=typeof x==='string'?x.slice(0,20000):DEFAULT[f];}if(!confirm('現在の入力を読み込んだデータに置き換えますか？'))return;setState(data);save();}catch(e){status('読み込めないJSON形式です');}});
$('clearBtn')?.addEventListener('click',()=>{if(!confirm('この端末の入力内容を初期化しますか？先にJSONを書き出してください。'))return;setState(Object.fromEntries(fields.map(f=>[f,''])));save();});
$('resetSample')?.addEventListener('click',()=>{if(!confirm('5つの項目を入力例に戻しますか？その他の商品設計項目は保持します。'))return;for(const f of ['experience','audience','problem','outcome','productName'])state[f]=DEFAULT[f];render();scheduleSave();});

// 学習記事から来た人に、対応する既存入力欄を案内する。保存形式は変更しない。
const lessonTargets={
  problem:{name:'課題の切り取り',tab:'map',field:'audience',hint:'まず想定する読者を書き、その人の困りごとと解決後の変化を続けて記入します。'},
  design:{name:'商品化とカリキュラム設計',tab:'sheet',field:'outline',hint:'使い終わった人ができることから逆算し、章立てと確認課題を目次欄に整理します。'},
  offer:{name:'オファーと価格',tab:'sheet',field:'value',hint:'商品の内容と比較できる価値を先に記入し、その根拠がある価格案を考えます。'},
  sales:{name:'販売ページ',tab:'sheet',field:'evidence',hint:'目次・サンプル・実体験など、買い手に見せられる根拠を記録します。'},
  reach:{name:'集客（検索・SNS）',tab:'sheet',field:'channel',hint:'読者の質問に答える無料記事と、商品を届ける場所のつながりを記入します。'},
  improve:{name:'分析と改善',tab:'review',field:null,hint:'完成チェックで未確定の項目を確認し、次に見直す一か所を選びます。'}
};
const lessonId=new URLSearchParams(location.search).get('lesson');
const selectedLesson=Object.prototype.hasOwnProperty.call(lessonTargets,lessonId)?lessonTargets[lessonId]:null;
if(selectedLesson){
  const guide=$('lessonGuide');
  const target=selectedLesson.field?byName(selectedLesson.field):$('reviewList');
  const tab=document.querySelector(`.tab[data-panel="${selectedLesson.tab}"]`);
  if(guide && tab && target){
    const caption=document.createElement('div');caption.className='eyebrow';caption.textContent='学習記事からの実践';
    const title=document.createElement('strong');title.textContent=selectedLesson.name;
    const description=document.createElement('p');description.textContent=selectedLesson.hint;
    const row=document.createElement('div');row.className='lesson-guide-actions';
    const go=document.createElement('button');go.type='button';go.className='button primary';go.textContent='該当項目を開く →';
    const back=document.createElement('a');back.href='/learn/'+lessonId+'/';back.className='button secondary';back.textContent='記事に戻る';
    row.append(go,back);guide.append(caption,title,description,row);guide.hidden=false;
    function openField(){
      tab.click();
      if(selectedLesson.field){const label=target.closest('label');if(label)label.classList.add('guided-target');}
      target.scrollIntoView({behavior:'smooth',block:'center'});
      if(selectedLesson.field)target.focus({preventScroll:true});
    }
    go.addEventListener('click',openField);
    tab.click();
  }
}

window.addEventListener('pagehide',()=>{if(dirty){clearTimeout(saveTimer);save();}});
})();
