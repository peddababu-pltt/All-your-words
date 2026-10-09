// App state lives only in the platform Drive (Data Room "다, 너의 단어 (All your Words)").
//
// On open:  POST /drive/init  → the backend creates/reuses the data room (+ State/,
//           Sessions/ folders) and returns the newest State/…-records.json.
//           That state is loaded into the app (in-memory storage, see storage-shim).
//           If the Drive has no state yet but an older version left data in the
//           browser, that data is moved into the Drive and removed from the browser.
// On change: when saved words / memos / settings change, a new snapshot is written
//           (debounced) with PUT /drive/state. Viewing or searching alone writes nothing.
import { LEGACY_HOST } from "./dom-setup"
import { LEGACY_STATE, STATE_KEY, forgetLegacyState } from "./storage-shim"
import { msg, resetSavedBaseline, toast, trackSavedWords } from "./drive-sync"
import type { ApiFetch } from "./runtime"

const INIT_PATH = "/api/v1/plugins/allyourwords/drive/init"
const STATE_PATH = "/api/v1/plugins/allyourwords/drive/state"
const MEANINGFUL = ["saved", "notes", "profile", "fields", "onboarded", "compare"] as const
const SAVE_DEBOUNCE_MS = 1500

let apiFetch: ApiFetch | null = null
let ready = false // no Drive writes until the Drive state has been loaded
let lastMeaningful = ""
let pending: Record<string, unknown> | null = null
let timer: ReturnType<typeof setTimeout> | undefined
let nativeSetItem: ((k: string, v: string) => void) | null = null

const meaningful = (s: Record<string, unknown> | null) => JSON.stringify(MEANINGFUL.map((k) => s?.[k] ?? null))

// Normalize exactly like app.js's validate() so the first save after loading
// (which only adds defaults) is not mistaken for a real change.
function normalized(raw: Record<string, unknown>): Record<string, unknown> {
  try {
    const g = window as unknown as {
      WORD_DATA: { entries: unknown[]; fields: unknown[]; redirects?: unknown }
      WordCore: { validateState: (r: unknown, e: unknown, f: unknown, d: unknown) => Record<string, unknown> }
      WorkspaceCore: { normalize: (r: unknown, e: unknown, f: unknown, d: unknown) => Record<string, unknown> }
    }
    const D = g.WORD_DATA
    return { ...g.WordCore.validateState(raw, D.entries, D.fields, D.redirects), ...g.WorkspaceCore.normalize(raw, D.entries, D.fields, D.redirects) }
  } catch {
    return raw
  }
}

async function call(path: string, init: RequestInit) {
  if (!apiFetch) throw new Error("platform apiFetch missing")
  let res: Response
  try {
    res = await apiFetch(path, init)
  } catch (err) {
    const e = err as { status?: number; detail?: unknown; message?: string }
    throw new Error(`${e?.status || "network"}${e?.detail ? ` · ${typeof e.detail === "string" ? e.detail : JSON.stringify(e.detail)}` : e?.message ? ` · ${e.message}` : ""}`)
  }
  if (!res.ok) {
    let detail = ""
    try {
      detail = (await res.clone().json())?.detail ?? ""
    } catch {
      /* not json */
    }
    throw new Error(`${res.status}${detail ? ` · ${detail}` : ""}`)
  }
  return res.json()
}

async function putState(state: Record<string, unknown>) {
  return call(STATE_PATH, {
    method: "PUT",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ data: state }),
  })
}

function schedulePut(state: Record<string, unknown>) {
  pending = state
  if (timer) clearTimeout(timer)
  timer = setTimeout(async () => {
    const snapshot = pending
    pending = null
    if (!snapshot) return
    try {
      await putState(snapshot)
    } catch (err) {
      toast(msg(`Drive save failed (${(err as Error).message})`, `Drive 저장 실패 (${(err as Error).message})`))
    }
  }, SAVE_DEBOUNCE_MS)
}

function onStateWrite(json: string) {
  trackSavedWords(json) // per-word Sessions/…-word-… folders
  if (!ready) return
  let state: Record<string, unknown>
  try {
    state = JSON.parse(json)
  } catch {
    return
  }
  const m = meaningful(normalized(state))
  if (m === lastMeaningful) return
  lastMeaningful = m
  schedulePut(state)
}

// Hook the storage prototype once (assigning localStorage.setItem is not a
// reliable override). Works for the in-memory storage used by the app.
let hooked = false
function hookStorage() {
  if (hooked) return
  hooked = true
  try {
    const proto = Object.getPrototypeOf(localStorage) as { setItem: (this: Storage, k: string, v: string) => void }
    const original = proto.setItem
    nativeSetItem = (k, v) => original.call(localStorage, k, v)
    proto.setItem = function (this: Storage, k: string, v: string) {
      original.call(this, k, v)
      if (this === localStorage && k === STATE_KEY) onStateWrite(v)
    }
  } catch (err) {
    console.error("[all-your-words] could not hook storage", err)
  }
}

function seed(state: Record<string, unknown>) {
  const json = JSON.stringify(state)
  ;(nativeSetItem ?? ((k: string, v: string) => localStorage.setItem(k, v)))(STATE_KEY, json)
  lastMeaningful = meaningful(normalized(state))
  resetSavedBaseline(json)
  window.dispatchEvent(new StorageEvent("storage", { key: STATE_KEY, newValue: json }))
  // app.js does not re-render the welcome screen on storage events
  if (state.onboarded && location.hash.startsWith("#/welcome")) location.replace("#/")
}

function showOverlay() {
  if (LEGACY_HOST.querySelector(".drive-loading")) return
  const el = document.createElement("div")
  el.className = "drive-loading"
  el.setAttribute("role", "status")
  el.textContent = msg("Loading from Drive…", "Drive에서 불러오는 중…")
  LEGACY_HOST.appendChild(el)
}
function hideOverlay() {
  LEGACY_HOST.querySelector(".drive-loading")?.remove()
}

let booted = false
export async function bootFromDrive(fetcher: ApiFetch) {
  apiFetch = fetcher
  hookStorage()
  if (booted) return
  booted = true
  showOverlay()
  try {
    const body = await call(INIT_PATH, { method: "POST" })
    let state = (body?.state as Record<string, unknown> | null) ?? null
    if (!state && LEGACY_STATE) {
      // move data saved in the browser by older versions into the Drive
      try {
        state = JSON.parse(LEGACY_STATE)
      } catch {
        state = null
      }
      if (state) await putState(state)
    }
    if (state) seed(state)
    if (LEGACY_STATE) forgetLegacyState() // the Drive now holds the data
    ready = true
  } catch (err) {
    console.error("[all-your-words] drive init failed", err)
    toast(
      msg(
        `Could not connect to Drive — changes will not be saved (${(err as Error).message})`,
        `Drive에 연결하지 못했어요 — 이번 변경은 저장되지 않아요 (${(err as Error).message})`,
      ),
    )
  } finally {
    hideOverlay()
  }
}
