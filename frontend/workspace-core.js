/* Local-only personalization and document matching. No network requests. */
(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory();else root.WorkspaceCore=factory();})(typeof window==='object'?window:this,()=>{
'use strict';
const PURPOSES=[['meeting','회의·협업','회의|기획|커뮤니케이션|현장 표현|조직'],['planning','기획·제안','기획|전략|광고|브랜드|예산'],['handoff','제작·인수인계','제작|공정|개발|편집|촬영|봉제|가공|디자인'],['reporting','보고·분석','분석|지표|성과|데이터|회계|재무'],['hiring','채용·인사','채용|인사|평가|급여|근태|조직|퇴직'],['budget','예산·정산','예산|원가|자금|매출|결산|세무|정산']];
const ROLES=[['','선택하지 않음'],['planner','기획·마케팅'],['maker','개발·디자인·제작'],['people','인사·운영'],['finance','재무·회계'],['lead','팀·프로젝트 관리']];
const COMPANIES=[['','선택하지 않음'],['agency','대행사·제작사'],['brand','브랜드·유통'],['tech','IT·서비스'],['factory','제조·섬유'],['other','기타·프리랜서']];
const uniq=a=>[...new Set(a)];
function normalize(raw,entries,fields,redirects={}){
 raw=raw&&typeof raw==='object'?raw:{};const ids=new Set(entries.map(e=>e.id)),fs=new Set(fields.map(f=>f.id));
 const validIds=a=>uniq((Array.isArray(a)?a:[]).map(id=>redirects[id]||id).filter(id=>ids.has(id)));
 const validFields=a=>uniq((Array.isArray(a)?a:[]).filter(id=>fs.has(id)));
 const p=raw.profile&&typeof raw.profile==='object'?raw.profile:{};
 const workFields=validFields(p.workFields||raw.fields),interestFields=validFields(p.interestFields).filter(f=>!workFields.includes(f));
 const profile={completed:p.completed===true,workFields,interestFields,role:ROLES.some(x=>x[0]===p.role)?p.role:'',companyType:COMPANIES.some(x=>x[0]===p.companyType)?p.companyType:'',experience:['familiar','expert'].includes(p.experience)?'familiar':'new',purposes:uniq((Array.isArray(p.purposes)?p.purposes:[]).filter(id=>PURPOSES.some(x=>x[0]===id))),density:p.density==='compact'?'compact':'comfortable'};
 const notes={};Object.entries(raw.notes&&typeof raw.notes==='object'?raw.notes:{}).forEach(([old,n])=>{const id=redirects[old]||old;if(!ids.has(id)||!n||typeof n!=='object')return;const text=typeof n.text==='string'?n.text.slice(0,2000):'',collection=typeof n.collection==='string'?n.collection.trim().slice(0,40):'';if(text||collection)notes[id]={text,collection};});
 return {profile,fields:workFields,notes,viewed:validIds(raw.viewed).slice(0,20),compare:validIds(raw.compare).slice(0,3)};
}
function scope(entries,scopeId,profile){const ids=scopeId==='work'?profile.workFields:scopeId==='interest'?profile.interestFields:null;return ids?entries.filter(e=>!ids.length||ids.includes(e.field)):scopeId&&scopeId!=='all'?entries.filter(e=>e.field===scopeId):entries;}
function priorities(p){return uniq([...p.workFields,...p.interestFields]);}
function situations(p){const selected=uniq((p.purposes||[]).filter(id=>PURPOSES.some(x=>x[0]===id)));return (selected.length?selected:['meeting','planning','reporting']).map(id=>PURPOSES.find(x=>x[0]===id));}
function situationEntries(entries,id){
 const purpose=PURPOSES.find(x=>x[0]===id);if(!purpose)return entries;const re=new RegExp(purpose[2]);
 return entries.filter(e=>{
  // Finance topics use words such as 평가 too; they are not hiring topics.
  if(id==='hiring'&&e.field==='hrfinance'&&/^(재무|자금|결산|매출|원가|세무|실적|예산|기업재무)/.test(e.category||''))return false;
  const category=(e.category||'').replace(/인사·재무|마케팅·광고|패션·섬유|영상·촬영|개발·IT|업무 공통/g,'');
  return re.test(category+' '+e.term+' '+e.definition);
 });
}
function extract(text,entries){
 // Whitespace variations are accepted. Short Latin abbreviations need boundaries;
 // Korean heads allow particles, but one-character matches are too ambiguous.
 const normalized=String(text).slice(0,20000).normalize('NFKC').toLowerCase();const matched=[];
 for(const e of entries){let found='';for(const raw of [e.term,e.english,...e.aliases]){const n=raw.normalize('NFKC').toLowerCase().trim();if(n.replace(/\s/g,'').length<2)continue;const escaped=n.replace(/[.*+?^${}()|[\]\\]/g,'\\$&').replace(/\s+/g,'\\s*');const latin=/^[a-z0-9 .&/()+-]+$/.test(n);const re=new RegExp((latin?'(?<![a-z0-9])':'')+escaped+(latin?'(?![a-z0-9])':''),'i');if(re.test(normalized)){found=raw;break;}}if(found)matched.push({...e,matched:found});}
 return matched;
}
// Return non-overlapping original-text ranges. Normalize graphemes with an offset
// map so full-width letters, ligatures and decomposed Korean never shift highlights.
function annotate(input,entries){
 const text=String(input).slice(0,20000),starts=[],ends=[];let normalized='';
 const segments=typeof Intl.Segmenter==='function'?new Intl.Segmenter('ko',{granularity:'grapheme'}).segment(text):Array.from(text).map((segment,i,a)=>({segment,index:a.slice(0,i).join('').length}));
 for(const {segment,index} of segments){const n=segment.normalize('NFKC').toLowerCase();normalized+=n;for(let i=0;i<n.length;i++){starts.push(index);ends.push(index+segment.length);}}
 const tokens=new Map();
 for(const e of entries)for(const raw of [e.term,e.english,...(e.aliases||[])]){
  const n=String(raw||'').normalize('NFKC').toLowerCase().trim();if(n.replace(/\s/g,'').length<2)continue;
  if(!tokens.has(n))tokens.set(n,new Map());tokens.get(n).set(e.id,e);
 }
 const ranges=new Map();
 for(const [n,meanings] of tokens){
  const escaped=n.replace(/[.*+?^${}()|[\]\\]/g,'\\$&').replace(/\s+/g,'\\s*'),latin=/^[a-z0-9 .&/()+-]+$/.test(n);
  const re=new RegExp((latin?'(?<![a-z0-9])':'')+escaped+(latin?'(?![a-z0-9])':''),'g');
  for(const match of normalized.matchAll(re)){
   const from=starts[match.index],to=ends[match.index+match[0].length-1],key=from+':'+to;
   if(!ranges.has(key))ranges.set(key,{start:from,end:to,entries:new Map()});
   for(const [id,e] of meanings)ranges.get(key).entries.set(id,e);
  }
 }
 const ordered=[...ranges.values()].sort((a,b)=>a.start-b.start||b.end-a.end),spans=[];let end=0;
 for(const r of ordered){if(r.start<end)continue;spans.push({...r,entries:[...r.entries.values()]});end=r.end;}
 return {text,spans};
}
function csv(entries,notes,fields){const cell=v=>'"'+String(v??'').replace(/^[=+@-]/,"'$&").replace(/"/g,'""')+'"';return '\ufeff'+[['단어','분야','뜻','예문','내 메모','모음'],...entries.map(e=>[e.term,fields.find(f=>f.id===e.field)?.name,e.definition,e.example,notes[e.id]?.text,notes[e.id]?.collection])].map(r=>r.map(cell).join(',')).join('\r\n');}
return {PURPOSES,ROLES,COMPANIES,normalize,scope,priorities,situations,situationEntries,extract,annotate,csv};
});
