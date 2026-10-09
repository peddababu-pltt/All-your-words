// Choose the dictionary dataset BEFORE app.js reads window.WORD_DATA.
// When the saved language is English and an English dataset is bundled, swap
// window.WORD_DATA to the EN dataset so app.js (which captures it once at boot)
// renders English content. Language changes trigger a reload (see Controls), so
// this runs with the right choice on every load.
import { IS_LOCAL } from "./env"

const LANG_KEY = "daneo-lang"

try {
  // English is a localhost-only feature; hosted builds always use Korean.
  const lang = IS_LOCAL ? localStorage.getItem(LANG_KEY) : "ko"
  const en = (window as unknown as { WORD_DATA_EN?: { entries?: unknown[] } }).WORD_DATA_EN
  if (lang === "en" && en && Array.isArray(en.entries) && en.entries.length) {
    ;(window as unknown as { WORD_DATA: unknown }).WORD_DATA = en
  }
} catch {
  /* ignore: fall back to the Korean dataset */
}
