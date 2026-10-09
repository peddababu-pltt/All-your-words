from pathlib import Path
import importlib.util,json,collections,re,hashlib
ROOT=Path(__file__).resolve().parents[1]
# Split layout: backend/ holds data + scripts; frontend/ holds the served app.
FRONTEND=ROOT.parent/'frontend'
spec=importlib.util.spec_from_file_location('seed',ROOT/'data'/'seed.py');seed=importlib.util.module_from_spec(spec);spec.loader.exec_module(seed)
fields=[{'id':'marketing','name':'마케팅·광고','icon':'megaphone'},{'id':'dev','name':'개발·IT','icon':'code'},{'id':'fashion','name':'패션·섬유','icon':'fashion'},{'id':'film','name':'영상·촬영','icon':'film'},{'id':'design','name':'디자인','icon':'design'},{'id':'hrfinance','name':'인사·재무','icon':'folder'},{'id':'common','name':'업무 공통','icon':'book'}]
sources={k:dict(id=k,publisher=v[0],title=v[1],url=v[2],published=v[3],historical=v[4],checkedAt='2026-09-15') for k,v in seed.SOURCES.items()}
entries=[]; counts=collections.Counter()
id_path=ROOT/'data'/'id-map.json'
id_map=json.loads(id_path.read_text()) if id_path.exists() else {}
for fixed in id_map.values():
    prefix,number=fixed.rsplit('-',1);counts[prefix]=max(counts[prefix],int(number))
def add(field,kind,source,row):
    term,en,aliases,definition,example,phrases=row
    key=field+'|'+term
    if key not in id_map:
        counts[field]+=1
        id_map[key]=field+'-'+str(counts[field]).zfill(3)
    e=dict(id=id_map[key],term=term,english=en,aliases=[x for x in aliases.split(';') if x],field=field,kind=kind,definition=definition,example=example,phrases=[x for x in phrases.split(';') if x],note=seed.NOTES.get(term,''),sources=[s for s in source.split(',') if s],checkedAt='2026-09-15' if source else '')
    e['historical']=any(sources[s]['historical'] for s in e['sources'])
    e['evidence']=('복수 자료 대조' if len(e['sources'])>1 else '공개 자료 확인') if source else '일반 지식 기반 · 외부 출처 미첨부'
    if not source:e['writtenAt']='2026-09-15'
    entries.append(e)
for field,kind,source,raw in seed.GROUPS:
    for line in raw.strip().splitlines():
        parts=line.strip().split('|')
        if len(parts)!=6: raise ValueError((field,line,len(parts)))
        # Explicitly cross-check the two documented finishing terms.
        evidence=source
        if parts[0] in ('마도메','시아게') and source=='sewing': evidence='sewing,sewing-stats,sewing-news'
        add(field,kind,evidence,parts)
for field,term,en,aliases,definition,example,phrases,source in seed.SINGLE:
    add(field,'전문 용어',source,[term,en,aliases,definition,example,phrases])
# Curated expansions use the same schema, with explicit topic groups.
spec2=importlib.util.spec_from_file_location('expansion',ROOT/'data'/'expansion.py');expansion=importlib.util.module_from_spec(spec2);spec2.loader.exec_module(expansion)
sources.update({k:dict(id=k,publisher=v[0],title=v[1],url=v[2],published=v[3],historical=v[4],checkedAt='2026-09-15') for k,v in expansion.SOURCES.items()})
seed.NOTES.update(expansion.NOTES)
for field,kind,category,source,raw in expansion.GROUPS:
    for line in raw.strip().splitlines():
        parts=line.strip().split('|')
        if len(parts)!=6: raise ValueError((field,line,len(parts)))
        add(field,kind,expansion.SOURCE_OVERRIDES.get(parts[0],source),parts)
        entries[-1]['category']=category
# Workplace meanings are explicitly shared across relevant fields, even when
# their definitions are identical. Preserve existing meanings and bookmark IDs.
spec3=importlib.util.spec_from_file_location('workplace',ROOT/'data'/'workplace.py');workplace=importlib.util.module_from_spec(spec3);spec3.loader.exec_module(workplace)
sources.update({k:dict(id=k,publisher=v[0],title=v[1],url=v[2],published=v[3],historical=v[4],checkedAt='2026-09-15') for k,v in workplace.SOURCES.items()})
for target_fields,kind,category,source,raw in workplace.GROUPS:
    for line in raw.strip().splitlines():
        parts=line.strip().split('|')
        if len(parts)!=6: raise ValueError((target_fields,line,len(parts)))
        for target in target_fields.split(','):
            assert target!='film', 'Workplace expansion must not modify filming'
            add(target,kind,source,parts)
            entries[-1].update(category=category,note=workplace.NOTES.get(parts[0],''))
for origin,term,target,category,example in workplace.COPIES:
    original=next(e for e in entries if e['field']==origin and e['term']==term)
    add(target,original['kind'],','.join(original['sources']),[term,original['english'],';'.join(original['aliases']),original['definition'],example,';'.join(original['phrases'])])
    entries[-1].update(category=category,note=original['note'])
for e in entries:
    if (e['field'],e['term']) in workplace.EXAMPLES:
        e['example']=workplace.EXAMPLES[(e['field'],e['term'])]
# Field slang and the search aliases collected from public glossaries.
spec4=importlib.util.spec_from_file_location('slang',ROOT/'data'/'slang.py');slang=importlib.util.module_from_spec(spec4);spec4.loader.exec_module(slang)
assert not (set(slang.SOURCES) & set(sources)), 'Source IDs must be unique'
sources.update({k:dict(id=k,publisher=v[0],title=v[1],url=v[2],published=v[3],historical=v[4],checkedAt='2026-09-15') for k,v in slang.SOURCES.items()})
for target_fields,kind,category,source,raw in slang.GROUPS:
    for line in raw.strip().splitlines():
        parts=line.strip().split('|')
        if len(parts)!=6: raise ValueError((target_fields,line,len(parts)))
        for target in target_fields.split(','):
            assert target in {f['id'] for f in fields},target
            add(target,kind,source,parts)
            e=entries[-1]
            notes=[slang.NOTES.get(e['term'],''),slang.FIELD_NOTES.get((target,e['term']),'')]
            if source=='sl-film-old':notes.append('1985년 순화 자료에 기록된 표현입니다. 오늘날 모든 촬영 현장에서 통용된다는 뜻은 아닙니다.')
            elif source=='sl-broadcast':notes.append('2009년 방송작가의 사용 기록을 참고했습니다. 프로그램·팀마다 사용 범위가 다릅니다.')
            elif source=='sl-sew':notes.append('2023년 실무자 글에 수록된 과거 봉제 자료를 참고했습니다. 공장마다 호칭과 표기가 다를 수 있습니다.')
            elif source=='sl-ddm':notes.append('2020년 동대문시장 취재 자료의 사용 사례입니다. 거래처별 표현은 다를 수 있습니다.')
            e.update(category=category,note=' '.join(n for n in notes if n))
for field,term,aliases,source,note in slang.ALIAS_UPDATES:
    matches=[e for e in entries if e['field']==field and e['term']==term]
    assert len(matches)==1,(field,term)
    e=matches[0]
    e['aliases']=list(dict.fromkeys(e['aliases']+aliases))
    e['sources']=list(dict.fromkeys(e['sources']+[source]))
    e['note']=' '.join(n for n in [e['note'],note] if n)
    e['historical']=any(sources[s]['historical'] for s in e['sources'])
    e['evidence']='복수 자료 대조' if len(e['sources'])>1 else '공개 자료 확인'
# Korean shortforms keep their source and expanded spelling together.
spec5=importlib.util.spec_from_file_location('korean_shortforms',ROOT/'data'/'korean_shortforms.py');shortforms=importlib.util.module_from_spec(spec5);spec5.loader.exec_module(shortforms)
assert not (set(shortforms.SOURCES) & set(sources)), 'Source IDs must be unique'
sources.update({k:dict(id=k,publisher=v[0],title=v[1],url=v[2],published=v[3],historical=v[4],checkedAt='2026-09-15') for k,v in shortforms.SOURCES.items()})
for target_fields,category,source,raw in shortforms.GROUPS:
    for line in raw.strip().splitlines():
        parts=line.strip().split('|')
        if len(parts)!=6: raise ValueError((target_fields,line,len(parts)))
        for target in target_fields.split(','):
            assert target in {f['id'] for f in fields},target
            add(target,'현장 표현',source,parts)
            entries[-1].update(category=category,note=shortforms.NOTES.get(parts[0],''))
for field,term,aliases,source in shortforms.ALIAS_UPDATES:
    matches=[e for e in entries if e['field']==field and e['term']==term]
    assert len(matches)==1,(field,term)
    e=matches[0]
    e['aliases']=list(dict.fromkeys(e['aliases']+aliases))
    e['sources']=list(dict.fromkeys(e['sources']+source.split(',')))
    e['evidence']='복수 자료 대조' if len(e['sources'])>1 else '공개 자료 확인'
    e['historical']=any(sources[s]['historical'] for s in e['sources'])
# Detailed industry coverage may include confidently known concepts without
# external citations, as requested. Keep their provenance explicit.
spec6=importlib.util.spec_from_file_location('industry_detail',ROOT/'data'/'industry_detail.py');detail=importlib.util.module_from_spec(spec6);spec6.loader.exec_module(detail)
assert not (set(detail.SOURCES) & set(sources)), 'Source IDs must be unique'
sources.update({k:dict(id=k,publisher=v[0],title=v[1],url=v[2],published=v[3],historical=v[4],checkedAt='2026-09-15') for k,v in detail.SOURCES.items()})
detail_keys={(e['field'],e['term']) for e in entries}
authored_keys=set()
for target_fields,kind,category,source,raw in detail.GROUPS:
    for line in raw.strip().splitlines():
        parts=line.strip().split('|')
        if len(parts)!=6:raise ValueError((target_fields,line,len(parts)))
        for target in target_fields.split(','):
            assert target in {f['id'] for f in fields},target
            key=(target,parts[0])
            assert key not in authored_keys,('Repeated detail row',key)
            authored_keys.add(key)
            if key in detail_keys:continue # preserve existing definitions and IDs
            add(target,kind,source,parts)
            entries[-1].update(category=category,note=detail.NOTES.get(key,detail.NOTES.get(parts[0],'')))
            detail_keys.add(key)
for origin,term,targets in detail.COPIES:
    original=next(e for e in entries if e['field']==origin and e['term']==term)
    for target in targets.split(','):
        assert target in {f['id'] for f in fields},target
        if (target,term) in detail_keys:continue
        add(target,original['kind'],','.join(original['sources']),[term,original['english'],';'.join(original['aliases']),original['definition'],original['example'],';'.join(original['phrases'])])
        entries[-1].update(category=original.get('category','업무 협업'),note=original['note'],evidence=original['evidence'])
        detail_keys.add((target,term))
# User submissions are candidate lists; only explicitly curated rows are published.
retired_names=[]
for module_name in ['curated_submission','curated_followup','curated_round4','keycopy','audit_additions','meeting_language','meeting_expansion','hr_finance']:
    module_path=ROOT/'data'/f'{module_name}.py'
    if not module_path.exists():continue
    spec_cur=importlib.util.spec_from_file_location(module_name,module_path)
    curated=importlib.util.module_from_spec(spec_cur);spec_cur.loader.exec_module(curated)
    retired_names.extend(getattr(curated,'RETIRED_NAMES',[]))
    assert not (set(curated.SOURCES)&set(sources)), 'Source IDs must be unique'
    sources.update({k:dict(id=k,publisher=v[0],title=v[1],url=v[2],published=v[3],historical=v[4],checkedAt=curated.DATE) for k,v in curated.SOURCES.items()})
    curated_keys={(e['field'],e['term']) for e in entries}
    for target_fields,kind,category,source,raw in curated.GROUPS:
        for line in raw.strip().splitlines():
            parts=line.strip().split('|')
            assert len(parts)==6,(module_name,line)
            for target in target_fields.split(','):
                assert target in {f['id'] for f in fields},target
                key=(target,parts[0]);assert key not in curated_keys,('Duplicate curated meaning',key)
                add(target,kind,source,parts)
                entries[-1].update(category=category,note=getattr(curated,'FIELD_NOTES',{}).get(key,curated.NOTES.get(parts[0],'')))
                entries[-1]['checkedAt']=curated.DATE if source else ''
                if not source:entries[-1]['writtenAt']=curated.DATE
                curated_keys.add(key)
    for field,term,aliases in curated.ALIASES:
        matches=[e for e in entries if e['field']==field and e['term']==term]
        assert len(matches)==1,(module_name,field,term)
        matches[0]['aliases']=list(dict.fromkeys(matches[0]['aliases']+aliases))
for e in entries:
    if e['field']=='film' and 'category' not in e:
        e['category']='카메라 움직임' if e['term']=='트래킹' else '샷 크기' if e['sources']==['shot-settings'] and e['term']!='탑 샷' else '앵글·구도'
    # Search-only orthographic variants, never counted as separate meanings.
    if e['field']=='film':
        for name in [e['term']]+e['aliases'][:]:
            if '샷' in name:
                e['aliases'] += [name.replace('샷','숏'),name.replace('샷','쇼트')]
        e['aliases']=list(dict.fromkeys(e['aliases']))

# Extensions remain reviewable alongside the first collection.
extra=ROOT/'data'/'extended.json'
if extra.exists():
    x=json.loads(extra.read_text());sources.update(x['sources'])
    for e in x['entries']:
        assert e['field'] in {f['id'] for f in fields}
        entries.append(e)
# Explicit scope review promotes generic concepts without losing old IDs.
spec_scope=importlib.util.spec_from_file_location('scope_audit',ROOT/'data'/'scope_audit.py');scope=importlib.util.module_from_spec(spec_scope);spec_scope.loader.exec_module(scope)
for origin,term,category in scope.COMMON:
    original=next(e for e in entries if e['field']==origin and e['term']==term)
    assert not any(e['field']=='common' and e['term']==term for e in entries),term
    add('common',original['kind'],','.join(original['sources']),[term,original['english'],';'.join(original['aliases']),original['definition'],original['example'],';'.join(original['phrases'])])
    promoted=entries[-1];identity=promoted['id'];promoted.update(original);promoted.update(id=identity,field='common',category=category)
# Apply reviewed field boundaries before publishing search and learning data.
spec7=importlib.util.spec_from_file_location('field_review',ROOT/'data'/'field_review.py');field_review=importlib.util.module_from_spec(spec7);spec7.loader.exec_module(field_review)
field_review.MOVES.extend((origin,term,target) for origin,term,target,reason in scope.MOVES)
entries,redirects=field_review.apply(entries,sources,id_map)
entries=scope.finish(entries)
spec_editorial=importlib.util.spec_from_file_location('editorial_audit',ROOT/'data'/'editorial_audit.py');editorial=importlib.util.module_from_spec(spec_editorial);spec_editorial.loader.exec_module(editorial)
entries=editorial.apply(entries,sources)
# Explicitly reviewed contexts survive older global consolidation rules.
spec_coverage=importlib.util.spec_from_file_location('coverage_expansion',ROOT/'data'/'coverage_expansion.py');coverage=importlib.util.module_from_spec(spec_coverage);spec_coverage.loader.exec_module(coverage)
entries=coverage.apply(entries,sources,id_map)
# A reinstated field-specific ID must resolve to itself, not its old common row.
active_ids={e['id'] for e in entries}
redirects={old:target for old,target in redirects.items() if old not in active_ids}

for field,old_name,target_name in retired_names:
    old_id=id_map.get(field+'|'+old_name)
    target=next(e for e in entries if e['field']==field and e['term']==target_name)
    if old_id:
        assert not any(e['id']==old_id for e in entries),old_id
        redirects[old_id]=target['id']
ids=[e['id'] for e in entries];assert len(ids)==len(set(ids))
seen=set()
for e in entries:
    assert e['term'] and e['definition'] and e['example'] and e['phrases']
    assert isinstance(e.get('category',''),str),('Invalid category',e['id'])
    key=(e['field'],e['term']);assert key not in seen,key;seen.add(key)
    assert all(s in sources for s in e['sources']),e
    assert all(sources[s]['url'].startswith('https://') for s in e['sources'])
# Frozen editorial record: reject unreviewed copies/meaning changes before publishing.
spec_review=importlib.util.spec_from_file_location('check_editorial_review',ROOT/'scripts'/'check_editorial_review.py');review=importlib.util.module_from_spec(spec_review);spec_review.loader.exec_module(review)
review.check(entries)
spec_meanings=importlib.util.spec_from_file_location('meaning_groups',ROOT/'data'/'meaning_groups.py');meanings=importlib.util.module_from_spec(spec_meanings);spec_meanings.loader.exec_module(meanings)
entries=meanings.apply(entries)
id_path.write_text(json.dumps(id_map,ensure_ascii=False,indent=2)+'\n')
sources={k:v for k,v in sources.items() if any(k in e['sources'] for e in entries)}
payload=dict(version=1,updatedAt='2026-10-07',fields=fields,sources=sources,entries=entries,redirects=redirects)
(ROOT/'data'/'dictionary.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
(FRONTEND/'data.js').write_text('/* Generated by scripts/build_data.py. No network requests. */\nwindow.WORD_DATA = '+json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+';\n')
# A content version makes changed local scripts load even in caching webviews.
index=FRONTEND/'index.html'
html=index.read_text()
for asset in ['data.js','core.js','app.js','app.css','workspace-core.js','workspace.css']:
    revision=hashlib.sha256((FRONTEND/asset).read_bytes()).hexdigest()[:12]
    attr='href' if asset.endswith('.css') else 'src'
    html=re.sub(attr+r'="'+re.escape(asset)+r'(?:\?[^\"]*)?"',attr+'="'+asset+'?v='+revision+'"',html)
index.write_text(html)
report=['# 수집 자료와 등록 항목','',f"확인 기준일: {payload['updatedAt']} · 분야별 뜻 {len(entries)}개 · 출처 {len(sources)}개",'',
 '뜻과 예문은 직접 작성했습니다. 출처는 개념 또는 사용 사례의 근거이며, 한국어 호칭이 모든 회사에서 통용된다는 뜻은 아닙니다.',
 '동일한 뜻도 해당 업무에서 사용하는 분야별로 포함합니다. 표기 변형은 별칭으로 연결하며 항목 수에 더하지 않습니다.','']
uncited=[e for e in entries if not e['sources']]
report += [f'일반 지식 기반 항목: {len(uncited)}개 뜻. 사용자의 요청에 따라 외부 출처가 없어도 확실히 설명할 수 있는 개념을 직접 작성했습니다. 공개 자료 확인이나 전문가 감수로 표시하지 않습니다.','']
for f in fields:
    report += [f"- {f['name']}: "+', '.join(e['term'] for e in uncited if e['field']==f['id'])]
report.append('')
for sid,s in sources.items():
    report += [f"## {s['publisher']} · {s['title']}",'',f"[자료 원문]({s['url']})",'']
    for f in fields:
        terms=[e['term'] for e in entries if e['field']==f['id'] and sid in e['sources']]
        if terms:report.append(f"- {f['name']}: "+', '.join(terms))
    report.append('')
(ROOT/'data'/'COLLECTION.md').write_text('\n'.join(report)+'\n')
print(json.dumps({'entries':len(entries),'sources':len(sources),'byField':dict(collections.Counter(e['field'] for e in entries)),'fieldExpressions':sum(e['kind']=='현장 표현' for e in entries)},ensure_ascii=False))
