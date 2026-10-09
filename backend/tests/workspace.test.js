const test=require('node:test'),assert=require('node:assert/strict');
const W=require('../../frontend/workspace-core.js'),C=require('../../frontend/core.js'),D=require('../data/dictionary.json');
const normalize=raw=>W.normalize(raw,D.entries,D.fields,D.redirects);
test('legacy fields migrate without losing IDs; invalid profile values are removed',()=>{
 const n=normalize({fields:['film','dev','film','missing'],viewed:['film-105','missing'],notes:{'film-105':{text:'맥락',collection:' 회의 '},missing:{text:'x'}}});
 assert.deepEqual(n.profile.workFields,['film','dev']);assert.deepEqual(n.profile.interestFields,[]);assert.equal(n.profile.completed,false);assert.deepEqual(n.viewed,['film-105']);assert.deepEqual(n.notes['film-105'],{text:'맥락',collection:'회의'});
});
test('work and curiosity are separate multi-select scopes with work first',()=>{
 const {profile:p}=normalize({profile:{completed:true,workFields:['hrfinance','marketing'],interestFields:['dev','fashion','marketing'],role:'finance',purposes:['budget','bogus']}});
 assert.deepEqual(p.interestFields,['dev','fashion']);assert.deepEqual(W.priorities(p),['hrfinance','marketing','dev','fashion']);
 assert(W.scope(D.entries,'work',p).every(e=>['hrfinance','marketing'].includes(e.field)));
 assert(W.scope(D.entries,'interest',p).every(e=>['dev','fashion'].includes(e.field)));
 assert.equal(W.scope(D.entries,'all',p).length,D.entries.length);
 assert.equal(C.search(D.entries,'리텐션',{fields:W.priorities(p)})[0].field,'hrfinance');
});
test('empty scopes show all; explicit fields are independent of preferences',()=>{
 const {profile:p}=normalize(null);assert.equal(W.scope(D.entries,'work',p).length,D.entries.length);assert.equal(W.scope(D.entries,'hrfinance',p).length,524);assert.equal(W.scope(D.entries,'missing',p).length,0);
});
test('only explicit purposes shape situation links; removed questions do not infer preferences',()=>{
 const {profile:p}=normalize({profile:{role:'finance',companyType:'agency',purposes:['hiring']}});
 assert.deepEqual(W.situations(p).map(x=>x[0]),['hiring']);
 const entries=W.situationEntries(W.scope(D.entries,'hrfinance',p),'hiring');assert(entries.some(e=>e.term==='채용계획'));for(const term of ['손금불산입','가수금','가지급금','가결산','역분개','결산조정','자산평가'])assert(!entries.some(e=>e.term===term),term);
});
test('document matching retains ambiguous meanings and respects Latin boundaries',()=>{
 const result=W.extract('리텐션과 AP, 근로 계약서를 검토합니다. JavaScript와 APPROACH는 별개의 말.',D.entries);
 assert(result.some(e=>e.term==='리텐션'&&e.field==='hrfinance'));assert(result.some(e=>e.term==='리텐션'&&e.field==='marketing'));assert(result.some(e=>e.term==='매입채무'));
 assert(!W.extract('APPROACH',D.entries).some(e=>e.term==='매입채무'));assert(!W.extract('script',D.entries).some(e=>e.term==='PR'));
 assert(!W.extract('',D.entries).length);
});
test('aliases, multiple meanings and document input are not mutated',()=>{
 const text='급여대장을 확인한 뒤 페이롤 마감. HC와 ATS를 확인하고 백필을 진행해요.';const result=W.extract(text,D.entries.filter(e=>e.field==='hrfinance'));
 for(const term of ['급여대장','페이롤','헤드카운트','지원자추적시스템','대체 채용'])assert(result.some(e=>e.term===term),term);
 assert(D.entries.every(e=>!('matched' in e)));
});
test('notes and selections survive JSON round trip, with bounded user text',()=>{
 const raw={profile:{completed:true,workFields:['hrfinance'],interestFields:['film'],density:'compact'},notes:{'hrfinance-318':{text:'<script>메모</script>',collection:'월간회의'}},viewed:['hrfinance-318'],compare:['hrfinance-318','marketing-546']};
 const a=normalize(raw),b=normalize(JSON.parse(JSON.stringify(a)));assert.deepEqual(a,b);assert.equal(b.notes['hrfinance-318'].text,raw.notes['hrfinance-318'].text);
 assert.equal(normalize({notes:{'hrfinance-318':{text:'x'.repeat(3000),collection:'y'.repeat(90)}}}).notes['hrfinance-318'].text.length,2000);
});
test('CSV preserves Korean, quotes and newlines and neutralizes formulas',()=>{
 const e=D.entries.find(e=>e.id==='hrfinance-318');const csv=W.csv([e],{[e.id]:{text:'=SUM(1,2)\n"note"',collection:'회의'}},D.fields);
 assert(csv.startsWith('\ufeff'));assert(csv.includes('인사·재무'));assert(csv.includes("\"'=SUM(1,2)"));assert(csv.includes('""note""'));
});
test('HR/finance has 524 distinct reviewed definitions and contextual examples',()=>{
 const entries=D.entries.filter(e=>e.field==='hrfinance');assert.equal(entries.length,524);assert.equal(new Set(entries.map(e=>e.term)).size,524);assert.equal(new Set(entries.map(e=>e.definition)).size,524);assert.equal(new Set(entries.map(e=>e.example)).size,524);
 assert(new Set(entries.map(e=>e.category)).size>=24);assert(entries.every(e=>e.example&&e.definition&&e.meaningKey));assert(entries.filter(e=>e.sources.length).length>=35);
 for(const q of ['HRBP','DB','DC','IRP','AP','FP&A','페이롤','백필','법인세','원천징수','기표'])assert(C.search(entries,q).length,q);
});
test('new HR synonyms do not masquerade as different meanings across industries',()=>{
 const pairs=C.contrastPairs(D.entries);for(const term of ['인사팀','회계팀','직급','직책','피플팀','온보딩','미결'])assert(!pairs.some(p=>p.term===term),term);
 assert(pairs.some(p=>p.term==='리텐션'&&p.entries.some(e=>e.field==='hrfinance')));assert(pairs.some(p=>p.term==='AP'&&p.entries.some(e=>e.field==='hrfinance')));assert(pairs.some(p=>p.term==='CFO'&&p.entries.some(e=>e.term==='영업활동현금흐름')));
});
const entry=(id,term,aliases=[],field='marketing')=>({id,term,aliases,english:'',field});
test('inline highlights prefer whole phrases, repeat occurrences and group same-range meanings',()=>{
 const entries=[entry('short','카피'),entry('long','키카피',['키 카피']),entry('other','키카피',[],'design')];
 const text='키카피와 카피. 키카피, 키 카피!';const a=W.annotate(text,entries);
 assert.deepEqual(a.spans.map(s=>a.text.slice(s.start,s.end)),['키카피','카피','키카피','키 카피']);
 assert.deepEqual(a.spans[0].entries.map(e=>e.id),['long','other']);assert.equal(a.spans[3].entries.length,1);
 assert(a.spans.every((s,i)=>!i||s.start>=a.spans[i-1].end));assert.deepEqual(entries[0],entry('short','카피'));
});
test('highlight offsets preserve fullwidth, combining Korean, emoji and exact original text',()=>{
 const text='👋 ＰＲ & PR\n근로 계약서 <b>리텐션</b> ﬂow';
 const a=W.annotate(text,[entry('pr','PR'),entry('contract','근로 계약서'),entry('ret','리텐션'),entry('flow','flow')]);
 assert.equal(a.text,text);assert.deepEqual(a.spans.map(s=>text.slice(s.start,s.end)),['ＰＲ','PR','근로 계약서','리텐션','ﬂow']);
 let reconstructed='',end=0;for(const s of a.spans){reconstructed+=text.slice(end,s.start)+text.slice(s.start,s.end);end=s.end;}reconstructed+=text.slice(end);assert.equal(reconstructed,text);
});
test('highlight boundaries, field filtering, empty and bounded documents',()=>{
 const entries=[entry('pr','PR'),entry('ap','AP'),entry('one','말'),entry('ad','리텐션'),entry('hr','리텐션',[],'hrfinance')];
 assert.equal(W.annotate('APPROACH script 말',entries).spans.length,0);
 const a=W.annotate('리텐션과 PR, pr.',W.scope(entries,'hrfinance',{}));assert.equal(a.spans.length,1);assert.deepEqual(a.spans[0].entries.map(e=>e.id),['hr']);
 assert.deepEqual(W.annotate('',entries),{text:'',spans:[]});assert.equal(W.annotate('a'.repeat(20000)+' PR',entries).spans.length,0);
});

test('first-run shortcuts stay unchecked, explicit choices survive, all selected links remain visible',()=>{
 const fresh=normalize(null).profile;assert.deepEqual(fresh.purposes,[]);
 assert.deepEqual(W.situations(fresh).map(x=>x[0]),['meeting','planning','reporting']);assert.deepEqual(fresh.purposes,[]);
 const saved=normalize({profile:{purposes:['hiring','budget']}}).profile;assert.deepEqual(saved.purposes,['hiring','budget']);assert.deepEqual(W.situations(saved).map(x=>x[0]),['hiring','budget']);
 const all=normalize({profile:{purposes:W.PURPOSES.map(x=>x[0])}}).profile;assert.equal(W.situations(all).length,6);
 const cleared=normalize({profile:{role:'finance',companyType:'factory',purposes:[]}}).profile;assert.deepEqual(W.situations(cleared),W.situations(fresh));
});
test('legacy familiarity levels migrate to two actual reading orders',()=>{
 assert.equal(normalize({profile:{experience:'expert'}}).profile.experience,'familiar');
 assert.equal(normalize({profile:{experience:'familiar'}}).profile.experience,'familiar');
 assert.equal(normalize({profile:{experience:'new'}}).profile.experience,'new');
});
