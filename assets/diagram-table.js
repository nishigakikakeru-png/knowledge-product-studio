/* TSV/Markdown table importer for KPS diagram-v1. No network, HTML evaluation, or shared storage. */
(function(root){
 'use strict';
 const MAX_CELLS=100, MAX_TEXT=50000;
 const PRESETS={
  table:{font:'sans',size:21,padding:16,minWidth:114,maxWidth:380,minHeight:56,gap:6,margin:36,radius:12,
   fill:'#ffffff',alternate:'#fbfaf7',headerRow:'#e5d5c5',headerCol:'#f3e7da',stroke:'#e8dfd5',color:'#263845'},
  diagram:{font:'sans',size:22,padding:20,minWidth:135,maxWidth:420,minHeight:72,gap:16,margin:40,radius:22,
   fill:'#ffffff',alternate:'#f9fcfc',headerRow:'#d9e9e7',headerCol:'#eaf2f1',stroke:'#dce8e8',color:'#203b45'}
 };
 function tableError(message){throw new Error(message);}
 function parseTSV(text){
  const rows=[];let row=[],field='',quoted=false,atStart=true;
  for(let i=0;i<text.length;i++){
   const ch=text[i];
   if(ch==='"' && quoted && text[i+1]==='"'){field+='"';i++;continue;}
   if(ch==='"' && quoted){quoted=false;continue;}
   if(ch==='"' && atStart){quoted=true;atStart=false;continue;}
   if(ch==='\t' && !quoted){row.push(field);field='';atStart=true;continue;}
   if(ch==='\n' && !quoted){row.push(field);rows.push(row);row=[];field='';atStart=true;continue;}
   field+=ch;atStart=false;
  }
  if(quoted)tableError('引用符が閉じていません。貼り付けた表を確認してください。');
  row.push(field);rows.push(row);
  while(rows.length && rows[rows.length-1].every(c=>c===''))rows.pop();
  return rows;
 }
 function parseMarkdown(text){
  const lines=text.split('\n').filter(line=>line.trim()!=='');
  if(lines.length<2 || !lines[0].trim().startsWith('|'))return null;
  const row=line=>{
   const str=line.trim().replace(/^\|/,'').replace(/\|$/,'');
   return str.split(/(?<!\\)\|/).map(c=>c.replace(/\\\|/g,'|').trim());
  };
  const rows=lines.map(row);
  if(!rows.every(r=>r.length===rows[0].length))return null;
  const divider=rows.findIndex((r,i)=>i>0&&r.every(c=>/^:?-{3,}:?$/.test(c.replace(/\s+/g,''))));
  if(divider!==1)return null;
  rows.splice(divider,1);
  return rows;
 }
 function parse(raw){
  const text=String(raw||'').replace(/^\uFEFF/,'').replace(/\r\n?/g,'\n');
  if(!text.trim())tableError('表の文字を貼り付けてください。');
  if(text.length>MAX_TEXT)tableError('表の文字数が多すぎます（最大50,000文字）。');
  const rows=text.includes('\t')?parseTSV(text):parseMarkdown(text);
  if(!rows||!rows.length||rows.every(r=>r.length<2))
   tableError('タブ区切り（TSV）またはMarkdown表を貼り付けてください。空白区切りは使えません。');
  const cols=Math.max(...rows.map(r=>r.length));
  if(rows.length*cols>MAX_CELLS)
   tableError('表は最大100セルです（現在 '+rows.length+'行×'+cols+'列＝'+(rows.length*cols)+'セル）。');
  if(cols>25)tableError('横幅が多すぎます。列を25列以下にしてください。');
  if(rows.some(r=>r.some(cell=>cell.length>2500)))tableError('1セルの文字数は2,500文字以下にしてください。');
  return rows.map(row=>Array.from({length:cols},(_,i)=>(row[i]||'').trim()));
 }
 function charWidth(ch,size){
  if(ch===' ')return size*.34;
  if(/[\u0000-\u00ff]/.test(ch))return size*.57;
  return size;
 }
 function lineWidth(text,size){return Array.from(text).reduce((sum,ch)=>sum+charWidth(ch,size),0);}
 function wrapText(text,width,size){
  const result=[];
  for(const paragraph of String(text).split('\n')){
   let line='',used=0;
   for(const ch of Array.from(paragraph)){
    const w=charWidth(ch,size);
    if(line && used+w>width){result.push(line);line='';used=0;}
    line+=ch;used+=w;
   }
   result.push(line);
  }
  return result;
 }
 function fitWidths(widths,space,minWidth){
  if(space<widths.length*minWidth)tableError('キャンバス幅に列が収まりません。自動サイズか列数の削減を選んでください。');
  let sizes=widths.map(()=>minWidth);
  const excess=Math.max(0,space-minWidth*widths.length);
  const weights=widths.map(w=>Math.max(1,w-minWidth));
  const sum=weights.reduce((a,b)=>a+b,0);
  sizes=sizes.map((v,i)=>Math.floor(v+excess*weights[i]/sum));
  sizes[sizes.length-1]+=space-sizes.reduce((a,b)=>a+b,0);
  return sizes;
 }
 function layout(rows,options={}){
  const style=PRESETS[options.style]||PRESETS.table;
  if(!Array.isArray(rows)||!rows.length||!Array.isArray(rows[0]))tableError('表データが不正です。');
  const cols=rows[0].length;
  if(rows.length*cols>MAX_CELLS)tableError('表は最大100セルです。');
  const margin=style.margin,gap=style.gap,pad=style.padding;
  const widths=Array.from({length:cols},(_,c)=>{
   let measured=0;
   for(const row of rows){
    for(const part of String(row[c]||'').split('\n'))measured=Math.max(measured,lineWidth(part,style.size));
   }
   return Math.max(style.minWidth,Math.min(style.maxWidth,Math.ceil(measured+pad*2+8)));
  });
  const desired=options.canvas==='note'?1100:null;
  const available=(desired||4096)-margin*2-gap*(cols-1);
  if(available<=0)tableError('表の列数に対して余白が大きすぎます。');
  let colWidths=widths;
  let used=widths.reduce((a,b)=>a+b,0);
  if(desired || used>available){
   colWidths=fitWidths(widths,available,Math.min(style.minWidth,72));
   used=colWidths.reduce((a,b)=>a+b,0);
  }
  const canvasWidth=desired||Math.max(320,Math.ceil(used+gap*(cols-1)+margin*2));
  const wrapped=rows.map(row=>row.map((cell,c)=>wrapText(cell,Math.max(20,colWidths[c]-2*pad-4),style.size)));
  const heights=wrapped.map(row=>Math.max(style.minHeight,...row.map(lines=>Math.ceil(lines.length*style.size*1.48+2*pad))));
  const canvasHeight=Math.max(200,Math.ceil(heights.reduce((a,b)=>a+b,0)+gap*(rows.length-1)+margin*2));
  if(canvasHeight>4096)tableError('表の高さが4,096pxを超えます。セル内の文章を短くするか、表を分割してください。');
  const elements=[];let y=margin;
  for(let r=0;r<rows.length;r++){
   let x=margin;
   for(let c=0;c<cols;c++){
    const rowHead=options.headerRow!==false&&r===0;
    const colHead=options.headerCol!==false&&c===0;
    const fill=rowHead?style.headerRow:colHead?style.headerCol:r%2?style.alternate:style.fill;
    elements.push({
     id:options.uid?options.uid():'table-'+r+'-'+c,type:'box',
     x,y,w:colWidths[c],h:heights[r],text:wrapped[r][c].join('\n'),
     fill,stroke:style.stroke,color:style.color,size:style.size,
     radius:style.radius,angle:0,opacity:100,font:style.font,align:'left',
     padding:pad,weight:rowHead||colHead?'bold':'normal',z:elements.length+1
    });
    x+=colWidths[c]+gap;
   }
   y+=heights[r]+gap;
  }
  return{schema:'kps-diagram-v1',width:canvasWidth,height:canvasHeight,background:options.style==='diagram'?'#f6faf9':'#fbfaf8',elements};
 }
 const api={parse,layout,PRESETS,MAX_CELLS};
 if(typeof module!=='undefined'&&module.exports)module.exports=api;
 root.KPSTable=api;
})(typeof window!=='undefined'?window:typeof globalThis!=='undefined'?globalThis:{});
