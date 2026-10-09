const test=require('node:test'),assert=require('node:assert/strict');
const D=require('../data/dictionary.json'),C=require('../../frontend/core.js'),W=require('../../frontend/workspace-core.js');
const field=f=>D.entries.filter(e=>e.field===f);
test('finance abbreviations and spoken pronunciations resolve to reviewed headwords',()=>{
 for(const [q,t] of [['에비따','EBITDA'],['에비타','EBITDA'],['에빗다','EBITDA'],['역분','역분개'],['와이오와이','YoY'],['MoM','MoM'],['CF','CF'],['캐펙스','자본적지출'],['오펙스','운영비']])assert.equal(C.search(field('hrfinance'),q)[0]?.term,t,q);
 assert.match(C.search(field('hrfinance'),'에비따')[0].note,/현금흐름/);
});
test('every field contains kickoff with an individual example and the same meaning',()=>{
 const entries=D.fields.map(f=>C.search(field(f.id),'킥오프')[0]);assert(entries.every(e=>e?.term==='킥오프'));
 assert.equal(new Set(entries.map(e=>e.example)).size,7);assert.equal(new Set(entries.map(e=>e.meaningKey)).size,1);
 for(const name of ['킥오프','컨펌','팔로업','사인오프'])assert(!C.contrastPairs(D.entries).some(p=>p.term===name),name);
});
test('slang additions are discoverable inside their own field and document tool',()=>{
 const words={marketing:'예산 태우다',dev:'로그 심다',fashion:'깔별',film:'핀 나가다',design:'앉히다',hrfinance:'장부 털다',common:'케바케'};
 for(const [f,q] of Object.entries(words)){assert.equal(C.search(field(f),q)[0]?.term,q);assert(W.annotate(q,field(f)).spans.length);}
});
test('all entries retain complete metadata, valid sources, unique field headwords and stable redirects',()=>{
 assert.equal(D.entries.length,2882);assert.equal(new Set(D.entries.map(e=>e.id)).size,D.entries.length);
 assert.equal(new Set(D.entries.map(e=>e.field+'|'+e.term)).size,D.entries.length);
 for(const e of D.entries){assert(D.fields.some(f=>f.id===e.field));for(const k of ['term','definition','example','category','meaningKey'])assert(e[k],e.id+':'+k);for(const s of e.sources)assert(D.sources[s]?.url.startsWith('https://'));if(!e.sources.length)assert.match(e.evidence,/일반 지식/);}
 const ids=new Set(D.entries.map(e=>e.id));for(const [a,b] of Object.entries(D.redirects)){assert(!ids.has(a),a);assert(ids.has(b),b);}
});
test('suggestions match partial aliases, ignore definition prose and deduplicate headwords',()=>{
 assert.equal(C.suggest(field('hrfinance'),'에비')[0]?.entry.term,'EBITDA');
 assert(C.suggest(field('hrfinance'),'ebi').some(x=>x.entry.term==='EBITDA'));
 assert.equal(C.suggest(field('hrfinance'),'역분')[0]?.entry.term,'역분개');
 const shared=C.suggest(D.entries,'킥오',{fields:['dev']});assert.equal(shared.filter(x=>x.entry.term==='킥오프').length,1);assert.equal(shared[0].entry.field,'dev');assert.equal(shared[0].fields.length,7);
 const a={id:'1',field:'dev',term:'ABC',english:'',aliases:['에이비씨'],definition:'없는말'},b={...a,id:'2',term:'XYZ',aliases:[]};
 assert.equal(C.suggest([a,b],'없는말').length,0);assert.equal(C.suggest([a],'a')[0].entry.id,'1');assert.equal(C.search([a],'a').length,0);
 assert.equal(C.suggest(D.entries,'').length,0);assert.equal(C.suggest(D.entries,'a',{limit:2}).length,2);assert.equal(C.suggest(D.entries,'a',{limit:0}).length,0);
});
test('suggestions obey kind, topic and field scopes without modifying data',()=>{
 const before=JSON.stringify(D.entries);const pool=field('marketing');
 const s=C.suggest(pool,'예산',{kind:'현장 표현',category:'광고·마케팅 현장 말'});assert(s.some(x=>x.entry.term==='예산 태우다'));assert(s.every(x=>x.entry.field==='marketing'&&x.entry.kind==='현장 표현'));
 assert(!C.suggest(field('fashion'),'에비따').length);assert.equal(JSON.stringify(D.entries),before);
});
