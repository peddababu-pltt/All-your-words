// Shared runtime: the host-provided apiFetch (usePlatform().apiFetch).
export type ApiFetch = (path: string, init?: RequestInit) => Promise<Response>

export const runtime = {
  // latest host-provided apiFetch; updated on every render of the plugin root
  hostFetch: null as ApiFetch | null,
  hostFetchType: "unset" as string,
}

// Stable function handed to long-lived modules (Drive state, Drive sessions).
// Always calls the latest host apiFetch, so remounts never leave a stale one.
export const platformFetch: ApiFetch = (path, init) =>
  runtime.hostFetch
    ? runtime.hostFetch(path, init)
    : Promise.reject(new Error(`platform apiFetch missing (${runtime.hostFetchType})`))
