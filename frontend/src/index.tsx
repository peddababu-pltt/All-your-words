// Palette plugin root for "다, 너의 단어 (All your Words)".
//
// Wrap-and-reuse: the verbatim vanilla app (../app.js) + search logic
// (../core.js, ../workspace-core.js) run unchanged. Side-effect imports run in
// order at bundle load: styles, dark theme, the DOM the app needs, the data and
// logic globals, then app.js. The React shell adds Palette context, a backend
// Drive state bridge, a theme + language toggle, and the user/org identity line.

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
// 3) data (KO) + EN dataset + language-based dataset choice, then logic globals
import "../data.js"
import "../data.en.js"
import "./dataset-select"
import "./globals"
// 4) boot the app (reads #app / #toast / localStorage / window.WORD_DATA)
import "../app.js"

import { useEffect, useRef, useState } from "react"
import {
  PluginProvider,
  usePlatform,
  type PluginComponentProps,
} from "@palettelab/sdk"
import { LEGACY_HOST } from "./dom-setup"
import { platformFetch, runtime } from "./runtime"
import { applyLanguage, type Lang } from "./translate"
import { installDriveSync } from "./drive-sync"
import { bootFromDrive } from "./drive-state"
import { installSelectEnhancer } from "./select-enhance"
import { IS_LOCAL } from "./env"

const THEME_KEY = "daneo-theme"
const LANG_KEY = "daneo-lang"

type Theme = "light" | "dark"

function readStored<T extends string>(key: string, fallback: T): T {
  try {
    return (localStorage.getItem(key) as T) || fallback
  } catch {
    return fallback
  }
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

function Controls() {
  const platform = usePlatform()
  const { user, organizationId, setColorMode, setLanguage } = platform

  const [theme, setTheme] = useState<Theme>(() =>
    readStored<Theme>(THEME_KEY, (platform.colorMode as Theme) || "light"),
  )
  const [lang, setLang] = useState<Lang>(() =>
    readStored<Lang>(LANG_KEY, (platform.language as Lang) === "en" ? "en" : "ko"),
  )

  // apply theme: set <html data-color-mode>, inform the OS, persist
  useEffect(() => {
    document.documentElement.dataset.colorMode = theme
    try {
      setColorMode?.(theme)
    } catch {
      /* OS may not accept in sim */
    }
    try {
      localStorage.setItem(THEME_KEY, theme)
    } catch {
      /* ignore */
    }
  }, [theme, setColorMode])

  // apply language: translate the legacy host, inform the OS, persist
  useEffect(() => {
    applyLanguage(LEGACY_HOST, lang)
    try {
      setLanguage?.(lang)
    } catch {
      /* ignore */
    }
    try {
      localStorage.setItem(LANG_KEY, lang)
    } catch {
      /* ignore */
    }
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
        top: 12,
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
        aria-label="Toggle theme"
        title="Toggle light / dark"
      >
        {theme === "dark" ? "🌙 Dark" : "☀️ Light"}
      </button>

      <button
        type="button"
        style={pill}
        onClick={() => {
          const next: Lang = lang === "en" ? "ko" : "en"
          try {
            localStorage.setItem(LANG_KEY, next)
          } catch {
            /* ignore */
          }
          // reload so the dataset (KO/EN content) is chosen before app.js boots
          location.reload()
        }}
        aria-label="Toggle language"
        title="Toggle KO / EN"
      >
        {lang === "en" ? "EN" : "KO"}
      </button>
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
      {IS_LOCAL && <Controls />}
      <LegacyBridge />
    </PluginProvider>
  )
}
