// Choose the dictionary dataset BEFORE app.js reads window.WORD_DATA.
// app.js captures window.WORD_DATA once at boot, so it gets a live copy in the
// saved language; later language changes update that copy in place
// (language-switch.ts) instead of reloading the page.
import { readLang } from "./lang"
import { createLiveDataset, setBootLanguage } from "./language-switch"

try {
  const lang = readLang()
  ;(window as unknown as { WORD_DATA: unknown }).WORD_DATA = createLiveDataset(lang)
  setBootLanguage(lang)
  document.documentElement.lang = lang
} catch {
  /* ignore: fall back to the Korean dataset */
}
