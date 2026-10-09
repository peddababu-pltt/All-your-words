"""한국어 업무 줄임말. 원문/예문을 독립 작성하고 기존 뜻은 별칭으로 보강한다."""
import json
SOURCES = json.loads(r'''{
  "ko-brand": [
    "AMPM",
    "브랜드검색광고 꼭 해야하나요?",
    "https://ampm.co.kr/home/ae-bhha1229/insight/10033",
    "",
    false
  ],
  "ko-workorder": [
    "세경실업",
    "의류 작업지시서 작성법",
    "https://www.sekyungapparel.com/journal/apparel-work-order-sheet-guide",
    "",
    false
  ],
  "ko-detail": [
    "네슬로 · 크몽",
    "쇼핑몰 상세페이지 제품설명 상페",
    "https://kmong.com/gig/677601",
    "",
    false
  ],
  "ko-coding": [
    "프로그래머스 스쿨 · 풀이 작성자",
    "코테 초보자를 위한 해설",
    "https://school.programmers.co.kr/questions/58394",
    "",
    false
  ],
  "ko-computer": [
    "우아한형제들",
    "9X년생 개발자 모임 참석 후기",
    "https://techblog.woowahan.com/2510/",
    "",
    false
  ],
  "ko-photoshop": [
    "Adobe Community · 질문 작성자",
    "Photoshop 구독 질문의 포샵 사용 사례",
    "https://community.adobe.com/%EC%A7%88%EB%AC%B8-335/%EA%B5%AC%EB%8F%85%EC%9D%84-%ED%96%88%EB%8B%A4%EA%B0%80-%EC%A7%80%EA%B8%88-%EC%95%88%ED%95%98%EA%B3%A0-%EC%9E%88%EB%8A%94%EB%8D%B0-%EB%8B%A4%EC%8B%9C-%EA%B5%AC%EB%8F%85%ED%95%98%EB%A0%A4-%ED%95%A9%EB%8B%88%EB%8B%A4-%EA%B7%B8%EB%9F%B0%EB%8D%B0-1002276",
    "",
    false
  ],
  "ko-effects": [
    "Adobe Community · 질문 작성자",
    "Premiere와 After Effects 연결 문제",
    "https://community.adobe.com/bug-reports-728/premiere-after-effects-dynamic-link-%EC%97%B0%EA%B2%B0-%EB%AC%B8%EC%A0%9C-1625995",
    "",
    false
  ],
  "ko-hair": [
    "외국인 모델 섭외 제공자 · 크몽",
    "촬영 헤메 패키지 안내",
    "https://kmong.com/gig/620288",
    "",
    false
  ],
  "ko-portfolio": [
    "Adobe Community · 질문 작성자",
    "포트폴리오·영상·AI 이미지까지 한 번에",
    "https://community.adobe.com/%EC%A7%88%EB%AC%B8-372/%ED%8F%AC%ED%8A%B8%ED%8F%B4%EB%A6%AC%EC%98%A4-%EC%98%81%EC%83%81-ai-%EC%9D%B4%EB%AF%B8%EC%A7%80%EA%B9%8C%EC%A7%80-%ED%95%9C-%EB%B2%88%EC%97%90-%EA%B5%AC%EB%8F%85-%EC%88%98%EB%A5%BC-%EC%B5%9C%EC%86%8C%ED%99%94%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95-1625254",
    "",
    false
  ],
  "ko-expense": [
    "잡아바 · 잡플래닛 재게시",
    "비즈니스 용어 모음 · 검색 색인 확인",
    "https://job.gg.go.kr/thema/exprcDtl.do?cntntsSeCd=04&seq=5972&shareUsr=",
    "",
    false
  ],
  "ko-fashiontrend": [
    "디자인플러스",
    "패알못을 위한 패션 용어",
    "https://design.co.kr/article/12598/",
    "",
    false
  ],
  "ko-livecommerce": [
    "카페24 뉴스룸",
    "라이브 커머스 · 라방",
    "https://news.cafe24.com/kr/e-commerce-dictionary-live/amp/",
    "",
    false
  ],
  "ko-broadcast": [
    "김세정 공식 위버스",
    "더쇼 사전녹화·본방송·공개방송 참여 안내",
    "https://weverse.io/kimsejeong/notice/15199?hl=ja",
    "",
    false
  ],
  "ko-resume": [
    "원티드 커뮤니티 · 작성자",
    "경력 이직 자소서 질문",
    "https://social.wanted.co.kr/community/post/6918",
    "",
    false
  ],
  "ko-shoppingad": [
    "네이버 광고 도움말",
    "쇼핑검색광고 추천 및 콘텐츠 지면",
    "https://ads.naver.com/help/faq/196?t=1748210486972",
    "",
    false
  ],
  "ko-fullstack": [
    "Kakao Tech",
    "AI 협업을 위한 개발 환경과 평가 시스템",
    "https://tech.kakao.com/posts/753",
    "",
    false
  ],
  "ko-certificate": [
    "길벗",
    "시나공 정보처리기사 실기 기출문제집",
    "https://www.gilbut.co.kr/book/view?bookcode=BN004721",
    "",
    false
  ],
  "ko-js": [
    "인프런 · 수강생과 강사",
    "자바스크립트 질문 · 자스",
    "https://www.inflearn.com/community/questions/1708163/%EC%9E%90%EB%B0%94%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8-%EC%A7%88%EB%AC%B8",
    "",
    false
  ],
  "ko-ts": [
    "인프런 · 수강생과 강사",
    "프로젝트 중간에 언어 변경 · 타스",
    "https://www.inflearn.com/community/questions/1212194/%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EC%A4%91%EA%B0%84%EC%97%90-%ED%94%84%EB%A0%88%EC%9E%84%EC%9B%8C%ED%81%AC%EC%99%80-%EC%96%B8%EC%96%B4%EB%A5%BC-%EB%B3%80%EA%B2%BD%ED%95%A0%EC%88%98-%EC%9E%88%EB%82%98%EC%9A%94",
    "",
    false
  ],
  "ko-db": [
    "우아한형제들",
    "배민상품시스템팀에서 1년 동안 배운 것들",
    "https://techblog.woowahan.com/2708/",
    "",
    false
  ],
  "ko-illustrator": [
    "Adobe Community · 질문 작성자",
    "Illustrator와 일러 사용 사례",
    "https://community.adobe.com/%EC%A7%88%EB%AC%B8-372/creative-cloud-%EA%B5%AC%EB%8F%85%EC%9D%B4-%EC%A0%95%EB%A7%90-%EB%B3%B8%EC%A0%84%EC%9D%B4-%EB%90%98%EB%8A%94%EA%B0%80-%EB%B9%84%EC%9A%A9-%EC%A0%88%EA%B0%90%EC%95%A1%EC%9D%84-%EC%A7%81%EC%A0%91-%EA%B3%84%EC%82%B0%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95-1559260",
    "",
    false
  ],
  "ko-clothes": [
    "대원여자고등학교 · 나라장터",
    "체육복 디자인 사양서 · 폴리와 스판",
    "https://www.g2b.go.kr/pn/pnp/pnpe/UntyAtchFile/downloadFile.do?bidPbancNo=R25BK01027463&bidPbancOrd=000&fileSeq=2&fileType=",
    "",
    false
  ],
  "ko-copy": [
    "디스켓 운영팀",
    "노션 동기화 블록 · 복붙 사용 사례",
    "https://d-sket.io/blog/how-to-use-notion-synced-blocks-guide",
    "",
    false
  ],
  "ko-length": [
    "세경실업",
    "롱패딩 제작 · 총장 기준",
    "https://www.sekyungapparel.com/journal/long-padding-oem-guide",
    "",
    false
  ],
  "ko-product": [
    "아가방앤컴퍼니",
    "품번·품명 확인 안내",
    "https://www.agabangncompany.com/sub/ascenter/productInfo.asp",
    "",
    false
  ],
  "ko-leave": [
    "다우오피스HR",
    "조직문화와 근무 시스템",
    "https://hr.daouoffice.com/blog/organizational-culture-system",
    "",
    false
  ],
  "ko-free": [
    "에스토리",
    "무료배송 상품 · 무배 표시",
    "https://m.estorymall.com/",
    "",
    false
  ],
  "ko-groupbuy": [
    "AMPM",
    "공구 마케팅",
    "https://inside.ampm.co.kr/insight/9468",
    "",
    false
  ],
  "ko-typo": [
    "어떤이 · 브런치스토리",
    "디자인에 생기를 불어넣는 방법",
    "https://brunch.co.kr/%40sujin910504/5",
    "",
    false
  ],
  "ko-project": [
    "인프런 · 프로젝트 모집 작성자",
    "사이드프로젝트 프론트엔드 모집",
    "https://www.inflearn.com/projects/1586010/%EC%82%AC%EC%9D%B4%EB%93%9C%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EC%A7%84%ED%96%89%ED%95%98%EC%8B%A4-%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%94%EB%93%9C-%ED%95%9C-%EB%B6%84-%EA%B5%AC%ED%95%A9%EB%8B%88%EB%8B%A4",
    "",
    false
  ],
  "ko-ownedmall": [
    "카페24 뉴스룸",
    "농심몰의 D2C 전략",
    "https://news.cafe24.com/kr/nongshim-mall-catches-the-attention-of-mz-fansumers-with-d2c-strategy/",
    "",
    false
  ],
  "ko-smartstore": [
    "스마트스토어 운영자 · 예스24 리뷰",
    "스마트스토어 실무서 리뷰 · 스스",
    "https://m.yes24.com/Goods/Review/119578288",
    "",
    false
  ],
  "ko-cut": [
    "편집 서비스 제공자 · 크몽",
    "컷편집·자막편집 서비스",
    "https://kmong.com/gig/512681",
    "",
    false
  ],
  "ko-onlineedit": [
    "종합편집 실무자 · 크몽",
    "종합편집 서비스",
    "https://kmong.com/gig/471440",
    "",
    false
  ],
  "ko-dp": [
    "촬영팀 구인자 · 필름메이커스",
    "뷰티브랜드 TVC 촬영팀 구인",
    "https://www.filmmakers.co.kr/proCrewRecruiting/30246913",
    "",
    false
  ],
  "ko-live": [
    "민경아 공식 위버스",
    "라이브 방송 목록 · 라방",
    "https://weverse.io/minkyoungah/live",
    "",
    false
  ],
  "ko-onair": [
    "홍은채 · 공식 위버스",
    "사녹·생방 참여 기록",
    "https://weverse.io/lesserafim/artist/2-6245",
    "",
    false
  ],
  "ko-card": [
    "직장인 작성자 · 블라인드",
    "법인카드 영수증 정리",
    "https://theqoo.net/job/3895720030",
    "",
    false
  ],
  "ko-office": [
    "효성",
    "직장인 용어사전",
    "https://blog.hyosung.com/4080",
    "2018-07-09",
    false
  ],
  "ko-process": [
    "스튜디오 모락",
    "기업 홍보영상 제작 과정",
    "https://studiomorak.com/insights/corporate-video-production-process",
    "2026-08-04",
    false
  ]
}''')

SOURCES.update({
 'ko-test-short': ('thinkhub · 서비스기획 기록', '단테·통테 표기 사용 사례', 'https://thinkhubhee.tistory.com/32', '2024-08-20', False),
 'ko-regex': ('MDN Web Docs', '정규식', 'https://developer.mozilla.org/ko/docs/Glossary/Regular_expression', '', False),
 'ko-remote': ('다우오피스HR', '재택근무 안내 · 재택 호칭', 'https://hr.daouoffice.com/blog/work-from-home-employment-contract/', '2026-07-14', False),
})
SOURCES['ko-card']=('직장인 작성자 · 더쿠','법카·지결 현장 사용 사례','https://theqoo.net/job/3895720030','',False)

GROUPS = [
('dev', '개발 표현 줄임말', 'ko-regex', '''
정규식|Regular expression|정규 표현식;정규표현식;regex;regexp|정규 표현식을 짧게 부르는 말. 일정한 문자 패턴을 표현하여 문자열을 찾거나 검사할 때 쓴다.|입력한 코드의 형식을 정규식으로 검사해요.|문자 패턴 찾아내는 표현;정규표현식 줄임말
'''),
('common,dev,design,marketing,fashion,film', '근무 줄임말', 'ko-remote', '''
재택|Work from home|재택근무;재택 근무;WFH|근무 일정에서 재택근무를 짧게 부르는 말. 사무실에 출근하는 대신 집에서 일하는 방식.|내일은 재택이라 회의에 온라인으로 참여해요.|집에서 일하는 근무;재택근무 줄임말
'''),
('common', '직장·경력 줄임말', 'ko-office', '''
취준생||취업준비생;취업 준비생|취업준비생의 줄임말. 입사를 목표로 채용 전형이나 필요한 역량을 준비하는 사람.|취준생 대상 직무 설명회를 준비해요.|취업 준비하는 사람 줄임말
퇴준생||퇴사준비생;퇴사 준비생|퇴사준비생의 줄임말. 재직하면서 퇴사 이후의 진로나 생활을 준비하는 사람을 가리키는 비공식 표현.|퇴준생 인터뷰에서 이직을 결심한 계기를 물었어요.|회사 다니면서 퇴사 준비하는 사람
'''),
('marketing,fashion', '광고·매체 줄임말', 'ko-brand', '''
브검|Brand search advertising|브랜드 검색 광고;브랜드검색광고;브랜드검색|브랜드 검색 광고의 줄임말. 브랜드명 등을 검색한 사람에게 브랜드 소개와 연결 링크를 보여 주는 광고.|브검 소재를 여름 컬렉션 이미지로 바꿔주세요.|브랜드 이름 검색할 때 맨 위 광고;브랜드검색 줄임말
'''),
('marketing,fashion', '광고·매체 줄임말', 'ko-shoppingad', '''
쇼검|Shopping search advertising|쇼핑 검색 광고;쇼핑검색광고;쇼핑검색|쇼핑 검색 광고를 줄인 말. 상품 정보와 이미지를 검색 결과 등의 광고 지면에 노출하는 광고.|쇼검에 연결된 상품명과 품절 상태를 확인해요.|쇼핑검색 줄임말;상품 사진이 뜨는 검색 광고
'''),
('marketing,fashion,design', '콘텐츠·제작 줄임말', 'ko-detail', '''
상페|Product detail page|상세페이지;상세 페이지;상품 상세페이지|상세페이지의 줄임말. 상품 특징·구성·이용 정보를 설명하는 판매 페이지.|상페 첫 화면에 소재와 핏이 잘 보이게 해주세요.|상품을 자세히 설명하는 페이지;상세페이지 줄임말
'''),
('marketing,fashion,design,film', '매체 줄임말', 'sl-ampm-variation', '''
인스타|Instagram|인스타그램;Instagram|인스타그램을 줄여 부르는 말. 브랜드 콘텐츠와 광고를 운영하는 소셜미디어 채널 중 하나.|인스타에 올릴 새 컬렉션 콘텐츠를 준비해요.|인스타그램 줄임말;사진과 릴스 올리는 채널
페북|Facebook|페이스북;Facebook|페이스북을 줄여 부르는 말. 페이지·게시물·광고 등의 업무에서 쓰는 채널 이름.|페북 게시물용 이미지도 함께 전달해주세요.|페이스북 줄임말;페북용 광고 소재
'''),
('marketing,fashion', '판매·유통 줄임말', 'ko-groupbuy', '''
공구|Group buying|공동구매;공동 구매;공구 마케팅|공동구매의 줄임말. 참여자를 모아 정해진 조건이나 기간에 상품을 함께 판매·구매하는 방식.|이번 공구의 수량과 배송 일정을 먼저 확정해요.|여럿이 함께 사는 행사;공동구매 줄임말
'''),
('marketing,fashion', '판매·유통 줄임말', 'ko-livecommerce', '''
라방|Live commerce|라이브 방송;라이브방송;라이브 커머스;라이브커머스|라이브 방송의 줄임말. 판매 업무에서는 실시간 방송으로 상품을 소개하고 주문을 받는 라이브 커머스를 가리키기도 한다.|라방 전에 사이즈별 재고를 확인해요.|실시간으로 옷 보여주며 판매;방송 보면서 구매하는
'''),
('film', '방송 줄임말', 'ko-live', '''
라방|Live broadcast|라이브 방송;라이브방송|라이브 방송의 줄임말. 촬영과 송출이 실시간으로 이어지는 온라인 방송을 말한다.|오늘 라방은 출연자와 실시간 질의응답으로 진행해요.|실시간 인터넷 방송;라이브방송 줄임말
'''),
('marketing,fashion', '판매·유통 줄임말', 'ko-smartstore', '''
스스|Naver Smart Store|스마트스토어;스마트 스토어;네이버 스마트스토어|스마트스토어를 줄여 부르는 판매자들의 표현. 네이버의 온라인 판매점 서비스를 뜻한다.|스스 상품 옵션을 자사몰과 맞춰주세요.|스마트스토어 줄임말;네이버에 만든 판매점
'''),
('marketing,fashion,dev,design', '온라인 판매', 'ko-ownedmall', '''
자사몰|Brand-owned online store|자사 쇼핑몰;자사쇼핑몰;자체 쇼핑몰|회사가 직접 운영하는 온라인 쇼핑몰을 짧게 부르는 말.|자사몰 상세페이지 개편 일정을 공유해요.|우리 회사가 직접 운영하는 쇼핑몰;브랜드 자체 온라인 매장
'''),
('marketing,fashion', '판매·유통 줄임말', 'ko-free', '''
무배|Free shipping|무료배송;무료 배송|무료배송의 줄임말. 구매자가 배송비를 별도로 부담하지 않는 조건을 말한다.|무배 적용 금액을 배너에 함께 적어주세요.|배송료가 없는 조건;무료배송 줄임말
'''),
('fashion', '소재 줄임말', 'ko-clothes', '''
폴리|Polyester|폴리에스터;폴리에스테르;polyester|의류 원단 업무에서 폴리에스터를 짧게 부르는 말.|이 원단은 폴리 비율이 높아요.|폴리에스터 줄임말;원단 성분에 폴리라고 적힌
스판|Spandex|스판덱스;폴리우레탄 탄성섬유;elastane|스판덱스를 짧게 부르는 말. 원단에 신축성을 주는 탄성섬유를 뜻하며, 신축성 있는 원단을 넓게 지칭하기도 한다.|스판 함량과 늘어나는 방향을 확인해주세요.|쭉 늘어나는 옷감의 성분;스판덱스 줄임말
'''),
('fashion', '상품 정보·치수', 'ko-length', '''
총장|Garment length|전체 길이;총기장;옷 전체 길이|옷의 전체 길이를 가리키는 치수 표기. 시작점과 끝점은 품목과 측정 기준에 따라 정한다.|샘플 총장은 목옆점부터 밑단까지 측정해주세요.|옷 전체 길이를 뭐라고;치수표의 총장
'''),
('fashion', '상품 관리 줄임말', 'ko-product', '''
품명|Product name|품목명;제품명;상품명|품목의 이름을 짧게 부르는 말. 번호로 구분하는 품번과 달리 제품 이름을 표시한다.|발주서에 품명과 품번을 함께 적어주세요.|품목 이름의 줄임말;상품 이름과 번호 구분
'''),
('fashion,marketing', '소비자·스타일 표현', 'ko-fashiontrend', '''
얼죽코||얼어 죽어도 코트|추워도 코트를 고집한다는 뜻의 줄임말. 스타일 취향을 표현하는 소비자 신조어.|코트 콘텐츠 제목에 얼죽코라는 표현을 썼어요.|겨울에도 코트만 입는 취향;얼어 죽어도 코트
얼죽크||얼어 죽어도 크롭|추워도 짧은 기장의 크롭 스타일을 즐긴다는 뜻의 줄임말.|크롭 상의 기획에 얼죽크 스타일 이미지를 참고해요.|추워도 짧은 상의 입는;얼어 죽어도 크롭
추구미||추구하는 아름다움;지향하는 이미지|자신이 추구하는 아름다움이나 닮고 싶은 스타일을 가리키는 합성 표현.|타깃 고객의 추구미를 무드보드로 정리해요.|내가 닮고 싶은 분위기;추구하는 스타일
'''),
('film,marketing,fashion', '촬영 준비 줄임말', 'ko-hair', '''
헤메|Hair and makeup|헤어 메이크업;헤어메이크업;헤어·메이크업;헤메팀|헤어와 메이크업을 묶어 짧게 부르는 말. 촬영 준비 작업이나 그 담당팀을 가리킨다.|첫 촬영 한 시간 전에 헤메를 시작해요.|촬영 전에 머리와 화장을 하는;헤어메이크업 줄임말
'''),
('film,marketing,fashion', '촬영 인력 줄임말', 'ko-dp', '''
촬감|Director of photography|촬영감독;촬영 감독;DP;DOP|촬영감독의 줄임말. 카메라와 촬영 방식 등 화면의 기술적·시각적 구현을 맡는 책임자.|촬감님과 제품 클로즈업 구도를 상의해요.|촬영감독 줄임말;카메라 촬영 책임자
'''),
('film,marketing,design', '편집 줄임말', 'ko-onlineedit', '''
종편|Online editing|종합편집;종합 편집|종합편집의 줄임말. 영상에 자막·그래픽·음향 등을 반영해 납품 형태로 마무리하는 작업.|자막 수정까지 반영한 종편본을 전달해주세요.|편집 마지막에 자막 효과 합치는;종합편집 줄임말
'''),
('film,marketing,design', '편집 줄임말', 'ko-cut', '''
컷편|Cut editing|컷편집;컷 편집|컷편집의 줄임말. 사용할 장면을 고르고 자르거나 이어 영상 흐름을 만드는 작업.|컷편을 먼저 확정한 뒤 자막을 넣어요.|장면을 자르고 이어 붙이는;컷편집 줄임말
'''),
('film', '방송 줄임말', 'ko-broadcast', '''
사녹|Pre-recording|사전녹화;사전 녹화|사전녹화의 줄임말. 실제 방송 시점보다 앞서 장면이나 공연을 녹화하는 것.|사녹 시작 전에 출연자 동선을 확인해요.|방송 전에 미리 녹화하는;사전녹화 줄임말
본방|Original broadcast|본방송;본 방송|본방송의 줄임말. 재방송과 구별하여 예정된 회차를 처음 내보내는 방송.|본방 송출 시간을 기준으로 최종본을 전달해요.|본방송 줄임말;재방송이 아닌 첫 방송
공방|Public broadcast|공개방송;공개 방송|공개방송의 줄임말. 관객이 현장에 참여할 수 있도록 공개해서 진행하는 방송.|공방 관객 입장과 카메라 동선을 분리해요.|공개방송 줄임말;관객이 참여하는 방송
'''),
('film', '방송 줄임말', 'ko-onair', '''
생방|Live broadcast|생방송;생 방송|생방송의 줄임말. 현장의 영상이나 음성을 진행과 거의 동시에 내보내는 방송.|생방 시작 전에 송출 상태를 점검해요.|생방송 줄임말;녹화하지 않고 바로 방송
'''),
('design,film,marketing,fashion', '제작 도구 줄임말', 'ko-photoshop', '''
포샵|Adobe Photoshop|포토샵;포토숍;Photoshop;포샵 작업|포토샵을 짧게 부르는 말. 사진 보정이나 이미지 합성 작업을 가리키는 말로도 쓴다.|포샵에서 제품 사진의 먼지를 정리했어요.|포토샵 줄임말;사진 합성하고 보정하는 프로그램
'''),
('design,film,marketing,fashion', '제작 도구 줄임말', 'ko-illustrator', '''
일러|Adobe Illustrator|일러스트레이터;어도비 일러스트레이터;Illustrator|도구를 말하는 문맥에서 어도비 일러스트레이터를 줄여 부르는 말. 로고·도형 등 벡터 그래픽 제작에 사용한다.|일러 원본에 로고 수정 내용을 반영해주세요.|일러스트레이터 줄임말;벡터 로고 만드는 프로그램
'''),
('design,film,marketing', '제작 도구 줄임말', 'ko-effects', '''
에펙|Adobe After Effects|애프터 이펙트;애프터이펙트;에프터 이펙트;에프터이펙트;After Effects|애프터 이펙트를 줄여 부르는 말. 모션그래픽과 영상 합성 등에 사용하는 제작 도구.|에펙에서 로고 등장 모션을 만들어요.|애프터이펙트 줄임말;로고 움직이는 영상 제작 도구
'''),
('design,dev,marketing,fashion,film,common', '작업·경력 줄임말', 'ko-portfolio', '''
포폴|Portfolio|포트폴리오;포트 폴리오|포트폴리오의 줄임말. 수행한 프로젝트와 자신의 역할·결과를 모아 보여 주는 자료.|포폴에 이번 프로젝트에서 맡은 역할을 적었어요.|작업 결과 모아 보여주는 자료;포트폴리오 줄임말
'''),
('dev', '채용·학습 줄임말', 'ko-coding', '''
코테|Coding test|코딩 테스트;코딩테스트|코딩 테스트의 줄임말. 주어진 문제를 코드로 해결하는 능력을 확인하는 평가.|코테 연습에서는 풀이가 맞는 이유도 설명해봐요.|코딩시험 줄임말;코드로 문제 푸는 채용 시험
'''),
('dev', '채용·학습 줄임말', 'ko-computer', '''
컴공|Computer engineering|컴퓨터공학;컴퓨터 공학;컴퓨터공학과|컴퓨터공학이나 컴퓨터공학과를 줄여 부르는 말.|컴공 전공에서 배운 내용을 실무와 연결해보고 있어요.|컴퓨터공학과 줄임말;개발자 전공을 짧게 부르는
'''),
('dev', '채용·학습 줄임말', 'ko-certificate', '''
정처기||정보처리기사;정보 처리 기사|정보처리기사 자격을 줄여 부르는 말.|정처기 공부한 내용을 개발 기초 복습에 활용해요.|정보처리기사 줄임말;개발 자격증 정처기
'''),
('dev', '개발 언어 줄임말', 'ko-ts', '''
타스|TypeScript|타입스크립트;타입 스크립트;TypeScript;TS|타입스크립트를 짧게 부르는 말. 자바스크립트에 타입 표현과 검사를 더한 언어.|다음 기능은 타스로 작성하기로 했어요.|타입스크립트 줄임말;자바스크립트에 타입 붙인 언어
'''),
('dev,design', '개발 협업 줄임말', 'ko-fullstack', '''
프론트|Frontend|프론트엔드;프런트엔드;프론트 엔드;FE|프론트엔드를 짧게 부르는 말. 사용자가 직접 보는 화면과 그 상호작용을 구현하는 영역.|디자인 변경 사항을 프론트 담당자에게 전달해요.|사용자가 보는 화면 만드는 개발;프론트엔드 줄임말
'''),
('dev', '데이터 줄임말', 'ko-db', '''
디비|Database|DB;데이터베이스;데이터 베이스|DB를 한국어로 읽는 현장 호칭. 데이터를 체계적으로 저장하고 조회하는 데이터베이스를 뜻한다.|디비에 저장된 상품 옵션을 확인해요.|데이터베이스를 짧게 부르는;디비 뜻
'''),
('dev,design,marketing,fashion,film,common', '협업·수정 줄임말', 'ko-db', '''
원복|Restore to previous state|원상복구;원상 복구;원복하다|원상복구를 짧게 부르는 말. 변경한 작업물이나 설정을 이전 상태로 되돌리는 것.|비교 검토를 위해 이전 버전으로 원복해주세요.|수정 전 상태로 돌리는;원상복구 줄임말
'''),
('dev,design,marketing,fashion,film,common', '문서·작업 줄임말', 'ko-copy', '''
복붙|Copy and paste|복사 붙여넣기;복사하여 붙여넣기;복사·붙여넣기;복붙하다|복사와 붙여넣기를 묶어 짧게 부르는 말. 글·코드·이미지 등을 복제해 다른 위치에 넣는 작업.|지난 문구를 복붙한 뒤 바뀐 날짜를 수정해요.|복사해서 붙이는 작업;복사 붙여넣기 줄임말
'''),
('dev,design,marketing,fashion,film,common', '프로젝트 줄임말', 'ko-project', '''
플젝|Project|프로젝트;플젝 진행|프로젝트를 짧게 부르는 비공식 표현. 정해진 목표를 위해 수행하는 작업 단위를 말한다.|이번 플젝의 담당자와 일정을 공유해요.|프로젝트 줄임말;같이 진행하는 작업
'''),
('common,dev,design,marketing,fashion,film', '경력·채용 줄임말', 'ko-resume', '''
자소서|Personal statement|자기소개서;자기 소개서|자기소개서의 줄임말. 지원 동기와 경험 등을 글로 설명하는 채용 자료.|자소서에 프로젝트에서 해결한 문제를 적었어요.|자기소개서 줄임말;입사 지원할 때 쓰는 소개글
'''),
('common,marketing,fashion,dev,design,film', '비용·문서 줄임말', 'ko-expense,ko-office', '''
지결|Expense approval|지출결의;지출 결의;지출결의서;지결서|지출결의 또는 그 문서를 줄여 부르는 말. 사용하거나 사용할 비용의 내역과 증빙을 정리해 승인을 받는 업무.|영수증을 첨부해 지결을 올려주세요.|지출결의서 줄임말;회사 비용 승인 문서
'''),
('common,marketing,fashion,dev,design,film', '비용 줄임말', 'ko-card', '''
법카|Corporate card|법인카드;법인 카드|법인카드의 줄임말. 회사의 업무 비용을 결제하는 카드를 말한다.|촬영 소품은 법카로 결제하고 증빙을 챙겨요.|법인카드 줄임말;회사 카드
'''),
('common,dev,design,marketing,fashion,film', '근무 표현', 'ko-leave', '''
칼퇴||칼퇴근;정시 퇴근|정해진 퇴근 시간에 맞춰 바로 퇴근하는 것을 짧게 부르는 말.|오늘은 일정을 맞춰 마무리하고 칼퇴할게요.|퇴근 시간 되자마자 나가는;칼퇴근 줄임말
'''),
('common,dev,design,marketing,fashion,film', '근무 표현', 'ko-office', '''
워라밸|Work-life balance|워크 라이프 밸런스;일과 삶의 균형|워크 라이프 밸런스를 줄인 말. 업무와 개인 생활 사이의 균형을 뜻한다.|일정 계획을 세울 때 팀의 워라밸도 고려해요.|일과 생활 균형;워라밸 뜻
'''),
('marketing,fashion', '소비자 표현', 'ko-office', '''
가성비|Value for money|가격 대비 성능;가격대비성능|가격과 비교해 성능이나 효용이 어느 정도인지 나타내는 줄임말.|실용성과 가격을 함께 보여주는 가성비 기획을 준비해요.|가격 대비 성능 줄임말;싸고 쓸 만한 정도
가심비||가격 대비 심리적 만족;가격 대비 만족|가격 대비 얻는 심리적 만족을 가리키는 줄임말. 기능 외에 취향이나 감정적 만족을 강조한다.|패키지가 주는 가심비를 고객 인터뷰에서 살펴봐요.|가격보다 마음의 만족을 중시하는;가격 대비 심리적 만족
'''),
]

# Reuse topic filters instead of creating a separate topic for each shortform family.
TOPICS = {
 '개발 표현 줄임말':'웹·프로그래밍','근무 줄임말':'조직·일하는 방식',
 '직장·경력 줄임말':'경력·채용','광고·매체 줄임말':'광고 운영',
 '콘텐츠·제작 줄임말':'상품 소개','매체 줄임말':'미디어 전략',
 '판매·유통 줄임말':'판매·운영','방송 줄임말':'방송·구성',
 '온라인 판매':'판매·운영','소재 줄임말':'봉제·제작 현장',
 '상품 정보·치수':'샘플·피팅','상품 관리 줄임말':'상품기획·직무',
 '소비자·스타일 표현':'고객 이해','촬영 준비 줄임말':'제작·기획',
 '촬영 인력 줄임말':'제작·기획','편집 줄임말':'편집',
 '제작 도구 줄임말':'제작 도구','작업·경력 줄임말':'경력·채용',
 '채용·학습 줄임말':'경력·채용','개발 언어 줄임말':'웹·프로그래밍',
 '개발 협업 줄임말':'개발 협업','데이터 줄임말':'웹·프로그래밍',
 '협업·수정 줄임말':'협업·커뮤니케이션','문서·작업 줄임말':'협업·커뮤니케이션',
 '프로젝트 줄임말':'회의·협업','경력·채용 줄임말':'경력·채용',
 '비용·문서 줄임말':'비용·정산','비용 줄임말':'비용·정산',
 '근무 표현':'조직·일하는 방식','소비자 표현':'고객 이해',
}
GROUPS = [(fields,TOPICS[category],source,raw) for fields,category,source,raw in GROUPS]

# field, existing headword, additional search spellings, evidence source(s)
ALIAS_UPDATES = [
 ('dev','단위 테스트',['단테'],'ko-test-short'),
 ('dev','통합 테스트',['통테'],'ko-test-short'),
 ('fashion','테크팩',['작지'],'ko-workorder'),
 ('fashion','품번',['품목 번호','품목번호'],'ko-product'),
 ('dev','JavaScript',['자스'],'ko-js'),
 ('design','타이포그래피',['타이포'],'ko-typo'),
 ('film','러프 컷',['가편','가편본','가편집본'],'ko-process'),
]

NOTES = {
 '종편':'여기서는 종합편집을 뜻합니다. 방송 매체를 말할 때의 종합편성채널과는 구별합니다. 작업 범위는 제작사마다 다를 수 있습니다.',
 '본방':'본방송이 반드시 생방송이라는 뜻은 아닙니다. 사전 제작한 영상의 첫 방송도 본방송입니다.',
 '공방':'방송 업무에서의 뜻입니다. 물건을 만드는 작업 공간인 공방과 구별합니다.',
 '일러':'그림 자체를 말하는 문맥에서는 일러스트레이션을 줄여 부르는 경우도 있으므로 도구명인지 확인합니다.',
 '스판':'소재의 정확한 종류와 혼용률은 라벨·사양서로 확인합니다. 스판이라는 말만으로 모든 탄성 소재를 같은 성분으로 보지 않습니다.',
 '원복':'업무별로 되돌리는 대상은 다릅니다. 개발에서는 코드·설정·데이터를, 제작에서는 시안·편집본 등을 가리킬 수 있습니다.',
 '지결':'회사별로 지출 전 승인과 지출 후 정산 절차 및 서식 이름이 다릅니다.',
 '라방':'라이브 방송의 줄임말이며, 방송에 판매 기능이 있는지는 문맥에 따라 다릅니다.',
 '추구미':'순수한 두문자 약어가 아닌 합성 표현으로, 소비자와 스타일을 이해하기 위한 항목입니다.',
 '얼죽크':'2024년 패션 기사에 기록된 소비자 표현입니다. 모든 패션 회사의 공식 업무 용어라는 뜻은 아닙니다.',
}
