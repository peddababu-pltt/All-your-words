/* Browser + Node: pure search, persistence validation and learning queue. */
(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.WordCore=factory();})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const normalize=s=>String(s||'').normalize('NFKC').toLowerCase().replace(/[^a-z0-9가-힣]/g,'');
const names=e=>[e.term,e.english,...(e.aliases||[])].map(normalize).filter(Boolean);
function score(e,query){const q=normalize(query);if(!q)return 1;const ns=names(e);if(ns.includes(q))return 10000;
 // Short Latin acronyms must stand alone: PT should find 경쟁 PT, not depth
 // or JavaScript. NFKC also supports full-width Latin input.
 if(/^[a-z0-9]{1,3}$/.test(q)){
   const token=new RegExp('(^|[^a-z0-9])'+q+'([^a-z0-9]|$)');
   return [e.term,e.english,...(e.aliases||[])].some(n=>token.test(String(n||'').normalize('NFKC').toLowerCase()))?6000:0;
 }
 if(ns.some(n=>n.startsWith(q)))return 6000;if(ns.some(n=>n.includes(q))){
   // A short Korean alias must not be formed across unrelated word boundaries.
   const originals=[e.term,e.english,...(e.aliases||[])];
   if(!/^[가-힣]{2}$/.test(q)||originals.some(n=>String(n||'').normalize('NFKC').includes(q)))return 5000;
 }
 const phrases=(e.phrases||[]).map(normalize);if(phrases.some(p=>p.includes(q)||q.length>=5&&q.includes(p)))return 3000;
 const text=normalize([e.definition,...(e.phrases||[]),e.category||''].join(' '));if(text.includes(q))return 2200;
 const tokens=String(query).toLowerCase().split(/\s+/).map(t=>normalize(t.replace(/(하는|하고|에서|으로|처럼|까지|부터|은|는|을|를|이|가|게|요)$/,''))).filter(t=>t.length>=2);
 const hits=tokens.filter(t=>text.includes(t)||ns.some(n=>n.includes(t))).length;
 if(hits&&hits/tokens.length>=.5)return 1000+Math.round(hits/tokens.length*400);
 if(q.length>=7){const grams=new Set(Array.from({length:q.length-1},(_,i)=>q.slice(i,i+2)));let best=0;for(const p of phrases){let match=0;for(const g of grams)if(p.includes(g))match++;best=Math.max(best,match/grams.size);}if(best>=.45)return Math.round(best*800);}
 return 0;}
function search(entries,q='',{fields=[],field='',kind='',category=''}={}){const scored=entries.filter(e=>(!field||e.field===field)&&(!kind||e.kind===kind)&&(!category||e.category===category)).map(e=>({entry:e,score:score(e,q)}));const exactShortKorean=/^[가-힣]{2,3}$/.test(normalize(q))&&scored.some(x=>x.score===10000);const floor=exactShortKorean?5000:normalize(q).length>=5&&scored.some(x=>x.score>=2200)?2000:scored.some(x=>x.score>=1000)?1000:1;return scored.filter(x=>x.score>=floor).sort((a,b)=>b.score-a.score||(fields.includes(a.entry.field)?fields.indexOf(a.entry.field):fields.length)-(fields.includes(b.entry.field)?fields.indexOf(b.entry.field):fields.length)||a.entry.term.localeCompare(b.entry.term,'ko')).map(x=>x.entry);}
// Suggestions match names, not prose. Short acronym prefixes are useful here
// even though submitted searches deliberately require complete short tokens.
function suggest(entries,query,{fields=[],kind='',category='',limit=6}={}){
 const q=normalize(query);if(!q)return [];
 const rank=e=>fields.includes(e.field)?fields.indexOf(e.field):fields.length;
 const matches=[];
 for(const e of entries){
  if(kind&&e.kind!==kind||category&&e.category!==category)continue;
  let best=0,matched='';
  for(const [i,name] of [e.term,...(e.aliases||[]),e.english].entries()){
   const n=normalize(name);if(!n)continue;
   const s=n===q?(i===0?100:95):n.startsWith(q)?(i===0?80:75):q.length>=2&&n.includes(q)?(i===0?60:55):0;
   if(s>best){best=s;matched=name;}
  }
  if(best)matches.push({entry:e,score:best,matched});
 }
 matches.sort((a,b)=>b.score-a.score||rank(a.entry)-rank(b.entry)||a.entry.term.localeCompare(b.entry.term,'ko')||a.entry.id.localeCompare(b.entry.id));
 const groups=new Map();
 for(const m of matches){const key=normalize(m.entry.term);if(!groups.has(key))groups.set(key,{entry:m.entry,matched:m.matched,fields:[]});const group=groups.get(key);if(!group.fields.includes(m.entry.field))group.fields.push(m.entry.field);}
 return [...groups.values()].slice(0,Math.max(0,Math.min(10,limit)));
}
function validateState(raw,entries,fields,redirects={}){
 const ids=new Set(entries.map(e=>e.id)),fids=new Set(fields.map(f=>f.id));
 const obj=raw&&typeof raw==='object'?raw:{};
 const resolve=id=>typeof id==='string'?(ids.has(id)?id:ids.has(redirects[id])?redirects[id]:null):null;
 const review={};
 for(const [id,value] of Object.entries(obj.review&&typeof obj.review==='object'&&!Array.isArray(obj.review)?obj.review:{})){
  const target=resolve(id);if(target&&['known','again'].includes(value))review[target]=review[target]==='again'?'again':value;
 }
 return {version:1,onboarded:obj.onboarded===true,fields:[...new Set(Array.isArray(obj.fields)?obj.fields.filter(x=>fids.has(x)):[])],saved:[...new Set(Array.isArray(obj.saved)?obj.saved.map(resolve).filter(Boolean):[])],review,recent:Array.isArray(obj.recent)?obj.recent.filter(x=>typeof x==='string'&&x.length<=200).slice(0,6):[]};
}
function shuffle(items,rng=Math.random){const out=[...items];for(let i=out.length-1;i>0;i--){const j=Math.floor(rng()*(i+1));[out[i],out[j]]=[out[j],out[i]];}return out;}
function daily(entries,fields,date=new Date()){const pool=entries.filter(e=>!fields.length||fields.includes(e.field));const list=pool.length?pool:entries;const day=Math.floor(Date.UTC(date.getFullYear(),date.getMonth(),date.getDate())/86400000);return list[day%list.length];}
// Discover from current data. Meaning identity excludes paraphrases of one concept.
// Aliases participate only when they match a headword, not arbitrary shared prose.
function contrastPairs(entries,fields=[]){
 const labels=new Map(entries.map(e=>[normalize(e.term),e.term])),groups=new Map();
 for(const e of entries)for(const name of new Set([e.term,...(e.aliases||[])].map(normalize))){
  if(!name||!labels.has(name))continue;
  if(!groups.has(name))groups.set(name,[]);groups.get(name).push(e);
 }
 const result=[];
 for(const [name,group] of groups){
  const senses=new Map();
  for(const e of group){const key=e.meaningKey||normalize(e.definition);if(!key)continue;if(!senses.has(key))senses.set(key,[]);senses.get(key).push(e);}
  const meanings=[...senses].sort(([a],[b])=>a.localeCompare(b));
  for(let i=0;i<meanings.length;i++)for(let j=i+1;j<meanings.length;j++){
   const options=[];
   for(const a of meanings[i][1])for(const b of meanings[j][1]){
    if(a.field===b.field||a.id===b.id||normalize(a.definition)===normalize(b.definition))continue;
    options.push([a,b]);
   }
   // Choose one representative per meaning, prioritizing the user's fields.
   const rank=e=>Number(fields.includes(e.field))*10+Number(normalize(e.term)===name);
   options.sort((a,b)=>rank(b[0])+rank(b[1])-rank(a[0])-rank(a[1])||a[0].id.localeCompare(b[0].id)||a[1].id.localeCompare(b[1].id));
   if(options.length)result.push({id:JSON.stringify([name,meanings[i][0],meanings[j][0]]),term:labels.get(name),entries:options[0].sort((a,b)=>rank(b)-rank(a)||a.id.localeCompare(b.id))});
  }
 }
 return result.sort((a,b)=>a.term.localeCompare(b.term,'ko')||a.id.localeCompare(b.id));
}
function nextCard(items,currentId,seen=[],rng=Math.random){
 const others=items.filter(e=>e.id!==currentId);
 if(!others.length)return {item:items[0]||null,seen:[...seen]};
 let history=seen,available=others.filter(e=>!history.includes(e.id));
 if(!available.length){history=currentId?[currentId]:[];available=others;}
 const item=available[Math.floor(rng()*available.length)];
 return {item,seen:[...new Set([...history,item.id])]};
}
return {normalize,names,score,search,suggest,validateState,shuffle,daily,contrastPairs,nextCard};
});
