// core.js and workspace-core.js are UMD modules. Because they reference
// `module.exports`, esbuild bundles them as CommonJS and captures their export
// instead of running the UMD `window.*` branch. Re-attach them to window here,
// which app.js reads as window.WordCore / window.WorkspaceCore.
//
// This module is imported before "../app.js" so the globals exist at boot.
import WordCore from "../core.js"
import WorkspaceCore from "../workspace-core.js"

;(window as unknown as Record<string, unknown>).WordCore = WordCore
;(window as unknown as Record<string, unknown>).WorkspaceCore = WorkspaceCore
