const test=require('node:test'),assert=require('node:assert/strict'),C=require('../../frontend/core.js'),D=require('../data/dictionary.json');
const find=(q,opt)=>C.search(D.entries,q,opt);
test('한국어 줄임말과 풀어 쓴 이름이 같은 항목을 찾음',()=>{
 for(const [field,q,full,term] of [
  ['marketing','브검','브랜드검색광고','브검'],['marketing','쇼검','쇼핑검색광고','쇼검'],
  ['fashion','작지','작업지시서','테크팩'],['fashion','무배','무료배송','무배'],
  ['dev','자스','자바스크립트','JavaScript'],['dev','타스','타입스크립트','타스'],
  ['dev','단테','단위 테스트','단위 테스트'],['dev','통테','통합 테스트','통합 테스트'],
  ['film','가편','가편집','러프 컷'],['film','촬감','촬영감독','촬감'],
  ['design','상페','상세페이지','상페'],['design','타이포','타이포그래피','타이포그래피'],
  ['common','법카','법인카드','법카'],['common','지결','지출결의서','지결']
 ]){
  const a=find(q,{field})[0],b=find(full,{field})[0];
  assert.equal(a.term,term,field+':'+q);assert.equal(a.id,b.id,q+' / '+full);
 }
});
test('일반 업무 줄임말은 공통에서 한 번만 검색·학습',()=>{
 for(const q of ['원복','복붙','포폴','플젝','법카','재택']){
  assert.equal(find(q)[0].field,'common');
  assert(C.shuffle(D.entries.filter(e=>e.field==='common')).some(e=>e.term===q));
  for(const f of D.fields.filter(f=>f.id!=='common'))assert(!D.entries.some(e=>e.field===f.id&&e.term===q));
 }
});
test('한국어 줄임말의 분야별 의미 및 설명 검색',()=>{
 assert.deepEqual(find('작지').map(e=>e.term),['테크팩']);
 assert.equal(find('가편')[0].term,'러프 컷');
 assert(find('가편').every(e=>['러프 컷','오프라인 편집'].includes(e.term)));
 assert(find('법카').every(e=>e.term==='법카'));
 assert(find('가라').some(e=>e.field==='fashion'));
 assert(find('가라').some(e=>e.field==='common'));
 assert.equal(find('실시간으로 옷 보여주며 판매',{field:'fashion'})[0].term,'라방');
 assert.equal(find('집에서 일하는 근무',{field:'common'})[0].term,'재택');
 assert.equal(find('방송 전에 미리 녹화하는',{field:'film'})[0].term,'사녹');
 assert.notEqual(find('라방',{field:'film'})[0].definition,find('라방',{field:'fashion'})[0].definition);
 assert.match(find('본방',{field:'film'})[0].note,/반드시 생방송/);
 assert.match(find('종편',{field:'film'})[0].note,/종합편성채널/);
});
test('카드 새로고침은 한 바퀴 동안 중복 없이, 경계에서도 직전 항목 제외',()=>{
 const items=['a','b','c','d'].map(id=>({id}));let id='a',seen=['a'];const shown=[id];
 for(let i=0;i<11;i++){const next=C.nextCard(items,id,seen,()=>0);assert.notEqual(next.item.id,id);id=next.item.id;seen=next.seen;shown.push(id);}
 assert.equal(new Set(shown.slice(0,4)).size,4);
 assert.equal(C.nextCard([],null).item,null);assert.equal(C.nextCard([{id:'a'}],'a').item.id,'a');
 assert.deepEqual(items.map(e=>e.id),['a','b','c','d']);
});
test('다른 의미 카드는 단순 분야별 복사나 문장 차이를 제외',()=>{
 const pairs=C.contrastPairs(D.entries);
 for(const term of ['레퍼런스','트래킹','가라','PO','레이어','노출','미싱','프록시','프레임','편집','폴리','앞단','뒷단','PR','PD','페이싱'])assert(pairs.some(p=>p.term===term),term);
 for(const p of pairs){assert.notEqual(p.entries[0].field,p.entries[1].field);assert.notEqual(p.entries[0].meaningKey,p.entries[1].meaningKey);assert(p.entries.every(e=>C.names(e).includes(C.normalize(p.term))));}
 assert.equal(new Set(pairs.map(p=>p.id)).size,pairs.length);
 assert.deepEqual(C.contrastPairs([]),[]);
 assert(!pairs.some(p=>['시마이','PT','시안','카피','패딩','렌더링','색보정','콘셉트','자간','행간','마스킹','랜딩','팝업'].includes(p.term)));
 assert(pairs.filter(p=>p.term==='리텐션').every(p=>p.entries.some(e=>e.field==='hrfinance')));
 assert(D.entries.every(e=>typeof e.meaningKey==='string'&&e.meaningKey));
 assert.equal(pairs.filter(p=>p.term==='노출').length,1);
});
test('새 표제어와 별칭은 카드 목록 등록 없이 자동 편입',()=>{
 const entry=(id,field,term,definition,more={})=>({id,field,term,definition,aliases:[],...more});
 const a=entry('new-a','dev','새 비교어','요청을 처리하는 장치');
 const b=entry('new-b','film','새 비교어','촬영할 때 쓰는 장치');
 assert.equal(C.contrastPairs([a]).length,0);
 assert.equal(C.contrastPairs([a,b]).length,1);
 assert.equal(C.contrastPairs([a,{...b,term:'다른 표제어',aliases:['새 비교어']}]).length,1);
 assert.equal(C.contrastPairs([a,{...b,definition:a.definition,example:'예문만 다름'}]).length,0);
 assert.equal(C.contrastPairs([{...a,meaningKey:'one-concept'},{...b,meaningKey:'one-concept'}]).length,0);
 assert.equal(C.contrastPairs([a,{...b,field:'dev'}]).length,0);
 assert.equal(C.contrastPairs([a,{...b,term:'새 비교 어'}]).length,1);
 assert.equal(C.contrastPairs([a,{...b,term:'별개 단어',aliases:['요청']}]).length,0);
});
test('세 가지 이상 의미와 관심 분야, 데이터 삭제를 자동 반영',()=>{
 const entries=['dev','film','fashion'].map((field,i)=>({id:field,field,term:'테스트 동형어',definition:'서로 다른 뜻 '+i,meaningKey:'sense-'+i}));
 const copy={...entries[0],id:'design',field:'design',definition:'동일 개념의 다른 문장'};
 const pairs=C.contrastPairs([...entries,copy],['design']);
 assert.equal(pairs.length,3);
 assert.equal(pairs.filter(p=>p.entries.some(e=>e.id==='design')).length,2);
 assert(pairs.every(p=>!p.entries.some(e=>e.id==='dev')));
 assert.equal(C.contrastPairs(entries.slice(0,2)).length,1);
 assert.equal(C.contrastPairs(entries.slice(0,1)).length,0);
 const live=C.contrastPairs(D.entries,['film']);
 assert(live.find(p=>p.term==='프록시').entries.some(e=>e.field==='film'));
 assert.equal(live.filter(p=>p.term==='레이어').length,3);
 let current=pairs[0],seen=[current.id];const visited=[current.id];
 for(let i=1;i<pairs.length;i++){const next=C.nextCard(pairs,current.id,seen,()=>0);current=next.item;seen=next.seen;visited.push(current.id);}
 assert.equal(new Set(visited).size,pairs.length);
});
test('요청한 촬영 단어와 표기 변형',()=>{for(const [q,expected] of [['앵글','앵글'],['부감','부감'],['앙감','앙감'],['바스트샷','바스트 샷'],['바스트 숏','바스트 샷'],['팔로우','팔로우'],['시마이','시마이'],['ＢＳ','바스트 샷'],['하이 앵글','부감']])assert.equal(find(q,{fields:['film']})[0].term,expected,q);});
test('설명으로 용어 검색',()=>{for(const [q,expected] of [['가슴부터 찍는','바스트 샷'],['위에서 내려다보는','부감'],['사람을 따라가면서 찍는','팔로우'],['촬영 마무리','시마이'],['배경 흐리게','얕은 심도'],['다음 장면 소리 먼저','J컷']])assert.equal(find(q,{fields:['film']})[0].term,expected,q);});
test('동일 단어는 내 분야 우선, 다른 분야 정확한 단어도 찾음',()=>{assert.equal(find('레퍼런스',{fields:['dev']})[0].field,'dev');assert.equal(find('레퍼런스',{fields:['design']})[0].field,'design');assert.equal(find('가라',{fields:['common']})[0].field,'common');assert.equal(find('QA',{fields:['film']})[0].field,'dev');});
test('필터와 빈 결과',()=>{assert.equal(find('zzzzzzzzz').length,0);assert.equal(find('QA',{field:'film'}).length,0);assert(find('',{field:'film',category:'조명'}).every(e=>e.field==='film'&&e.category==='조명'));assert(find('',{kind:'현장 표현'}).every(e=>e.kind==='현장 표현'));});
test('잘못된 저장 데이터와 삭제된 단어를 정리',()=>{const id=D.entries[0].id;const s=C.validateState({fields:['film','film','bad'],saved:[id,id,'bad'],review:{[id]:'again',bad:'known',x:'evil'},recent:[null,1,'부감'],onboarded:1},D.entries,D.fields);assert.deepEqual(s.fields,['film']);assert.deepEqual(s.saved,[id]);assert.deepEqual(s.review,{[id]:'again'});assert.deepEqual(s.recent,['부감']);assert.equal(s.onboarded,false);assert.equal(C.validateState(null,D.entries,D.fields).saved.length,0);});
test('한 학습 세션 안에서 중복 없음, 원본 불변',()=>{const pool=D.entries.map(e=>e.id),old=[...pool],queue=C.shuffle(pool);assert.equal(new Set(queue).size,pool.length);assert.deepEqual(pool,old);assert.deepEqual(C.shuffle([]),[]);assert.deepEqual(C.shuffle(['a']),['a']);});
test('날짜와 분야가 같으면 오늘의 단어 동일',()=>{const dt=new Date(2026,8,15);assert.equal(C.daily(D.entries,['film'],dt).id,C.daily(D.entries,['film'],dt).id);assert.equal(C.daily(D.entries,['film'],dt).field,'film');});
test('모든 항목에 작성 근거·예시, ID와 분야별 표제어 중복 없음',()=>{assert.equal(new Set(D.entries.map(e=>e.id)).size,D.entries.length);assert.equal(new Set(D.entries.map(e=>e.field+'|'+e.term)).size,D.entries.length);for(const e of D.entries){assert(e.example&&e.definition&&e.phrases.length);assert(e.sources.every(s=>D.sources[s]&&D.sources[s].url.startsWith('https://')));assert(D.fields.some(f=>f.id===e.field));}});

test('내려다보는 설명에 반대 앵글을 섞지 않음',()=>{assert(!find('위에서 내려다보는').some(e=>e.term==='앙감'));});

test('회사 업무 용어가 각 분야의 검색과 학습 풀에 포함됨',()=>{
  const expected={marketing:['PT','경쟁 PT','시안','키비주얼','AE','키카피','광고 소재'],fashion:['시안','키비주얼','MD','SKU','MOQ','PO','라인시트','룩북','판매율','테크팩','ROAS','리오더'],dev:['PO','CI','기술 부채','코드 리뷰','핸드오프','디자인 시스템','CTA'],design:['시안','키비주얼','도련','별색','오토 레이아웃','디자인 토큰','핸드오프']};
  for(const [field,terms] of Object.entries(expected))for(const term of terms){
    assert(find(term,{field}).some(e=>e.term===term&&e.field===field),field+':'+term);
    assert(D.entries.filter(e=>e.field===field).some(e=>e.term===term));
  }
});
test('같은 뜻도 분야별 유지하고 내 분야를 먼저 표시',()=>{
  for(const [term,fields] of [['시안',['marketing','fashion','dev','design']],['키비주얼',['marketing','fashion','design']],['ROAS',['marketing','fashion']]]){
    const matches=D.entries.filter(e=>e.term===term&&fields.includes(e.field));
    assert.equal(matches.length,fields.length);
    assert.equal(new Set(matches.map(e=>e.definition)).size,1);
    for(const field of fields)assert.equal(find(term,{fields:[field]})[0].field,field);
  }
});
test('PO의 분야별 다른 의미와 약자 검색',()=>{
  assert.equal(find('PO',{field:'fashion'})[0].english,'Purchase order');
  assert.equal(find('PO',{field:'dev'})[0].english,'Product owner');
  assert.equal(find('KV',{field:'marketing'})[0].term,'키비주얼');
  assert.equal(find('컴펌',{field:'common'})[0].term,'컨펌');
});
test('추가한 현장 상황으로 해당 단어를 찾음',()=>{
  for(const [q,field,term] of [['캠페인 대표 이미지','marketing','키비주얼'],['최소 몇 개 주문해야 하는지','fashion','MOQ'],['공장이 옷 만들 때 보는 문서','fashion','테크팩'],['동작 안 바꾸고 코드 정리','dev','리팩터링'],['디자인을 개발자에게 넘기는','design','핸드오프']])assert.equal(find(q,{field})[0].term,term,q);
});
test('짧은 약자는 영문 단어 일부와 혼동하지 않음',()=>{
  assert.deepEqual(new Set(find('PT').map(e=>e.term)),new Set(['PT','경쟁 PT','장표']));
  assert.equal(find('ＰＴ',{field:'common'})[0].term,'PT');
  assert(!find('PO').some(e=>e.term==='POS'));
  assert.equal(find('JS')[0].term,'JavaScript');
  assert.equal(find('BS',{field:'film'})[0].term,'바스트 샷');
  assert.deepEqual(new Set(find('CD',{field:'dev'}).map(e=>e.term)),new Set(['지속적 제공','지속적 배포','CI/CD']));
});

test('분야별 새 은어와 실무 표현을 검색하고 학습 풀에 포함',()=>{
  const groups={marketing:['T&D','구좌','OT','PPM','시딩','후킹','바리에이션','위닝 소재'],fashion:['장끼','미송','나오시','랍빠','나나인찌','시딩'],dev:['LGTM','Nit','WIP','삽질','온콜'],design:['하리꼬미','도무송','반칼','베다','바리에이션'],film:['야마','시바이','입봉','도리나오시','PPM'],common:['아삽','핑','R&R','팔로업','얼터안']};
  for(const [field,terms] of Object.entries(groups))for(const term of terms){
    assert.equal(find(term,{field,kind:'현장 표현'})[0]?.term,term,field+':'+term);
    assert(D.entries.some(e=>e.field===field&&e.term===term));
  }
});
test('현장 호칭은 기존 뜻의 별칭으로 연결',()=>{
  for(const [field,q,term] of [['film','데모찌','핸드헬드'],['design','돈보','맞춤표'],['fashion','누이시로','시접'],['fashion','다찌','재단'],['common','듀데잇','데드라인']]){
    assert.equal(find(q,{field})[0]?.term,term,q);
    assert.equal(D.entries.filter(e=>e.field===field&&e.term===q).length,0,q);
  }
});
test('비슷한 은어와 문장 검색의 의미 구분',()=>{
  for(const [q,field,term] of [['시바이','film','시바이'],['촬영 마무리','film','시마이'],['돈 먼저 내고 나중에 받는','fashion','미송'],['스티커 뒷지 안 자르고 칼집','design','반칼'],['코드 리뷰 승인 약자','dev','LGTM'],['팀끼리 방향을 맞추는','common','얼라인']])assert.equal(find(q,{field})[0]?.term,term,q);
  assert.notEqual(find('목',{field:'dev'})[0].definition,find('스텁',{field:'dev'})[0].definition);
});
test('공유하는 새 뜻과 문장부호 포함 약자 검색',()=>{
  for(const field of ['common','marketing','dev','design','fashion']){
    assert.equal(find('R&R',{fields:[field]})[0].field,field);
    assert.equal(find('F/up',{field:'common'})[0].term,'팔로업');
  }
  assert.equal(find('Ｔ＆Ｄ',{field:'marketing'})[0].term,'T&D');
  assert.deepEqual(new Set(find('WIP',{field:'dev'}).map(e=>e.term)),new Set(['WIP','WIP 제한']));
  for(const term of ['얼라인','핑','도무송'])assert.equal(new Set(D.entries.filter(e=>e.term===term).map(e=>e.definition)).size,1);
});
test('오래된 현장 자료와 문맥 차이에 메모 유지',()=>{
  for(const term of ['갇와리','야마','나오시']){
    const e=D.entries.find(e=>e.term===term);assert(e.historical);assert(e.note);assert(e.sources.some(s=>D.sources[s].historical));
  }
  for(const [field,term,context] of [['film','시바이','시마이'],['fashion','라이브','마케팅팀'],['fashion','도무송','인쇄물'],['dev','RFC','인터넷']])assert(D.entries.find(e=>e.field===field&&e.term===term).note.includes(context));
});

test('요청한 광고 기본 직무·공정과 구어 활용형 검색',()=>{
 const cases=[['pd','PD'],['덕션','덕션'],['pd프로덕션','PD 프로덕션'],['PD덕션','PD 프로덕션'],['기획실','기획실'],['플래너','플래너'],['ECD','ECD'],['EPD','EPD'],['조감독','조감독'],['연출','연출'],['연출부','연출부'],['조명','조명'],['2d','2D'],['D.I','D.I'],['디아이','D.I'],['d.i.','D.I'],['편집','편집'],['녹음','녹음'],['인서트','인서트'],['썬다','썰다'],['썰어넣는다','썰어 넣다'],['듀레이션','듀레이션']];
 for(const [q,term] of cases)assert(find(q,{field:'marketing'}).some(e=>e.term===term),q);
 assert(!find('PD',{field:'marketing'}).some(e=>e.term==='EPD'));
 assert(!find('D.I',{field:'marketing'}).some(e=>e.term==='DIT'));
});
test('일반 회사 용어는 공통에, 업계 조직·공정은 해당 분야에 포함',()=>{
 for(const f of D.fields.filter(f=>f.id==='common'))for(const term of ['클라이언트','외주','사업부','인사팀','운영팀','팀장','과장','직책','견적서','요구사항','발주','검수','납품','정산','인수인계','리뷰','홀드']){
  assert(find(term,{field:f.id}).some(e=>e.term===term),f.id+':'+term);
 }
 const groups={
  marketing:['광고대행사','기획실','EPD','SA','D.I','컷다운','마스터','가녹음'],
  film:['PD 프로덕션','연출부','라인 PD','조감독','조명감독','믹싱','컨폼','썰다'],
  fashion:['프로모션 업체','소재팀','TD','패터너','랩딥','제직','PP 샘플','검침','탕 차이'],
  dev:['SI','개발팀','CTO','SRE','PRD','ERD','스테이징','회귀 테스트','물리다'],
  design:['디자인 에이전시','디자인팀','UX 리서처','편집 디자이너','저니맵','아웃라인','제판','중철','톤 다운']
 };
 for(const [f,terms] of Object.entries(groups))for(const term of terms)assert(find(term,{field:f}).some(e=>e.term===term),f+':'+term);
});
test('업계별로 뜻이 다른 짧은 말과 약자를 분리',()=>{
 for(const [q,a,b] of [['PD','film','design'],['SA','marketing','dev'],['미싱','fashion','design'],['프록시','film','dev'],['큐','film','dev']]){
  const x=find(q,{field:a})[0],y=find(q,{field:b})[0];
  assert(x&&y,q);assert.notEqual(x.definition,y.definition,q);
  assert.equal(find(q,{fields:[a]})[0].field,a,q);
  assert.equal(find(q,{fields:[b]})[0].field,b,q);
 }
});
test('외부 출처 없는 지식은 확인 자료로 표시하지 않음',()=>{
 const uncited=D.entries.filter(e=>!e.sources.length);assert(uncited.length>0);
 for(const e of uncited){assert.equal(e.evidence,'일반 지식 기반 · 외부 출처 미첨부');assert.equal(e.checkedAt,'');assert.match(e.writtenAt,/^\d{4}-\d{2}-\d{2}$/);assert.equal(e.historical,false);}
 for(const e of D.entries.filter(e=>e.sources.length)){assert(e.checkedAt);assert(!e.evidence.includes('미첨부'));}
});
test('추가한 상황 검색과 공유 작업도 학습 풀에서 조회',()=>{
 for(const [q,f,t] of [['영상 짧게 잘라 나누는','marketing','썰다'],['광고 영상 색보정 공정','marketing','D.I'],['원단 옷에 무늬 인쇄','fashion','나염'],['실서비스 전 검증 환경','dev','스테이징'],['종이 뜯는 점선 가공','design','미싱']])assert.equal(find(q,{field:f})[0].term,t,q);
 for(const f of ['marketing','film','design']){
  const e=find('썬다',{field:f})[0];assert.equal(e.term,'썰다');assert(C.shuffle(D.entries.filter(x=>x.field===f)).some(x=>x.id===e.id));
 }
});

test('패션의 2D·3D는 광고 후반이 아닌 패턴·가상 의상 뜻',()=>{
 const two=find('2D',{field:'fashion'})[0],three=find('3D',{field:'fashion'})[0];
 assert.match(two.definition,/패턴/);assert.match(three.definition,/의상/);
 assert.equal(two.category,'디지털 패션·패턴');assert.equal(three.category,'디지털 패션·패턴');
 assert.equal(two.aliases.includes('2D팀'),false);assert.equal(three.aliases.includes('3D팀'),false);
 assert.notEqual(three.definition,find('3D',{field:'marketing'})[0].definition);
 assert.equal(find('가상 착장',{field:'fashion'})[0].id,three.id);
 assert(C.score(two,'광고 후반 투디 작업')<2000);
 assert(!two.phrases.includes('광고 후반 투디 작업'));
 assert(two.sources.includes('field-clo-modes'));assert(!two.sources.includes('detail-2d'));
 const layer=find('레이어',{field:'fashion'})[0];assert.match(layer.definition,/의상/);assert.equal(layer.category,'디지털 패션·패턴');
});
test('전문 공정을 다른 업계로 복제하지 않고 관련 실무는 유지',()=>{
 const fashion=D.entries.filter(e=>e.field==='fashion');
 for(const term of ['D.I','녹음','썰다','썰어 넣다','덕션','기획실','조감독','연출부','ISO','마스크','아웃라인','MVP'])assert(!fashion.some(e=>e.term===term),term);
 for(const term of ['키비주얼','브랜드 매니저','ROAS','시딩','MD','테크팩','촬영','헤메','제품 컷','패터너','제직'])assert(fashion.some(e=>e.term===term),term);
 assert.equal(find('썬다',{field:'fashion'}).length,0);
 assert.equal(find('D.I',{field:'fashion'}).length,0);
 for(const term of ['D.I','컨폼','생산관리팀','물류팀'])assert(!D.entries.some(e=>e.field==='design'&&e.term===term),term);
 for(const term of ['D.I','녹음','썰다','조감독'])assert(find(term,{field:'film'}).some(e=>e.term===term),term);
});
test('분류가 이동된 단어의 저장·학습 기록은 원래 의미로 이어짐',()=>{
 assert(Object.keys(D.redirects).length>0);
 for(const [old,target] of Object.entries(D.redirects)){
  assert(!D.entries.some(e=>e.id===old));assert(D.entries.some(e=>e.id===target));
  const s=C.validateState({saved:[old,target],review:{[old]:'again',[target]:'known'},fields:['fashion'],onboarded:true},D.entries,D.fields,D.redirects);
  assert.deepEqual(s.saved,[target]);assert.deepEqual(s.review,{[target]:'again'});assert.deepEqual(s.fields,['fashion']);
  assert.deepEqual(C.validateState(s,D.entries,D.fields,D.redirects),s);
 }
});

test('패션 PT 오분류를 방지하고 검토한 공통 개념은 분야별 예문으로 제공',()=>{
 for(const f of ['fashion','dev','design']){
  assert.equal(find('PT',{field:f}).length,0,f);
  for(const term of ['결재','인사팀','팀장','법카','견적서'])assert(!D.entries.some(e=>e.field===f&&e.term===term),f+':'+term);
 }
 assert.equal(find('PT',{field:'common'})[0].term,'PT');
 assert.match(find('PT',{field:'marketing'})[0].definition,/광고주/);
 assert.notEqual(find('PT',{field:'common'})[0].definition,find('PT',{field:'marketing'})[0].definition);
 const common=new Map(D.entries.filter(e=>e.field==='common').map(e=>[e.term,e.definition]));
 for(const e of D.entries.filter(e=>e.field!=='common'&&e.definition===common.get(e.term))){const shared=D.entries.find(x=>x.field==='common'&&x.term===e.term);assert.equal(e.meaningKey,shared.meaningKey);assert.notEqual(e.example,shared.example);}
 const old='fashion-021',target=D.entries.find(e=>e.field==='common'&&e.term==='PT').id;
 assert.equal(D.redirects[old],target);
 assert.deepEqual(C.validateState({saved:[old]},D.entries,D.fields,D.redirects).saved,[target]);
});

test('첨부 후보의 새 단어와 별칭을 적절한 분야에서 검색',()=>{
 for(const [field,q,term] of [
  ['marketing','embargo','엠바고'],['marketing','GA4','GA4'],['dev','테스트 주도 개발','TDD'],
  ['fashion','머서라이징','실켓 가공'],['fashion','DTG','DTG'],['film','NG','NG'],
  ['film','핸들 프레임','핸들'],['film','프로레스','ProRes'],['design','리거처','합자'],
  ['design','폰트 깨기','아웃라인'],['common','비밀유지계약','NDA'],['common','인도물','산출물']
 ])assert.equal(find(q,{field})[0]?.term,term,field+':'+q);
});
test('GTM의 두 개념과 공통·전문 분야의 범위 유지',()=>{
 const gtm=find('GTM',{field:'marketing'});
 assert.deepEqual(new Set(gtm.map(e=>e.term)),new Set(['GTM','구글 태그 매니저']));
 assert.notEqual(gtm[0].definition,gtm[1].definition);
 for(const term of ['NDA','TBD','TBA','맨먼스']){
  assert.deepEqual(D.entries.filter(e=>e.term===term).map(e=>e.field),['common']);
 }
 for(const term of ['JWT','ProRes','핸들','픽처 락','디에서'])assert(!D.entries.some(e=>e.field==='fashion'&&e.term===term));
 for(const term of ['GUI','마이크로인터랙션'])assert.deepEqual(new Set(D.entries.filter(e=>e.term===term).map(e=>e.field)),new Set(['dev','design']));
 assert.notEqual(find('커버리지',{field:'film'})[0].definition,find('커버리지',{field:'dev'})[0].definition);
});
test('원문의 잘못된 풀이 대신 검토한 개념과 주의점을 제공',()=>{
 const entry=(f,t)=>D.entries.find(e=>e.field===f&&e.term===t);
 assert.equal(entry('marketing','PPL').english,'Product placement');
 assert.match(entry('dev','JWT').note,/인코딩은 암호화가 아닙니다/);
 assert.match(entry('dev','OAuth 2.0').definition,/인가/);
 assert.match(entry('film','ProRes').definition,/압축/);assert(!entry('film','ProRes').definition.includes('비압축'));
 assert.match(entry('film','CBR').note,/같은 파일 크기/);
 assert.match(entry('fashion','승화 전사').definition,/염료/);
 assert.match(entry('design','리치 블랙').note,/고정된 만능.*없습니다/);
 assert.match(entry('marketing','반송률').definition,/참여 세션/);
});
test('과장·비하·통용 근거 부족 후보는 표제어·별칭으로 등록하지 않음',()=>{
 const names=new Set(D.entries.flatMap(e=>[e.term,...e.aliases]).map(C.normalize));
 for(const name of ['NGE','광까','렌더링 옥쇄','기획자 뚝배기','치찰음 날상','자리 차개','도메키','피그마 잼','통기사','외드','역역직구'])assert(!names.has(C.normalize(name)),name);
});
test('주제는 필터에 표시할 수 있는 문자열이고 추가 뜻은 작성 근거를 구분',()=>{
 for(const e of D.entries)assert.equal(typeof(e.category||''),'string',e.id);
 assert.equal(D.entries.find(e=>e.field==='marketing'&&e.term==='PT').category,'대행사 제안');
 for(const [f,t,source] of [['marketing','엠바고',true],['dev','JWT',true],['fashion','실켓 가공',true],['common','TBD',false]]){
  const e=D.entries.find(e=>e.field===f&&e.term===t);
  assert.equal(Boolean(e.sources.length),source);
  assert.equal(e.checkedAt||e.writtenAt,'2026-09-16');
 }
});

test('네 번째 후보 목록의 새 개념과 활용 표기를 검색',()=>{
 for(const [field,q,term] of [['common','어라인','얼라인'],['fashion','덴타','텐타'],['fashion','시보리','립'],['fashion','공임','공임'],['fashion','SPI','땀수'],['dev','더미 데이터','더미 데이터'],['dev','OOM','OOM'],['design','파비콘','파비콘'],['film','타임코드','타임코드'],['marketing','GFA','GFA']])assert.equal(find(q,{field})[0]?.term,term,q);
 assert.notEqual(find('더미',{field:'dev'})[0].id,find('더미 데이터',{field:'dev'})[0].id);
 assert(find('트래킹',{field:'film'}).some(e=>e.term==='트래킹'));
 assert(find('트래킹',{field:'film'}).some(e=>e.term==='모션 트래킹'));
 assert.match(find('main',{field:'dev'})[0].note,/보장하지 않습니다/);
});
test('제출 문장의 잘못된 동의어·원인 단정을 옮기지 않음',()=>{
 const get=(f,t)=>D.entries.find(e=>e.field===f&&e.term===t);
 assert(!get('fashion','패터너').aliases.includes('오야지'));
 assert(!get('fashion','시침질').aliases.includes('시치미'));
 assert.match(get('film','클린본').definition,/납품 조건/);
 assert.match(get('film','RAW').note,/같은 파일 종류로 합치지/);
 assert.match(get('dev','OOM').note,/항상.*종료인 것은 아닙니다/);
 assert.match(get('fashion','땀수').note,/무조건 좋은 봉제는 아닙니다/);
 assert.match(get('dev','레거시').note,/잘못된 코드라는 뜻은 아닙니다/);
 assert.equal(get('marketing','PPL').english,'Product placement');
});

test('광고 키카피와 띄어쓰기 별칭은 키메시지와 구분해 검색',()=>{
 for(const q of ['키카피','키 카피','메인카피']) assert.equal(find(q,{field:'marketing'})[0]?.term,'키카피');
 const e=find('키카피',{field:'marketing'})[0];assert.match(e.definition,/중심 문구/);assert(e.sources.length);
 assert.notEqual(e.id,find('키메시지',{field:'marketing'})[0].id);
});
test('동형어는 해당 분야의 뜻·예문·검색 문장·메모로 연결',()=>{
 const cases=[
  ['dev','레이어',/논리적 계층/,/비즈니스 레이어/,/프로그램/],
  ['design','레이어',/편집/,/레이어/,/레이어|이미지|겹/],
  ['fashion','레이어',/의상/,/셔츠/,/의상|옷/],
  ['dev','컴포넌트',/소프트웨어/,/속성/,/코드|구현/],
  ['design','컴포넌트',/디자인/,/인스턴스/,/디자인/],
  ['marketing','노출',/광고/,/광고/,/광고/],
  ['film','노출',/빛/,/창밖/,/밝기|빛/],
  ['design','프레임',/작업 영역/,/모바일/,/디자인/],
  ['film','프레임',/정지 화면/,/프레임/,/영상|프레임/],
  ['design','편집',/페이지/,/카탈로그/,/지면|페이지/],
  ['film','편집',/촬영본/,/인터뷰/,/영상/],
 ];
 for(const [field,term,def,example,phrase] of cases){
  const e=D.entries.find(e=>e.field===field&&e.term===term);assert(e,field+term);
  assert.match(e.definition,def);assert.match(e.example,example);assert.match(e.phrases.join(' '),phrase);
  assert.equal(find(term,{field})[0].id,e.id);
 }
 assert.equal(find('프로그램 책임별 계층 분리',{field:'dev'})[0].term,'레이어');
 assert.equal(find('상품 사진 색보정',{field:'fashion'})[0].term,'색보정');
 assert.equal(find('심지 떴다',{field:'fashion'})[0].term,'심지 들뜸');
 assert(!find('뜬다',{field:'fashion'})[0].aliases.some(a=>a.includes('심지')));
});
test('분야가 다른 주석을 표제어만으로 덮어쓰지 않음',()=>{
 const entry=(field,term)=>D.entries.find(e=>e.field===field&&e.term===term);
 assert.match(entry('fashion','미싱').note,/봉제의 재봉틀/);
 assert(!entry('fashion','미싱').note.startsWith('이 항목은 인쇄'));
 assert.match(entry('dev','프록시').note,/IT의 요청/);
 assert(!entry('dev','프록시').note.startsWith('영상 편집의'));
 assert.match(entry('dev','레이어').sources.join(),/audit-layers/);
 assert(!entry('dev','레이어').phrases.join().includes('이미지'));
 assert(!entry('marketing','노출').aliases.includes('익스포저'));
});
test('같은 개념의 예문도 실제 분야 업무에 맞춰 작성',()=>{
 for(const [term,contexts] of [
  ['키비주얼',{marketing:/캠페인/,fashion:/룩북|컬렉션/,design:/포스터/,film:/영상/}],
  ['프록시',{dev:/요청/,film:/편집/,design:/합성/}],
  ['QC',{fashion:/봉제|치수/,design:/인쇄|재단/}],
  ['UTM',{marketing:/링크/,fashion:/룩북/,dev:/리디렉션/}],
  ['색보정',{fashion:/셔츠|실물/,film:/카메라/}],
 ])for(const [field,pattern] of Object.entries(contexts)){
  const e=D.entries.find(e=>e.field===field&&e.term===term);assert.match(e.example,pattern,field+':'+term);
 }
 const fashionChurn=D.entries.find(e=>e.field==='fashion'&&e.term==='이탈률');
 assert.match(fashionChurn.definition,/재구매/);assert(!fashionChurn.aliases.includes('구독 이탈'));
});
test('범용 제안·협업 의미는 공통으로 이동하고 기존 링크 보존',()=>{
 for(const term of ['RFP','제안서','컨센서스','피저빌리티','얼터안']){
  const e=find(term)[0];assert.equal(e.field,'common');
  assert.equal(D.entries.filter(e=>e.term===term).length,1);
  assert(Object.values(D.redirects).includes(e.id));
 }
 for(const [field,terms] of Object.entries({dev:['자사몰'],design:['미디어 플래너','홍보팀','매체팀'],film:['매체팀','미디어 플래너'],fashion:['DAU','MAU']})){
  for(const term of terms)assert(!D.entries.some(e=>e.field===field&&e.term===term),field+term);
 }
 for(const field of ['marketing','film'])for(const term of ['PD','D.I','녹음','2D'])assert(D.entries.some(e=>e.field===field&&e.term===term));
 for(const term of ['ROAS','키비주얼','시딩','촬영','색보정'])assert(D.entries.some(e=>e.field==='fashion'&&e.term===term));
});
test('검토 기록은 모든 항목을 포함하고 내용·분야 변경을 탐지',()=>{
 const crypto=require('node:crypto'),ledger=require('../data/reviewed-meanings.json');
 const signature=e=>crypto.createHash('sha256').update(JSON.stringify(ledger.contentKeys.map(k=>e[k]??null))).digest('hex');
 const approved=new Map(ledger.entries.map(e=>[e.id,e.signature]));
 assert.equal(approved.size,D.entries.length);
 for(const e of D.entries)assert.equal(signature(e),approved.get(e.id),'재검토 필요: '+e.field+' '+e.term);
 const layer=D.entries.find(e=>e.field==='dev'&&e.term==='레이어');
 for(const change of [{definition:'이미지 편집의 층'},{example:'텍스트와 배경 레이어를 분리해요.'},{field:'fashion'}])assert.notEqual(signature({...layer,...change}),approved.get(layer.id));
 for(const row of ledger.redirected)assert.equal(D.redirects[row.id],row.target);
});

test('회의 표현은 여섯 분야에 개별 작성한 뜻과 예문으로 수록',()=>{
 const ledger=require('../data/reviewed-meanings.json');
 const rows=ledger.entries.filter(e=>e.reviewBatch==='meeting-2026-09-16');
 assert.equal(rows.length,178);
 const counts={marketing:26,dev:24,fashion:28,design:26,film:30,common:44};
 for(const [field,count] of Object.entries(counts))assert.equal(rows.filter(e=>e.field===field).length,count);
 const newEntries=rows.map(row=>D.entries.find(e=>e.id===row.id));
 assert.equal(new Set(newEntries.map(e=>e.example)).size,newEntries.length);
 for(const e of newEntries){
  assert.equal(find(e.term,{field:e.field})[0]?.id,e.id,e.field+':'+e.term);
  assert(C.shuffle(D.entries.filter(x=>x.field===e.field)).some(x=>x.id===e.id));
  if(!e.sources.length){assert.equal(e.checkedAt,'');assert.match(e.evidence,/일반 지식/);}
 }
});
test('논리와 앞단·뒷단을 분야별 설명과 예문으로 구별',()=>{
 const lookup=(field,term)=>D.entries.find(e=>e.field===field&&e.term===term);
 for(const term of ['앞단','뒷단']){
  const rows=['marketing','dev','film'].map(field=>lookup(field,term));
  assert.equal(new Set(rows.map(e=>e.definition)).size,3);
  assert.equal(new Set(rows.map(e=>e.example)).size,3);
  assert.match(rows[0].definition,/기획서/);assert.match(rows[1].definition,/요청|데이터/);assert.match(rows[2].definition,/영상|편집/);
  assert.match(rows[1].note,/항상.*같은 말로 보지/);
  for(const e of rows)assert.equal(find(term,{fields:[e.field]})[0].id,e.id);
 }
 assert.equal(find('논리',{field:'marketing'})[0].term,'논리');
 assert.equal(find('논리',{field:'dev'})[0].term,'로직');
 assert.equal(find('논리',{field:'design'})[0].term,'디자인 의도');
 assert.equal(find('앞 단',{field:'marketing'})[0].term,'앞단');
 assert.equal(find('뒤단',{field:'dev'})[0].term,'뒷단');
 assert.equal(find('콘셉트 전 배경과 문제 정리',{field:'marketing'})[0].term,'앞단');
});
test('회의 약자와 현장 표현의 다른 개념을 자동으로 합치지 않음',()=>{
 const rtbs=find('RTB',{field:'marketing'});
 assert.deepEqual(new Set(rtbs.map(e=>e.term)),new Set(['RTB','리즌 투 빌리브']));
 assert.match(rtbs.find(e=>e.term==='리즌 투 빌리브').note,/Real-time bidding/);
 const ppms=find('PPM',{field:'fashion'});
 assert(ppms.some(e=>e.term==='생산 전 미팅'));
 assert(ppms.some(e=>e.term==='PPM'));
 assert.notEqual(ppms[0].definition,ppms[1].definition);
 assert.equal(find('드롭',{field:'fashion'})[0].term,'드롭 출시');
 assert.equal(find('드롭',{field:'common'})[0].term,'드롭');
 assert.equal(find('세이프티 테이크',{field:'film'})[0].term,'백업 촬영');
 assert.equal(find('물량 배분',{field:'fashion'})[0].term,'배분');
 assert.equal(find('회의 안건',{field:'common'})[0].term,'어젠다');
 assert.equal(find('시안 리뷰',{field:'design'})[0].term,'시안');
});
