// Save every input and its generated output to the Palette Drive (Data Room),
// one session folder per submission (Sessions/<session>/input + /output).
//
// Hooks the legacy UI without editing app.js, via capture-phase listeners:
//   - "Back up my data"      -> session "backup"   (records.json -> backup JSON + CSV)
//   - Tools › "Find terms"   -> session "document" (document.txt -> terms.json + terms.csv)
//   - "Import backup" file   -> session "import"   (uploaded file -> merge-result.json)
// Uploads go through the backend into the platform Drive (ctx.data_rooms).
// When the Drive is not available, backup falls back to a file download.
import { isPaletteApiError } from "@palettelab/sdk"
import { IS_LOCAL } from "./env"
import { LEGACY_HOST } from "./dom-setup"
import type { ApiFetch } from "./runtime"

// platform-provided fetch (usePlatform().apiFetch), set by installDriveSync
let apiFetch: ApiFetch = () => Promise.reject(new Error("drive sync not installed"))

const KEY = "daneoword.v1"
const SESSIONS_PATH = "/api/v1/plugins/allyourwords/drive/sessions"
const BACKUP_NAME = "다너의단어-내기록.json"

type DriveFile = { name: string; content: string; content_type?: string }
type Entry = { id: string; term: string; field: string; definition: string; example: string }
type Dataset = { entries: Entry[]; fields: { id: string; name: string }[]; redirects?: Record<string, string> }
type Workspace = {
  annotate: (text: string, entries: Entry[]) => { text: string; spans: { start: number; end: number; entries: Entry[] }[] }
  scope: (entries: Entry[], scopeId: string, profile: unknown) => Entry[]
  csv: (entries: Entry[], notes: Record<string, unknown>, fields: Dataset["fields"]) => string
}

const g = window as unknown as { WORD_DATA: Dataset; WorkspaceCore: Workspace }
const isEn = () => {
  if (!IS_LOCAL) return false // English is localhost-only
  try {
    return localStorage.getItem("daneo-lang") === "en"
  } catch {
    return false
  }
}
export const msg = (en: string, ko: string) => (isEn() ? en : ko)

// The OS may render the plugin inside an isolated root (iframe body / shadow
// DOM). Look elements up inside the app's own host first, then the document,
// and read the real event target through composedPath() (events crossing a
// shadow boundary are retargeted to the shadow host).
const q = <T extends Element = HTMLElement>(sel: string): T | null =>
  LEGACY_HOST.querySelector<T>(sel) ?? document.querySelector<T>(sel)
const evTarget = (ev: Event) => ((ev.composedPath?.()[0] ?? ev.target) as Element | null)

function readState(): Record<string, any> {
  try {
    return JSON.parse(localStorage.getItem(KEY) || "{}") || {}
  } catch {
    return {}
  }
}

let toastTimer: ReturnType<typeof setTimeout> | undefined
export function toast(text: string) {
  const el = q("#toast")
  if (!el) return
  el.textContent = text
  el.classList.add("show")
  if (toastTimer) clearTimeout(toastTimer)
  toastTimer = setTimeout(() => el.classList.remove("show"), 3200)
}

// One call into the plugin backend; never throws: returns status + parsed body
// so failures can be shown to the user with their real reason.
async function api(path: string, init?: RequestInit) {
  try {
    const res = await apiFetch(path, init)
    let body: any = null
    try {
      body = await res.clone().json()
    } catch {
      /* not JSON (e.g. a file) */
    }
    return { ok: res.ok, status: res.status, body, res }
  } catch (err) {
    console.error("[all-your-words] api", path, err)
    // The host apiFetch may throw PaletteApiError {status, detail} on non-2xx
    // responses; keep that status so 401/403/503 are shown, not "network".
    const e = err as { status?: unknown; detail?: unknown; message?: string }
    const status = isPaletteApiError(err) || typeof e?.status === "number" ? Number(e.status) || 0 : 0
    const detail = e?.detail ?? e?.message ?? String(err)
    return { ok: false, status, body: { detail }, res: null }
  }
}
const reason = (r: { status: number; body: any }) =>
  `${r.status || "network"}${r.body?.detail ? ` · ${typeof r.body.detail === "string" ? r.body.detail : JSON.stringify(r.body.detail)}` : ""}`

let lastFailure = ""
async function saveSession(kind: "backup" | "document" | "import" | "word", inputs: DriveFile[], outputs: DriveFile[]) {
  const r = await api(SESSIONS_PATH, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ kind, inputs, outputs }),
  })
  if (!r.ok) {
    lastFailure = reason(r)
    throw new Error(lastFailure)
  }
  lastFailure = ""
  return r.body as { session: string; path: string }
}

const fieldName = (id: string) => g.WORD_DATA.fields.find((f) => f.id === id)?.name ?? id
const word = (id: string) => {
  const real = g.WORD_DATA.redirects?.[id] || id
  return g.WORD_DATA.entries.find((e) => e.id === real)
}
const csvCell = (v: unknown) => {
  const s = String(v ?? "")
  const safe = /^[=+\-@\t\r]/.test(s) ? `'${s}` : s // neutralize spreadsheet formulas
  return /[",\n\r]/.test(safe) ? `"${safe.replace(/"/g, '""')}"` : safe
}

function download(content: string, filename: string, type: string) {
  const url = URL.createObjectURL(new Blob([content], { type }))
  const a = Object.assign(document.createElement("a"), { href: url, download: filename })
  document.body.appendChild(a)
  a.click()
  a.remove()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}

// --- 1) Back up my data -> Drive ----------------------------------------
async function backupToDrive() {
  const state = readState()
  const backup = JSON.stringify({ app: "daneoword", ...state }, null, 2)
  const saved = (state.saved || []).map(word).filter(Boolean) as Entry[]
  const csv = g.WorkspaceCore.csv(saved, state.notes || {}, g.WORD_DATA.fields)
  try {
    const res = await saveSession(
      "backup",
      [{ name: "records.json", content: JSON.stringify(state), content_type: "application/json" }],
      [
        { name: "all-your-words-backup.json", content: backup, content_type: "application/json" },
        { name: "my-words.csv", content: csv, content_type: "text/csv" },
      ],
    )
    toast(msg(`Saved to Drive · ${res.path}`, `Drive에 저장했어요 · ${res.path}`))
  } catch (err) {
    download(backup, BACKUP_NAME, "application/json")
    const why = String((err as Error)?.message || err)
    toast(msg(`Drive save failed (${why}) — downloaded the backup instead.`, `Drive 저장 실패 (${why}) — 백업 파일로 내려받았어요.`))
  }
}

// --- 2) Tools › Find terms -> Drive -------------------------------------
async function documentToDrive(text: string, scopeId: string) {
  const state = readState()
  let entries = g.WORD_DATA.entries
  try {
    entries = g.WorkspaceCore.scope(entries, scopeId, state.profile)
  } catch {
    /* fall back to every entry */
  }
  const doc = g.WorkspaceCore.annotate(text, entries)
  const terms = doc.spans.map((s) => ({
    text: text.slice(s.start, s.end),
    start: s.start,
    end: s.end,
    meanings: s.entries.map((e) => ({
      id: e.id,
      term: e.term,
      field: fieldName(e.field),
      definition: e.definition,
      example: e.example,
    })),
  }))
  const rows = [["text", "start", "end", "term", "field", "definition"].join(",")]
  for (const t of terms) for (const m of t.meanings) rows.push([t.text, t.start, t.end, m.term, m.field, m.definition].map(csvCell).join(","))
  try {
    const res = await saveSession(
      "document",
      [{ name: "document.txt", content: text, content_type: "text/plain" }],
      [
        { name: "terms.json", content: JSON.stringify({ scope: scopeId, count: terms.length, terms }, null, 2), content_type: "application/json" },
        { name: "terms.csv", content: rows.join("\n") + "\n", content_type: "text/csv" },
      ],
    )
    toast(msg(`${terms.length} terms saved to Drive · ${res.path}`, `용어 ${terms.length}개를 Drive에 저장했어요 · ${res.path}`))
  } catch {
    /* Drive unavailable: the on-screen result still works; stay quiet */
  }
}

// --- 3) Import backup -> Drive ------------------------------------------
async function importToDrive(file: File) {
  if (file.size > 20 * 1024 * 1024) return
  const before = readState()
  const content = await file.text()
  await new Promise((r) => setTimeout(r, 700)) // let app.js finish merging
  const after = readState()
  const count = (s: Record<string, any>) => ({ saved: (s.saved || []).length, notes: Object.keys(s.notes || {}).length })
  const result = {
    file: file.name,
    before: count(before),
    after: count(after),
    added_saved: (after.saved || []).filter((id: string) => !(before.saved || []).includes(id)),
  }
  try {
    const res = await saveSession(
      "import",
      [{ name: file.name || "import.json", content, content_type: file.type || "application/json" }],
      [{ name: "merge-result.json", content: JSON.stringify(result, null, 2), content_type: "application/json" }],
    )
    setTimeout(() => toast(msg(`Import saved to Drive · ${res.path}`, `가져온 파일을 Drive에 저장했어요 · ${res.path}`)), 2700)
  } catch {
    /* Drive unavailable: import itself already happened locally */
  }
}

// --- 4) Saved words (내 단어장) -> Drive -----------------------------------
// Every newly saved word, and every memo/collection change on a saved word,
// becomes its own "word" session: input/word.json + output/my-words.csv.
type Note = { text?: string; collection?: string }
let baseline: { saved: Set<string>; notes: Record<string, Note> } | null = null

function snapshot(json: string | null) {
  try {
    const s = JSON.parse(json || "{}") || {}
    return { saved: new Set<string>(s.saved || []), notes: (s.notes || {}) as Record<string, Note>, state: s }
  } catch {
    return null
  }
}

// Reset the comparison point without uploading (app boot, or data pulled from the backend).
export function resetSavedBaseline(json: string | null) {
  const snap = snapshot(json)
  if (snap) baseline = { saved: snap.saved, notes: snap.notes }
}

// Called on every save of the app state; uploads only what the user just added/changed.
export function trackSavedWords(json: string) {
  const snap = snapshot(json)
  if (!snap) return
  if (!baseline) {
    baseline = { saved: snap.saved, notes: snap.notes }
    return
  }
  const prev = baseline
  baseline = { saved: snap.saved, notes: snap.notes }
  const changed: Array<[string, "saved" | "memo"]> = []
  for (const id of snap.saved) {
    if (!prev.saved.has(id)) changed.push([id, "saved"])
    else {
      const a = prev.notes[id] || {}, b = snap.notes[id] || {}
      if ((a.text || "") !== (b.text || "") || (a.collection || "") !== (b.collection || "")) changed.push([id, "memo"])
    }
  }
  // A bulk change (e.g. "백업 가져오기" merging many words) already has its own
  // import session; don't create one folder per merged word.
  if (changed.length > 5) return
  for (const [id, action] of changed) void wordToDrive(id, action, snap.state)
}

async function wordToDrive(id: string, action: "saved" | "memo", state: Record<string, any>) {
  const e = word(id)
  if (!e) return
  const note = (state.notes || {})[id] || {}
  const item = {
    id: e.id,
    term: e.term,
    field: fieldName(e.field),
    definition: e.definition,
    example: e.example,
    memo: note.text || "",
    collection: note.collection || "",
    action,
    saved_at: new Date().toISOString(),
  }
  const saved = (state.saved || []).map(word).filter(Boolean) as Entry[]
  const csv = g.WorkspaceCore.csv(saved, state.notes || {}, g.WORD_DATA.fields)
  try {
    const res = await saveSession(
      "word",
      [{ name: "word.json", content: JSON.stringify(item, null, 2), content_type: "application/json" }],
      [{ name: "my-words.csv", content: csv, content_type: "text/csv" }],
    )
    // after app.js's own "내 단어장에 담았어요" toast
    setTimeout(() => toast(msg(`"${e.term}" saved to Drive · ${res.path}`, `"${e.term}" Drive에 저장했어요 · ${res.path}`)), 2700)
  } catch {
    /* reason is shown in the Drive panel (last save failed …) */
  }
}

let installed = false
export function installDriveSync(platformFetch: ApiFetch) {
  apiFetch = platformFetch
  if (installed) return
  installed = true

  LEGACY_HOST.addEventListener(
    "click",
    (ev) => {
      const btn = evTarget(ev)?.closest?.('[data-action="export"]')
      if (!btn) return
      ev.preventDefault()
      ev.stopPropagation() // replace the legacy download with a Drive save
      void backupToDrive()
    },
    true,
  )

  LEGACY_HOST.addEventListener(
    "submit",
    (ev) => {
      const form = evTarget(ev)?.closest?.("form") as HTMLFormElement | null
      if (form?.id !== "extract-form") return
      const data = new FormData(form)
      const text = String(data.get("text") ?? "").slice(0, 20000)
      if (!text.trim()) return
      const scopeId = String(data.get("scope") ?? "work")
      setTimeout(() => void documentToDrive(text, scopeId), 0) // app.js renders first
    },
    true,
  )

  LEGACY_HOST.addEventListener(
    "change",
    (ev) => {
      const input = evTarget(ev) as HTMLInputElement | null
      if (input?.id !== "import-file" || !input.files?.[0]) return
      void importToDrive(input.files[0])
    },
    true,
  )
}
