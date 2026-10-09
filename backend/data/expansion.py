"""Expanded filming vocabulary. Short original definitions; examples are editorial.
Each group is field, kind, category, sources, pipe-delimited six-column rows.
"""
SOURCES = {
 'shot-book':('골든래빗','촬영 바이블: 영상의 단위와 화면 구성','https://goldenrabbit.co.kr/articles/OGw0DMQGadCAtky4Yr4I','2024-03-29',False),
 'modelcast':('모델캐스트 · 뉴스와이어','인물사진 촬영용어, 이것만은 기억하자','https://www.newswire.co.kr/newsRead.php?no=660891','2012-11-01',True),
 'onset-kr':('식스원','영상 촬영 현장에서 자주 쓰는 용어','https://sixonebiz.com/blog/video-shoot-terms-glossary','',False),
 'shimai':('국립국어원','시마이의 순화어','https://www.korean.go.kr/front/mcfaq/mcfaqView.do?mcfaq_seq=9025&mn_id=62&pageIndex=1','2020-01-16',True),
 'movement':('StudioBinder','Types of Camera Movements in Film','https://www.studiobinder.com/blog/different-types-of-camera-movements-in-film/','2025-02-02',False),
 'movement-index':('StudioBinder','Camera Movements','https://www.studiobinder.com/camera-shots/camera-movements/','',False),
 'rigs':('StudioBinder','Every Type of Camera Rig Explained','https://www.studiobinder.com/blog/types-of-camera-rigs-in-film/','2020-08-31',False),
 'lenses':('StudioBinder','Different Types of Camera Lenses','https://www.studiobinder.com/blog/different-types-camera-lenses-explained/','',False),
 'focus':('StudioBinder','The Rack Focus Shot','https://www.studiobinder.com/blog/rack-focus-shot-camera-movement-angles/','2025-01-02',False),
 'lighting':('StudioBinder','Film Lighting Terms','https://www.studiobinder.com/blog/film-lighting-terms/','2020-04-29',False),
 'lighting-tech':('StudioBinder','Film Lighting Techniques','https://www.studiobinder.com/blog/film-lighting-techniques/','',False),
 'exposure':('Adobe','Exposure in photography','https://www.adobe.com/creativecloud/photography/discover/exposure-in-photography.html','',False),
 'edit-jl':('Adobe','J cuts and L cuts','https://www.adobe.com/uk/creativecloud/video/discover/j-cut-and-l-cut.html','',False),
 'edit-glossary':('Adobe','Premiere Elements glossary','https://helpx.adobe.com/no/premiere-elements/desktop/using/glossary.html','',False),
 'jump':('Adobe','What is a jump cut','https://www.adobe.com/creativecloud/video/post-production/cuts-in-film/jump-cut.html','',False),
 'sound':('RØDE','Three Tips for Recording Great Documentary Sound','https://rode.com/en-ca/about/news-info/three-tips-for-recording-great-documentary-sound','',False),
 'phantom':('RØDE','What is Phantom Power?','https://help.rode.com/hc/en-us/articles/8533525730063-What-is-Phantom-Power','2026-03-31',False),
 'production':('StudioBinder','Stages of Film Production','https://www.studiobinder.com/blog/stages-of-film-production/','',False),
 'film-glossary':('StudioBinder','Film Terms: Filmmaking Glossary','https://www.studiobinder.com/blog/movie-film-terms/','',False),
 'grading':('Adobe','Color grading overview','https://helpx.adobe.com/premiere/desktop/correct-color/color-correction-fundamentals/about-color-grading.html','2026-01-07',False),
 'color-workflow':('Adobe MAX','Get the Look: Color Correction and Grading','https://www.adobe.com/max/2024/sessions/get-the-look-color-correction-and-grading-s6614.html','2024',False),
}
GROUPS = [
('film','전문 용어','앵글·구도','shots','''
앵글|Camera angle|카메라 앵글;카메라 각도|피사체를 바라보는 카메라의 높이와 방향.|앵글을 낮춰볼게요.|촬영 각도;어디서 바라보는지
'''),
('film','전문 용어','샷 크기','modelcast','''
바스트 샷|Bust shot|바스트;버스트 샷;BS;가슴 샷|대략 가슴 위부터 머리까지 담는 인물 구도.|인터뷰는 바스트 샷으로 갈게요.|가슴부터 찍는;상반신 가슴 위;얼굴과 어깨 담기
웨이스트 샷|Waist shot|웨스트 샷;허리 샷;WS|허리 부근부터 머리까지 담는 인물 구도.|손동작은 웨이스트 샷으로 담아요.|허리부터 찍는;상체와 손동작
풀 샷|Full shot|풀샷;전신 샷;FS;full figure|머리부터 발끝까지 인물 전체를 담는 구도.|신발까지 풀 샷에 넣어주세요.|전신 찍는;머리부터 발끝
'''),
('film','전문 용어','샷 크기','shot-book','''
니 샷|Knee shot|니샷;무릎 샷;KS|무릎 부근부터 머리까지 담는 구도.|니 샷으로 동작을 보여줘요.|무릎부터 찍는;무릎 위 인물
원 샷|One shot|원샷;싱글 샷;single shot|한 사람을 중심으로 담는 숏.|각자 원 샷도 찍어요.|한 사람만 담는
투 샷|Two shot|투샷;2 shot|두 사람을 함께 담는 숏.|대화는 투 샷으로 시작해요.|두 사람 같이 찍는
그룹 샷|Group shot|그룹샷;단체 샷|여러 사람을 한 화면에 담는 숏.|마지막은 그룹 샷이에요.|여럿 같이 찍는;단체 촬영
'''),
('film','전문 용어','영상 단위','shot-book','''
샷|Shot|숏;쇼트;shot|하나의 구도로 담은 영상의 기본 단위.|이 샷 뒤에 반응을 붙여요.|영상 기본 단위;하나의 화면
씬|Scene|신;장면|대체로 같은 시간·장소에서 이어지는 이야기 단위.|이 씬은 카페에서 진행돼요.|한 장소 이야기;장면 단위
시퀀스|Sequence|sequence|연관된 장면들이 모여 이루는 이야기의 묶음.|추격 시퀀스가 끝났어요.|여러 장면 묶음;이야기 덩어리
롱 테이크|Long take|롱테이크;긴 테이크|중간에 끊지 않고 길게 이어 찍는 숏.|입장부터 롱 테이크로 담아요.|끊지 않고 길게;원테이크 긴 촬영
'''),
('film','전문 용어','앵글·구도','shot-book','''
헤드 룸|Headroom|헤드룸|머리 위와 화면 상단 사이의 여백.|헤드 룸을 조금 줄여요.|머리 위 빈 공간
아이 룸|Eye room|아이룸;룩킹 룸;노즈 룸|인물의 시선 방향에 두는 여백.|아이 룸을 오른쪽에 주세요.|시선 쪽 빈 공간
리드 룸|Lead room|리드룸|인물이나 물체가 이동하는 방향의 여백.|달리는 앞쪽에 리드 룸을 둬요.|진행 방향 여백;움직이는 앞 공간
'''),
('film','현장 표현','현장 진행','onset-kr','''
팔로우|Follow|팔로;팔로우 샷;follow shot|움직이는 대상을 화면 안에서 따라가는 촬영 지시.|걸어오는 배우를 팔로우해요.|사람을 따라가면서 찍는;대상 따라가는;움직이는 사람 따라 촬영
테이크|Take|테잌;take|같은 숏을 찍은 각각의 시도.|세 번째 테이크로 확인해요.|같은 장면 몇 번째 촬영
오케이 컷|OK take|오케이컷;OK 컷;오케이|사용할 만하다고 선택한 촬영분.|이번 테이크는 오케이 컷이에요.|잘 나온 촬영분;쓸 장면 확정
킵|Keep|keep;킵 컷|바로 버리지 않고 후보로 남기는 촬영분.|이 버전도 킵해두죠.|버리지 않고 남겨두는
'''),
('film','전문 용어','화면 구성','onset-kr','''
인서트|Insert shot|인서트 샷;삽입 컷|장면의 중요한 사물·동작을 따로 강조하는 숏.|서명하는 손 인서트가 필요해요.|손만 따로 찍는;제품 세부 장면
B롤|B-roll|비롤;B roll;보조 영상|주요 영상에 덧붙여 상황과 분위기를 보여주는 보조 촬영분.|작업실 B롤도 찍어주세요.|인터뷰 위 덮는 영상;보조 화면;스케치 영상
'''),
('film','현장 표현','현장 진행','shimai','''
시마이|Wrap up|시마이하다;시마이 치다|하던 일을 끝내고 마무리한다는 말.|오늘 촬영은 여기서 시마이해요.|촬영 마무리;촬영 끝내는;오늘 일 끝;정리하고 퇴근
'''),
('common','현장 표현','현장 표현','shimai','''
시마이|Wrap up|시마이하다;시마이 치다|일을 마무리하고 끝낸다는 표현.|이 작업은 여기서 시마이하죠.|일 끝내는;마감하고 퇴근
'''),
('film','전문 용어','카메라 움직임','movement','''
팬|Pan|패닝;panning;팬 레프트;팬 라이트|카메라 위치를 유지하며 좌우로 방향을 돌리는 동작.|입구 쪽으로 팬해요.|카메라 좌우 돌리는;가로로 훑는
틸트|Tilt|틸팅;tilting;틸트 업;틸트 다운|카메라 위치를 유지하며 위아래로 방향을 돌리는 동작.|발부터 얼굴까지 틸트 업해요.|카메라 위아래 돌리는;세로로 훑는
휩 팬|Whip pan|스위시 팬;스윙 팬|화면이 흐려질 만큼 빠르게 좌우로 돌리는 팬.|휩 팬으로 다음 인물을 보여줘요.|빠르게 좌우 돌리는;휙 돌아가는 화면
달리 인|Dolly in|푸시 인;push in;돌리 인|카메라 자체가 피사체 쪽으로 가까워지는 이동.|표정에 맞춰 달리 인해요.|카메라 가까이 다가가는;앞으로 이동
달리 아웃|Dolly out|풀 아웃;pull out;돌리 아웃|카메라 자체가 피사체에서 멀어지는 이동.|공간이 보이게 달리 아웃해요.|카메라 뒤로 빠지는;멀어지는 이동
줌 인|Zoom in|줌인|초점거리를 늘려 대상을 화면에서 크게 보이게 하는 것.|표지판을 줌 인해요.|렌즈로 당기는;이동 없이 확대
줌 아웃|Zoom out|줌아웃|초점거리를 줄여 화면에 더 넓은 범위를 담는 것.|주변이 보이게 줌 아웃해요.|렌즈로 빼는;이동 없이 축소
달리 줌|Dolly zoom|돌리 줌;버티고 효과;zolly|카메라 이동과 반대 방향 줌을 함께 써 원근감을 변화시키는 기법.|불안한 순간에 달리 줌을 써요.|인물 크기 같은데 배경 변하는;배경 밀리는 효과
롤|Roll|카메라 롤;roll shot|렌즈를 향하는 축을 중심으로 카메라를 회전시키는 동작.|롤로 기울어지는 느낌을 줘요.|화면이 빙글 도는;카메라 축 회전
아크 샷|Arc shot|아크;아크숏|대상을 중심으로 원호를 그리며 이동하는 숏.|두 사람 주위를 아크 샷으로 담아요.|인물 주위 도는;원형 카메라 이동
'''),
('film','전문 용어','카메라 움직임','movement-index,rigs','''
픽스 샷|Static shot|픽스;고정 샷;fixed shot;스태틱 샷|카메라의 위치와 구도를 움직이지 않는 숏.|이번 장면은 픽스 샷이에요.|고정해서 찍는;카메라 안 움직이는
페데스털|Pedestal|페데스탈;페데스털 업;페데스털 다운|카메라 전체의 높이를 수직으로 올리거나 내리는 동작.|페데스털 업으로 눈높이를 맞춰요.|카메라 통째로 위로;높이 수직 이동
트럭|Truck|트러킹;trucking;트럭 레프트;트럭 라이트|카메라가 옆으로 평행 이동하는 동작.|인물과 나란히 트럭 라이트해요.|카메라 옆으로 이동;좌우 평행 이동
붐 샷|Boom shot|붐 업;붐 다운|크레인·지브 암으로 카메라를 위아래로 이동시키는 숏.|붐 업으로 마당을 드러내요.|암으로 카메라 올리는
'''),
('film','전문 용어','장비·리그','rigs','''
핸드헬드|Handheld|핸드 헬드;핸드헬드 샷|손이나 어깨로 카메라를 지지하며 찍는 방식.|이동 장면은 핸드헬드로 가요.|들고 찍는;손 떨림 촬영
삼각대|Tripod|트라이포드|세 다리로 카메라를 받치는 장비.|삼각대에 카메라를 올려요.|카메라 세워두는 장비
달리|Camera dolly|돌리;카메라 달리|카메라를 싣고 부드럽게 이동시키는 바퀴 달린 받침 장비.|달리 이동 경로를 확인해요.|카메라 이동 수레
슬라이더|Camera slider|카메라 슬라이더|레일을 따라 카메라를 짧게 이동시키는 장비.|제품 옆으로 슬라이더를 밀어요.|짧은 레일 이동 장비
지브|Jib|지브 암;지미집;크레인;camera crane|긴 암에 카메라를 달아 넓게 움직이는 장비.|지브로 무대 전체를 담아요.|긴 팔 카메라;카메라 크레인
스테디캠|Steadicam|스테디 캠|몸에 장착하는 안정화 장치 계열로 부드러운 이동 촬영에 쓰이는 이름.|스테디캠으로 복도를 따라가요.|몸에 다는 안정화 장비
짐벌|Gimbal|김벌;카메라 짐벌|회전축을 제어해 카메라 흔들림을 줄이는 안정화 장비.|짐벌 균형을 먼저 맞춰요.|흔들림 줄이는 장비
스노리캠|Snorricam|바디 마운트;body rig|배우 몸에 카메라를 고정해 함께 움직이도록 하는 장치.|스노리캠으로 인물을 고정해 보여줘요.|배우 몸에 카메라 다는
'''),
('film','전문 용어','렌즈·초점','lenses','''
단렌즈|Prime lens|프라임 렌즈;프라임|초점거리가 하나로 고정된 렌즈.|오늘은 50mm 단렌즈를 써요.|줌 안 되는 렌즈
줌 렌즈|Zoom lens|줌렌즈|초점거리를 바꿀 수 있는 렌즈.|줌 렌즈로 구도를 조절해요.|확대 축소 가능한 렌즈
광각 렌즈|Wide-angle lens|광각;와이드 렌즈|같은 촬상면에서 넓은 화각을 담는 짧은 초점거리 렌즈.|좁은 실내는 광각으로 담아요.|넓게 보이는 렌즈
망원 렌즈|Telephoto lens|망원;텔레포토|먼 대상을 크게 담는 긴 초점거리 렌즈.|먼 무대는 망원으로 찍어요.|멀리 있는 것 크게 찍는 렌즈
표준 렌즈|Normal lens|노멀 렌즈|촬상면 대각선 길이 부근의 초점거리를 가진 렌즈.|표준 렌즈로 구도를 확인해요.|표준 화각 렌즈
매크로 렌즈|Macro lens|마크로;접사 렌즈|작은 대상을 가까이에서 크게 담도록 설계된 렌즈.|질감은 매크로 렌즈로 찍어요.|작은 물건 접사 렌즈
파포컬|Parfocal|파포컬 렌즈;동초점 렌즈|줌을 바꿔도 맞춘 초점이 유지되는 렌즈 특성.|파포컬인지 확인하고 줌해요.|줌해도 초점 유지
아나모픽|Anamorphic lens|아나모픽 렌즈|영상을 가로 방향으로 압축해 기록하고 후에 펼치는 렌즈 방식.|아나모픽에 맞춰 화면을 펼쳐요.|가로 압축 촬영 렌즈
'''),
('film','전문 용어','렌즈·초점','focus','''
랙 포커스|Rack focus|랙포커스;포커스 이동;초점 이동|한 숏 안에서 서로 다른 거리의 대상으로 초점을 옮기는 기법.|컵에서 인물로 랙 포커스해요.|앞에서 뒤로 초점 옮기는
포커스 풀러|Focus puller|퍼스트 AC;1st AC|촬영 중 초점을 맞추고 유지하는 촬영 보조 담당자.|포커스 풀러와 동선을 맞춰요.|초점 맞추는 사람
팔로우 포커스|Follow focus|팔로 포커스;팔포|렌즈 초점을 정밀하게 조작하도록 돕는 장치.|팔로우 포커스에 거리를 표시해요.|초점 조절 다이얼 장치
얕은 심도|Shallow depth of field|쉘로 포커스;shallow focus;아웃포커싱|선명하게 보이는 앞뒤 거리 범위가 좁은 상태.|얕은 심도로 인물을 강조해요.|배경 흐리게;인물만 선명하게
깊은 심도|Deep depth of field|딥 포커스;deep focus;팬 포커스|가까운 곳부터 먼 곳까지 넓게 선명해 보이는 상태.|깊은 심도로 공간을 보여줘요.|앞뒤 모두 선명하게;배경까지 또렷하게
'''),
('film','전문 용어','조명','lighting','''
키 라이트|Key light|키라이트;주광;메인 라이트|피사체를 비추는 중심 조명.|키 라이트를 왼쪽에 둬요.|주된 조명;메인 빛
필 라이트|Fill light|필라이트;보조광|주광이 만든 그림자를 완화하는 빛.|필 라이트를 조금 줄여요.|그림자 채우는 빛
백 라이트|Backlight|백라이트;백광|피사체 뒤에서 비춰 배경과 구분하는 빛.|백 라이트로 인물을 분리해요.|뒤에서 비추는 빛
림 라이트|Rim light|림라이트;윤곽광|피사체 가장자리에 밝은 윤곽을 만드는 빛.|어깨에 림 라이트를 줘요.|테두리 빛;윤곽 밝게
프랙티컬|Practical light|프랙티컬 라이트;실용광|화면 안에 실제로 보이는 조명 광원.|스탠드를 프랙티컬로 써요.|화면 속 전등;보이는 조명
바운스|Bounce light|바운스 라이트;반사광|벽이나 반사판에 반사시켜 비추는 빛.|천장 바운스로 부드럽게 해요.|벽에 튕겨 비추는
하드 라이트|Hard light|경광;하드광|경계가 뚜렷한 그림자를 만드는 빛.|하드 라이트로 질감을 살려요.|딱딱한 그림자 빛
소프트 라이트|Soft light|연광;소프트광|경계가 부드러운 그림자를 만드는 빛.|소프트 라이트로 얼굴을 비춰요.|부드러운 그림자 빛
플래그|Flag|차광판;플래그 조명|빛을 막거나 범위를 제한하는 불투명한 판·천.|플래그로 벽의 빛을 막아요.|빛 가리는 판
반도어|Barndoors|반도아;바른도어|조명 앞에서 빛의 퍼짐을 조절하는 날개.|반도어로 옆빛을 줄여요.|조명 금속 날개
'''),
('film','전문 용어','조명','lighting-tech','''
3점 조명|Three-point lighting|삼점 조명;쓰리 포인트 라이팅|주광·보조광·후면광을 조합하는 기본 조명 구성.|인터뷰는 3점 조명으로 시작해요.|조명 세 개 구성
하이 키|High-key lighting|하이키|명암 차이를 작게 하고 밝은 톤을 유지하는 조명 방식.|밝은 광고라 하이 키로 가요.|밝고 그림자 적은 조명
로우 키|Low-key lighting|로 키;로우키|어두운 영역과 강한 명암 대비를 활용하는 조명 방식.|로우 키로 긴장감을 만들어요.|어둡고 대비 큰 조명
디퓨전|Diffusion|디퓨저;디퓨전 천;확산재|빛을 분산시켜 부드럽게 만드는 재료나 처리.|창에 디퓨전을 설치해요.|빛 부드럽게 하는 천
네거티브 필|Negative fill|네거티브필;검은 반사판|반사되는 빛을 흡수·차단해 그림자를 짙게 만드는 방법.|검은 천으로 네거티브 필을 줘요.|반사 빛 빼기;그림자 더 어둡게
'''),
('film','전문 용어','노출·색','exposure','''
노출|Exposure|익스포저|촬상면에 들어오는 빛의 양과 관련된 밝기 조절.|창밖에 맞춰 노출을 확인해요.|영상 밝기;얼마나 빛 받는지
조리개|Aperture|아이리스;iris;F값;F스톱|렌즈 안에서 빛이 통과하는 구멍의 크기를 조절하는 부분.|조리개를 조여 심도를 늘려요.|빛 들어오는 구멍;렌즈 밝기 조절
셔터 스피드|Shutter speed|셔터 속도;노출 시간|한 프레임을 기록할 때 빛을 받는 시간.|움직임에 맞춰 셔터를 조절해요.|움직임 잔상;노출되는 시간
ISO|ISO sensitivity|아이에스오;감도|영상 밝기 처리와 노이즈에 영향을 주는 감도 설정값.|조명과 ISO를 함께 확인해요.|어두울 때 감도;카메라 노이즈 설정
과다 노출|Overexposure|오버 노출;노출 오버|필요보다 밝게 기록되어 밝은 부분의 정보가 사라질 수 있는 상태.|하늘의 과다 노출을 확인해요.|너무 밝게 찍힌;하얗게 날아간
노출 부족|Underexposure|언더 노출;노출 언더|필요보다 어둡게 기록되어 어두운 부분을 구분하기 힘든 상태.|얼굴의 노출 부족을 보완해요.|너무 어둡게 찍힌
'''),
('film','전문 용어','편집','edit-jl','''
J컷|J-cut|제이 컷;J 컷;오디오 선행|다음 장면의 소리를 화면보다 먼저 들려주는 편집.|J컷으로 다음 대사를 먼저 들려줘요.|다음 장면 소리 먼저
L컷|L-cut|엘 컷;L 컷;오디오 후행|화면이 바뀐 뒤에도 앞 장면의 소리가 이어지는 편집.|L컷으로 반응을 보여줘요.|화면 바뀌어도 앞 소리 계속
스플릿 편집|Split edit|스플릿 에디트|소리와 화면의 전환 시점을 다르게 하는 편집.|스플릿 편집으로 대화를 연결해요.|소리와 영상 따로 전환
'''),
('film','전문 용어','편집','jump','''
점프 컷|Jump cut|점프컷|비슷한 구도에서 시간·동작이 불연속적으로 뛰어 보이게 자르는 편집.|멈춘 부분은 점프 컷으로 줄여요.|동작 튀는 편집;중간 시간 생략
매치 컷|Match cut|매치컷|형태·동작·소리 등의 유사성을 이용해 서로 다른 숏을 잇는 편집.|둥근 형태를 매치 컷으로 연결해요.|비슷한 모양 장면 연결
'''),
('film','전문 용어','편집','edit-glossary','''
클립|Clip|clip|편집에 사용하는 영상·음성의 한 조각.|클립을 타임라인에 놓아요.|편집하는 영상 조각
프레임|Frame|frame|영상을 구성하는 한 장의 정지 화면.|한 프레임씩 확인해요.|영상 한 장
프레임 레이트|Frame rate|프레임률;FPS;프레임 속도|1초 동안 기록·재생하는 프레임 수.|프레임 레이트를 맞춰요.|초당 화면 수
코덱|Codec|codec|영상·음성을 압축하고 복원하는 방식이나 프로그램.|납품 코덱을 확인해요.|영상 압축 방식
렌더링|Rendering|렌더;render|편집·효과 결과를 계산해 화면으로 만드는 과정.|효과 구간을 렌더링해요.|효과 계산하는;최종 화면 만드는
크로마키|Chroma key|크로마 키;그린 스크린 합성|특정 색 영역을 투명하게 만들어 다른 화면과 합성하는 기법.|초록 배경을 크로마키로 빼요.|초록 배경 지우기
키프레임|Keyframe|키 프레임|특정 시점의 속성값을 지정하는 애니메이션 기준점.|위치에 키프레임을 넣어요.|시간 따라 위치 바꾸는
레터박스|Letterbox|레터 박스|화면 비율을 유지할 때 위아래에 남기는 띠 영역.|레터박스 없이 비율을 맞춰요.|위아래 검은 띠
러프 컷|Rough cut|러프컷;가편집|정밀한 다듬기 전 주요 흐름을 조립한 편집본.|러프 컷에서 구성을 확인해요.|초기 편집본;대략 연결한 영상
'''),
('film','전문 용어','녹음·음향','sound','''
룸 톤|Room tone|룸톤;공간음|대사나 동작 없이 녹음한 장소 고유의 배경 소리.|이 방의 룸 톤을 따요.|조용한 공간 소리 녹음;편집 빈 소리 채우기
라발리에|Lavalier microphone|핀 마이크;라발리어;lav mic|옷이나 몸에 부착하는 작은 마이크.|라발리에 옷 스침을 확인해요.|옷에 다는 작은 마이크
샷건 마이크|Shotgun microphone|샷건;지향성 샷건|정면 소리를 중심으로 받도록 설계된 길쭉한 지향성 마이크.|샷건을 화자 쪽으로 향해요.|긴 마이크;앞쪽 소리 받기
붐 폴|Boom pole|붐대;붐 마이크 대|마이크를 화면 밖에서 화자 가까이 두기 위한 긴 막대.|붐 폴이 화면에 안 들어오게 해요.|긴 막대 마이크;머리 위 마이크
'''),
('film','전문 용어','녹음·음향','phantom','''
팬텀 파워|Phantom power|팬텀 전원;48V;P48|마이크 케이블을 통해 공급하는 직류 전원.|마이크의 팬텀 파워 요구를 확인해요.|마이크 전원 공급;48볼트 전원
'''),
('film','전문 용어','제작·기획','production','''
프리프로덕션|Pre-production|프리 프로덕션;프리프로;사전 제작|본 촬영 전 기획·섭외·준비를 진행하는 단계.|프리프로덕션에서 동선을 정해요.|촬영 전 준비 단계
프로덕션|Production|본 촬영;production|계획한 장면을 실제로 촬영하는 제작 단계.|프로덕션 일정이 시작돼요.|실제로 촬영하는 단계
포스트프로덕션|Post-production|포스트 프로덕션;포스트;후반 작업|촬영 후 편집·색·음향 등을 완성하는 단계.|포스트프로덕션 일정을 잡아요.|촬영 끝나고 하는 작업
콜 시트|Call sheet|콜시트;촬영 일일 계획표|당일 촬영 일정·장소·참여자 등을 안내하는 문서.|내일 콜 시트를 확인해요.|촬영 당일 일정표
콜 타임|Call time|콜타임;집합 시간|촬영 참여자가 현장에 도착해야 하는 지정 시각.|팀마다 콜 타임이 달라요.|현장 도착 시간
블로킹|Blocking|배우 동선;동선 설계|장면 속 배우의 위치와 움직임을 정하는 작업.|블로킹에 맞춰 카메라를 옮겨요.|배우 움직임 정하는
'''),
('film','현장 표현','현장 진행','production','''
롤 카메라|Roll camera|카메라 롤;카메라 돌아|카메라 녹화를 시작하라는 지시.|롤 카메라, 준비됐습니다.|녹화 시작 지시
롤 사운드|Roll sound|사운드 롤|소리 녹음을 시작하라는 지시.|롤 사운드 후 신호를 기다려요.|녹음 시작 지시
액션|Action|액션 큐|배우의 연기·동작을 시작하라는 신호.|액션 후 문을 열어요.|연기 시작 신호
컷|Cut|커트;컷 사인|진행 중인 연기·촬영을 멈추라는 신호.|컷, 동선을 다시 맞춰요.|촬영 멈추는 신호
'''),
('film','전문 용어','제작·기획','film-glossary','''
스토리보드|Storyboard|스토리 보드;콘티;그림 콘티|숏의 순서와 구도를 그림으로 정리한 계획.|스토리보드로 흐름을 맞춰요.|촬영 전 그림 계획;장면 그림 순서
데일리스|Dailies|러시;러시스;rushes|그날 촬영분을 점검하기 위한 확인용 영상.|데일리스에서 연결을 확인해요.|당일 촬영본 확인
호리존|Cyclorama|사이클로라마;호리존 스튜디오;싸이클로라마|벽과 바닥의 경계를 곡면으로 이은 촬영 배경.|호리존에서 제품을 찍어요.|경계 없는 스튜디오 배경
'''),
('film','전문 용어','녹음·음향','film-glossary','''
폴리|Foley|폴리 사운드;폴리 효과|화면에 맞춰 동작 소리를 후반에 직접 만들어 녹음하는 작업.|발소리를 폴리로 보완해요.|발소리 따로 만드는;움직임 효과음
'''),
('film','전문 용어','화면 구성','film-glossary','''
컷어웨이|Cutaway|컷어웨이 샷|주요 행동에서 잠시 다른 대상·반응으로 시선을 돌리는 숏.|듣는 사람 컷어웨이를 넣어요.|다른 대상 끼워 넣는 장면
데이 포 나이트|Day for night|데이포나이트;낮밤 촬영|낮에 찍은 장면을 밤처럼 보이게 만드는 촬영·보정 방식.|데이 포 나이트를 테스트해요.|낮에 밤 장면 찍는
'''),
('film','전문 용어','노출·색','grading','''
색보정|Color correction|컬러 코렉션;색 보정|노출·색 균형 등을 조정해 영상의 기본 색 상태를 맞추는 작업.|카메라별 색보정을 맞춰요.|색상 밝기 맞추는
컬러 그레이딩|Color grading|그레이딩;색감 연출|장면의 감정과 분위기를 위해 색·명암을 설계하는 작업.|그레이딩으로 차가운 분위기를 줘요.|영화 색감 만드는
웨이브폼|Waveform monitor|웨이브 폼;파형 모니터|영상 신호의 밝기 등을 파형으로 확인하는 표시.|웨이브폼으로 밝기를 확인해요.|영상 밝기 그래프
'''),
('film','전문 용어','노출·색','color-workflow','''
LUT|Look-up table|룩업 테이블;루트;러트|입력 색 값을 정해진 출력 값으로 바꾸는 변환 표.|소스에 맞는 LUT를 적용해요.|색 변환 표;색감 프리셋 파일
로그 촬영|Log recording|로그;Log;로그 감마|밝기 정보를 로그 곡선으로 기록하는 촬영 방식.|로그 촬영본에 맞는 변환을 적용해요.|뿌옇게 찍는 영상;넓은 명암 기록
DIT|Digital imaging technician|디지털 이미징 테크니션;디아이티|현장에서 디지털 영상의 색·신호·작업 흐름을 관리하는 기술 담당자.|DIT와 모니터 색을 확인해요.|현장 디지털 색 관리 담당
'''),
]
NOTES={
'바스트 샷':'샷의 경계는 현장 관행에 따라 달라집니다. 가슴의 어느 지점까지 담을지 구체적으로 맞춰보세요.',
'웨이스트 샷':'WS는 문서에 따라 Wide Shot의 약자이기도 합니다. 약자만 보지 말고 프레이밍을 확인하세요.',
'팔로우':'대상을 따라가는 목적을 말합니다. 제자리에서 팬으로 따라갈 수도, 카메라가 이동할 수도 있어요. 초점 조작 장치인 팔로우 포커스와는 다릅니다.',
'시마이':'여러 작업 현장에서 일 마무리를 뜻하는 공통 표현입니다. 영상 항목의 예문은 촬영 상황에 맞춰 작성했습니다. ‘촬영 종료’, ‘마무리’로 바꿔 말할 수 있어요.',
'시퀀스':'여기서는 이야기 단위를 뜻합니다. 편집 프로그램에서는 여러 클립을 배치하는 타임라인 작업 단위를 가리키기도 합니다.',
'샷':'샷·숏·쇼트는 같은 영어 shot을 옮긴 표기입니다. 다른 단어 수로 부풀리지 않고 한 항목에 연결했습니다.',
'롤':'촬영 현장의 ‘롤 카메라’는 녹화 시작 지시이며, 여기서 설명한 카메라 회전과는 다른 쓰임입니다.',
'지브':'지미집(Jimmy Jib)은 장비 이름에서 온 현장 호칭입니다. 모든 지브가 해당 브랜드 제품인 것은 아닙니다.',
'스테디캠':'Steadicam은 장비 브랜드 이름입니다. 모든 안정화 장비나 전자식 짐벌을 뜻하는 일반명으로 혼동하지 마세요.',
'얕은 심도':'‘아웃포커싱’은 배경을 흐리게 만드는 효과를 찾는 검색 표현으로 연결했습니다. 화면 전체의 초점이 어긋난 상태와는 구별하세요.',
'팬텀 파워':'필요 전압과 지원 여부는 마이크·입력 장치에 따라 다릅니다. 모든 마이크에 켜야 하는 기능은 아닙니다.',
'로그 촬영':'Log는 RAW와 같은 뜻이 아닙니다. 기록 곡선과 카메라별 색 공간에 맞는 변환이 필요합니다.',
'LUT':'기술적인 색 공간 변환과 창작용 색감 적용 등 용도가 다릅니다. 어느 카메라·색 공간용인지 확인하세요.',
'호리존':'영문 자료의 cyclorama를 국내 촬영 배경 표현과 연결했습니다. 구체적인 공간 형태는 스튜디오마다 다릅니다.',
}

SOURCES.update({
 'slate':('StudioBinder','How to Use a Film Slate','https://www.studiobinder.com/blog/how-to-use-a-film-slate/','',False),
 'edit-tools':('Adobe','Premiere: Tools panel options','https://helpx.adobe.com/au/premiere/desktop/get-started/tour-the-workspace/tools-panel-and-options-panel.html','',False),
 'seoul-words':('서울특별시','슬기로운 말글살이 7: 이 말도 일본어?','https://mediahub.seoul.go.kr/archives/1298643','2020',True),
 'figma-dict':('Figma','Design dictionary','https://www.figma.com/dictionary/','',False),
 'figma-proto':('Figma','What is prototyping','https://www.figma.com/resource-library/what-is-prototyping/','',False),
 'mc-ab':('Mailchimp','About A/B tests','https://mailchimp.com/help/about-ab-tests/','',False),
 'mc-landing':('Mailchimp','What is a Landing Page?','https://mailchimp.com/marketing-glossary/landing-pages/','2026-05-07',False),
 'mc-cta':('Mailchimp','What is a CTA?','https://mailchimp.com/marketing-glossary/what-is-a-cta/','',False),
})
GROUPS.extend([
('film','전문 용어','현장 진행','slate','''
슬레이트|Film slate|클래퍼보드;딱판;clapperboard|숏 정보를 적고 소리와 화면을 맞추는 기준을 남기는 판.|슬레이트 번호를 확인해요.|촬영 전 딱 치는 판
싱크|Synchronization|싱크 맞추기;동기화;sync|따로 기록한 소리와 영상의 시점을 일치시키는 것.|슬레이트로 싱크를 맞춰요.|입모양과 소리 맞추는
MOS|MOS|엠오에스;무음 촬영|해당 촬영분에 소리를 녹음하지 않는다는 표시.|이 인서트는 MOS로 찍어요.|소리 없이 찍는;음성 녹음 없는 촬영
스크립트 슈퍼바이저|Script supervisor|스크립터;스크립티;scripty|테이크와 장면 연결 상태 등을 기록·점검하는 담당자.|스크립터가 연결을 확인해요.|촬영 기록 담당;장면 연결 체크
'''),
('film','현장 표현','현장 진행','slate','''
테일 슬레이트|Tail slate|엔드 슬레이트;꼬리 슬레이트|테이크 시작 대신 끝에서 슬레이트를 치는 방식.|이번에는 테일 슬레이트로 남겨요.|끝나고 슬레이트 치는
소프트 스틱스|Soft sticks|소프트 스틱|슬레이트를 약하게 치겠다는 안내.|얼굴 가까우니 소프트 스틱스로 가요.|슬레이트 살살 치기
세컨드 스틱스|Second sticks|세컨 스틱|슬레이트를 다시 치겠다는 신호.|소리가 작아 세컨드 스틱스로 갑니다.|슬레이트 다시 치기
'''),
('film','전문 용어','편집','edit-tools','''
리플 편집|Ripple edit|리플 에디트;잔물결 편집|클립 길이를 조절하며 뒤 클립들도 함께 밀거나 당기는 편집.|리플 편집으로 빈틈을 없애요.|잘라낸 만큼 뒤 영상 당기기
롤링 편집|Rolling edit|롤링 에디트;롤 편집|맞닿은 두 클립의 경계를 옮겨 전체 길이를 유지하는 편집.|롤링 편집으로 전환 시점을 옮겨요.|전체 길이 그대로 컷 경계 이동
슬립 편집|Slip edit|슬립 에디트|클립의 위치·길이를 유지하며 내부 시작·끝 프레임을 바꾸는 편집.|슬립 편집으로 표정을 바꿔요.|같은 자리 다른 구간 보여주기
슬라이드 편집|Slide edit|슬라이드 에디트|클립을 이동하고 인접 클립 길이를 조절해 전체 길이를 유지하는 편집.|슬라이드 편집으로 위치를 옮겨요.|양옆 길이 조절하며 클립 이동
트리밍|Trimming|트림;trim|클립의 시작점·끝점을 다듬는 작업.|숨 고르는 부분을 트리밍해요.|영상 앞뒤 잘라내기
'''),
('common','현장 표현','현장 표현','seoul-words','''
단도리|Preparation|단도리하다;채비|일이 잘 진행되도록 준비하고 챙긴다는 표현.|행사 전 단도리를 확인해요.|일 전 준비;미리 챙기는
기스|Scratch|기스나다;흠집|물건 표면에 난 흠이나 긁힌 자국을 부르는 말.|패널에 기스가 있는지 봐요.|표면 긁힌 자국
잇파이|Full|잇빠이;이빠이;입빠이|가득 또는 한껏이라는 뜻으로 쓰는 표현.|이 표현의 잇파이는 가득이라는 뜻이에요.|가득 채우는;한껏
구루마|Handcart|구르마;손수레|짐을 옮기는 수레를 부르는 현장 표현.|상자를 구루마로 옮겨요.|짐 옮기는 수레
'''),
('design','전문 용어','시각·편집 디자인','figma-dict','''
정렬|Alignment|얼라인;얼라인먼트|요소들을 일정한 기준선에 맞춰 배치하는 것.|제목을 왼쪽 정렬해요.|요소 줄 맞추기
대체 텍스트|Alternative text|alt text;알트 텍스트|이미지가 전달하는 내용을 글로 설명하는 정보.|사진에 대체 텍스트를 넣어요.|이미지 대신 읽어주는 설명
화면비|Aspect ratio|종횡비;가로세로비|화면 가로와 세로 길이의 비율.|화면비를 16대9로 맞춰요.|가로 세로 비율
베이스라인|Baseline|기준선;글자 기준선|글자가 놓이는 타이포그래피의 기준선.|본문 베이스라인을 맞춰요.|글자 아래 기준 선
불리언 연산|Boolean operation|도형 합치기;불리언|도형의 합치기·빼기·교차 등으로 형태를 만드는 연산.|불리언 연산으로 구멍을 뚫어요.|도형 합치고 빼는
베지어 곡선|Bézier curve|베지에;베지어;bezier|제어점으로 모양을 조절하는 수학적 곡선.|베지어 곡선으로 윤곽을 다듬어요.|점으로 곡선 조절
카피|Copy|문구;카피라이팅|디자인에 실제로 들어가는 제목·본문 등의 글.|버튼 카피를 짧게 줄여요.|디자인에 들어갈 글
어센더|Ascender|어센더 라인|소문자에서 x 높이 위로 올라온 부분.|어센더가 긴 서체예요.|소문자 위로 올라온 획
접근성|Accessibility|접근 가능한 디자인;A11y|다양한 능력과 환경의 사람이 제품을 이용할 수 있는 정도.|키보드 접근성을 확인해요.|누구나 사용 가능;장애 고려 디자인
'''),
('design','전문 용어','제품 디자인','figma-proto','''
프로토타입|Prototype|프로토타이핑;시제품|아이디어와 사용 흐름을 시험하기 위한 모형.|프로토타입으로 이동을 확인해요.|미리 눌러보는 모형
와이어프레임|Wireframe|와이어 프레임;화면 뼈대|세부 시각 표현 전 구조·배치를 나타내는 화면 설계.|와이어프레임에서 순서를 정해요.|화면 뼈대;레이아웃만 그린 화면
'''),
('marketing','전문 용어','실험·전환','mc-ab','''
A/B 테스트|A/B test|AB 테스트;에이비 테스트;분할 테스트|서로 다른 버전의 성과를 비교하는 실험.|제목 두 개를 A/B 테스트해요.|두 버전 성과 비교
'''),
('marketing','전문 용어','실험·전환','mc-landing','''
랜딩 페이지|Landing page|랜딩;랜딩페이지|광고·이메일 등을 눌러 도착하며 특정 행동을 유도하는 페이지.|광고와 랜딩 메시지를 맞춰요.|광고 누르면 나오는 페이지
전환|Conversion|컨버전;conversion|구매·가입 등 미리 정한 목표 행동을 완료하는 것.|신청 완료를 전환으로 잡아요.|목표 행동 달성;가입 완료
리드|Lead|잠재 고객;가망 고객|관심을 보여 향후 고객이 될 가능성이 있는 대상.|신청 폼으로 리드를 모아요.|관심 있는 잠재 고객
리드 캡처|Lead capture|리드 수집|후속 소통을 위해 잠재 고객의 연락 정보 등을 받는 것.|리드 캡처 폼을 줄여요.|잠재 고객 연락처 받기
'''),
('marketing','전문 용어','실험·전환','mc-cta','''
CTA|Call to action|씨티에이;콜 투 액션;행동 유도|다음 행동을 안내하거나 유도하는 문구·버튼·링크.|CTA를 신청하기로 바꿔요.|누르도록 유도하는 버튼;행동 유도 문구
'''),
])
MDN_ROWS='''
DNS|DNS|Domain Name System|디엔에스|도메인 이름을 IP 주소 등 관련 정보로 연결하는 이름 체계.|DNS 설정을 확인해요.|주소 이름을 IP로 찾는
URL|URL|Uniform Resource Locator|유알엘;웹 주소|인터넷 자원의 위치와 접근 방법을 나타내는 주소.|URL을 공유해 주세요.|웹페이지 주소
HTTPS|HTTPS|HTTP Secure|에이치티티피에스|TLS로 보호된 연결을 사용하는 HTTP 통신.|로그인 페이지는 HTTPS를 사용해요.|암호화된 웹 연결
REST|REST|Representational State Transfer|레스트;REST API|자원·표현·일관된 인터페이스 등의 원칙을 갖는 소프트웨어 구조 방식.|REST 원칙으로 API를 검토해요.|자원 중심 인터페이스
CRUD|CRUD|Create Read Update Delete|크러드|데이터의 생성·조회·수정·삭제를 묶어 부르는 말.|게시물 CRUD를 구현해요.|생성 조회 수정 삭제
CORS|CORS|Cross-origin resource sharing|코르스;교차 출처 리소스 공유|서버가 다른 출처의 브라우저 접근을 허용하도록 알리는 체계.|CORS 응답 헤더를 확인해요.|다른 도메인 요청 허용
Cookie|쿠키|Cookie|HTTP 쿠키;cookie|사이트가 브라우저에 저장하고 요청에 함께 보낼 수 있는 작은 데이터.|세션 쿠키를 확인해요.|브라우저 작은 저장 데이터
Authentication|인증|Authentication|어센티케이션;로그인 인증|사용자 등이 주장한 신원을 확인하는 과정.|인증 후 계정 화면을 열어요.|누구인지 확인;신원 확인
Asynchronous|비동기|Asynchronous|어싱크;async|작업 완료를 기다리는 동안 다른 처리를 진행할 수 있는 방식.|파일을 비동기로 읽어요.|기다리지 않고 다른 작업
Callback_function|콜백|Callback function|콜백 함수;callback|다른 함수에 전달되어 정해진 시점에 호출되는 함수.|완료 콜백을 등록해요.|나중에 호출할 함수 전달
Promise|프로미스|Promise|프라미스;promise|비동기 작업의 향후 완료·실패와 결과를 나타내는 객체.|프로미스 실패를 처리해요.|비동기 결과 객체
Array|배열|Array|어레이;array|여러 값을 순서대로 담는 자료 구조.|검색 결과를 배열에 담아요.|순서 있는 여러 값
Boolean|불리언|Boolean|불린;참거짓;bool|참 또는 거짓을 나타내는 논리 자료형.|저장 여부는 불리언이에요.|참 거짓 값
Function|함수|Function|펑션;function|특정 작업을 수행하도록 묶어 호출하는 코드 단위.|검색 로직을 함수로 묶어요.|다시 부르는 코드 묶음
Variable|변수|Variable|variable|값을 저장하거나 참조하기 위해 이름을 붙인 대상.|입력값을 변수에 담아요.|이름 붙여 값 저장
Null|null|Null|널;null 값|의도적으로 값이나 객체가 없음을 나타내는 값.|선택이 없으면 null로 둬요.|의도적으로 비어 있는 값
Undefined|undefined|Undefined|언디파인드|JavaScript에서 값이 정해지지 않은 상태를 나타내는 원시 값.|반환값이 undefined인지 확인해요.|값이 아직 정의되지 않은
Algorithm|알고리즘|Algorithm|알고리듬|문제를 풀거나 결과를 구하기 위한 일련의 절차.|검색 알고리즘을 비교해요.|문제 푸는 절차
SPA|SPA|Single-page application|싱글 페이지 앱;단일 페이지 앱|문서 전체를 매번 새로 받지 않고 화면 내용을 바꾸는 웹 앱 방식.|이 사전은 SPA로 동작해요.|한 페이지에서 화면 전환
'''
for line in MDN_ROWS.strip().splitlines():
 key,term,en,aliases,definition,example,phrases=line.split('|')
 source='mdn-'+key
 SOURCES[source]=('MDN Web Docs',key.replace('_',' '),'https://developer.mozilla.org/en-US/docs/Glossary/'+key,'',False)
 GROUPS.append(('dev','전문 용어','웹·프로그래밍',source,'|'.join([term,en,aliases,definition,example,phrases])))
NOTES.update({
'MOS':'약자의 유래에는 여러 설이 있어 단정하지 않았습니다. 여기서는 무음 촬영 표기라는 실제 용도만 설명합니다.',
'소프트 스틱스':'영어권 촬영 현장 자료에 나온 지시어입니다. 국내 모든 현장에서 같은 호칭을 쓰는 것은 아닙니다.',
'세컨드 스틱스':'영어권 촬영 현장 자료에 나온 지시어입니다. 국내에서는 ‘슬레이트 다시’ 등으로 말하기도 합니다.',
'잇파이':'‘가득’, ‘최대로’처럼 구체적인 말로 바꿀 수 있습니다. 장비 조절 지시라면 정확한 수치를 확인하세요.',
'인증':'신원을 확인하는 인증과 어떤 자원에 접근 가능한지 정하는 권한 부여는 구분합니다.',
'리드':'구체적인 리드 인정 기준은 조직과 캠페인마다 다릅니다.',
})

SOURCES.update({
 'negative-fill':('StudioBinder','What is Fill Light: Negative Fill','https://www.studiobinder.com/blog/what-is-fill-light-photography-definition/','2020-10-11',False),
 'anamorphic':('StudioBinder','What is an Anamorphic Lens?','https://www.studiobinder.com/blog/what-is-an-anamorphic-lens-definition/','',False),
 'macro':('StudioBinder','Macro Lens Shot','https://www.studiobinder.com/camera-shots/camera-lenses/macro-lens-shot/','',False),
})
# Point narrower concepts to the page that actually defines them.
SOURCE_OVERRIDES={'네거티브 필':'negative-fill','아나모픽':'anamorphic','매크로 렌즈':'macro'}
SOURCES['modelcast']=(*SOURCES['modelcast'][:3],'2012',True)
