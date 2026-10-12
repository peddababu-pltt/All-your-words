// Local-only features: the theme / language toggles and the user·org identity
// line are shown only when the app runs on localhost (pltt dev / local
// server). Hosted Palette OS (staging, dev, qa) follows the OS language and
// light/dark mode instead.
export const IS_LOCAL = ["localhost", "127.0.0.1", "::1", "[::1]"].includes(window.location.hostname)

// lets CSS reserve topbar space for the controls only where they exist
if (IS_LOCAL) document.documentElement.classList.add("daneo-local")
