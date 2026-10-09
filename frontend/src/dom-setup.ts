// Create the DOM the legacy app.js expects (icon sprite + #app + #toast) BEFORE
// app.js runs (this module is imported above "../app.js"). It is parked on
// document.body so app.js can bind to #app at boot; the React shell then
// relocates this host node into the plugin's own container so it renders inside
// the Palette OS content area instead of below the OS chrome.
import { SPRITE } from "./sprite"

export const LEGACY_HOST_ID = "daneo-legacy-host"

function createHost(): HTMLElement {
  const existing = document.getElementById(LEGACY_HOST_ID)
  if (existing) return existing
  const host = document.createElement("div")
  host.id = LEGACY_HOST_ID
  host.innerHTML = SPRITE + '<div id="app"></div><div id="toast" role="status" aria-live="polite"></div>'
  ;(document.body || document.documentElement).appendChild(host)
  return host
}

// Kept as a module reference so a remount can re-attach it even when the node
// is no longer in the document (getElementById would return null then).
export const LEGACY_HOST: HTMLElement = createHost()

// If the OS renders the plugin inside an isolated root (shadow DOM), the legacy
// app's document.getElementById("toast" | "main" | …) would return null once the
// host is moved there. Fall back to a lookup inside the host — only when the
// document has no such element, so nothing else on the page is affected.
const nativeGetById = Document.prototype.getElementById
Document.prototype.getElementById = function (this: Document, id: string) {
  const found = nativeGetById.call(this, id)
  if (found || this !== document) return found
  try {
    const safe = typeof CSS !== "undefined" && CSS.escape ? CSS.escape(id) : String(id).replace(/[^\w-]/g, "\\$&")
    return LEGACY_HOST.querySelector<HTMLElement>(`#${safe}`)
  } catch {
    return null
  }
}

// The host scopes plugin CSS to [data-palette-plugin-root]; html/body selectors
// are rewritten to that root. app.js toggles layout classes on <body>
// (is-home, compact-list, …) and env.ts marks <html> with daneo-local — both
// outside the plugin root. Mirror those classes onto the legacy host so the
// scoped selectors still match.
const MIRROR_MARK = "data-mirrored"
function mirrorClasses() {
  const prev = (LEGACY_HOST.getAttribute(MIRROR_MARK) || "").split(" ").filter(Boolean)
  const next = [
    ...Array.from(document.body?.classList ?? []),
    ...Array.from(document.documentElement.classList).filter((c) => c === "daneo-local"),
  ]
  for (const c of prev) if (!next.includes(c)) LEGACY_HOST.classList.remove(c)
  for (const c of next) LEGACY_HOST.classList.add(c)
  LEGACY_HOST.setAttribute(MIRROR_MARK, next.join(" "))
}
mirrorClasses()
const classWatch = new MutationObserver(mirrorClasses)
if (document.body) classWatch.observe(document.body, { attributes: true, attributeFilter: ["class"] })
classWatch.observe(document.documentElement, { attributes: true, attributeFilter: ["class"] })
