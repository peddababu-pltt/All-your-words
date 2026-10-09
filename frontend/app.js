'use strict';
(()=>{
const D=window.WORD_DATA,C=window.WordCore,W=window.WorkspaceCore,KEY='daneoword.v1',root=document.getElementById('app');
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const icon=n=>`<svg class="icon" aria-hidden="true"><use href="#i-${n}"/></svg>`;
const field=id=>D.fields.find(f=>f.id===id);const word=id=>D.entries.find(e=>e.id===(D.redirects?.[id]||id));
const brand=(mobile=false)=>`<a class="brand ${mobile?'mobile-brand':''}" href="#/" aria-label="다, 너의 단어 홈"><span class="wordmark"><span class="brand-color">다, 너</span><span class="brand-particle">의</span> <span class="brand-color">단어</span></span></a>`;
let state,storageOK=true,profileDraft=null,profileStep=0,lastRoute='',visible=40,extractText='',extractScope='work',extractDocument=null;
let activeHighlight=null,popoverTimer=0,pointerFocus=false,suppressHighlightFocus=false;
function validate(raw){return {...C.validateState(raw,D.entries,D.fields,D.redirects),...W.normalize(raw,D.entries,D.fields,D.redirects)};}
function priorities(){return W.priorities(state.profile);}
function scopeEntries(scope='work'){return W.scope(D.entries,scope,state.profile);}
// A URL may occur more than once in history, with a different scroll/list state.
// Key snapshots by history entry, not by URL, and restore after rebuilding rows.
const views=new Map();
const newViewId=()=>crypto.randomUUID();
let activeView=history.state?.daneoView||newViewId(),restoreFrame=0;
history.replaceState({...history.state,daneoView:activeView},'');
history.scrollRestoration='manual';
function rememberView(clicked){
 if(!lastRoute)return;
 const focused=clicked||document.activeElement;
 views.set(activeView,{x:window.scrollX,y:window.scrollY,visible,
  focusHref:root.contains(focused)?focused?.getAttribute('href'):null,
  searchText:root.querySelector('#search-form input')?.value,
  documentScroll:root.querySelector('.annotated-document')?.scrollTop});
}
function navigateHash(hash,clicked){
 if(hash===location.hash){render();return;}
 rememberView(clicked);
 const parent={id:activeView,hash:location.hash||'#/'};
 activeView=newViewId();
 history.pushState({daneoView:activeView,daneoParent:parent},'',hash);
 render(null,true);
}
function historyChanged(){
 if(location.hash==='#main'){document.getElementById('main')?.focus();return;}
 const nextId=history.state?.daneoView;
 const {path,params}=route();
 if(nextId===activeView&&lastRoute===path+'?'+params)return;
 rememberView();
 activeView=nextId||newViewId();
 if(!nextId)history.replaceState({...history.state,daneoView:activeView},'');
 render(views.get(activeView),true);
}
try{state=validate(JSON.parse(localStorage.getItem(KEY)));}catch{state=validate(null);storageOK=false;}
function persist(){try{localStorage.setItem(KEY,JSON.stringify(state));}catch{storageOK=false;toast('현재 브라우저에 저장할 수 없어요. 이번 탭에서만 유지돼요.');}}
let toastTimer;function toast(text){const el=document.getElementById('toast');el.textContent=text;el.classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>el.classList.remove('show'),2600);}
function route(){const raw=location.hash.slice(1)||'/';const [path,query='']=raw.split('?');return {path,params:new URLSearchParams(query)};}
function href(path,params={}){const p=new URLSearchParams(Object.entries(params).filter(([,v])=>v));return '#'+path+(p.size?'?'+p.toString():'');}
function goto(path,params){navigateHash(href(path,params));}
const link=(text,url,cls='small-link',sym='arrow')=>`<a class="${cls}" href="${esc(url)}">${esc(text)}${sym?icon(sym):''}</a>`;
function detailBack(e){const parent=history.state?.daneoParent;return parent&&views.has(parent.id)?link('뒤로 가기',parent.hash,'small-link','left'):link('단어 찾기로',href('/search',{field:e.field}),'small-link','left');}
function saveButton(e){const on=state.saved.includes(e.id);return `<button class="bookmark ${on?'is-saved':''}" data-save="${e.id}" aria-pressed="${on}" aria-label="${esc(e.term)} ${on?'저장 취소':'저장'}">${icon('bookmark')}</button>`;}
const tag=e=>`<span class="tag">${field(e.field).name}${state.fields.includes(e.field)?' · 내 분야':''}</span>`;
function shell(content,title,navKey='찾기'){const nav=[['찾기','/','search'],['업무 도구','/tools','folder'],['내 단어장','/saved','bookmark']].map(([name,url,sym])=>`<a class="nav-link ${navKey===name?'active':''}" ${navKey===name?'aria-current="page"':''} href="#${url}">${icon(sym)}<span>${name}</span></a>`).join('');const current=state.fields.length?field(state.fields[0]).name+(state.fields.length>1?` +${state.fields.length-1}`:''):'모든 분야';
return `<a class="skip-link" href="#main">본문으로 바로가기</a><aside class="sidebar">${brand()}<div class="sidebar-caption">일하는 사람의 언어 사전</div><nav class="nav" aria-label="주요 메뉴">${nav}</nav><div class="sidebar-bottom"><a class="sidebar-settings" href="#/settings">${icon('sliders')}나의 맞춤 설정</a><a class="sidebar-settings secondary-setting" href="#/about">자료와 백업</a></div></aside><div class="workspace"><header class="topbar"><div class="topbar-title">${title}</div>${brand(true)}<a class="current-context" href="#/settings" aria-label="맞춤 설정 · ${current}"><span class="dot"></span>${current}${icon('down')}</a></header><main id="main" tabindex="-1">${content}</main><footer class="footer"><span>단어 하나로, 조금 더 넓은 세계.</span><a href="#/about">${D.entries.length.toLocaleString()}개 뜻 · 자료와 백업</a></footer></div><nav class="mobile-nav" aria-label="모바일 주요 메뉴">${nav}</nav>`;}
let suggestions=[],suggestionIndex=-1,searchComposing=false;
function searchBox(q=''){return `<form class="search-box" id="search-form" role="search">${icon('search')}<input type="search" name="q" value="${esc(q)}" maxlength="200" aria-label="단어 또는 궁금한 상황 검색" placeholder="단어를 찾거나, 궁금한 상황을 적어보세요" autocomplete="off" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="search-suggestions"><button class="search-submit" aria-label="검색">${icon('arrow')}</button><div class="search-suggestion-panel" hidden><div class="suggestion-heading">이 단어를 찾으세요?</div><ul id="search-suggestions" role="listbox" aria-label="예상 검색어"></ul><div class="suggestion-hint">↑ ↓ 선택 <span>Enter 검색</span></div></div><span class="visually-hidden suggestion-status" role="status" aria-live="polite"></span></form>`;}
function closeSuggestions(){
 suggestions=[];suggestionIndex=-1;
 const form=root.querySelector('#search-form');if(!form)return;
 form.querySelector('.search-suggestion-panel').hidden=true;
 const input=form.elements.q;input.setAttribute('aria-expanded','false');input.removeAttribute('aria-activedescendant');
 form.querySelector('.suggestion-status').textContent='';
}
function showSuggestions(){
 const form=root.querySelector('#search-form');if(!form||searchComposing)return;
 const p=route().params,pool=W.situationEntries(scopeEntries(p.get('field')||'work'),p.get('situation')||'');
 suggestions=C.suggest(pool,form.elements.q.value,{fields:priorities(),kind:p.get('kind'),category:p.get('category')});suggestionIndex=-1;
 form.elements.q.removeAttribute('aria-activedescendant');
 const panel=form.querySelector('.search-suggestion-panel');panel.hidden=!suggestions.length;
 form.elements.q.setAttribute('aria-expanded',String(!!suggestions.length));
 form.querySelector('.suggestion-status').textContent=suggestions.length?`${suggestions.length}개 예상 검색어. 아래 방향키로 선택할 수 있어요.`:'';
 form.querySelector('#search-suggestions').innerHTML=suggestions.map((s,i)=>`<li id="suggestion-${i}" role="option" tabindex="-1" aria-selected="false" data-suggestion="${i}"><span class="suggestion-copy"><strong>${esc(s.entry.term)}</strong>${C.normalize(s.matched)!==C.normalize(s.entry.term)?`<small>${esc(s.matched)}</small>`:''}</span><span class="suggestion-field">${esc(field(s.fields[0]).name)}${s.fields.length>1?` 외 ${s.fields.length-1}`:''}</span>${icon('arrow')}</li>`).join('');
 const viewport=window.visualViewport,bottom=viewport?viewport.offsetTop+viewport.height:window.innerHeight;
 panel.style.maxHeight=Math.max(96,Math.min(390,bottom-form.getBoundingClientRect().bottom-14))+'px';
}
function selectSuggestion(index){
 const choice=suggestions[index],form=root.querySelector('#search-form');if(!choice||!form)return;
 form.elements.q.value=choice.entry.term;closeSuggestions();form.requestSubmit();
}
root.addEventListener('compositionstart',ev=>{if(ev.target.matches('#search-form input')){searchComposing=true;closeSuggestions();}});
root.addEventListener('compositionend',ev=>{if(ev.target.matches('#search-form input')){searchComposing=false;showSuggestions();}});
root.addEventListener('focusin',ev=>{if(ev.target.matches('#search-form input'))showSuggestions();});
root.addEventListener('focusout',ev=>{if(ev.target.matches('#search-form input')&&!ev.relatedTarget?.closest('[data-suggestion]'))closeSuggestions();});
root.addEventListener('pointerdown',ev=>{if(ev.target.closest('[data-suggestion]')&&ev.pointerType!=='touch')ev.preventDefault();});
root.addEventListener('keydown',ev=>{
 if(!ev.target.matches('#search-form input')||searchComposing||ev.isComposing||ev.keyCode===229)return;
 if(ev.key==='Escape'){ev.preventDefault();closeSuggestions();return;}
 if(ev.key==='Tab'){closeSuggestions();return;}
 if(ev.key==='ArrowDown'||ev.key==='ArrowUp'){
  if(!suggestions.length)showSuggestions();if(!suggestions.length)return;ev.preventDefault();
  suggestionIndex=ev.key==='ArrowDown'?(suggestionIndex+1)%suggestions.length:(suggestionIndex<=0?suggestions.length-1:suggestionIndex-1);
  root.querySelectorAll('[data-suggestion]').forEach((el,i)=>el.setAttribute('aria-selected',String(i===suggestionIndex)));
  ev.target.setAttribute('aria-activedescendant','suggestion-'+suggestionIndex);
  root.querySelector('#suggestion-'+suggestionIndex)?.scrollIntoView({block:'nearest'});
 }else if(ev.key==='Enter'&&suggestionIndex>=0){ev.preventDefault();selectSuggestion(suggestionIndex);}
});
document.addEventListener('pointerdown',ev=>{if(!ev.target.closest('#search-form'))closeSuggestions();});

function row(e){return `<div class="term-row"><a class="term-open" href="#/word/${e.id}"><span class="term-symbol">${icon(field(e.field).icon)}</span><div class="term-info"><h3>${esc(e.term)}<span>${field(e.field).name}</span></h3><p>${esc(e.definition)}</p><small class="row-meta">${esc(e.category||e.kind)}${e.kind==='현장 표현'?' · 현장 표현':''}</small></div></a>${saveButton(e)}</div>`;}
let homeFeatureTab='daily';
let discoveryKey='',dailyChoice=null,dailySeen=[],contrastChoice=null,contrastSeen=[];
let contrasts=[];
function ensureDiscovery(){
 const now=new Date(),key=[now.getFullYear(),now.getMonth(),now.getDate(),...state.fields].join('|');
 if(discoveryKey===key)return;
 discoveryKey=key;dailyChoice=C.daily(D.entries,state.fields);dailySeen=[C.normalize(dailyChoice.term)];
 contrasts=C.contrastPairs(D.entries,state.fields);
 contrastChoice=C.nextCard(contrasts,null).item;contrastSeen=contrastChoice?[contrastChoice.id]:[];
}
function refreshButton(action,label,disabled=false){return `<button type="button" class="card-refresh" data-action="${action}" aria-label="${label}" title="${label}" ${disabled?'disabled':''}><span>${action==='refresh-daily'?'다른 단어':'다른 예시'}</span>${icon('shuffle')}</button>`;}
function dailyPool(){const pool=D.entries.filter(e=>!state.fields.length||state.fields.includes(e.field));return [...new Map((pool.length?pool:D.entries).map(e=>[C.normalize(e.term),{id:C.normalize(e.term),entry:e}])).values()];}
function dailyCard(){const e=dailyChoice;return `<div class="card-top"><span class="eyebrow">오늘, 하나의 단어</span>${refreshButton('refresh-daily','오늘 하나의 단어 새로고침',dailyPool().length<2)}</div><a class="daily-content" href="#/word/${e.id}"><div class="daily-word"><h2>${esc(e.term)}</h2>${tag(e)}</div><p class="daily-description">${esc(e.definition)}</p><span class="small-link daily-read">뜻과 쓰임 ${icon('arrow')}</span></a>`;}
function contrastCard(){const pair=contrastChoice;return `<div class="card-top"><span class="eyebrow">같은 단어, 다른 의미</span>${refreshButton('refresh-contrast','같은 단어 다른 의미 새로고침',contrasts.length<2)}</div>${pair?`<div class="contrast-inline"><h2>${esc(pair.term)}</h2><div class="meaning-list">${pair.entries.map(e=>`<a class="meaning-row" href="#/word/${e.id}"><div><h3>${field(e.field).name}${icon('arrow')}</h3><p>${esc(e.definition)}</p></div></a>`).join('')}</div></div>`:'<p>새로운 뜻을 준비하고 있어요.</p>'}`;}
function refreshDiscovery(action){
 ensureDiscovery();const isDaily=action==='refresh-daily';
 if(isDaily){const next=C.nextCard(dailyPool(),C.normalize(dailyChoice.term),dailySeen);if(!next.item)return;dailyChoice=next.item.entry;dailySeen=next.seen;}
 else{const next=C.nextCard(contrasts,contrastChoice?.id,contrastSeen);if(!next.item)return;contrastChoice=next.item;contrastSeen=next.seen;}
 const card=root.querySelector(isDaily?'#daily-feature':'#contrast-feature');if(!card)return;
 card.innerHTML=isDaily?dailyCard():contrastCard();
 card.querySelector('.card-refresh')?.focus({preventScroll:true});
 let status=root.querySelector('.discovery-status');if(!status){status=document.createElement('span');status.className='discovery-status';status.setAttribute('role','status');root.querySelector('.home-feature').append(status);}status.textContent=isDaily?`새 단어 · ${dailyChoice.term}`:`다른 분야의 뜻 · ${contrastChoice.term}`;
}
function home(){ensureDiscovery();const recent=state.viewed.map(word).filter(Boolean).slice(0,3);return shell(`<div class="home-dashboard"><section class="hero"><div class="hero-heading"><div><div class="hero-kicker">당신의 일을 이해하는 사전</div><h1>낯선 말도, <em>내 말이 되도록.</em></h1></div><span class="home-index">7개의 세계, ${D.entries.length.toLocaleString()}개의 뜻</span></div>${searchBox()}<div class="home-context"><span>${state.fields.length?'내 업무 분야에서 먼저 찾아요.':'단어, 줄임말, 궁금한 상황을 검색해 보세요.'}</span>${link(state.profile.completed?'내 분야·관심 설정':'내게 맞게 설정하기','#/settings','small-link','sliders')}</div></section><section class="field-section"><div class="section-heading"><h2>어떤 세계가 궁금하세요?</h2>${link('전체 사전',href('/search',{field:'all'}))}</div><div class="industry-grid">${D.fields.map(f=>`<a class="industry ${state.fields.includes(f.id)?'selected':''}" href="${href('/search',{field:f.id})}"><span class="industry-top">${icon(f.icon)}${state.fields.includes(f.id)?'<small>내 업무</small>':state.profile.interestFields.includes(f.id)?'<small>관심</small>':''}</span><strong>${f.name}</strong><small>${D.entries.filter(e=>e.field===f.id).length}개 뜻</small></a>`).join('')}</div></section><section class="home-feature" aria-label="오늘의 발견" data-active="${homeFeatureTab}"><div class="discovery-switch" role="group" aria-label="발견 카드 선택"><button data-action="feature-tab" data-tab="daily" aria-pressed="${homeFeatureTab==='daily'}">오늘의 단어</button><button data-action="feature-tab" data-tab="contrast" aria-pressed="${homeFeatureTab==='contrast'}">다른 분야의 뜻</button></div><article class="daily-card" id="daily-feature">${dailyCard()}</article><article class="discovery-card" id="contrast-feature">${contrastCard()}</article></section><section class="recent-strip"><span>최근 본 단어</span>${recent.length?recent.map(e=>link(e.term+' · '+field(e.field).name,'#/word/'+e.id,'recent-word','')).join(''):'<span class="recent-empty">살펴본 단어를 여기서 다시 만나요.</span>'}${recent.length?link('모두 보기','#/tools?tab=recent','small-link',''):''}</section></div>`,'나의 사전');}
function options(selected,all='모든 분야'){return [['all',all],['work','내 업무 분야'],['interest','궁금한 분야'],...D.fields.map(f=>[f.id,f.name])].map(([v,n])=>`<option value="${v}" ${v===(selected||'all')?'selected':''}>${n}</option>`).join('');}
function filters(p){const scope=p.get('field')||'work',cats=[...new Set(scopeEntries(scope).map(e=>e.category).filter(Boolean))];return `<form class="filters" id="filter-form"><label>분야<select name="field">${options(scope)}</select></label><label>단어 종류<select name="kind"><option value="">모든 단어</option>${['전문 용어','현장 표현'].map(k=>`<option ${p.get('kind')===k?'selected':''}>${k}</option>`).join('')}</select></label><label>주제<select name="category"><option value="">모든 주제</option>${cats.map(c=>`<option ${p.get('category')===c?'selected':''}>${esc(c)}</option>`).join('')}</select></label></form>`;}
function results(p){const q=p.get('q')||'',scope=p.get('field')||'work',situation=p.get('situation')||'',pool=W.situationEntries(scopeEntries(scope),situation),all=C.search(pool,q,{fields:priorities(),kind:p.get('kind'),category:p.get('category')}),situationName=W.PURPOSES.find(x=>x[0]===situation)?.[1];return shell(`<section class="page-heading"><div><div class="eyebrow">필요한 순간, 바로 찾는 말</div><h1>${situationName?esc(situationName)+'에 쓰는 말':'단어를 찾거나, 상황을 적어보세요.'}</h1></div>${situationName?link('상황 조건 해제',href('/search',{field:scope})) :''}</section>${searchBox(q)}${filters(p)}${scope==='work'&&!state.fields.length||scope==='interest'&&!state.profile.interestFields.length?`<p class="inline-note">선택한 분야가 없어 모든 분야를 보여드려요. ${link('분야 설정','#/settings','small-link','')}</p>`:''}<div class="results-heading"><h2>${q?`‘${esc(q)}’`:'전체 단어'} <span>${all.length}개 뜻</span></h2>${q?link('검색어 지우기',href('/search',{field:scope,situation})):''}</div>${all.length?`<div class="results-list">${all.slice(0,visible).map(row).join('')}</div>${all.length>visible?`<button class="secondary-button load-more" data-action="more">더 보기 (${visible} / ${all.length})</button>`:''}`:`<div class="empty-state">${icon('search')}<h2>선택한 조건에 맞는 말이 없어요.</h2><p>다른 분야에 있는 뜻도 찾아보세요.</p>${link('모든 분야에서 찾기',href('/search',{q,field:'all'}),'primary-button')}</div>`}`,'단어 찾기');}
function profileSelect(label,name,items){return `<label>${label}<select name="${name}" aria-label="${label}">${items.map(([v,n])=>`<option value="${v}" ${profileDraft[name]===v?'selected':''}>${n}</option>`).join('')}</select></label>`;}
function settings(isFirst){const p=profileDraft,step=profileStep,work=step===0,selection=work?p.workFields:p.interestFields;return `<div class="welcome-page"><header class="welcome-top">${brand()}${isFirst?'<span>나만의 사전 준비하기</span>':link('돌아가기','#/','small-link','left')}</header><main id="main" class="welcome-main" tabindex="-1"><nav class="profile-steps" aria-label="맞춤 설정 단계">${['내 업무 분야','관심 분야','보기 설정'].map((t,i)=>`<button data-profile-step="${i}" class="${step===i?'active':''}" ${step===i?'aria-current="step"':''}>${String(i+1).padStart(2,'0')} ${t}</button>`).join('')}</nav><div class="profile-heading"><div class="eyebrow">${step<2?'여러 개를 골라도 좋아요':'모두 선택 사항이에요'}</div><h1 tabindex="-1">${step===0?'어떤 세계에서 일하고 있나요?':step===1?'또 어떤 세계가 궁금하세요?':'사전을 보기 편하게.'}</h1><p>${step===0?'선택한 분야를 기본 검색 범위로 설정해요.':step===1?'다른 분야도 따로 모아 빠르게 찾아볼 수 있어요.':'설명을 읽는 순서와 목록의 간격을 정해요.'}</p></div>${step<2?`<div class="profile-fields" role="group" aria-label="${work?'내 업무 분야':'궁금한 분야'}">${D.fields.map(f=>{const own=!work&&p.workFields.includes(f.id);return `<button class="profile-field ${selection.includes(f.id)?'selected':''}" data-profile-field="${f.id}" aria-pressed="${selection.includes(f.id)}" ${own?'disabled':''}>${icon(f.icon)}<strong>${f.name}</strong><small>${own?'내 업무에 포함됨':D.entries.filter(e=>e.field===f.id).length+'개 뜻'}</small><span class="profile-check">${selection.includes(f.id)?icon('check'):icon('plus')}</span></button>`;}).join('')}</div><p class="profile-selection">${selection.length?selection.map(id=>field(id).name).join(' · '):work?'아직 정하지 않았다면 모든 분야로 시작해도 좋아요.':'관심 분야는 나중에 추가해도 좋아요.'}</p>`:`<form id="profile-form" class="profile-form"><div class="profile-selects">${profileSelect('설명 순서','experience',[['new','예문 먼저 보기'],['familiar','뜻 먼저 보기']])}${profileSelect('목록의 간격','density',[['comfortable','여유롭게'],['compact','촘촘하게']])}</div></form>`}<div class="welcome-actions">${step?'<button class="secondary-button" data-action="profile-prev">이전</button>':''}<button class="primary-button" data-action="${step<2?'profile-next':'profile-save'}">${step<2?'다음':isFirst?'내 사전 시작하기':'설정 저장하기'}${icon('arrow')}</button>${isFirst&&step===0?'<button class="small-link plain-button" data-action="skip">먼저 둘러보기</button>':''}</div></main><footer class="welcome-footer">회사명·개인정보 없이, 선택한 내용만 이 브라우저에 저장해요.</footer></div>`;}

function detail(id){const e=word(id);if(!e)return shell(`<div class="empty-state"><h1>단어를 찾을 수 없어요.</h1>${link('전체 단어 보기','#/search')}</div>`,'단어 찾기');if(state.viewed[0]!==e.id){state.viewed=[e.id,...state.viewed.filter(x=>x!==e.id)].slice(0,20);persist();}const other=D.entries.filter(x=>x.field!==e.field&&C.names(x).some(n=>C.names(e).includes(n)));const related=D.entries.filter(x=>x.id!==e.id&&x.field===e.field&&(e.category?x.category===e.category:x.sources.some(s=>e.sources.includes(s)))).slice(0,6);return shell(`<div class="back-link">${detailBack(e)}</div><div class="detail-layout"><div><article class="detail-main ${state.profile.experience==='new'?'example-first':''}"><div class="card-top">${tag(e)}${saveButton(e)}</div><div class="detail-title"><h1>${esc(e.term)}</h1><span>${esc(e.english)}</span></div><div class="word-labels"><span>${esc(e.category||e.kind)}</span>${e.kind==='현장 표현'?'<span>현장 표현</span>':''}</div><p class="definition">${esc(e.definition)}</p>${e.aliases.length?`<p class="definition-sub">이렇게도 찾아요 · ${e.aliases.map(esc).join(', ')}</p>`:''}<section class="detail-section"><h2>현장에서는 이렇게 말해요</h2><div class="example">“${esc(e.example)}”<small>쓰임을 설명하기 위해 직접 작성한 예시</small></div></section>${e.note?`<div class="usage-note">${icon('book')}<p>${esc(e.note)}</p></div>`:''}<section class="detail-section"><h2>함께 알아두면 좋은 말</h2><div class="related-tags">${related.map(x=>link(x.term,'#/word/'+x.id,'tag-link','')).join('')}</div></section><details class="sources"><summary>${e.sources.length?`뜻을 확인한 자료 · ${e.sources.length}곳`:'뜻 작성 안내'}</summary><p>${esc(e.evidence)} · ${esc(e.checkedAt||e.writtenAt||D.updatedAt)}<br>${!e.sources.length?'일반 지식을 바탕으로 뜻과 예문을 직접 작성했어요. 별도로 확인한 외부 출처는 첨부하지 않았어요.':e.historical?'과거 문헌에 기록된 표현을 포함합니다. 현장마다 쓰임이 다를 수 있어요.':'공개 자료를 바탕으로 뜻을 짧게 다시 썼어요.'}</p>${e.sources.map(id=>{const s=D.sources[id];return `<a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">${esc(s.publisher)} · ${esc(s.title)}${s.published?` (${esc(s.published)})`:''}${icon('arrow')}</a>`;}).join('')}</details></article>${noteEditor(e)}<div class="word-bottom"><button class="primary-button" data-save="${e.id}">${icon('bookmark')}<span>${state.saved.includes(e.id)?'내 단어장에서 빼기':'내 단어장에 담기'}</span></button><button class="secondary-button" data-action="copy-word" data-id="${e.id}">뜻 복사</button><button class="secondary-button" data-action="compare-add" data-id="${e.id}">${state.compare.includes(e.id)?'비교에서 빼기':'뜻 비교에 담기'}</button></div></div><aside class="detail-aside"><div class="eyebrow">다른 분야의 쓰임</div><h2>${other.length?'다른 분야에서는<br>이렇게 쓰여요.':'이 분야의 말,<br>조금 더 알아볼까요?'}</h2>${other.length?other.map(x=>`<a class="other-meaning" href="#/word/${x.id}">${tag(x)}<p>${esc(x.definition)}</p></a>`).join(''):`<p class="aside-note">${field(e.field).name}에서 쓰이는 ${D.entries.filter(x=>x.field===e.field).length}개의 뜻을 모았어요.</p>${link('분야 둘러보기',href('/search',{field:e.field}))}`}<p class="aside-note">같은 표현도 팀과 상황에 따라 다르게 쓰일 수 있어요.</p></aside></div>`,'단어 읽기');}
function noteEditor(e){const n=state.notes[e.id]||{};const collections=[...new Set(Object.values(state.notes).map(n=>n.collection).filter(Boolean))];return `<form class="note-editor" id="note-form" data-id="${e.id}"><div class="section-heading"><h2>나의 메모</h2><span>나만 볼 수 있어요</span></div><textarea name="note" maxlength="2000" rows="3" aria-label="${esc(e.term)} 개인 메모" placeholder="우리 팀에서 쓰는 뜻, 회의에서 들었던 맥락을 남겨보세요.">${esc(n.text||'')}</textarea><div class="note-actions"><label>업무별 모음<input name="collection" list="collections" maxlength="40" value="${esc(n.collection||'')}" placeholder="예: 신규 캠페인, 월말 결산"></label><datalist id="collections">${collections.map(n=>`<option value="${esc(n)}"></option>`).join('')}</datalist><button class="primary-button" type="submit">메모 저장</button></div></form>`;}
function saved(p){const f=p.get('field')||'',collection=p.get('collection')||'',q=p.get('q')||'';const all=state.saved.map(word).filter(Boolean).reverse(),list=all.filter(e=>(!f||e.field===f)&&(!collection||state.notes[e.id]?.collection===collection)&&(!q||C.normalize(e.term+' '+e.definition+' '+(state.notes[e.id]?.text||'')).includes(C.normalize(q))));const collections=[...new Set(all.map(e=>state.notes[e.id]?.collection).filter(Boolean))];return shell(`<section class="page-heading"><div><div class="eyebrow">내 업무에 남겨 둔 말</div><h1>나의 단어장</h1><p>${all.length}개의 뜻과 나만의 메모.</p></div>${all.length?'<button class="secondary-button" data-action="export-csv">표로 내보내기</button>':''}</section><form id="saved-filter" class="saved-filter"><label>단어·메모 검색<input name="q" value="${esc(q)}" placeholder="내 단어장 검색"></label><label>분야<select name="field"><option value="">모든 분야</option>${D.fields.map(x=>`<option value="${x.id}" ${f===x.id?'selected':''}>${x.name}</option>`).join('')}</select></label><label>업무별 모음<select name="collection"><option value="">모든 모음</option>${collections.map(n=>`<option ${collection===n?'selected':''}>${esc(n)}</option>`).join('')}</select></label><button class="primary-button">찾기</button></form>${list.length?`<div class="results-list saved-list">${list.map(e=>`<div>${row(e)}${state.notes[e.id]?.text?`<a class="saved-note" href="#/word/${e.id}">${icon('pencil')}<span>${esc(state.notes[e.id].text)}</span></a>`:''}${state.notes[e.id]?.collection?`<span class="collection-label">${esc(state.notes[e.id].collection)}</span>`:''}</div>`).join('')}</div>`:`<div class="empty-state">${icon('bookmark')}<h2>${all.length?'조건에 맞는 단어가 없어요.':'다시 만나고 싶은 말을 담아보세요.'}</h2><p>단어를 저장하고, 업무별 모음과 메모를 남길 수 있어요.</p>${link('단어 찾으러 가기','#/search','primary-button')}</div>`}`,'내 단어장','내 단어장');}
function highlightedDocument(){
 let html='',cursor=0;
 extractDocument.spans.forEach((span,i)=>{const label=extractDocument.text.slice(span.start,span.end);html+=esc(extractDocument.text.slice(cursor,span.start))+`<button type="button" class="word-highlight" data-highlight="${i}" aria-label="${esc(label)} 뜻 보기" aria-haspopup="dialog" aria-controls="term-popover" aria-expanded="false">${esc(label)}</button>`;cursor=span.end;});
 return html+esc(extractDocument.text.slice(cursor));
}
function extractPage(){
 const reading=extractDocument!==null,count=reading?extractDocument.spans.length:0;
 const distinct=reading?new Set(extractDocument.spans.map(s=>s.entries.map(e=>e.id).sort().join('|'))).size:0;
 return `<div class="tool-heading"><div><h1>문서 속 낯선 말을 한 번에.</h1><p>회의록·메일을 붙여 넣고, 낯선 단어 위에서 뜻을 확인하세요.</p></div></div><form id="extract-form">${reading?`<div class="document-toolbar"><span id="extraction-results" role="status">${count?`<strong>${distinct}개 표현</strong> · ${count}곳에 표시했어요`:'표시할 용어를 찾지 못했어요'}</span><div><button type="button" class="small-link plain-button" data-action="edit-extract">원문 수정</button><button type="button" class="small-link plain-button" data-action="clear-extract">지우기</button></div></div><div class="annotated-document" aria-label="용어가 표시된 원문" tabindex="0">${highlightedDocument()}</div><p class="highlight-hint">${count?'표시된 단어에 마우스를 올리거나 눌러보세요.':'찾을 분야를 바꾸거나 원문을 수정해 보세요.'}</p>`:`<label class="visually-hidden" for="extract-text">용어를 찾을 문서</label><textarea id="extract-text" name="text" maxlength="20000" placeholder="예: 키카피와 키비주얼의 톤앤매너를 맞추고, 내일 PT 전에 시안을 디벨롭해 주세요." required>${esc(extractText)}</textarea>`}<div class="extract-actions"><label>찾을 분야<select name="scope">${options(extractScope)}</select></label><span>입력한 문서는 저장·전송하지 않아요.</span><button class="primary-button">${reading?'다시 찾기':'용어 찾기'}${icon('search')}</button></div></form>${reading?'':`<div class="tool-hint">${icon('book')}<div><strong>원문을 읽으며, 필요한 뜻만.</strong><p>수록된 단어와 별칭을 형광펜으로 표시해요. 여러 뜻이 있으면 분야와 예문을 함께 확인하세요.</p></div></div>`}<div id="term-popover" class="term-popover" role="dialog" aria-label="용어 뜻" hidden></div>`;
}
function closeTermPopover(returnFocus=false){
 clearTimeout(popoverTimer);const trigger=activeHighlight,panel=root.querySelector('#term-popover');activeHighlight=null;
 trigger?.setAttribute('aria-expanded','false');if(panel)panel.hidden=true;
 if(returnFocus&&trigger?.isConnected){suppressHighlightFocus=true;trigger.focus({preventScroll:true});suppressHighlightFocus=false;}
}
function openTermPopover(trigger){
 clearTimeout(popoverTimer);if(activeHighlight===trigger)return;
 const span=extractDocument?.spans[Number(trigger.dataset.highlight)],panel=root.querySelector('#term-popover');if(!span||!panel)return;
 closeTermPopover();activeHighlight=trigger;trigger.setAttribute('aria-expanded','true');
 const entries=C.search(span.entries,'',{fields:priorities()});
 panel.innerHTML=`<div class="popover-heading"><span>${entries.length>1?entries.length+'개의 뜻':'문서 속 용어'}</span><button type="button" class="small-link plain-button" data-action="close-term">닫기</button></div>${entries.map(e=>`<article class="popover-meaning"><div class="popover-term"><h2>${esc(e.term)}</h2>${tag(e)}</div><p>${esc(e.definition)}</p>${e.example?`<blockquote>${esc(e.example)}</blockquote>`:''}${link('사전에서 자세히 보기','#/word/'+e.id,'small-link')}</article>`).join('')}`;
 panel.hidden=false;panel.scrollTop=0;
 const rect=trigger.getBoundingClientRect(),v=window.visualViewport,left=v?.offsetLeft||0,top=v?.offsetTop||0,vw=v?.width||innerWidth,vh=v?.height||innerHeight;
 panel.style.maxHeight=Math.max(80,Math.min(360,vh-24))+'px';panel.style.width=Math.min(360,vw-24)+'px';
 const h=panel.offsetHeight,w=panel.offsetWidth;
 panel.style.left=Math.max(left+12,Math.min(rect.left,left+vw-w-12))+'px';
 const below=rect.bottom+8;
 panel.style.top=Math.max(top+12,Math.min(below+h<=top+vh-12?below:rect.top-h-8,top+vh-h-12))+'px';
}
function scheduleTermClose(){clearTimeout(popoverTimer);popoverTimer=setTimeout(()=>closeTermPopover(),160);}
root.addEventListener('pointerover',ev=>{
 if(ev.pointerType==='touch')return;
 const trigger=ev.target.closest('[data-highlight]');
 if(trigger&&!trigger.contains(ev.relatedTarget))openTermPopover(trigger);
 else if(ev.target.closest('#term-popover'))clearTimeout(popoverTimer);
});
root.addEventListener('pointerout',ev=>{
 if(ev.pointerType==='touch')return;
 const area=ev.target.closest('[data-highlight],#term-popover');
 if(area&&!area.contains(ev.relatedTarget))scheduleTermClose();
});
root.addEventListener('focusin',ev=>{
 if(pointerFocus||suppressHighlightFocus)return;
 const trigger=ev.target.closest('[data-highlight]');if(trigger)openTermPopover(trigger);
 else if(ev.target.closest('#term-popover'))clearTimeout(popoverTimer);
});
root.addEventListener('focusout',ev=>{
 if(!activeHighlight)return;
 if(ev.relatedTarget?.closest('[data-highlight],#term-popover'))return;
 scheduleTermClose();
});
document.addEventListener('pointerdown',ev=>{
 pointerFocus=true;
 if(!ev.target.closest('[data-highlight],#term-popover'))closeTermPopover();
});
document.addEventListener('pointerup',()=>{pointerFocus=false;});
document.addEventListener('pointercancel',()=>{pointerFocus=false;});
document.addEventListener('keydown',ev=>{
 pointerFocus=false;
 if(ev.key==='Escape'&&activeHighlight){ev.preventDefault();closeTermPopover(true);}
 if(ev.key==='ArrowDown'&&ev.target===activeHighlight){ev.preventDefault();root.querySelector('#term-popover button')?.focus();}
});
window.addEventListener('resize',()=>closeTermPopover());
window.addEventListener('scroll',ev=>{if(!root.querySelector('#term-popover')?.contains(ev.target))closeTermPopover();},true);
window.visualViewport?.addEventListener('resize',()=>closeTermPopover());

function toolsPage(p){const tab=p.get('tab')||'extract';let body='';if(tab==='recent')body=`<div class="tool-heading"><div><h1>어제 찾은 말, 다시 찾기.</h1><p>최근 본 단어 20개와 최근 검색을 모았어요.</p></div><button class="small-link plain-button" data-action="clear-recent">기록 지우기</button></div><div class="recent-queries">${state.recent.map(q=>link(q,href('/search',{q,field:'all'}),'tag-link','')).join('')}</div>${state.viewed.length?state.viewed.map(word).filter(Boolean).map(row).join(''):'<div class="empty-state"><p>단어를 열어 보면 여기에 기록돼요.</p></div>'}`;
else if(tab==='compare'){const entries=state.compare.map(word).filter(Boolean);body=`<div class="tool-heading"><div><h1>나란히 놓고, 뜻 비교.</h1><p>단어 상세 화면에서 최대 3개의 뜻을 담아 비교하세요.</p></div></div>${entries.length?`<div class="compare-grid">${entries.map(e=>`<article><div class="card-top">${tag(e)}<button class="small-link plain-button" data-action="compare-remove" data-id="${e.id}">빼기</button></div><h2>${link(e.term,'#/word/'+e.id,'compare-term','')}</h2><p>${esc(e.definition)}</p><blockquote>${esc(e.example)}</blockquote>${link('자세히 보기','#/word/'+e.id)}</article>`).join('')}</div>`:`<div class="empty-state">${icon('cards')}<h2>뜻을 함께 보면 차이가 보여요.</h2>${link('비교할 단어 찾기','#/search','primary-button')}</div>`}`;}
else body=extractPage();
return shell(`<div class="tool-tabs tabs">${[['extract','문서 속 용어'],['compare','뜻 비교'+(state.compare.length?' '+state.compare.length:'')],['recent','최근 기록']].map(([id,name])=>link(name,href('/tools',{tab:id}),'tab '+(tab===id?'active':''),'')).join('')}</div><section class="tools-panel">${body}</section>`,'업무 도구','업무 도구');}

function about(){return shell(`<section class="page-heading"><div><div class="eyebrow">나의 기록, 사전의 근거</div><h1>자료와 보관 안내</h1><p>${D.updatedAt} · 7개 분야 · ${D.entries.length.toLocaleString()}개 뜻</p></div></section><section class="about-compact"><div class="backup-panel"><h2>내 기록을 다른 곳에서도.</h2><p>단어장·메모·맞춤 설정은 이 브라우저에 저장돼요.<br>기기를 바꾸기 전에 백업 파일을 내려받으세요.</p><div class="backup-actions"><button class="primary-button" data-action="export">내 기록 백업하기</button><label class="secondary-button file-label">백업 가져오기<input type="file" id="import-file" accept="application/json,.json" aria-label="백업 파일 가져오기"></label></div><small>가져오면 단어장과 메모를 합치고 맞춤 설정을 복원해요. 같은 단어의 기존 메모는 유지해요.</small></div><details class="info-disclosure"><summary>뜻과 예문은 어떻게 만들었나요?</summary><p>공공기관·제작사·소프트웨어 제작사 등의 공개 자료와 일반 지식을 바탕으로 직접 작성했어요. ${D.entries.filter(e=>e.sources.length).length}개 뜻에는 확인한 자료를, 나머지에는 ‘일반 지식 기반’이라는 작성 안내를 표시해요. 외부 전문가의 감수를 뜻하지 않으며, 현장마다 쓰임이 다를 수 있어요.</p></details><details class="info-disclosure"><summary>검색과 문서 도구는 어떻게 작동하나요?</summary><p>등록된 단어·별칭·뜻·검색 문장을 비교해서 찾아요. 문서 도구는 입력한 글에 있는 수록 표현을 찾아주며, 전체 맥락이나 의도를 판단하지 않아요. 입력한 문서는 서버로 보내거나 브라우저 저장소에 보관하지 않아요. 생성형 AI와 외부 API를 사용하지 않아요.</p></details><details class="info-disclosure"><summary>현재 수록 분야 · 7개</summary><div class="coverage">${D.fields.map(f=>link(f.name+' · '+D.entries.filter(e=>e.field===f.id).length+'개 뜻',href('/search',{field:f.id}),'coverage-row')).join('')}</div></details></section>`,'자료와 백업');}
function render(restored=null,navigation=false){closeTermPopover();closeSuggestions();searchComposing=false;let {path,params}=route();if(!state.onboarded&&path!=='/welcome'){location.replace('#/welcome');return;}
const changed=navigation||lastRoute!==path+'?'+params;
const position=restored||(changed?{x:0,y:0}:{x:window.scrollX,y:window.scrollY});
cancelAnimationFrame(restoreFrame);
document.body.classList.toggle('is-welcome',path==='/welcome'||path==='/settings');document.body.classList.toggle('compact-list',state.profile.density==='compact');document.body.classList.toggle('is-home',path==='/');
if(changed){visible=restored?.visible||40;if(path==='/welcome'||path==='/settings'){profileDraft=structuredClone(state.profile);profileStep=0;}}
lastRoute=path+'?'+params;
root.innerHTML=path==='/'?home():path==='/search'?results(params):path==='/welcome'||path==='/settings'?settings(path==='/welcome'):path.startsWith('/word/')?detail(path.slice(6)):path==='/saved'?saved(params):path==='/tools'||path==='/learn'?toolsPage(params):path==='/about'?about():shell(`<div class="empty-state"><h1>페이지를 찾을 수 없어요.</h1>${link('처음으로','#/')}</div>`,'찾기');document.title=(root.querySelector('.topbar-title')?.textContent||'당신의 분야')+' · 다, 너의 단어';if(restored?.searchText!==undefined){const input=root.querySelector('#search-form input');if(input)input.value=restored.searchText;}
if(restored?.documentScroll!==undefined){const documentView=root.querySelector('.annotated-document');if(documentView)documentView.scrollTop=restored.documentScroll;}
if(changed){
 const focus=restored?.focusHref?[...root.querySelectorAll('a[href]')].find(a=>a.getAttribute('href')===restored.focusHref):null;
 (focus||root.querySelector('main'))?.focus({preventScroll:true});
}
window.scrollTo({left:position.x,top:position.y,behavior:'instant'});
if(changed){const view=activeView;restoreFrame=requestAnimationFrame(()=>{if(view===activeView)window.scrollTo({left:position.x,top:position.y,behavior:'instant'});});}
}
function captureProfile(){const f=root.querySelector('#profile-form');if(!f)return;const data=new FormData(f);['experience','density'].forEach(k=>profileDraft[k]=data.get(k));}
function downloadFile(text,name,type){const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([text],{type}));a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);}
root.addEventListener('submit',ev=>{
const id=ev.target.id;if(!['search-form','extract-form','saved-filter','note-form','profile-form'].includes(id))return;ev.preventDefault();const data=new FormData(ev.target);
if(id==='search-form'){if(searchComposing)return;const q=data.get('q').trim();if(q){state.recent=[q,...state.recent.filter(x=>x!==q)].slice(0,6);persist();}const p=route().params;goto('/search',{q,field:p.get('field')||'work',kind:p.get('kind'),category:p.get('category'),situation:p.get('situation')});}
if(id==='extract-form'){extractText=String(data.get('text')??extractText).slice(0,20000);extractScope=data.get('scope');if(!extractText.trim())return;extractDocument=W.annotate(extractText,scopeEntries(extractScope));render();root.querySelector('.annotated-document')?.focus({preventScroll:true});}
if(id==='saved-filter')goto('/saved',Object.fromEntries(data));
if(id==='note-form'){const wordId=ev.target.dataset.id,text=String(data.get('note')).trim(),collection=String(data.get('collection')).trim();if(text||collection){state.notes[wordId]={text,collection};if(!state.saved.includes(wordId))state.saved.push(wordId);}else delete state.notes[wordId];persist();render();root.querySelector('#note-form button')?.focus({preventScroll:true});toast('메모와 모음을 저장했어요.');}
});
root.addEventListener('input',ev=>{if(ev.target.id==='extract-text')extractText=ev.target.value;if(ev.target.matches('#search-form input')&&!ev.isComposing)showSuggestions();});
root.addEventListener('click',async ev=>{
const suggestion=ev.target.closest('[data-suggestion]');if(suggestion){selectSuggestion(Number(suggestion.dataset.suggestion));return;}
const highlighted=ev.target.closest('[data-highlight]');if(highlighted){openTermPopover(highlighted);return;}
const anchor=ev.target.closest('a[href^="#/"]');
if(anchor&&!ev.defaultPrevented&&ev.button===0&&!ev.metaKey&&!ev.ctrlKey&&!ev.shiftKey&&!ev.altKey&&!anchor.hasAttribute('download')&&(!anchor.target||anchor.target==='_self')){
 ev.preventDefault();
 const parent=history.state?.daneoParent;
 if(anchor.closest('.back-link')&&parent&&views.has(parent.id)){history.back();return;}
 navigateHash(anchor.getAttribute('href'),anchor);return;
}
if(ev.target.closest('.skip-link')){ev.preventDefault();root.querySelector('main')?.focus();return;}const b=ev.target.closest('[data-save],[data-field],[data-action],[data-profile-step],[data-profile-field]');if(!b)return;
if(b.dataset.profileStep!==undefined){captureProfile();profileStep=Number(b.dataset.profileStep);render();root.querySelector(`[data-profile-step="${profileStep}"]`)?.focus();return;}
if(b.dataset.profileField){const key=profileStep===0?'workFields':'interestFields',id=b.dataset.profileField;profileDraft[key]=profileDraft[key].includes(id)?profileDraft[key].filter(x=>x!==id):[...profileDraft[key],id];profileDraft.interestFields=profileDraft.interestFields.filter(x=>!profileDraft.workFields.includes(x));render();root.querySelector(`[data-profile-field="${id}"]`)?.focus({preventScroll:true});return;}

if(b.dataset.save){const id=b.dataset.save,on=state.saved.includes(id);state.saved=on?state.saved.filter(x=>x!==id):[...state.saved,id];persist();if(route().path==='/saved'){render();}else{root.querySelectorAll('[data-save]').forEach(btn=>{if(btn.dataset.save!==id)return;btn.classList.toggle('is-saved',!on);if(btn.classList.contains('bookmark')){btn.setAttribute('aria-pressed',String(!on));btn.setAttribute('aria-label',word(id).term+' '+(!on?'저장 취소':'저장'));}else btn.innerHTML=icon('bookmark')+`<span>${!on?'내 단어장에서 빼기':'내 단어장에 담기'}</span>`;});}toast(on?'단어장에서 뺐어요.':'내 단어장에 담았어요.');return;}
switch(b.dataset.action){
case'feature-tab':homeFeatureTab=b.dataset.tab;root.querySelector('.home-feature').dataset.active=homeFeatureTab;root.querySelectorAll('[data-action="feature-tab"]').forEach(btn=>btn.setAttribute('aria-pressed',String(btn.dataset.tab===homeFeatureTab)));break;
case'refresh-daily':case'refresh-contrast':refreshDiscovery(b.dataset.action);break;
case'profile-next':case'profile-prev':captureProfile();profileStep+=b.dataset.action==='profile-next'?1:-1;render();root.querySelector('.profile-heading h1')?.focus({preventScroll:true});root.querySelector('.profile-heading')?.scrollIntoView({block:'nearest'});break;
case'profile-save':captureProfile();profileDraft.completed=true;state={...state,...W.normalize({...state,profile:profileDraft},D.entries,D.fields,D.redirects),onboarded:true};persist();goto('/');break;
case'skip':state.onboarded=true;state.profile.completed=true;persist();goto('/');break;
case'more':{const n=visible;visible+=40;render();root.querySelectorAll('.results-list .term-open')[n]?.focus({preventScroll:true});break;}
case'close-term':closeTermPopover(true);break;
case'edit-extract':extractDocument=null;render();root.querySelector('#extract-text')?.focus({preventScroll:true});break;
case'clear-recent':state.viewed=[];state.recent=[];persist();render();break;
case'clear-extract':extractText='';extractDocument=null;render();root.querySelector('#extract-text')?.focus();break;
case'compare-add':case'compare-remove':{const id=b.dataset.id;if(state.compare.includes(id))state.compare=state.compare.filter(x=>x!==id);else if(state.compare.length<3)state.compare.push(id);else{toast('최대 3개까지 비교할 수 있어요. 업무 도구에서 먼저 빼 주세요.');break;}persist();render();toast(state.compare.includes(id)?'업무 도구의 뜻 비교에 담았어요.':'비교에서 뺐어요.');break;}
case'copy-word':{const e=word(b.dataset.id);try{await navigator.clipboard.writeText(`${e.term} · ${field(e.field).name}\n${e.definition}\n예문: ${e.example}`);toast('뜻과 예문을 복사했어요.');}catch{toast('복사가 제한된 브라우저예요. 본문을 선택해 복사해 주세요.');}break;}
case'export-csv':downloadFile(W.csv(state.saved.map(word).filter(Boolean),state.notes,D.fields),'다너의단어-내단어장.csv','text/csv;charset=utf-8');break;
case'export':downloadFile(JSON.stringify({app:'daneoword',...state},null,2),'다너의단어-내기록.json','application/json');break;
}});
root.addEventListener('change',async ev=>{const form=ev.target.closest('form');if(form?.id==='profile-form')captureProfile();if(form?.id==='filter-form'){const p=route().params,data=new FormData(form);goto('/search',{q:p.get('q'),field:data.get('field'),kind:data.get('kind'),category:ev.target.name==='field'?'':data.get('category'),situation:p.get('situation')});}if(ev.target.id==='import-file'){const file=ev.target.files[0];if(!file)return;try{if(file.size>20*1024*1024)throw Error();const raw=JSON.parse(await file.text());if(raw.app!=='daneoword'||raw.version!==1||!Array.isArray(raw.saved))throw Error();const incoming=validate(raw);state.saved=[...new Set([...state.saved,...incoming.saved])];state.review={...incoming.review,...state.review};state.notes={...incoming.notes,...state.notes};state.viewed=[...new Set([...state.viewed,...incoming.viewed])].slice(0,20);state.compare=[...new Set([...state.compare,...incoming.compare])].slice(0,3);if(raw.profile){state.profile=incoming.profile;state.fields=incoming.fields;}persist();toast('단어장·메모를 합치고 맞춤 설정을 복원했어요.');}catch{toast('올바른 다, 너의 단어 백업 파일을 선택해 주세요.');}ev.target.value='';}});
window.addEventListener('storage',ev=>{if(ev.key!==KEY||!ev.newValue)return;try{state=validate(JSON.parse(ev.newValue));if(!['INPUT','SELECT','TEXTAREA'].includes(document.activeElement?.tagName)&&!['/settings','/welcome'].includes(route().path))render();}catch{}});
window.addEventListener('popstate',historyChanged);
window.addEventListener('hashchange',historyChanged);
render();if(!storageOK)toast('브라우저 저장소를 읽지 못했어요. 저장 가능 여부를 확인해 주세요.');
})();
