// core.js and workspace-core.js are UMD modules. Because they reference
// `module.exports`, esbuild bundles them as CommonJS and captures their export
// instead of running the UMD `window.*` branch. Re-attach them to window here,
// which app.js reads as window.WordCore / window.WorkspaceCore.
//
// This module is imported before "../app.js" so the globals exist at boot.
import WordCore from "../core.js"
import WorkspaceCore from "../workspace-core.js"
import { readLang } from "./lang"

;(window as unknown as Record<string, unknown>).WordCore = WordCore
;(window as unknown as Record<string, unknown>).WorkspaceCore = WorkspaceCore

// The legacy CSV export ("표로 내보내기" and the Drive my-words.csv) always
// writes a Korean header row. Swap it for the current language.

const CSV_HEADER: Record<string, string[]> = {
  en: ["Word", "Field", "Meaning", "Example", "My note", "Collection"],
  ja: ["単語", "分野", "意味", "例文", "マイメモ", "コレクション"],
}
const KO_HEADER = '\ufeff"단어","분야","뜻","예문","내 메모","모음"'
const legacyCsv = WorkspaceCore.csv as (...args: unknown[]) => string
WorkspaceCore.csv = (...args: unknown[]) => {
  const out = legacyCsv(...args)
  const header = CSV_HEADER[readLang()]
  return header && out.startsWith(KO_HEADER)
    ? "\ufeff" + header.map((h) => `"${h}"`).join(",") + out.slice(KO_HEADER.length)
    : out
}
