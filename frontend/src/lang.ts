// Saved interface/dictionary language. Korean is the default; the user picks
// English or Japanese from the language switcher.
export type Lang = "ko" | "en" | "ja"

export const LANG_KEY = "daneo-lang"
export const LANGS: Array<[Lang, string]> = [
  ["ko", "한국어"],
  ["en", "English"],
  ["ja", "日本語"],
]

export function toLang(value: unknown): Lang | null {
  const v = String(value || "").toLowerCase().slice(0, 2)
  return v === "ko" || v === "en" || v === "ja" ? v : null
}

// window.name survives the reload even in a sandboxed iframe without storage
const NAME_PREFIX = "daneo-lang:"

export function storedLang(): Lang | null {
  try {
    const saved = toLang(localStorage.getItem(LANG_KEY))
    if (saved) return saved
  } catch {
    /* storage blocked */
  }
  return window.name.startsWith(NAME_PREFIX) ? toLang(window.name.slice(NAME_PREFIX.length)) : null
}

export function saveLang(lang: Lang) {
  try {
    localStorage.setItem(LANG_KEY, lang)
  } catch {
    /* storage blocked */
  }
  window.name = NAME_PREFIX + lang
}

export function readLang(): Lang {
  return storedLang() ?? "ko"
}
