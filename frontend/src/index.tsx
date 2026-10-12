// Palette plugin root for "다, 너의 단어 (All your Words)".
//
// Wrap-and-reuse: the verbatim vanilla app (../app.js) + search logic
// (../core.js, ../workspace-core.js) run unchanged. Side-effect imports run in
// order at bundle load: styles, dark theme, the DOM the app needs, the data and
// logic globals, then app.js. The React shell adds Palette context and a backend
// Drive state bridge. Hosted (staging / dev / qa) follows the Palette OS
// language + light/dark mode; localhost adds dev toggles and the user/org line.

// 0) sandbox-safe localStorage (in-memory fallback when the iframe blocks it)
import "./storage-shim"
// 1) legacy styles + dark theme
import "../styles.css"
import "../app.css"
import "../workspace.css"
import "./dark.css"
import "./layout-fix.css"
// 2) DOM the legacy script needs (must precede app.js)
import "./dom-setup"
// 3) data (KO) + EN/JA datasets + language-based dataset choice, then logic globals
import "../data.js"
import "../data.en.js"
import "../data.ja.js"
import "./dataset-select"
import "./globals"
// 4) boot the app (reads #app / #toast / localStorage / window.WORD_DATA)
import "../app.js"

import { useEffect, useRef, useState } from "react"
import {
  normalizePaletteLanguage,
  PluginProvider,
  usePlatform,
  type PluginComponentProps,
} from "@palettelab/sdk"
import { LEGACY_HOST } from "./dom-setup"
import { platformFetch, runtime } from "./runtime"
import { applyLanguage } from "./translate"
import { LANGS, readLang, toLang, type Lang } from "./lang"
import { switchLanguage } from "./language-switch"
import { installDriveSync } from "./drive-sync"
import { bootFromDrive } from "./drive-state"
import { installSelectEnhancer } from "./select-enhance"
import { IS_LOCAL } from "./env"

const THEME_KEY = "daneo-theme"

type Theme = "light" | "dark"

function readStored<T extends string>(key: string, fallback: T): T {
  try {
    return (localStorage.getItem(key) as T) || fallback
  } catch {
    return fallback
  }
}

// phone layout of the legacy CSS (workspace.css switches at 700px)
const NARROW = "(max-width: 700px)"
function useNarrow() {
  const [narrow, setNarrow] = useState(() => window.matchMedia?.(NARROW).matches ?? false)
  useEffect(() => {
    const mq = window.matchMedia?.(NARROW)
    if (!mq) return
    const on = () => setNarrow(mq.matches)
    mq.addEventListener("change", on)
    return () => mq.removeEventListener("change", on)
  }, [])
  return narrow
}

function LegacyBridge() {
  const mount = useRef<HTMLDivElement>(null)
  // Backend calls must use the host's apiFetch (usePlatform().apiFetch): inside
  // the hosted sandbox iframe it is the only one wired to the plugin backend.
  const { apiFetch } = usePlatform()
  runtime.hostFetchType = typeof apiFetch
  runtime.hostFetch = typeof apiFetch === "function" ? apiFetch : null
  useEffect(() => {
    if (typeof apiFetch !== "function") console.error("[all-your-words] platform apiFetch missing — backend/Drive calls cannot run")
  }, [apiFetch])

  // Move the legacy host (sprite + #app + #toast) into this mount on every mount,
  // using the module reference so a remount re-attaches it even if detached.
  useEffect(() => {
    if (mount.current && LEGACY_HOST.parentElement !== mount.current) mount.current.appendChild(LEGACY_HOST)
  }, [])

  // Platform Drive: load app state from the data room (creating it on first
  // open), Drive session hooks, filter dropdowns
  useEffect(() => {
    installDriveSync(platformFetch)
    installSelectEnhancer(LEGACY_HOST)
    void bootFromDrive(platformFetch)
  }, [])

  return <div ref={mount} className="daneo-legacy-mount" />
}

// Hosted: no in-app toggles. Theme and language come from Palette OS and
// follow it live, switching in place (no reload). The language change waits a
// moment so a transient default value from the host can't win.
function OsSync() {
  const { language, colorMode } = usePlatform()
  const osLang: Lang = toLang(normalizePaletteLanguage(language, "en")) ?? "en"
  const theme: Theme = colorMode === "dark" ? "dark" : "light"

  useEffect(() => {
    document.documentElement.dataset.colorMode = theme
  }, [theme])

  useEffect(() => {
    applyLanguage(LEGACY_HOST, readLang())
  }, [])

  useEffect(() => {
    const timer = setTimeout(() => switchLanguage(osLang), 250)
    return () => clearTimeout(timer)
  }, [osLang])

  return null
}

// Localhost only: theme / language toggles and the user·org identity line.
function Controls() {
  const platform = usePlatform()
  const { user, organizationId } = platform

  const [theme, setTheme] = useState<Theme>(() =>
    readStored<Theme>(
      THEME_KEY,
      platform.colorMode === "dark" || platform.colorMode === "light"
        ? platform.colorMode
        : window.matchMedia?.("(prefers-color-scheme: dark)").matches
          ? "dark"
          : "light",
    ),
  )
  const [lang, setLang] = useState<Lang>(readLang)
  const narrow = useNarrow()

  // apply theme: set <html data-color-mode>, persist
  useEffect(() => {
    document.documentElement.dataset.colorMode = theme
    try {
      localStorage.setItem(THEME_KEY, theme)
    } catch {
      /* ignore */
    }
  }, [theme])

  // apply language: translate the legacy host
  useEffect(() => {
    applyLanguage(LEGACY_HOST, lang)
  }, [lang])

  const pill: React.CSSProperties = {
    display: "inline-flex",
    alignItems: "center",
    gap: 6,
    height: 30,
    padding: "0 10px",
    borderRadius: 999,
    border: "1px solid var(--line)",
    background: "var(--white)",
    color: "var(--ink)",
    fontSize: 12,
    fontWeight: 600,
    lineHeight: 1,
    cursor: "pointer",
  }

  const userId = user?.id ?? user?.email ?? null
  const hasIdentity = !!userId && organizationId != null

  return (
    <div
      style={{
        position: "fixed",
        top: narrow ? 14 : 18,
        right: 14,
        zIndex: 50,
        display: "flex",
        alignItems: "center",
        gap: 8,
        fontFamily: "var(--sans)",
      }}
    >
      {hasIdentity && (
        <span
          title="Palette identity"
          style={{
            fontSize: 10.5,
            color: "var(--muted)",
            background: "var(--white)",
            border: "1px solid var(--line)",
            borderRadius: 999,
            padding: "5px 9px",
            maxWidth: 200,
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
          }}
        >
          user {String(userId)} · org {String(organizationId)}
        </span>
      )}

      <button
        type="button"
        style={pill}
        onClick={() => setTheme((t) => (t === "dark" ? "light" : "dark"))}
        aria-label={theme === "dark" ? "Switch to light theme" : "Switch to dark theme"}
        title={theme === "dark" ? "Light" : "Dark"}
      >
        {theme === "dark" ? "☀️" : "🌙"}
      </button>

      <select
        style={{ ...pill, paddingRight: 8 }}
        value={lang}
        onChange={(ev) => {
          const next = ev.target.value as Lang
          setLang(next)
          switchLanguage(next)
        }}
        aria-label="Language"
        title="Language"
      >
        {LANGS.map(([id, name]) => (
          <option key={id} value={id}>
            {narrow ? id.toUpperCase() : name}
          </option>
        ))}
      </select>
    </div>
  )
}

export default function PluginRoot(props: PluginComponentProps) {
  // The host passes { platform }. Provide the platform context itself (not the
  // props wrapper), otherwise usePlatform().apiFetch is undefined and every
  // backend / Drive call fails before a request is sent.
  const platform = props.platform ?? (props as unknown as PluginComponentProps["platform"])
  return (
    <PluginProvider value={platform}>
      {IS_LOCAL ? <Controls /> : <OsSync />}
      <LegacyBridge />
    </PluginProvider>
  )
}
