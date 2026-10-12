// No browser storage for user data: the platform Drive is the only store.
//
// The legacy app reads/writes window.localStorage, so it gets an in-memory
// Storage instead (filled from the Drive at boot by drive-state.ts). Before
// switching, any data left in the real localStorage by older versions is
// captured once (LEGACY_STATE) so it can be moved into the Drive and then
// removed from the browser. The theme / language preferences (not user data)
// still persist in the real localStorage when the browser allows it.
export const STATE_KEY = "daneoword.v1"
const PREF_KEYS = new Set(["daneo-theme", "daneo-lang"])

function realStorage(): Storage | null {
  try {
    const ls = window.localStorage
    ls.getItem("__aw_probe__")
    return ls
  } catch {
    return null
  }
}

const REAL = realStorage()

// Data saved in the browser by versions before 1.1.0 (moved to Drive on boot).
export const LEGACY_STATE: string | null = (() => {
  try {
    return REAL?.getItem(STATE_KEY) ?? null
  } catch {
    return null
  }
})()

export function forgetLegacyState() {
  try {
    REAL?.removeItem(STATE_KEY)
  } catch {
    /* ignore */
  }
}

class MemoryStorage {
  private map = new Map<string, string>()
  get length() {
    return this.map.size
  }
  key(i: number) {
    return [...this.map.keys()][i] ?? null
  }
  getItem(k: string) {
    k = String(k)
    if (PREF_KEYS.has(k) && REAL) {
      try {
        return REAL.getItem(k)
      } catch {
        /* fall through */
      }
    }
    return this.map.has(k) ? this.map.get(k)! : null
  }
  setItem(k: string, v: string) {
    k = String(k)
    v = String(v)
    if (PREF_KEYS.has(k) && REAL) {
      try {
        REAL.setItem(k, v)
        return
      } catch {
        /* fall through */
      }
    }
    this.map.set(k, v)
  }
  removeItem(k: string) {
    this.map.delete(String(k))
  }
  clear() {
    this.map.clear()
  }
}

export type StorageMode = "memory"
export const STORAGE_MODE: StorageMode = "memory"

try {
  Object.defineProperty(window, "localStorage", { value: new MemoryStorage(), configurable: true })
} catch {
  /* the legacy app already wraps storage access in try/catch */
}
