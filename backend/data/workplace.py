"""Workplace collection. Definitions and examples are original editorial text.

Fields in a group are an explicit inclusion list, not a deduplication hint.
Identical meanings are intentionally retained in each relevant industry.
English documentation supports concepts, not claims of universal Korean usage.
"""
SOURCES = {
 'agency-roles':('HSAD','People: 광고·크리에이티브·미디어 직무','https://www.hsad.co.kr/kor/about/people','',False),
 'agency-client':('오픈애즈 · 실무자 기고','대행사 vs 브랜드사','https://openads.co.kr/content/contentDetail?contsId=2742','',False),
 'agency-rfp':('오픈애즈 · 실무자 기고','마케터, 어떤 광고 대행사를 선택해야 후회가 없을까?','https://www.openads.co.kr/content/contentDetail?contsId=2423','',False),
 'agency-display':('오픈애즈 · 실무자 기고','가맹 마케팅: 디스플레이 광고','https://www.openads.co.kr/content/contentDetail?contsId=14232','',False),
 'design-service':('디스페이스','브랜드·패키지 디자인 서비스','https://www.despace.kr/service','',False),
 'design-production':('Coloso · 문영','앨범 디자인 & 굿즈 포트폴리오 실무','https://coloso.co.kr/products/graphicdesign-moonyoung2','',False),
 'creative-brief':('Asana','Creative briefs: what to include','https://asana.com/resources/how-write-creative-brief-examples-template','',False),
 'work-kickoff':('Asana','효과적인 프로젝트 킥오프 미팅','https://asana.com/ko/resources/project-kickoff-meeting','',False),
 'work-agenda':('Asana','Meeting agenda templates and examples','https://asana.com/resources/meeting-agenda','',False),
 'work-terms':('Asana','Project management terms','https://asana.com/ko/resources/project-management-terms','',False),
 'work-scope':('Asana','Project scope','https://asana.com/resources/project-scope','',False),
 'work-milestone':('Asana','Project milestones','https://asana.com/resources/project-milestones','',False),
 'work-deliver':('Asana','What are project deliverables?','https://asana.com/resources/what-are-project-deliverables','',False),
 'brand-strategy':('Mailchimp','Brand marketing','https://mailchimp.com/resources/brand-marketing/','',False),
 'brand-manager':('Mailchimp','What is a brand manager?','https://mailchimp.com/marketing-glossary/brand-manager/','',False),
 'brand-media':('Mailchimp','Owned media','https://mailchimp.com/resources/owned-media/','',False),
 'brand-alignment':('Mailchimp','Brand alignment','https://mailchimp.com/resources/brand-alignment/','',False),
 'fashion-roles':('삼성물산 패션부문','채용안내: 주요 직무','https://www.samsungfashion.com/recruitGuide.do?TAB_ID=3','',False),
 'fashion-md':('Shopify','Fashion merchandising','https://www.shopify.com/blog/fashion-merchandising','',False),
 'wholesale':('Shopify','Wholesale terminology glossary','https://www.shopify.com/blog/wholesale-terminology','',False),
 'retail':('Shopify','Retail vocabulary guide','https://www.shopify.com/blog/retail-terms','',False),
 'retail-otb':('Shopify','Open-to-buy plans','https://www.shopify.com/blog/open-to-buy-plans','',False),
 'retail-performance':('Shopify','Product merchandising','https://www.shopify.com/blog/product-merchandising','',False),
 'retail-reorder':('Shopify','Reorder point formula','https://www.shopify.com/blog/reorder-point','',False),
 'fashion-linesheet':('Techpacker','How to create a fashion line sheet','https://techpacker.com/blog/design/how-to-create-a-fashion-line-sheet/','',False),
 'techpack':('Techpacker','How to create a tech pack for a baseball jacket','https://techpacker.com/blog/design/how-to-make-a-clothing-tech-pack/','',False),
 'techpack-details':('Techpacker','Tech packs for fashion startups','https://techpacker.com/blog/design/how-to-create-tech-packs-fashion-startups/','',False),
 'techpack-fit':('Techpacker','Garment fitting and fit sign-off process','https://techpacker.com/blog/manufacturing/end-to-end-garment-fitting-and-fit-sign-off-process/','',False),
 'techpack-settings':('Techpacker','Define and edit techpack settings','https://documentation.techpacker.com/techpack/edit.html','',False),
 'techpack-grading':('Techpacker','Grading','https://documentation.techpacker.com/add-ons/grading.html','',False),
 'dev-epic':('Atlassian','Epics, stories and initiatives','https://www.atlassian.com/agile/project-management/epics-stories-themes','',False),
 'dev-done':('Atlassian','Definition of done','https://www.atlassian.com/agile/project-management/definition-of-done','',False),
 'dev-debt':('Atlassian','Technical debt','https://www.atlassian.com/agile/software-development/technical-debt','',False),
 'dev-roles':('Atlassian','Agile scrum roles','https://www.atlassian.com/agile/scrum/roles','',False),
 'dev-ci':('Atlassian','Continuous integration','https://www.atlassian.com/continuous-delivery/continuous-integration','',False),
 'dev-cd':('Atlassian','Integration vs delivery vs deployment','https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment','',False),
 'dev-gitflow':('Atlassian','Gitflow workflow','https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow','',False),
 'dev-tests':('Atlassian','Types of software testing','https://www.atlassian.com/continuous-delivery/software-testing/types-of-software-testing','',False),
 'design-variants':('Figma','Create and use variants','https://help.figma.com/hc/en-us/articles/360056440594-Create-and-use-variants','',False),
 'design-tokens':('Figma','Tokens, variables and styles','https://help.figma.com/hc/en-us/articles/18490793776023-Update-1-Tokens-variables-and-styles','',False),
 'design-system':('Figma','Define your design system','https://help.figma.com/hc/en-us/articles/14552740206743-Lesson-2-Define-your-design-system','',False),
 'print-marks':('Adobe','Printer’s marks and bleeds','https://helpx.adobe.com/illustrator/using/printers-marks-bleeds.html','',False),
}

GROUPS = [
('marketing,dev,fashion,design,common','현장 표현','제안·협업','agency-client','''
PT|Presentation|피티;프레젠테이션;프리젠테이션|기획이나 제안을 설명하는 발표.|내일 PT에서 기획 의도를 설명해요.|제안 내용 발표하는;기획안을 발표
컨펌|Confirmation|컴펌;confirm;확인 승인|내용을 확인하거나 진행을 승인하는 것.|제작 전에 담당자 컨펌을 받아요.|진행해도 되는지 승인;최종 확인 받기
'''),
('marketing','현장 표현','대행사 제안','agency-client','''
경쟁 PT|Competitive presentation|경쟁피티;경쟁 프레젠테이션;비딩 PT|여러 업체가 수주를 위해 제안을 발표하는 심사.|경쟁 PT에 낼 전략을 점검해요.|대행사 뽑는 발표;여러 업체 제안 경쟁
수주|Winning a contract|프로젝트 수주|발주처의 일감을 계약으로 따내는 것.|이번 브랜드 캠페인을 수주했어요.|일감을 따내는;제안해서 계약 따기
'''),
('marketing,dev,design','전문 용어','제안·협업','agency-rfp','''
RFP|Request for proposal|제안요청서;알에프피|업체에 필요한 과업과 제안 조건을 알리는 문서.|RFP의 요구사항부터 확인해요.|업체에 제안 요청하는 문서;제안 조건이 적힌
제안서|Proposal|프로포절|문제 해결 방법과 수행 계획을 제시하는 문서.|제안서에 일정과 수행 범위를 넣어요.|프로젝트를 맡기 위해 쓰는 문서
'''),
('marketing,fashion,design','전문 용어','브랜드 제작','design-service','''
시안|Design draft|디자인 시안;초안;시안 작업|방향을 검토하기 위해 먼저 만든 디자인 안.|시안 두 가지를 비교해 주세요.|완성 전에 보여주는 디자인;디자인 후보안
키비주얼|Key visual|키 비주얼;KV;케이비주얼;키비쥬얼|캠페인이나 브랜드를 대표하는 중심 시각 이미지.|키비주얼을 배너와 패키지에 적용해요.|캠페인 대표 이미지;중심이 되는 비주얼
브랜드 가이드|Brand guidelines|브랜드 가이드라인;브랜드 가이드북|로고·색·글꼴 등의 사용 규칙을 정리한 자료.|브랜드 가이드에 맞춰 로고 여백을 지켜요.|브랜드 디자인 사용 규칙;로고 색상 규정
네이밍|Naming|브랜드 네이밍;제품명 기획|브랜드나 상품의 이름을 기획하는 작업.|신제품 네이밍 후보를 검토해요.|상품 이름 짓는;브랜드 이름 만들기
패키지 디자인|Packaging design|패키지;패키징 디자인|상품 포장에 필요한 형태와 시각 표현을 설계하는 작업.|패키지 디자인에 제품명을 반영해요.|제품 포장 디자인;상자 겉면 디자인
'''),
('marketing,fashion,design','전문 용어','브랜드 제작','creative-brief','''
브리프|Creative brief|브리핑 문서;크리에이티브 브리프|제작 목표·대상·핵심 요구를 요약한 문서.|브리프를 보고 시안 방향을 잡아요.|만들기 전에 요구사항 요약;제작 방향 정리 문서
키메시지|Key message|핵심 메시지;키 메시지|대상에게 가장 먼저 전달하려는 핵심 내용.|키메시지는 한 문장으로 정리해요.|가장 전하고 싶은 말;광고에서 핵심으로 말하는
'''),
('marketing,dev,fashion,design,common','현장 표현','회의·협업','work-kickoff','''
킥오프|Kickoff|킥오프 미팅;킥 오프|시작할 일의 목표·역할·일정을 맞추는 첫 회의.|킥오프에서 각 팀 역할을 정해요.|프로젝트 시작 회의;일 시작 전에 모이는
'''),
('marketing,dev,fashion,design,common','현장 표현','회의·협업','work-agenda','''
어젠다|Agenda|아젠다;회의 안건;의제|회의에서 논의할 주제와 순서.|회의 전에 어젠다를 공유해요.|회의에서 이야기할 주제;오늘 회의 안건
액션 아이템|Action item|액션아이템;후속 할 일|논의 후 담당자가 실행해야 할 구체적인 일.|액션 아이템마다 담당자를 적어요.|회의 끝나고 해야 할 일;논의 후 실행할 작업
'''),
('marketing,dev,fashion,design,common','전문 용어','일정·범위','work-scope','''
스코프|Project scope|업무 범위;과업 범위|이번 일에 포함할 작업과 결과의 범위.|추가 요청은 기존 스코프에 포함되는지 확인해요.|어디까지 해야 하는 일;이번 작업 범위
'''),
('marketing,dev,fashion,design,common','전문 용어','일정·범위','work-milestone','''
마일스톤|Milestone|주요 일정;중간 이정표|진행 상태를 판단하는 중요한 완료 지점.|중간 승인일을 마일스톤으로 잡아요.|프로젝트 중간 목표 지점;중요한 완료 시점
'''),
('marketing,dev,fashion,design,common','전문 용어','일정·범위','work-deliver','''
산출물|Deliverable|딜리버러블;결과물;납품물|업무를 통해 만들어 전달하기로 한 결과물.|최종 산출물 목록을 먼저 합의해요.|마지막에 납품할 결과;작업해서 전달하는 것
'''),
('marketing,dev,fashion,design,common','현장 표현','일정·범위','work-terms','''
리소스|Resource|인력과 자원;가용 자원|일에 투입할 사람·시간·예산 등의 자원.|이번 주에 쓸 수 있는 리소스를 확인해요.|작업할 사람과 시간;투입 가능한 인력
'''),
('marketing','전문 용어','대행사 직무','agency-roles','''
AE|Account executive|에이이;광고기획자|광고주와 소통하며 캠페인 진행을 조율하는 담당자.|AE가 광고주 요청을 제작팀에 전달해요.|광고주와 소통하는 사람;광고 프로젝트 담당
AP|Account planner|어카운트 플래너;전략 플래너|소비자·시장 조사로 브랜드 전략을 세우는 역할.|AP가 소비자 조사에서 전략 방향을 찾았어요.|광고 전략 세우는 사람;소비자 조사 기획자
미디어 플래닝|Media planning|매체 기획;미디어플래닝|목표에 맞춰 매체와 광고 예산을 계획하는 일.|미디어 플래닝 단계에서 매체 비중을 정해요.|어느 매체에 얼마 쓸지;광고 매체 계획
미디어 바잉|Media buying|매체 구매;미디어바잉|광고 지면·시간·노출을 구매하는 일.|미디어 바잉 담당자가 집행 조건을 협의해요.|광고 자리 구매;매체 광고 단가 협상
프로모션|Promotion|판촉;프로모션 기획|구매나 참여를 촉진하기 위해 벌이는 활동.|체험 행사 프로모션을 준비해요.|구매 촉진 행사;고객 참여 이벤트
PR|Public relations|피알;홍보;퍼블릭 릴레이션스|대중·언론 등과 관계를 만들고 소통하는 활동.|브랜드 PR 계획에 언론 소통을 넣어요.|언론과 대중에게 알리기;기업 홍보 활동
'''),
('marketing,design','전문 용어','크리에이티브 직무','agency-roles','''
아트 디렉터|Art director|AD;아트디렉터|프로젝트의 시각 표현 방향을 이끄는 역할.|아트 디렉터와 이미지 방향을 맞춰요.|비주얼 방향을 총괄하는 사람
카피라이터|Copywriter|CW;카피 라이터|광고·브랜드 메시지를 문장으로 만드는 역할.|카피라이터가 헤드라인을 제안해요.|광고 문구 쓰는 사람
'''),
('marketing,fashion','전문 용어','광고 운영','agency-display','''
광고 소재|Ad creative|소재;크리에이티브 소재|광고에 쓰는 이미지·문구·영상 등의 표현물.|상품별 광고 소재를 비교해요.|광고에 들어가는 이미지와 문구;광고용 제작물
디스플레이 광고|Display advertising|DA;디스플레이 애드;배너 광고|웹·앱 등의 지면에 시각 소재로 노출하는 광고.|디스플레이 광고용 이미지를 제작해요.|배너로 보이는 광고;이미지 광고 집행
'''),
('marketing,fashion','전문 용어','브랜드 전략','brand-strategy','''
브랜딩|Branding|브랜드 구축|브랜드의 정체성과 인식을 만들어 가는 활동.|브랜딩 방향에 맞춰 제품 경험을 정해요.|브랜드 이미지 만드는 일
포지셔닝|Brand positioning|브랜드 포지셔닝|경쟁 속에서 브랜드가 차지할 인식과 위치를 정하는 것.|프리미엄 일상복으로 포지셔닝해요.|경쟁사와 다르게 자리잡기
USP|Unique selling proposition|유에스피;차별적 판매 제안|고객이 선택할 이유가 되는 차별적 강점.|이 제품의 USP를 광고에 담아요.|우리 제품만의 판매 강점;왜 우리 제품을 사야 하는지
브랜드 아이덴티티|Brand identity|브랜드 정체성;BI|브랜드가 자신을 드러내는 고유한 성격과 표현 체계.|브랜드 아이덴티티를 새 시즌에도 유지해요.|브랜드 고유 정체성
'''),
('marketing,fashion','전문 용어','고객 이해','brand-manager','''
페르소나|Customer persona|고객 페르소나;타깃 페르소나|조사한 고객 특성을 구체적인 인물상으로 정리한 것.|핵심 페르소나의 구매 고민을 살펴요.|대표 고객을 가상 인물로;고객 유형 구체화
시장조사|Market research|마켓 리서치;시장 조사|시장과 고객 정보를 모아 의사결정에 쓰는 조사.|신상품 기획 전에 시장조사를 진행해요.|고객과 시장 알아보기
인사이트|Insight|소비자 인사이트;고객 통찰|자료에서 찾아낸 행동의 이유나 유의미한 이해.|반품 사유에서 개선 인사이트를 찾았어요.|데이터에서 얻은 깨달음;소비자 행동 이유
'''),
('marketing,fashion','전문 용어','미디어 전략','brand-media','''
온드 미디어|Owned media|온드미디어;자사 채널|브랜드가 직접 운영·관리하는 콘텐츠 채널.|자사 블로그를 온드 미디어로 운영해요.|회사가 직접 운영하는 채널
페이드 미디어|Paid media|페이드미디어;유료 매체|비용을 내고 노출을 확보하는 매체 활동.|유료 배너는 페이드 미디어 예산에 넣어요.|돈 내고 노출하는 매체
언드 미디어|Earned media|언드미디어;획득 미디어|자발적 공유·보도·후기 등으로 얻는 노출.|고객의 자발적 후기가 언드 미디어로 확산돼요.|돈 주고 산 게 아닌 자발적 입소문
'''),
('marketing,fashion,design','전문 용어','브랜드 제작','brand-alignment','''
톤앤매너|Tone and manner|톤 앤 매너;T&M;톤앤매너 가이드|브랜드 표현에 일관되게 유지하는 말투와 분위기.|상세페이지와 배너의 톤앤매너를 맞춰요.|디자인 분위기 통일;브랜드 말투와 느낌
터치포인트|Touchpoint|터치 포인트;고객 접점|고객이 브랜드와 만나 경험하는 지점.|매장과 앱의 터치포인트를 함께 살펴요.|고객이 브랜드를 접하는 곳
'''),
('fashion','전문 용어','상품기획·직무','fashion-md,fashion-roles','''
MD|Merchandiser|엠디;머천다이저|판매를 고려해 상품 구성과 운영을 기획하는 담당자.|MD와 신상품 구성 비중을 정해요.|어떤 상품을 팔지 기획하는 사람
상품기획|Merchandise planning|기획MD;상품 기획|고객·판매 목표에 맞춰 상품 구성을 계획하는 일.|상품기획 단계에서 가격대를 정해요.|시즌에 어떤 제품 만들지 계획
바이어|Buyer|바잉 담당;바잉|판매할 상품을 선정하고 구매 조건을 협의하는 담당자.|바이어에게 새 컬렉션을 소개해요.|매장에서 팔 제품 사오는 사람
VMD|Visual merchandising|브이엠디;비주얼 머천다이징;VM|브랜드와 상품이 잘 드러나도록 판매 공간을 연출하는 일.|VMD 팀과 쇼윈도 구성을 정해요.|매장 진열과 공간 연출
'''),
('fashion','전문 용어','발주·유통','wholesale','''
SKU|Stock keeping unit|에스케이유;재고 관리 단위|색·크기 등으로 구분한 개별 재고 관리 단위.|같은 셔츠도 색과 사이즈별 SKU를 나눠요.|색상 사이즈별 재고 구분
MOQ|Minimum order quantity|최소 주문 수량;미니멈;엠오큐|거래처가 받는 최소 주문 수량.|이 원단의 MOQ를 확인해요.|최소 몇 개 주문해야 하는지
PO|Purchase order|피오;발주서;구매 주문서|구매자가 품목·수량·조건을 적어 보내는 주문 문서.|수량 확정 후 거래처에 PO를 보내요.|공장에 주문하는 문서;상품 발주서
리드타임|Lead time|리드 타임;납기 소요 기간|주문 등 합의한 시작점부터 완료까지 걸리는 기간.|발주부터 입고까지 리드타임은 4주예요.|주문하고 들어올 때까지 기간
어소트먼트|Assortment|어소트;상품 구성|판매할 품목·색·사이즈 등을 조합한 구성.|어소트먼트에서 아우터 비중을 늘려요.|판매 상품 종류 구성
컬렉션|Collection|콜렉션;시즌 컬렉션|하나의 주제나 시즌으로 묶은 상품군.|가을 컬렉션의 주제를 소개해요.|시즌별 상품 묶음
위탁판매|Consignment|위탁;위탁 판매|판매처에 상품을 맡기고 판매분을 정산하는 방식.|위탁판매 조건과 반품 범위를 확인해요.|팔린 만큼 정산하는 판매
D2C|Direct to consumer|DTC;소비자 직접 판매|브랜드가 소비자에게 직접 판매하는 방식.|D2C 채널인 자사몰을 키워요.|브랜드가 고객에게 직접 판매
벤더|Vendor|공급업체;거래 공급사|제품이나 자재를 공급하는 거래 업체.|벤더와 생산 일정을 확인해요.|자재나 제품 납품하는 업체
백오더|Backorder|백 오더;미출고 주문|재고 부족 등으로 아직 출고하지 못한 주문.|품절 사이즈는 백오더 일정을 안내해요.|주문 받았는데 재고 없어 못 보냄
'''),
('fashion','전문 용어','상품 소개','fashion-linesheet','''
라인시트|Line sheet|라인 시트;상품 라인시트|바이어가 주문할 수 있도록 제품과 거래 정보를 정리한 자료.|라인시트에 품번과 도매가를 넣어요.|바이어에게 보내는 상품 주문 자료
룩북|Lookbook|룩 북;스타일북|제품의 스타일링과 컬렉션 분위기를 보여주는 이미지 자료.|신상품을 조합해 룩북을 만들어요.|옷 입은 스타일 모은 책;컬렉션 분위기 보여주는
품번|Style number|스타일 넘버;스타일 번호;스타일코드|상품 스타일을 식별하기 위해 붙인 관리 번호.|문의할 때 품번도 함께 보내주세요.|제품 스타일 구분 번호
'''),
('fashion','전문 용어','매장·유통','retail','''
POS|Point of sale|포스;판매 시점 시스템|결제와 판매 기록을 처리하는 시스템.|POS에서 매장별 판매 내역을 확인해요.|매장 계산대 결제 시스템
옴니채널|Omnichannel|옴니 채널|여러 판매 채널의 경험을 연결하는 운영 방식.|온라인 주문을 매장에서 받는 옴니채널 서비스를 열어요.|온라인과 오프라인 이어지는 판매
업셀링|Upselling|업셀;상위 상품 제안|더 높은 가치나 가격의 상품을 제안하는 판매 방식.|기본형 대신 프리미엄 소재로 업셀링해요.|더 높은 등급 상품 권하기
크로스셀링|Cross-selling|교차 판매;크로스 셀링|선택한 상품과 함께 쓸 다른 상품을 제안하는 것.|재킷과 어울리는 벨트를 크로스셀링해요.|함께 살 다른 제품 추천
객단가|Average transaction value|ATV;평균 구매 금액|한 거래당 평균 구매 금액.|매장 객단가를 거래 건수 기준으로 봐요.|한 번 결제할 때 평균 얼마 사는지
팝업 스토어|Pop-up store|팝업;팝업스토어|정해진 기간에만 운영하는 임시 매장.|신상품을 알리는 팝업 스토어를 열어요.|잠깐 열었다 닫는 매장
데드스톡|Dead stock|악성 재고;데드 스톡|장기간 팔리지 않고 남아 있는 재고.|데드스톡의 처리 방안을 정해요.|오랫동안 안 팔린 재고
'''),
('fashion','전문 용어','매출·재고','retail-otb','''
OTB|Open to buy|오픈투바이;오픈 투 바이|판매·재고 계획상 추가 구매에 쓸 수 있는 예산.|추가 바잉 전에 OTB를 확인해요.|상품 추가로 살 수 있는 예산
마크다운|Markdown|가격 인하;마크 다운|기존 판매 가격을 낮추는 것.|시즌 말 마크다운 폭을 정해요.|상품 판매가 내리기
'''),
('fashion','전문 용어','매출·재고','retail-performance','''
판매율|Sell-through rate|셀스루;셀 스루;소진율|정해진 기간의 입고 수량 대비 판매 수량 비율.|입고 100장 중 60장이 팔려 판매율은 60%예요.|들어온 상품 중 얼마나 팔렸는지
매장 전환율|Store conversion rate|구매 전환율;매장 구매율|매장 방문 중 구매로 이어진 비율.|방문객 수와 구매 건수를 함께 보며 매장 전환율을 확인해요.|매장에 온 사람 중 구매한 비율
'''),
('fashion','전문 용어','매출·재고','retail-reorder','''
리오더|Reorder|재주문;추가 발주|이미 주문한 상품을 추가로 주문하는 것.|잘 팔리는 색상은 리오더해요.|같은 상품 추가 주문;인기 제품 재생산 발주
재주문점|Reorder point|ROP;발주점|재고가 이 수준에 도달하면 추가 발주하는 기준 수량.|납기를 고려해 재주문점을 정해요.|재고 몇 개 남으면 다시 주문
안전재고|Safety stock|버퍼 재고;안전 재고|수요 증가나 입고 지연에 대비해 더 확보한 재고.|배송 지연에 대비해 안전재고를 둬요.|혹시 몰라 여유로 둔 재고
'''),
('fashion','전문 용어','제품개발·생산','techpack','''
테크팩|Tech pack|테크 팩;작업지시서;생산 작업지시서|치수·소재·구조 등 제품 제작 정보를 묶은 문서.|공장에 최신 테크팩을 전달해요.|공장이 옷 만들 때 보는 문서
도식화|Technical flat|플랫;플랫 스케치;테크니컬 플랫|옷의 형태와 봉제 구조를 평면으로 표현한 그림.|도식화에 뒤판 절개선도 표시해요.|옷 구조를 평면으로 그린 그림
BOM|Bill of materials|자재 명세서;비오엠|제품 제작에 필요한 자재와 수량 목록.|BOM에 지퍼와 라벨도 넣어요.|제품 하나 만들 재료 목록
스펙시트|Specification sheet|스펙 시트;치수표;사이즈 스펙|제품의 측정 부위와 규격을 정리한 표.|스펙시트의 소매 길이를 수정해요.|옷 치수 정리한 표
'''),
('fashion','전문 용어','제품개발·생산','techpack-details','''
POM|Point of measure|피오엠;측정 부위|치수를 재기로 정한 위치와 기준.|가슴둘레 POM을 도식화에 표시해요.|옷 어디를 재야 하는지
부자재|Trims|트림;트림스|단추·지퍼·라벨처럼 주원단 외에 쓰는 자재.|부자재 색상을 원단과 맞춰요.|단추 지퍼 라벨 같은 재료
허용오차|Tolerance|톨러런스;치수 허용오차|규격에서 벗어나도 허용하기로 한 차이의 범위.|총장 허용오차를 0.5cm로 정해요.|치수 차이 얼마나 허용하는지
시접|Seam allowance|솔기 여유|봉제를 위해 재단선과 봉제선 사이에 남긴 폭.|도식화에 시접 폭을 적어요.|박음질 위해 남기는 원단 여유
'''),
('fashion','전문 용어','샘플·피팅','techpack-fit','''
피팅|Fitting|핏 확인;착장 점검|옷을 입혀 착용감·치수·실루엣을 확인하는 작업.|샘플 피팅 후 어깨 폭을 조정해요.|샘플 옷 입혀서 확인
핏 샘플|Fit sample|피팅 샘플;핏샘플|착용 상태와 치수를 확인하기 위한 시험 제품.|핏 샘플로 소매 움직임을 점검해요.|맞음새 확인하는 샘플 옷
핏 코멘트|Fit comments|피팅 코멘트;샘플 코멘트|피팅 후 수정할 위치와 내용을 적은 의견.|핏 코멘트를 사진과 함께 전달해요.|옷 입어보고 수정 의견 쓰기
핏 승인|Fit sign-off|핏 컨펌;피팅 승인|맞음새 검토를 끝내고 기준을 승인하는 것.|핏 승인 후 다음 생산 단계로 넘겨요.|샘플 맞음새 최종 승인
'''),
('fashion','전문 용어','제품개발·생산','techpack-settings','''
컬러웨이|Colorway|컬러 웨이;컬러 옵션|같은 디자인에서 제공하는 색상 또는 배색 구성.|이번 스타일은 컬러웨이 세 가지예요.|같은 옷의 다른 색 조합
사이즈런|Size run|사이즈 런;사이즈 범위|상품이 제공되는 전체 사이즈 구성.|XS부터 XL까지 사이즈런을 잡아요.|제품이 나오는 전체 사이즈
'''),
('fashion','전문 용어','제품개발·생산','techpack-grading','''
그레이딩|Pattern grading|패턴 그레이딩;사이즈 전개|기준 패턴을 규칙에 따라 다른 사이즈로 전개하는 작업.|기준 M 사이즈에서 그레이딩해요.|패턴을 사이즈별로 늘리고 줄이기
'''),
('dev','전문 용어','요구사항·기획','dev-epic','''
에픽|Epic|에픽 이슈|여러 작은 작업이나 스토리로 나눌 수 있는 큰 업무 묶음.|회원 가입 개선을 에픽으로 묶어요.|큰 기능을 여러 작업으로 묶기
유저 스토리|User story|사용자 스토리;유저스토리|사용자 입장에서 원하는 기능과 이유를 적은 설명.|사용자가 왜 필요한지 유저 스토리에 적어요.|사용자 입장에서 기능 요구 쓰기
이니셔티브|Initiative|전략 과제|여러 에픽을 공통 목표 아래 묶은 상위 과제.|검색 경험 개선 이니셔티브를 추진해요.|큰 목표 아래 프로젝트 묶음
'''),
('dev','전문 용어','요구사항·기획','dev-done','''
DoD|Definition of done|완료 정의;디피니션 오브 던|팀이 일을 완료로 인정할 공통 기준.|테스트와 문서 갱신을 DoD에 넣어요.|어디까지 해야 완료인지
인수 조건|Acceptance criteria|AC;수용 기준;승인 기준|특정 요구사항을 충족했다고 판단할 조건.|빈 입력 처리도 인수 조건에 적어요.|기능 합격 조건;요구사항 충족 기준
'''),
('dev','전문 용어','개발 협업','dev-debt','''
기술 부채|Technical debt|테크 데트;테크니컬 데트|구조나 구현의 선택 때문에 추후 개선에 드는 부담.|중복 로직이 쌓인 기술 부채를 정리해요.|급히 만든 코드 나중에 고칠 부담
리팩터링|Refactoring|리팩토링;코드 구조 개선|외부 동작을 유지하며 코드 구조를 개선하는 작업.|기능은 그대로 두고 리팩터링해요.|동작 안 바꾸고 코드 정리
'''),
('dev','전문 용어','제품팀 직무','dev-roles','''
PO|Product owner|피오;프로덕트 오너;제품 책임자|제품 가치를 위해 백로그와 우선순위를 관리하는 역할.|PO와 다음 스프린트 우선순위를 정해요.|제품 우선순위 결정하는 역할
스크럼 마스터|Scrum master|SM;스크럼마스터|팀이 스크럼을 이해하고 효과적으로 일하도록 돕는 역할.|스크럼 마스터가 협업 장애 해결을 도와요.|스크럼 진행 돕는 사람
'''),
('dev','전문 용어','빌드·배포','dev-ci','''
CI|Continuous integration|지속적 통합;씨아이|변경 코드를 자주 합치고 자동 빌드·검증하는 방식.|PR마다 CI 테스트를 돌려요.|코드 합칠 때 자동 검증
빌드|Build|빌드 작업|소스에서 실행·배포할 결과물을 만드는 과정.|빌드가 실패한 원인을 확인해요.|코드를 실행 파일로 만드는
코드 리뷰|Code review|코드리뷰;리뷰어 검토|다른 개발자가 변경 코드를 읽고 검토하는 과정.|머지 전에 코드 리뷰를 받아요.|동료가 내 코드 확인
'''),
('dev','전문 용어','빌드·배포','dev-cd','''
지속적 제공|Continuous delivery|CD;컨티뉴어스 딜리버리|검증한 변경을 언제든 배포할 수 있게 준비하는 방식.|지속적 제공 파이프라인에 승인 단계를 둬요.|언제든 배포 가능한 상태 유지
지속적 배포|Continuous deployment|CD;컨티뉴어스 디플로이먼트|검증을 통과한 변경을 운영 환경까지 자동 반영하는 방식.|모든 검증을 통과하면 지속적 배포로 반영해요.|검사 통과하면 자동으로 실서비스 반영
배포|Deployment|디플로이;deploy|변경된 소프트웨어를 실행 환경에 반영하는 작업.|오늘 수정 사항을 운영 환경에 배포해요.|새 코드를 서버에 반영
운영 환경|Production environment|프로덕션;프로덕션 환경;프로덕션 서버;prod|실제 사용자에게 서비스를 제공하는 실행 환경.|운영 환경 반영 전에 검증해요.|실제 고객이 쓰는 서버 환경
'''),
('dev','현장 표현','빌드·배포','dev-gitflow','''
핫픽스|Hotfix|핫 픽스;긴급 패치|운영 중인 버전의 급한 문제를 해결하는 수정.|로그인 장애는 핫픽스로 처리해요.|실서비스 오류 급히 수정
릴리스|Release|릴리즈;버전 출시|사용할 수 있도록 소프트웨어 버전을 내놓는 것.|이번 릴리스에 개선 기능을 포함해요.|새 버전 공개;소프트웨어 출시
'''),
('dev','전문 용어','품질·테스트','dev-tests','''
E2E 테스트|End-to-end testing|이투이;엔드투엔드;종단간 테스트|사용자의 전체 흐름을 연결해서 확인하는 테스트.|로그인부터 주문까지 E2E 테스트를 해요.|처음부터 끝까지 사용 과정 검사
스모크 테스트|Smoke testing|스모크테스트;기본 동작 검사|핵심 기능이 기본적으로 작동하는지 빠르게 확인하는 테스트.|배포 후 스모크 테스트부터 해요.|핵심 기능만 빠르게 검사
인수 테스트|Acceptance testing|인수테스트;수용 테스트|제품이 업무 요구를 만족하는지 확인하는 테스트.|담당자가 실제 업무로 인수 테스트를 해요.|사용자가 요구한 대로 되는지 검사
성능 테스트|Performance testing|퍼포먼스 테스트;성능시험|속도·안정성 등 시스템 성능을 확인하는 테스트.|접속자가 많을 때 성능 테스트를 해요.|얼마나 빠르고 잘 버티는지 검사
수동 테스트|Manual testing|매뉴얼 테스트|사람이 직접 조작하고 결과를 확인하는 테스트.|화면 흐름은 수동 테스트로도 살펴요.|사람 손으로 기능 확인
자동화 테스트|Automated testing|테스트 자동화|스크립트나 도구로 검증 과정을 실행하는 테스트.|반복 검사는 자동화 테스트로 돌려요.|코드로 반복 검사하기
'''),
('dev,design','전문 용어','UI·협업','design-variants','''
컴포넌트|Component|컴포넌트 UI;UI 컴포넌트|여러 화면에서 재사용하는 인터페이스 단위.|버튼을 공통 컴포넌트로 관리해요.|여러 화면에서 재사용하는 UI
배리언트|Variant|베리언트;배리언츠;베리언츠|같은 컴포넌트의 크기·상태 등 변형.|버튼의 비활성 배리언트를 추가해요.|같은 버튼의 다른 상태 모음
컴포넌트 세트|Component set|컴포넌트셋|관련 배리언트를 함께 묶은 집합.|버튼 배리언트를 컴포넌트 세트로 묶어요.|UI 변형들을 하나로 묶기
'''),
('dev,design','전문 용어','UI·협업','design-tokens','''
디자인 토큰|Design token|디자인토큰;토큰|색·간격 등의 디자인 값에 이름을 붙인 공통 단위.|강조색을 디자인 토큰으로 관리해요.|디자인 색 간격을 이름으로 관리
테마|Theme|UI 테마;화면 테마|같은 UI에 적용하는 색·스타일 등의 표현 체계.|밝은 테마와 어두운 테마를 준비해요.|같은 화면의 밝은 어두운 스타일
핸드오프|Design handoff|핸드 오프;개발 전달|구현에 필요한 디자인 정보와 의도를 개발팀에 전달하는 과정.|핸드오프 때 상태별 동작도 설명해요.|디자인을 개발자에게 넘기는
'''),
('dev,design','전문 용어','UI·협업','design-system','''
디자인 시스템|Design system|디자인시스템;DS|일관된 제품을 만들기 위한 공통 규칙과 재사용 요소 체계.|새 화면도 디자인 시스템을 따라 만들어요.|화면을 일관되게 만드는 규칙과 요소
'''),
('design','전문 용어','인쇄·출력','print-marks','''
도련|Bleed|재단 여분;블리드;bleed|재단 오차에 대비해 완성선 밖으로 늘린 이미지 영역.|배경색을 도련까지 채워 주세요.|잘라도 흰 테두리 안 생기게 여유
재단선|Trim marks|트림 마크;크롭 마크;재단 표시|인쇄물을 자를 위치를 알려 주는 표시.|출력 파일에 재단선을 넣어요.|인쇄물 자르는 위치 표시
맞춤표|Registration marks|레지스트레이션 마크;핀 맞춤표|색판들이 같은 위치에 인쇄되도록 맞추는 표시.|맞춤표로 색판 어긋남을 확인해요.|인쇄 색판 위치 맞추는 표식
컬러바|Color bars|컬러 바;색상 막대|인쇄 색과 농도 점검에 쓰는 색상 패치 배열.|컬러바를 보고 인쇄 상태를 확인해요.|인쇄 색 농도 점검 막대
'''),
('design','전문 용어','인쇄·제작','design-production','''
별색|Spot color|스폿 컬러;스팟 컬러|지정한 색을 별도 잉크로 인쇄하는 방식이나 그 색.|브랜드 색은 별색 인쇄로 협의해요.|원하는 특정 색 잉크 따로 쓰기
팬톤|Pantone|판톤;팬톤 컬러;PANTONE|색을 번호 등으로 지정하고 소통하는 색상 체계.|팬톤 번호와 실물 칩을 함께 확인해요.|색상 번호로 지정;표준 색 견본
인쇄 감리|Print supervision|인쇄감리;인쇄 현장 확인|인쇄 현장에서 색과 제작 품질을 확인하는 일.|첫 인쇄 때 인쇄 감리를 진행해요.|인쇄소에서 색 제대로 나오는지 확인
굿즈|Merchandise|브랜드 굿즈;머천다이즈|브랜드나 콘텐츠를 바탕으로 만든 관련 상품.|앨범 콘셉트로 굿즈를 디자인해요.|브랜드 기념 상품;팬 상품
'''),
]

NOTES = {
 'PT':'업무 발표를 뜻합니다. 문맥에 따라 발표 자료까지 PT라고 부르기도 합니다.',
 '컨펌':'단순 확인인지 최종 승인인지 팀마다 다릅니다. 승인 대상과 담당자를 함께 확인하세요.',
 'MD':'조직에 따라 상품기획·바잉·온라인 판매 운영 등 담당 범위가 다릅니다.',
 'PO':'패션·유통의 구매 주문서와 개발·제품팀의 프로덕트 오너는 서로 다른 뜻입니다.',
 '리드타임':'시작점이 발주인지 생산 착수인지, 끝이 출고인지 입고인지 함께 정해야 합니다.',
 '판매율':'여기서는 판매 수량 ÷ 입고 수량 × 100입니다. 회사별 기간·반품·추가입고 반영 기준을 확인하세요.',
 '객단가':'여기서는 거래당 평균입니다. 고객당 평균으로 집계하는 경우에는 분모가 달라집니다.',
 '시안':'검토용 안으로, 승인된 최종 납품 파일과는 구별합니다.',
 '지속적 제공':'CD는 지속적 제공과 지속적 배포 양쪽의 약자로 쓰이므로 자동 운영 반영 여부를 확인하세요.',
 '지속적 배포':'배포와 사용자에게 기능을 공개하는 시점은 기능 플래그 등으로 달라질 수 있습니다.',
 '핸드오프':'파일만 전달하는 것뿐 아니라 상태·동작·예외 조건을 함께 설명하는 과정을 포함합니다.',
 '배리언트':'여기서는 UI 컴포넌트의 변형을 뜻합니다.',
 '팬톤':'소재·인쇄 방식과 코팅 유무에 따라 같은 번호도 보이는 색이 달라질 수 있습니다.',
}

# Existing definitions, notes and provenance are preserved when sharing a meaning.
# Each tuple is source field, term, destination field, category, original example.
COPIES = []
def share(source_field, destinations, category, raw):
    for line in raw.strip().splitlines():
        term, example = line.split('|')
        for destination in destinations.split(','):
            COPIES.append((source_field,term,destination,category,example))

share('marketing','fashion','마케팅·성과','''
CPC|신상품 광고의 CPC를 확인해요.
CPM|컬렉션 광고의 CPM을 비교해요.
CTR|상품 이미지별 CTR을 비교해요.
ROAS|자사몰 신상품 광고의 ROAS를 확인해요.
CVR|상세페이지 개선 후 CVR을 살펴요.
CPA|첫 구매 CPA를 기준으로 예산을 조정해요.
노출수|시즌 캠페인의 노출수를 확인해요.
도달수|컬렉션 광고의 도달수를 확인해요.
타겟팅|신규 고객에게 맞게 타겟팅해요.
오디언스|최근 구매한 고객 오디언스를 나눠요.
세그먼트|구매 주기별 세그먼트를 만들어요.
리타겟팅|장바구니 이탈 고객에게 리타겟팅해요.
랜딩 페이지|시즌 기획전 랜딩 페이지를 만들어요.
전환|이번 캠페인은 첫 구매를 전환으로 정해요.
CTA|신상품 구매 CTA를 눈에 잘 보이게 해요.
A/B 테스트|상세페이지 버튼을 A/B 테스트해요.
''')
share('design','marketing,fashion','브랜드 제작','''
누끼|상품 사진 누끼를 따서 배너에 넣어요.
무드보드|새 시즌 캠페인 무드보드를 공유해요.
레퍼런스|캠페인 레퍼런스를 모아 방향을 맞춰요.
목업|패키지 목업으로 적용 모습을 보여줘요.
카피|신상품 배너 카피를 검토해요.
''')
share('design','dev','UI·협업','''
와이어프레임|와이어프레임에서 화면 구성을 먼저 확인해요.
프로토타입|프로토타입으로 흐름을 검증하고 구현해요.
접근성|키보드로도 쓸 수 있게 접근성을 점검해요.
대체 텍스트|상품 이미지에 대체 텍스트를 넣어요.
''')
share('marketing','design,dev','화면·성과','''
CTA|가입 CTA의 위치를 검토해요.
랜딩 페이지|새 서비스 랜딩 페이지를 제작해요.
A/B 테스트|가입 화면을 A/B 테스트해요.
''')
share('marketing','fashion','판매·운영','''
프로모션|신상품 출시 프로모션을 준비해요.
PR|브랜드 PR 담당자와 보도자료를 확인해요.
''')
share('fashion','marketing,design','브랜드 제작','''
룩북|캠페인 룩북의 이미지 구성을 정해요.
팝업 스토어|브랜드 팝업 스토어를 기획해요.
''')
share('design','marketing,fashion','브랜드 제작','''
굿즈|캠페인 굿즈를 기획해요.
''')
share('marketing','dev','UI·협업','''
시안|구현할 화면 시안을 먼저 확인해요.
''')

EXAMPLES = {
 ('marketing','PT'):'광고주 PT에서 캠페인 전략과 시안을 발표해요.',
 ('fashion','PT'):'시즌 상품기획 PT에서 컬렉션 구성을 설명해요.',
 ('dev','PT'):'신규 기능 PT에서 구현 방향을 설명해요.',
 ('design','PT'):'브랜드 디자인 PT에서 키비주얼을 제안해요.',
 ('marketing','컨펌'):'광고주 컨펌을 받은 소재로 집행해요.',
 ('fashion','컨펌'):'샘플 컬러 컨펌 후 생산을 진행해요.',
 ('dev','컨펌'):'요구사항 컨펌 후 구현 범위를 정해요.',
 ('design','컨펌'):'시안 컨펌을 받은 뒤 납품 파일을 정리해요.',
 ('fashion','시안'):'신상품 상세페이지 시안을 검토해요.',
 ('marketing','시안'):'광고주에게 배너 시안 두 가지를 보내요.',
 ('design','시안'):'브랜드 로고 시안 두 가지를 비교해요.',
 ('fashion','키비주얼'):'가을 컬렉션 키비주얼을 자사몰과 매장에 적용해요.',
 ('marketing','키비주얼'):'캠페인 키비주얼을 매체별 소재로 확장해요.',
 ('design','키비주얼'):'키비주얼을 기준으로 포스터를 디자인해요.',
}

SOURCES.update({
 'office-kr':('잡플래닛','직장인 업무 용어 사전','https://www.jobplanet.co.kr/contents/news-5187','2023-08-14',False),
 'design-color':('Adobe','Color models and color spaces','https://helpx.adobe.com/creative-cloud/apps/colors/understand-color-modes.html','',False),
 'design-overprint':('Adobe','Overprinting in Illustrator','https://helpx.adobe.com/illustrator/using/overprinting.html','',False),
 'design-autolayout':('Figma','Guide to auto layout','https://help.figma.com/hc/en-us/articles/360040451373-Guide-to-auto-layout','',False),
 'marketing-crm':('Mailchimp','Customer relationship management','https://mailchimp.com/marketing-glossary/crm/','',False),
 'marketing-seo':('Mailchimp','Search engine optimization','https://mailchimp.com/marketing-glossary/seo/','',False),
 'marketing-utm':('Google 애널리틱스','맞춤 URL을 사용한 캠페인 데이터 수집','https://support.google.com/analytics/answer/10917952?hl=ko','',False),
 'work-kpi':('Asana','KPI: 핵심 성과 지표','https://asana.com/ko/resources/key-performance-indicator-kpi','',False),
})
GROUPS += [
('marketing,dev,fashion,design,common','현장 표현','회의·협업','office-kr','''
픽스|Fix (confirm)|확정;일정 픽스|협의한 내용을 확정하는 것.|회의 날짜를 금요일로 픽스해요.|최종으로 결정하는;일정 확정
디벨롭|Develop|디벨로프;구체화|아이디어나 안을 더 구체적으로 발전시키는 것.|선택한 방향을 조금 더 디벨롭해요.|아이디어 더 발전시키기;초안 구체화
러프|Rough|러프하게;러프안;개략안|세부를 다듬기 전 대략적인 상태.|먼저 러프한 방향부터 공유해요.|대략적으로 먼저 잡는;세부 작업 전 초안
피드백|Feedback|F/B;FB;피드 백|작업을 검토하고 전달하는 의견.|피드백을 모아서 한 번에 전달해요.|작업물 보고 수정 의견;검토 후 조언
데드라인|Deadline|마감;마감일;듀데이트;due date|일을 마쳐야 하는 기한.|이번 작업 데드라인은 목요일이에요.|언제까지 끝내야 하는지;작업 마감 기한
'''),
('marketing,dev,fashion,design,common','전문 용어','목표·성과','work-kpi','''
KPI|Key performance indicator|케이피아이;핵심 성과 지표|목표 달성 정도를 판단할 핵심 측정 지표.|캠페인 시작 전에 KPI를 합의해요.|성과를 무엇으로 측정할지
'''),
('design,marketing,fashion','전문 용어','색상·제작','design-color','''
RGB|Red green blue|알지비;빛의 삼원색|빨강·초록·파랑 빛으로 색을 표현하는 방식.|화면용 이미지는 RGB 기준으로 확인해요.|화면에서 쓰는 색상 모드
CMYK|Cyan magenta yellow key|씨엠와이케이;4도 컬러|청록·자홍·노랑·검정 잉크로 색을 표현하는 방식.|인쇄용 파일은 CMYK 변환 결과를 확인해요.|인쇄에서 쓰는 네 가지 잉크
'''),
('design','전문 용어','인쇄·출력','design-overprint','''
오버프린트|Overprint|오버프린팅;중복 인쇄|아래 색판을 비우지 않고 위에 겹쳐 인쇄하는 설정.|검정 글자의 오버프린트를 확인해요.|아래 색 위에 잉크 겹쳐 인쇄
녹아웃|Knockout|넉아웃;knockout|위 개체가 인쇄될 부분의 아래 색을 비우는 처리.|겹친 영역의 녹아웃 여부를 확인해요.|겹치는 아래 색을 빼고 인쇄
'''),
('design,dev','전문 용어','UI·협업','design-autolayout','''
오토 레이아웃|Auto layout|오토레이아웃;자동 레이아웃|내용과 규칙에 맞춰 요소 배치와 크기를 조정하는 기능.|문구가 늘어나도 오토 레이아웃으로 간격을 유지해요.|내용 따라 자동으로 크기 배치 조정
패딩|Padding|안쪽 여백;내부 여백|컨테이너 경계와 내부 내용 사이의 여백.|버튼 좌우 패딩을 늘려요.|버튼 글자와 테두리 사이 여백
갭|Gap|요소 간격;아이템 간격|나란히 배치한 요소 사이의 간격.|카드 사이 갭을 통일해요.|요소와 요소 사이 빈 공간
허그|Hug contents|허그 콘텐츠;내용에 맞춤|내부 콘텐츠를 감싸도록 크기를 정하는 설정.|라벨 프레임은 허그로 설정해요.|내용 크기만큼 감싸기
필 컨테이너|Fill container|필컨테이너;컨테이너 채우기|부모 컨테이너의 사용 가능한 공간을 채우는 설정.|입력창 너비를 필 컨테이너로 맞춰요.|부모의 남은 공간 채우기
'''),
('marketing,fashion,dev','전문 용어','고객·운영','marketing-crm','''
CRM|Customer relationship management|씨알엠;고객 관계 관리|고객 정보와 접촉 이력을 활용해 관계를 관리하는 활동과 체계.|구매 이력을 CRM에 연결해요.|고객 정보를 모아 관계 관리
'''),
('marketing,fashion,dev','전문 용어','검색·유입','marketing-seo','''
SEO|Search engine optimization|에스이오;검색 엔진 최적화|검색엔진이 콘텐츠를 이해하고 찾도록 사이트를 개선하는 일.|상품 설명과 제목의 SEO를 점검해요.|검색 결과에 잘 나오게 개선
오가닉 트래픽|Organic traffic|자연 검색 유입;오가닉 유입|유료 검색 광고가 아닌 자연 검색에서 들어온 방문.|오가닉 트래픽의 변화도 함께 봐요.|광고비 없이 검색으로 들어오는 방문
'''),
('marketing,fashion,dev','전문 용어','검색·유입','marketing-utm','''
UTM|UTM parameters|유티엠;캠페인 매개변수;UTM 태그|유입 출처와 캠페인을 구분하려고 URL에 붙이는 값.|배너 링크마다 UTM을 구분해요.|어느 광고에서 왔는지 링크에 표시
'''),
]
NOTES.update({
 '픽스':'여기서는 일정·안의 확정입니다. 개발에서 버그를 fix한다고 하면 오류를 수정한다는 뜻도 됩니다.',
 '러프':'완성도가 낮다는 평가보다, 초기에 세부를 생략한 상태를 설명하는 표현으로 정리했습니다.',
 'KPI':'지표 이름뿐 아니라 계산식·기간·데이터 출처·목표값을 함께 정해야 비교할 수 있습니다.',
 '허그':'Figma 오토 레이아웃의 크기 설정을 설명하는 표현입니다.',
 '필 컨테이너':'Figma 오토 레이아웃의 크기 설정입니다. 부모 프레임의 설정에 따라 적용 범위가 달라집니다.',
 '오가닉 트래픽':'여기서는 자연 검색 유입입니다. 일부 팀은 유료 집행 없이 얻은 유입 전반을 오가닉이라고도 부릅니다.',
 'UTM':'Google 문서에서는 source·medium·campaign 등을 구분합니다. 개인 식별 정보는 URL 값에 넣지 않습니다.',
})
EXAMPLES.update({
 ('dev','KPI'):'검색 응답 시간을 개선 KPI로 정해요.',
 ('fashion','KPI'):'시즌 판매율을 KPI로 정해요.',
 ('design','KPI'):'개선 화면의 과업 성공률을 KPI로 정해요.',
 ('common','KPI'):'팀 목표에 맞춰 KPI를 합의해요.',
 ('marketing','디벨롭'):'캠페인 아이디어를 실행안으로 디벨롭해요.',
 ('fashion','디벨롭'):'소재와 디테일을 정해 디자인을 디벨롭해요.',
 ('design','디벨롭'):'선택한 시안을 디벨롭해 최종안으로 만들어요.',
 ('dev','디벨롭'):'기능 아이디어를 구현 가능한 요구사항으로 디벨롭해요.',
})
