"""Explicit field audit: relevant shared work is allowed, indiscriminate copies are not.
Moved entries redirect to the same meaning in its appropriate field, preserving saved IDs.
Field-specific meanings replace definition, aliases, phrases and evidence together.
"""
DATE='2026-09-16'
SOURCES={
 'field-clo-modes': ('CLO','2D 패턴과 3D 의상 작업 모드','https://support.clo3d.com/hc/ko/articles/115012666427-%EA%B0%81-%EB%AA%A8%EB%93%9C%EC%97%90-%EB%8C%80%ED%95%B4-%EC%84%A4%EB%AA%85%ED%95%B4%EC%A3%BC%EC%84%B8%EC%9A%94','',False),
 'field-clo-layers': ('CLO','레이어 사용: 의상 추가 착장','https://support.clo3d.com/hc/ko/articles/115000294487-%EB%A0%88%EC%9D%B4%EC%96%B4-%EC%82%AC%EC%9A%A9-%EC%9D%98%EC%83%81-%EC%B6%94%EA%B0%80-%EC%B0%A9%EC%9E%A5','',False),
}
# Preserve garment development, brand marketing and lookbook collaboration;
# move specialist film/audio processes and tool-level graphic editing out of fashion.
MOVES=[]
def move(origin,target,terms):
 MOVES.extend((origin,term,target) for term in terms.split('|'))
move('fashion','film','PD|덕션|연출|감독|조감독|연출부|촬영팀|조명팀|미술팀|듀레이션|편집|D.I|녹음|내레이션|BGM|썰다|썰어 넣다|호흡|때깔|콜 시트|콜 타임|프리프로덕션|포스트프로덕션|컬러 그레이딩|조리개|ISO|셔터 스피드|짐벌|삼각대|노출')
move('fashion','marketing','기획실|플래너|미디어렙|미디어 플래너|미디어 바이어|매체팀|종합광고대행사|디지털 대행사')
move('fashion','design','리사이징|그리드|마스크|아웃라인|자간|행간|칼맞춤|먹선|눌리다|깨지다')
move('fashion','dev','MVP|POC')
move('design','fashion','생산관리팀|물류팀|입고|출고')
move('design','film','D.I|오프라인 편집|온라인 편집|컨폼')
move('common','dev','데이터 엔지니어|데이터 분석가|PM')

OVERRIDES={
 ('marketing','PT'): dict(definition='광고주에게 캠페인 전략·아이디어·시안을 제안하고 설명하는 발표. 경쟁 PT에서는 대행사 선정 등을 위해 제안을 비교·평가받는다.',example='광고주 PT에서 캠페인 전략과 시안을 발표해요.',phrases=['광고주에게 캠페인 제안 발표','대행사 광고 기획 발표'],note='광고 대행사의 제안 업무 문맥입니다. 일반적인 사내 발표·프레젠테이션은 업무 공통의 PT에서 설명합니다.'),
 ('fashion','2D'): dict(english='2D pattern design',aliases=['투디','2D 패턴','2D CAD','평면 패턴'],category='디지털 패션·패턴',
  definition='의류 개발에서 패턴 조각을 평면으로 설계·수정하는 작업 방식. 디지털 도구의 2D 패턴창에서 형태와 치수 등을 다룬다.',
  example='2D 패턴에서 소매 길이를 수정하고 3D 착장으로 확인해 주세요.',phrases=['옷 평면 패턴 설계','의류 이차원 패턴 수정'],
  note='패션의 패턴 개발 문맥입니다. 광고 후반의 합성·모션그래픽 파트를 뜻하는 2D와 구분합니다.',sources=['field-clo-modes']),
 ('fashion','3D'): dict(english='3D garment simulation',aliases=['쓰리디','스리디','3D 의상','3D 가상 의상','가상 착장','디지털 의상'],category='디지털 패션·패턴',
  definition='평면 패턴을 입체 의상으로 구성하고 가상으로 착장해 형태·핏·드레이프 등을 확인하는 디지털 의류 개발 방식.',
  example='실물 샘플을 만들기 전에 3D 의상으로 실루엣과 핏을 검토해요.',phrases=['가상으로 옷 입혀 핏 확인','디지털 의상 시뮬레이션'],
  note='의류 개발에서의 3D입니다. 광고용 입체 그래픽 제작과 구분하며, 가상 검토만으로 실물 착용·봉제 검증을 모두 대체하는 것은 아닙니다.',sources=['field-clo-modes']),
 ('fashion','레이어'): dict(english='Garment layer',aliases=['의상 레이어','착장 레이어','겹쳐 입기'],category='디지털 패션·패턴',
  definition='여러 의상을 겹쳐 입힐 때 안쪽과 바깥쪽에 놓이는 순서나 층. 가상 의상 작업에서도 의상 사이의 배치와 겹침을 조정한다.',
  example='셔츠 위에 재킷이 놓이도록 의상 레이어 순서를 확인해요.',phrases=['가상 의상 겹쳐 입는 순서','옷 안쪽 바깥쪽 층'],
  note='의상을 겹쳐 착장하는 문맥입니다. 이미지 편집 도구의 작업 레이어와 구분합니다.',sources=['field-clo-layers']),
}

# Labels describe why a shared term belongs in this field, rather than inheriting
# an unrelated source field's department/category name.
CATEGORY_OVERRIDES={('marketing','PT'):'대행사 제안'}
def category(field,name,terms):
 for term in terms.split('|'):CATEGORY_OVERRIDES[field,term]=name
category('fashion','패션 촬영·스타일링','촬영|로케이션|헌팅|캐스팅|리허설|세트|스타일리스트|메이킹|스틸|제품 컷|헤메|촬감|스토리보드|호리존|부감|앙감|앵글|풀 샷|바스트 샷|클로즈업|색보정|조명')
category('fashion','브랜드 비주얼','레이아웃|팔레트|채도|명도|색상|대비|여백|리터칭|톤 다운|빼기|키우다')
for f in ['marketing','fashion','film','design','common']:
 category(f,'협업·커뮤니케이션','FYI')
 category(f,'일정·범위','프로젝트 매니저')
category('fashion','고객·운영','데이터 분석가')
category('marketing','고객·운영','데이터 분석가')
category('design','제품 제작·품질','QC|OEM|ODM')

# A scope note makes cross-industry overlap explicit without changing valid meanings.
NOTES={
 ('fashion','조명'):'화보·룩북·상품 사진 촬영의 협업 문맥입니다. 조명팀 운영이나 전문 장비 용어는 영상·촬영 분야에서 다룹니다.',
 ('design','QC'):'패키지·인쇄물·실물 제품 등 디자인 결과물을 제작할 때의 품질 관리 문맥입니다.',
 ('design','OEM'):'디자인한 실물 제품·굿즈 등을 외부 제조사에 생산 의뢰하는 문맥입니다.',
 ('design','ODM'):'실물 제품 개발과 제조를 외부 제조사와 함께 진행하는 문맥입니다.',
}


def apply(entries,sources,id_map):
 sources.update({k:dict(id=k,publisher=v[0],title=v[1],url=v[2],published=v[3],historical=v[4],checkedAt=DATE) for k,v in SOURCES.items()})
 index={(e['field'],e['term']):e for e in entries}
 redirects={}
 for origin,term,target in MOVES:
  key=origin,term;target_key=target,term
  assert key in index and target_key in index,(key,target_key)
  old=index.pop(key);redirects[old['id']]=index[target_key]['id']
 # Generic meanings live once in common. Only a real, explicitly scoped
 # industry meaning may remain alongside them (advertising proposal PT).
 common={e['term']:e for e in index.values() if e['field']=='common'}
 for key,e in list(index.items()):
  canonical=common.get(e['term'])
  if e['field']=='common' or key==('marketing','PT') or not canonical:continue
  if e['definition']==canonical['definition']:
   index.pop(key);redirects[e['id']]=canonical['id']
 # Flatten explicit moves whose targets were also consolidated into common.
 for old,target in list(redirects.items()):
  visited={old}
  while target in redirects:
   assert target not in visited,('Redirect cycle',old)
   visited.add(target);target=redirects[target]
  redirects[old]=target
 for key,changes in OVERRIDES.items():
  e=index[key];e.update(changes,checkedAt=DATE,evidence='공개 자료 확인',historical=False)
  e.pop('writtenAt',None)
 for key,name in CATEGORY_OVERRIDES.items():
  if key in index:index[key]['category']=name
 for key,note in NOTES.items():
  index[key]['note']=note
 assert all(target in {e['id'] for e in index.values()} for target in redirects.values())
 return [e for e in entries if (e['field'],e['term']) in index],redirects
