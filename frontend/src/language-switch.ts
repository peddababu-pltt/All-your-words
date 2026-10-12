// Switch the dictionary language in place, without reloading the page.
//
// app.js captures `window.WORD_DATA` once at boot (const D) but reads
// D.entries / D.fields on every render, and keeps some entry objects (today's
// word, document scan results). So the live dataset is a private copy whose
// entry and field objects are updated in place from the chosen language's
// dataset; the original KO / EN / JA datasets are never modified.
import { applyLanguage } from "./translate"
import { LEGACY_HOST } from "./dom-setup"
import { saveLang, type Lang } from "./lang"

type Item = Record<string, unknown> & { id: string }
type Dataset = Record<string, unknown> & { entries: Item[]; fields: Item[] }

const w = window as unknown as {
  WORD_DATA: Dataset
  WORD_DATA_EN?: Dataset
  WORD_DATA_JA?: Dataset
}

const usable = (d?: Dataset) => (d && Array.isArray(d.entries) && d.entries.length ? d : undefined)

// captured before app.js boots (this module is imported by dataset-select)
const DATASETS: Record<Lang, Dataset | undefined> = {
  ko: w.WORD_DATA,
  en: usable(w.WORD_DATA_EN),
  ja: usable(w.WORD_DATA_JA),
}

const copy = (d: Dataset): Dataset => ({
  ...d,
  fields: d.fields.map((f) => ({ ...f })),
  entries: d.entries.map((e) => ({ ...e })),
})

/** Live dataset for app.js, starting in `lang` (falls back to Korean). */
export function createLiveDataset(lang: Lang): Dataset {
  return copy(DATASETS[lang] ?? (DATASETS.ko as Dataset))
}

function replaceInPlace(target: Item, source: Item) {
  for (const key of Object.keys(target)) if (!(key in source)) delete target[key]
  Object.assign(target, source)
}

function syncItems(live: Item[], source: Item[]) {
  const byId = new Map(source.map((item) => [item.id, item]))
  for (const item of live) {
    const next = byId.get(item.id)
    if (next) replaceInPlace(item, { ...next })
  }
}

let current: Lang | null = null

/** Change interface + dictionary language and re-render the current page. */
export function switchLanguage(lang: Lang) {
  const source = DATASETS[lang]
  if (!source || lang === current) return
  current = lang
  saveLang(lang)
  document.documentElement.lang = lang

  const live = w.WORD_DATA
  syncItems(live.entries, source.entries)
  syncItems(live.fields, source.fields)
  for (const key of Object.keys(source)) {
    if (key !== "entries" && key !== "fields") live[key] = source[key]
  }

  applyLanguage(LEGACY_HOST, lang)
  // app.js re-renders on hashchange when the history entry looks new
  history.replaceState({ ...(history.state ?? {}), daneoView: undefined }, "")
  window.dispatchEvent(new HashChangeEvent("hashchange"))
}

/** Record the language the app booted in (no re-render needed). */
export function setBootLanguage(lang: Lang) {
  current = lang
}
