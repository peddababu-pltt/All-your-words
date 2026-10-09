// Custom dropdown for the search filters (#filter-form: Field / Word type / Topic).
//
// The native <select> opens an OS popup that can cover the whole screen when
// the list is long (Topic has ~100 options). This replaces the visible control
// with a trigger + panel that always opens BELOW the field, scrolls inside, and
// offers a quick filter for long lists. The native <select> stays in the form
// (visually hidden): choosing an option sets its value and dispatches a
// bubbling "change", so app.js handles it exactly as before.
import { IS_LOCAL } from "./env"

const TARGET = "#filter-form select"
const SEARCHABLE_MIN = 12
const MAX_LIST_HEIGHT = 360

type Open = { wrap: HTMLElement; panel: HTMLElement; trigger: HTMLButtonElement }
let current: Open | null = null

const isEn = () => {
  try {
    return IS_LOCAL && localStorage.getItem("daneo-lang") === "en"
  } catch {
    return false
  }
}

function close(focusTrigger = false) {
  if (!current) return
  current.panel.remove()
  current.trigger.setAttribute("aria-expanded", "false")
  if (focusTrigger) current.trigger.focus()
  current = null
}

function enhance(select: HTMLSelectElement) {
  select.dataset.enhanced = "1"
  const wrap = document.createElement("div")
  wrap.className = "dd"
  select.parentNode!.insertBefore(wrap, select)
  // Keep the native select in the form (FormData + app.js change handler) but
  // outside the <label>, so the label's click activation targets our trigger.
  ;(select.closest("label") ?? wrap).after(select)
  select.classList.add("dd-native")
  select.tabIndex = -1
  select.setAttribute("aria-hidden", "true")

  const trigger = document.createElement("button")
  trigger.type = "button"
  trigger.className = "dd-trigger"
  trigger.setAttribute("aria-haspopup", "listbox")
  trigger.setAttribute("aria-expanded", "false")
  const label = document.createElement("span")
  label.className = "dd-label"
  trigger.append(label)
  trigger.insertAdjacentHTML(
    "beforeend",
    '<svg class="dd-chevron" viewBox="0 0 256 256" aria-hidden="true"><path d="M216.49,104.49l-80,80a12,12,0,0,1-17,0l-80-80a12,12,0,0,1,17-17L128,159l71.51-71.52a12,12,0,0,1,17,17Z"/></svg>',
  )
  wrap.appendChild(trigger)

  // label mirrors the selected option (also after the language layer rewrites option text)
  const sync = () => {
    label.textContent = select.selectedOptions[0]?.textContent?.trim() ?? ""
  }
  sync()
  new MutationObserver(sync).observe(select, { subtree: true, childList: true, characterData: true })

  const toggle = () => (current?.trigger === trigger ? close(true) : openPanel(wrap, select, trigger, sync))
  trigger.addEventListener("click", toggle)
  trigger.addEventListener("keydown", (ev) => {
    if (ev.key === "ArrowDown" || ev.key === "ArrowUp") {
      ev.preventDefault()
      if (current?.trigger !== trigger) openPanel(wrap, select, trigger, sync)
    }
  })
}

function openPanel(wrap: HTMLElement, select: HTMLSelectElement, trigger: HTMLButtonElement, sync: () => void) {
  close()
  const options = [...select.options]
  const panel = document.createElement("div")
  panel.className = "dd-panel"
  // the panel lives inside a <label>: don't let clicks re-activate the trigger
  panel.addEventListener("click", (ev) => ev.preventDefault())

  let search: HTMLInputElement | null = null
  if (options.length >= SEARCHABLE_MIN) {
    search = document.createElement("input")
    search.type = "search"
    search.className = "dd-search"
    search.placeholder = isEn() ? "Filter…" : "목록에서 찾기…"
    search.setAttribute("aria-label", search.placeholder)
    search.autocomplete = "off"
    // typing here must not reach app.js's filter-form "change" handler
    search.addEventListener("change", (ev) => ev.stopPropagation())
    panel.appendChild(search)
  }

  const list = document.createElement("ul")
  list.className = "dd-list"
  list.setAttribute("role", "listbox")
  const items = options.map((opt, i) => {
    const li = document.createElement("li")
    li.setAttribute("role", "option")
    li.dataset.index = String(i)
    li.textContent = opt.textContent?.trim() ?? ""
    li.setAttribute("aria-selected", String(i === select.selectedIndex))
    li.addEventListener("mousedown", (ev) => ev.preventDefault()) // keep focus in panel
    li.addEventListener("click", () => choose(i))
    list.appendChild(li)
    return li
  })
  const empty = document.createElement("div")
  empty.className = "dd-empty"
  empty.textContent = isEn() ? "No matches" : "일치하는 항목이 없어요"
  empty.hidden = true
  panel.append(list, empty)
  wrap.appendChild(panel)

  // open downward; the list scrolls inside instead of growing past the screen
  const rect = trigger.getBoundingClientRect()
  const below = window.innerHeight - rect.bottom - 24 - (search ? 46 : 0)
  list.style.maxHeight = `${Math.max(180, Math.min(MAX_LIST_HEIGHT, below))}px`
  if (panel.getBoundingClientRect().right > window.innerWidth - 8) panel.classList.add("dd-panel--right")
  panel.scrollIntoView({ block: "nearest" })

  let active = Math.max(0, select.selectedIndex)
  const visible = () => items.filter((li) => !li.hidden)
  const setActive = (i: number) => {
    items.forEach((li) => li.classList.remove("is-active"))
    const li = items[i]
    if (!li || li.hidden) return
    active = i
    li.classList.add("is-active")
    li.scrollIntoView({ block: "nearest" })
  }
  const move = (step: number) => {
    const vis = visible()
    if (!vis.length) return
    const pos = vis.indexOf(items[active])
    const next = vis[Math.min(vis.length - 1, Math.max(0, (pos < 0 ? -1 : pos) + step))]
    setActive(Number(next.dataset.index))
  }
  function choose(i: number) {
    const changed = i !== select.selectedIndex
    select.selectedIndex = i
    sync()
    close(true)
    if (changed) select.dispatchEvent(new Event("change", { bubbles: true }))
  }

  search?.addEventListener("input", () => {
    const q = search!.value.trim().toLowerCase()
    items.forEach((li) => (li.hidden = !!q && !li.textContent!.toLowerCase().includes(q)))
    const vis = visible()
    empty.hidden = vis.length > 0
    if (vis.length) setActive(Number(vis[0].dataset.index))
  })

  panel.addEventListener("keydown", (ev) => {
    if (ev.key === "ArrowDown") (ev.preventDefault(), move(1))
    else if (ev.key === "ArrowUp") (ev.preventDefault(), move(-1))
    else if (ev.key === "Enter") {
      ev.preventDefault()
      if (!items[active]?.hidden) choose(active)
    } else if (ev.key === "Escape") (ev.preventDefault(), close(true))
    else if (ev.key === "Tab") close()
  })

  trigger.setAttribute("aria-expanded", "true")
  current = { wrap, panel, trigger }
  setActive(active)
  if (search) search.focus()
  else {
    list.tabIndex = -1
    list.focus()
  }
}

let installed = false
export function installSelectEnhancer(host: HTMLElement) {
  if (installed) return
  installed = true
  const run = () => {
    if (current && !current.wrap.isConnected) current = null // re-rendered
    host.querySelectorAll<HTMLSelectElement>(`${TARGET}:not([data-enhanced])`).forEach(enhance)
  }
  run()
  new MutationObserver(run).observe(host, { childList: true, subtree: true })
  document.addEventListener(
    "mousedown",
    (ev) => {
      // composedPath: real target even when rendered inside a shadow root
      if (current && !(ev.composedPath?.() ?? [ev.target]).includes(current.wrap)) close()
    },
    true,
  )
  window.addEventListener("resize", () => close())
}
