// Local-only features: the theme / language toggles, the user·org identity
// line, and the English dataset are available only when the app runs on
// localhost (pltt dev / local server). Hosted Palette OS (staging, production)
// shows the plain Korean app.
export const IS_LOCAL = ["localhost", "127.0.0.1", "::1", "[::1]"].includes(window.location.hostname)

// lets CSS reserve topbar space for the controls only where they exist
if (IS_LOCAL) document.documentElement.classList.add("daneo-local")
