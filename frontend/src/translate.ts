// Full KO <-> EN layer for the legacy app's INTERFACE strings.
// Covers every rendered UI phrase in app.js (nav, headings, labels, buttons,
// toasts, aria). The dictionary ENTRY text (definitions / examples for the
// 2,882 Korean terms) lives in data.js and is content, not chrome — it stays
// Korean unless separately machine-translated.
//
// Exact full-text-node replacement + regex for counts, re-applied on every
// legacy re-render via MutationObserver. The wordmark 다, 너의 단어 is the brand and stays as-is.

type Lang = "ko" | "en"

const EN: Record<string, string> = {
  // field names (also dictionary field labels) — kept short so cards don't overflow
  "마케팅·광고": "Marketing",
  "개발·IT": "Dev & IT",
  "패션·섬유": "Fashion",
  "영상·촬영": "Film",
  "디자인": "Design",
  "인사·재무": "HR & Finance",
  "업무 공통": "Common",
  // card badges
  "내 업무": "My work",
  "관심": "Interest",
  // suggestion / hint lines
  "↑ ↓ 선택": "↑ ↓ Select",
  "Enter 검색": "Enter to search",
  "뜻과 쓰임": "Meaning & usage",
  // nav / shell
  "찾기": "Search",
  "업무 도구": "Tools",
  "내 단어장": "My Words",
  "나의 단어장": "My Words",
  "나의 사전": "My Dictionary",
  "일하는 사람의 언어 사전": "A language dictionary for people at work",
  "단어 하나로, 조금 더 넓은 세계.": "One word, a slightly wider world.",
  "나의 맞춤 설정": "My Settings",
  "자료와 백업": "Data & Backup",
  "주요 메뉴": "Main menu",
  "모바일 주요 메뉴": "Mobile main menu",
  "본문으로 바로가기": "Skip to content",
  "다, 너의 단어 홈": "All your Words home",

  // onboarding
  "나만의 사전 준비하기": "Set up your dictionary",
  "맞춤 설정 단계": "Setup steps",
  "내 업무 분야": "My field",
  "관심 분야": "Interests",
  "보기 설정": "Display",
  "여러 개를 골라도 좋아요": "Pick as many as you like",
  "어떤 세계에서 일하고 있나요?": "Which world do you work in?",
  "선택한 분야를 기본 검색 범위로 설정해요.": "Your choice sets the default search scope.",
  "아직 정하지 않았다면 모든 분야로 시작해도 좋아요.": "Not sure yet? You can start with every field.",
  "또 어떤 세계가 궁금하세요?": "What other worlds are you curious about?",
  "어떤 세계가 궁금하세요?": "Which worlds are you curious about?",
  "관심 분야는 나중에 추가해도 좋아요.": "You can add interests later.",
  "다른 분야도 따로 모아 빠르게 찾아볼 수 있어요.": "Other fields are grouped so you can find them fast.",
  "설명을 읽는 순서와 목록의 간격을 정해요.": "Choose the reading order and list spacing.",
  "설명 순서": "Explanation order",
  "예문 먼저 보기": "Example first",
  "뜻 먼저 보기": "Meaning first",
  "목록의 간격": "List spacing",
  "촘촘하게": "Compact",
  "여유롭게": "Comfortable",
  "사전을 보기 편하게.": "Make the dictionary easy to read.",
  "모두 선택 사항이에요": "All optional",
  "다음": "Next",
  "이전": "Back",
  "먼저 둘러보기": "Explore first",
  "내 사전 시작하기": "Start my dictionary",
  "내 사전 시작하기 ": "Start my dictionary",
  "내 분야·관심 설정": "Field & interest setup",
  "내게 맞게 설정하기": "Set up for me",
  "회사명·개인정보 없이, 선택한 내용만 이 브라우저에 저장해요.": "No company or personal info — only your choices are saved in this browser.",
  "당신의 분야": "Your field",
  "당신의 일을 이해하는 사전": "A dictionary that understands your work",
  "낯선 말도,": "Even unfamiliar words,",
  "내 말이 되도록.": "become your own.",
  "필요한 순간, 바로 찾는 말": "The word you need, right when you need it",

  // home
  "오늘, 하나의 단어": "Today, one word",
  "오늘의 단어": "Word of the day",
  "오늘의 발견": "Today's find",
  "오늘 하나의 단어 새로고침": "Refresh today's word",
  "같은 단어, 다른 의미": "Same word, different meaning",
  "같은 단어 다른 의미 새로고침": "Refresh same-word different-meaning",
  "최근 기록": "Recent",
  "최근 본 단어": "Recently viewed",
  "최근 본 단어 20개와 최근 검색을 모았어요.": "The last 20 words you viewed and your recent searches.",
  "발견 카드 선택": "Choose a discovery card",
  "단어, 줄임말, 궁금한 상황을 검색해 보세요.": "Search a word, abbreviation, or a situation.",
  "단어를 찾거나, 궁금한 상황을 적어보세요": "Search a word, or describe a situation",
  "단어를 찾거나, 상황을 적어보세요.": "Search a word, or describe a situation.",
  "단어 또는 궁금한 상황 검색": "Search a word or a situation",
  "나란히 놓고, 뜻 비교.": "Side by side — compare meanings.",
  "뜻을 함께 보면 차이가 보여요.": "Seeing meanings together reveals the difference.",
  "원문을 읽으며, 필요한 뜻만.": "Read the source — only the meanings you need.",

  // search / list
  "검색": "Search",
  "검색어 지우기": "Clear search",
  "예상 검색어": "Suggestions",
  "이 단어를 찾으세요?": "Looking for this word?",
  "모든 분야": "All fields",
  "모든 분야에서 찾기": "Search all fields",
  "모든 단어": "All words",
  "전체 단어": "All words",
  "전체 단어 보기": "See all words",
  "전체 사전": "Full dictionary",
  "궁금한 분야": "Fields of interest",
  "단어 종류": "Word type",
  "전문 용어": "Technical term",
  "현장 표현": "Field expression",
  "주제": "Topic",
  "모든 주제": "All topics",
  "분야": "Field",
  "찾을 분야": "Field to search",
  "분야 설정": "Field settings",
  "분야 둘러보기": "Browse fields",
  "모두 보기": "See all",
  "다른 단어": "Other words",
  "단어 찾기": "Find words",
  "단어 찾기로": "To word search",
  "단어 찾으러 가기": "Go find words",
  "용어 찾기": "Find terms",
  "비교할 단어 찾기": "Find words to compare",
  "상황 조건 해제": "Clear situation filter",
  "선택한 조건에 맞는 말이 없어요.": "No words match the selected filters.",
  "조건에 맞는 단어가 없어요.": "No words match the filters.",
  "찾을 분야를 바꾸거나 원문을 수정해 보세요.": "Try changing the field or editing the text.",
  "다른 분야에 있는 뜻도 찾아보세요.": "Look for meanings in other fields too.",
  "새로운 뜻을 준비하고 있어요.": "New meanings are on the way.",

  // detail
  "단어 읽기": "Reading",
  "뒤로 가기": "Back",
  "돌아가기": "Back",
  "처음으로": "Home",
  "현장에서는 이렇게 말해요": "How it's said on the job",
  "함께 알아두면 좋은 말": "Related terms",
  "다른 분야의 뜻": "Meaning in other fields",
  "다른 분야의 쓰임": "Use in other fields",
  "다른 예시": "Other example",
  "자세히 보기": "Details",
  "사전에서 자세히 보기": "See details in the dictionary",
  "용어 뜻": "Term meaning",
  "용어가 표시된 원문": "Source with terms marked",
  "문서 속 용어": "Terms in the document",
  "같은 표현도 팀과 상황에 따라 다르게 쓰일 수 있어요.": "The same expression can be used differently by team and situation.",
  "쓰임을 설명하기 위해 직접 작성한 예시": "An example written to show usage",
  "뜻 작성 안내": "About this definition",
  "공개 자료를 바탕으로 뜻을 짧게 다시 썼어요.": "The meaning was briefly rewritten from public sources.",
  "과거 문헌에 기록된 표현을 포함합니다. 현장마다 쓰임이 다를 수 있어요.": "Includes expressions recorded in older sources. Usage can vary by workplace.",
  "일반 지식을 바탕으로 뜻과 예문을 직접 작성했어요. 별도로 확인한 외부 출처는 첨부하지 않았어요.": "The meaning and example were written from general knowledge, with no separately verified external source attached.",
  "단어를 찾을 수 없어요.": "Word not found.",
  "페이지를 찾을 수 없어요.": "Page not found.",

  // saved / notes
  "나의 메모": "My note",
  "나만 볼 수 있어요": "Only you can see this",
  "메모 저장": "Save note",
  "메모와 모음을 저장했어요.": "Saved your note and collection.",
  "우리 팀에서 쓰는 뜻, 회의에서 들었던 맥락을 남겨보세요.": "Jot down your team's meaning or the context you heard in a meeting.",
  "내 단어장 검색": "Search my words",
  "단어·메모 검색": "Search words & notes",
  "업무별 모음": "Collections",
  "모든 모음": "All collections",
  "내 단어장에 담기": "Save to my words",
  "내 단어장에 담았어요.": "Saved to my words.",
  "내 단어장에서 빼기": "Remove from my words",
  "단어장에서 뺐어요.": "Removed from my words.",
  "다시 만나고 싶은 말을 담아보세요.": "Save the words you want to meet again.",
  "살펴본 단어를 여기서 다시 만나요.": "Meet the words you've viewed here again.",
  "단어를 저장하고, 업무별 모음과 메모를 남길 수 있어요.": "Save words and add collections and notes.",
  "표로 내보내기": "Export as table",
  "빼기": "Remove",
  "지우기": "Clear",
  "기록 지우기": "Clear history",
  "내 업무에 남겨 둔 말": "Words kept for my work",
  "내 업무에 포함됨": "Included in my work",
  "내 업무 분야에서 먼저 찾아요.": "Searches your field first.",

  // tools / compare
  "뜻 복사": "Copy meaning",
  "뜻과 예문을 복사했어요.": "Copied the meaning and example.",
  "뜻 비교": "Compare",
  "뜻 비교에 담기": "Add to compare",
  "업무 도구의 뜻 비교에 담았어요.": "Added to compare in Tools.",
  "비교에서 빼기": "Remove from compare",
  "비교에서 뺐어요.": "Removed from compare.",
  "최대 3개까지 비교할 수 있어요. 업무 도구에서 먼저 빼 주세요.": "You can compare up to 3. Remove one in Tools first.",
  "단어 상세 화면에서 최대 3개의 뜻을 담아 비교하세요.": "Add up to 3 meanings from a word page to compare.",
  "문서 속 낯선 말을 한 번에.": "Unfamiliar words in a document, all at once.",
  "회의록·메일을 붙여 넣고, 낯선 단어 위에서 뜻을 확인하세요.": "Paste a memo or email, and check meanings over unfamiliar words.",
  "용어를 찾을 문서": "Document to scan",
  "원문 수정": "Edit source",
  "다시 찾기": "Scan again",
  "표시된 단어에 마우스를 올리거나 눌러보세요.": "Hover or tap a highlighted word.",
  "표시할 용어를 찾지 못했어요": "No terms found to mark",
  "수록된 단어와 별칭을 형광펜으로 표시해요. 여러 뜻이 있으면 분야와 예문을 함께 확인하세요.": "Listed words and aliases are highlighted. If there are several meanings, check the field and example.",
  "입력한 문서는 저장·전송하지 않아요.": "Your text is not saved or sent.",
  "어제 찾은 말, 다시 찾기.": "Find yesterday's words again.",
  "단어를 열어 보면 여기에 기록돼요.": "Words you open are recorded here.",

  // about / backup / help
  "내 기록 백업하기": "Back up my data",
  "내 기록을 다른 곳에서도.": "Your data, anywhere.",
  "단어장·메모·맞춤 설정은 이 브라우저에 저장돼요.": "Your words, notes, and settings are saved in this browser.",
  "기기를 바꾸기 전에 백업 파일을 내려받으세요.": "Download a backup file before switching devices.",
  "백업 가져오기": "Import backup",
  "백업 파일 가져오기": "Import backup file",
  "가져오면 단어장과 메모를 합치고 맞춤 설정을 복원해요. 같은 단어의 기존 메모는 유지해요.": "Importing merges your words and notes and restores settings. Existing notes for the same word are kept.",
  "단어장·메모를 합치고 맞춤 설정을 복원했어요.": "Merged your words and notes and restored settings.",
  "올바른 다, 너의 단어 백업 파일을 선택해 주세요.": "Please choose a valid All your Words backup file.",
  "나의 기록, 사전의 근거": "My records, the dictionary's basis",
  "자료와 보관 안내": "Data & storage notice",
  "검색과 문서 도구는 어떻게 작동하나요?": "How do search and the document tool work?",
  "등록된 단어·별칭·뜻·검색 문장을 비교해서 찾아요. 문서 도구는 입력한 글에 있는 수록 표현을 찾아주며, 전체 맥락이나 의도를 판단하지 않아요. 입력한 문서는 서버로 보내거나 브라우저 저장소에 보관하지 않아요. 생성형 AI와 외부 API를 사용하지 않아요.": "It matches registered words, aliases, meanings, and search phrases. The document tool finds listed expressions in your text; it does not judge overall context or intent. Your text is not sent to a server or kept in browser storage. No generative AI or external APIs are used.",
  "뜻과 예문은 어떻게 만들었나요?": "How were the meanings and examples made?",
  "현재 수록 분야 · 7개": "Fields included · 7",

  // toasts / errors
  "저장": "Save",
  "저장 취소": "Unsave",
  "닫기": "Close",
  "현재 브라우저에 저장할 수 없어요. 이번 탭에서만 유지돼요.": "Can't save in this browser. Kept only in this tab.",
  "브라우저 저장소를 읽지 못했어요. 저장 가능 여부를 확인해 주세요.": "Couldn't read browser storage. Check whether saving is allowed.",
  "복사가 제한된 브라우저예요. 본문을 선택해 복사해 주세요.": "Copying is restricted in this browser. Select the text to copy.",

  // misc labels
  "내 분야": "My field",
  "설정 저장하기": "Save settings",
  "예: 신규 캠페인, 월말 결산": "e.g. new campaign, month-end closing",
  "예: 키카피와 키비주얼의 톤앤매너를 맞추고, 내일 PT 전에 시안을 디벨롭해 주세요.": "e.g. align the key copy and key visual tone, and develop the draft before tomorrow's presentation.",
}

// regex rules (both directions handled explicitly)
const KO_TO_EN_RX: Array<[RegExp, (m: RegExpMatchArray) => string]> = [
  [/^뜻 비교 (\d+)$/, (m) => `Compare ${m[1]}`],
  [/^(\d[\d,]*)개 표현$/, (m) => `${m[1]} terms`],
  [/^· (\d[\d,]*)곳에 표시했어요$/, (m) => `· highlighted in ${m[1]} places`],
  [/^(.+?) · (\d+)개 분야 · (\d[\d,]*)개 뜻$/, (m) => `${m[1]} · ${m[2]} fields · ${m[3]} meanings`],
  [/^(\d[\d,]*)개의 뜻과 나만의 메모\.$/, (m) => `${m[1]} meanings and your own notes.`],
  [/^(.+) 외 (\d+)$/, (m) => `${m[1]} +${m[2]}`],
  [/^더 보기 \((\d[\d,]*) \/ (\d[\d,]*)\)$/, (m) => `Show more (${m[1]} / ${m[2]})`],
  [/^(\d[\d,]*)개의 세계, (\d[\d,]*)개의 뜻$/, (m) => `${m[1]} worlds, ${m[2]} meanings`],
  [/^(\d[\d,]*)개 뜻 · 자료와 백업$/, (m) => `${m[1]} meanings · Data & Backup`],
  [/^(\d[\d,]*)개 뜻$/, (m) => `${m[1]} meanings`],
  [/^(\d[\d,]*)개의 뜻$/, (m) => `${m[1]} meanings`],
  [/^(\d[\d,]*)개$/, (m) => `${m[1]}`],
]
const EN_TO_KO_RX: Array<[RegExp, (m: RegExpMatchArray) => string]> = [
  [/^Compare (\d+)$/, (m) => `뜻 비교 ${m[1]}`],
  [/^(\d[\d,]*) terms$/, (m) => `${m[1]}개 표현`],
  [/^· highlighted in (\d[\d,]*) places$/, (m) => `· ${m[1]}곳에 표시했어요`],
  [/^(.+?) · (\d+) fields · (\d[\d,]*) meanings$/, (m) => `${m[1]} · ${m[2]}개 분야 · ${m[3]}개 뜻`],
  [/^(\d[\d,]*) meanings and your own notes\.$/, (m) => `${m[1]}개의 뜻과 나만의 메모.`],
  [/^Show more \((\d[\d,]*) \/ (\d[\d,]*)\)$/, (m) => `더 보기 (${m[1]} / ${m[2]})`],
  [/^(\d[\d,]*) worlds, (\d[\d,]*) meanings$/, (m) => `${m[1]}개의 세계, ${m[2]}개의 뜻`],
  [/^(\d[\d,]*) meanings · Data & Backup$/, (m) => `${m[1]}개 뜻 · 자료와 백업`],
  [/^(\d[\d,]*) meanings$/, (m) => `${m[1]}개 뜻`],
]

const KO: Record<string, string> = Object.fromEntries(
  Object.entries(EN).map(([k, v]) => [v, k]),
)

let currentLang: Lang = "ko"
let observer: MutationObserver | null = null

function swap(text: string, lang: Lang): string | null {
  const t = text.trim()
  if (!t) return null
  if (lang === "en") {
    if (EN[t]) return text.replace(t, EN[t])
    for (const [rx, fn] of KO_TO_EN_RX) {
      const m = t.match(rx)
      if (m) return text.replace(t, fn(m))
    }
  } else {
    if (KO[t]) return text.replace(t, KO[t])
    for (const [rx, fn] of EN_TO_KO_RX) {
      const m = t.match(rx)
      if (m) return text.replace(t, fn(m))
    }
  }
  return null
}

function walk(root: Node, lang: Lang) {
  const tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT)
  const nodes: Text[] = []
  let n: Node | null
  while ((n = tw.nextNode())) nodes.push(n as Text)
  for (const node of nodes) {
    const parent = node.parentElement
    if (parent && (parent.tagName === "SCRIPT" || parent.tagName === "STYLE")) continue
    const out = swap(node.nodeValue || "", lang)
    if (out != null) node.nodeValue = out
  }
  const el = root instanceof Element ? root : (root as Document).body
  if (el && "querySelectorAll" in el) {
    el.querySelectorAll<HTMLElement>("[placeholder],[aria-label]").forEach((e) => {
      for (const attr of ["placeholder", "aria-label"]) {
        const v = e.getAttribute(attr)
        if (!v) continue
        const out = swap(v, lang)
        if (out != null) e.setAttribute(attr, out)
      }
    })
  }
}

export function applyLanguage(host: HTMLElement, lang: Lang) {
  currentLang = lang
  walk(host, lang)
  if (!observer) {
    observer = new MutationObserver((muts) => {
      for (const m of muts) {
        // toasts and live labels change text in place (textContent / nodeValue)
        if (m.type === "characterData" && m.target.nodeType === Node.TEXT_NODE) {
          const out = swap(m.target.nodeValue || "", currentLang)
          if (out != null) m.target.nodeValue = out // swapped text never matches again: no loop
          continue
        }
        m.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE || node.nodeType === Node.TEXT_NODE) {
            walk(node, currentLang)
          }
        })
      }
    })
    observer.observe(host, { childList: true, subtree: true, characterData: true })
  }
}

export type { Lang }
