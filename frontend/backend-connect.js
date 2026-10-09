/* Backend connector for 다, 너의 단어.
 *
 * Links the static frontend to backend/server.py without touching app.js:
 *   - On load (before app.js reads storage): pull saved state from the backend
 *     and seed localStorage, so the app boots with server-synced data.
 *   - On every save: app.js calls localStorage.setItem(KEY, json); we wrap that
 *     to also PUT the blob to /api/state.
 *
 * Degrades to plain localStorage when the API is unreachable (file:// or no
 * server), so the app keeps working standalone.
 */
(function () {
  var KEY = "daneoword.v1";
  var API = "/api/state";

  // Push: wrap localStorage.setItem so every app save write-throughs to backend.
  try {
    var _set = localStorage.setItem.bind(localStorage);
    localStorage.setItem = function (k, v) {
      _set(k, v);
      if (k === KEY) {
        try {
          fetch(API, {
            method: "PUT",
            headers: { "content-type": "application/json" },
            body: JSON.stringify({ data: JSON.parse(v) }),
          }).catch(function () {});
        } catch (e) {}
      }
    };
  } catch (e) {}

  // Pull: seed localStorage from backend BEFORE app.js reads it.
  // Synchronous request guarantees the blob is present at boot.
  try {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", API, false);
    xhr.send(null);
    if (xhr.status === 200) {
      var body = JSON.parse(xhr.responseText);
      if (body && body.data != null) {
        var blob = typeof body.data === "string" ? body.data : JSON.stringify(body.data);
        localStorage.getItem(KEY); // no-op touch
        Object.getPrototypeOf(localStorage).setItem.call(localStorage, KEY, blob);
      }
    }
  } catch (e) {
    /* offline / no server: app uses existing localStorage */
  }
})();
