"""Second field audit: explicit placement decisions, not a keyword deletion rule."""
DATE='2026-09-16'
# Promote truly generic meanings into common before field_review consolidates copies.
COMMON=[
 ('marketing','RFP','업무 문서·진행'),('marketing','제안서','업무 문서·진행'),
 ('marketing','피저빌리티','일정·범위'),('marketing','컨센서스','협업·커뮤니케이션'),
 ('marketing','스펙 아웃','일정·범위'),('marketing','얼터안','기획·조율'),
 ('marketing','가성비','가치·선택'),('marketing','가심비','가치·선택'),
 ('marketing','인스타','플랫폼·줄임말'),('marketing','페북','플랫폼·줄임말'),
]
MOVES=[]
def move(origin,target,terms,reason):
 MOVES.extend((origin,term,target,reason) for term in terms.split('|'))
move('dev','marketing','오가닉 트래픽','자연 검색 유입 성과 개념; 구현 기술 자체와 구분')
move('dev','fashion','자사몰','판매 채널 개념의 중복; 쇼핑몰 개발 문맥 설명이 없는 복사')
move('marketing','fashion','얼죽코|얼죽크','의류 착용·소비 취향을 나타내는 표현')
move('marketing','dev','MVP|POC','제품 가설·기술 검증 개념을 소프트웨어·제품 개발 분야에서 유지')
move('marketing','film','랙 포커스|단렌즈|줌 렌즈|광각 렌즈|망원 렌즈|매크로 렌즈|얕은 심도|깊은 심도|조리개|셔터 스피드|ISO|DIT|스크립트 슈퍼바이저|롤 카메라|롤 사운드|스테디캠|3점 조명|키 라이트|필 라이트|백 라이트|하드 라이트|소프트 라이트|디퓨전','촬영 기술·장비 운용의 전문 뜻은 영상 분야로 집중; 광고 기획·제작 협업은 유지')
move('fashion','dev','DAU|MAU','서비스 활성 사용자 측정 정의를 의류 전문 뜻으로 복사한 항목')
move('film','marketing','미디어 플래너|매체팀|홍보팀|디지털 대행사|네이밍','매체 구매·홍보·브랜드 명명 전문 업무의 중복; 촬영 제작 협업 용어와 구분')
move('design','marketing','미디어 플래너|매체팀|홍보팀|디지털 대행사|콘텐츠 캘린더|보도자료|협찬|앰배서더','매체 집행·언론홍보·캠페인 운영 의미의 복사; 시각 제작과 구분')
move('design','fashion','자사몰','온라인 판매 채널의 일반 뜻; 디자인 전문 개념과 구분')

# These are editorial placements, not claims that nobody in another field uses a word.
CATEGORY_MAP={
 'fashion':{
  '마케팅·성과':'패션 브랜드·광고 성과','광고 운영':'패션 브랜드·광고 운영',
  '광고 운영·성과':'패션 브랜드·광고 운영','검색·유입':'자사몰·검색 유입',
  '브랜드 전략':'패션 브랜드 전략','전략·고객 이해':'패션 브랜드 전략',
  '미디어 전략':'패션 브랜드·매체','인플루언서·확산':'패션 브랜드·협찬',
  '광고 소재 제작':'패션 브랜드·콘텐츠','광고 소재·성과':'패션 브랜드·콘텐츠',
  '캠페인 기획·실행':'패션 브랜드·캠페인','광고 조직·직무':'패션 브랜드·마케팅 협업',
  '광고 제작·협업':'패션 브랜드·제작 협업','고객·운영':'자사몰·고객 운영',
  '제품·고객 지표':'자사몰·고객 지표','브랜드 제작':'패션 브랜드·시각 제작',
 },
 'dev':{'UI·협업':'UI 구현·디자인 협업','디자인 조직·직무':'제품팀·디자인 협업'},
 'film':{'브랜드 제작':'광고 영상·제작 협업','광고 조직·직무':'광고 영상·발주 협업','크리에이티브 직무':'광고 영상·크리에이티브 협업'},
 'design':{'영상 후반 작업':'모션·영상 디자인','편집':'모션·영상 편집','광고 조직·직무':'광고 디자인·협업'},
}
CATEGORIES={
 ('fashion','GSM'):'소재·원단 공정',
 ('marketing','키카피'):'광고 카피·메시지',
 ('marketing','헤드라인'):'광고 카피·메시지',('marketing','바디카피'):'광고 카피·메시지',
 ('marketing','슬로건'):'광고 카피·메시지',('marketing','키메시지'):'광고 카피·메시지',('marketing','카피'):'광고 카피·메시지',
}
# Definitions need an actual design context, not the copied advertising department label.
DESIGN_2D=dict(
 english='2D graphic design',aliases=['투디','2D 그래픽','평면 그래픽'],
 definition='평면에서 도형·이미지·글자 등을 구성하는 그래픽 작업. 모션 디자인에서는 시간에 따른 움직임을 더하기도 한다.',
 example='2D 그래픽으로 포스터와 타이틀 화면을 구성해요.',
 phrases=['평면 그래픽 디자인 작업','이차원 그래픽 제작'],category='시각 디자인·제작',
 note='디자인의 그래픽 제작 문맥입니다. 광고 후반의 2D 담당 파트와 구분합니다.',
 sources=[],evidence='일반 지식 기반 · 외부 출처 미첨부',checkedAt='',writtenAt=DATE,historical=False)

def finish(entries):
 for e in entries:
  current=e.get('category','')
  e['category']=CATEGORY_MAP.get(e['field'],{}).get(current,current)
  if (e['field'],e['term']) in CATEGORIES:e['category']=CATEGORIES[e['field'],e['term']]
  if e['field']=='design' and e['term']=='2D':e.update(DESIGN_2D)
  # Fill previously unlabelled seed rows with real topics, not generic placeholders.
  if not e['category']:
   defaults={'marketing':'광고 운영·성과','dev':'웹·프로그래밍','fashion':'봉제·소재 기초','design':'시각·편집 디자인','common':'현장 표현'}
   e['category']=defaults[e['field']]
  if e['field']=='marketing' and e['category']=='업무 협업':
   e['category']='광고 콘티·샷 구성'
  if e['field']=='dev' and e['term'] in '커밋|브랜치|머지|풀 리퀘스트|포크|리포지토리|이슈|충돌|클론|푸시|풀|리버트'.split('|'):e['category']='코드·버전 관리'
  if e['field']=='dev' and e['term'] in '애자일|스크럼|스프린트|스탠드업|회고|스토리 포인트|백로그|번다운 차트'.split('|'):e['category']='개발 협업'
  if e['field']=='dev' and e['term'] in ['QA','단위 테스트','통합 테스트']:e['category']='품질·테스트'
 return entries
