# All-your-words

**다, 너의 단어 (All your Words)**: a dictionary of workplace terms (7 fields, 2,882 meanings), built as a Palette
platform app (plugin id `allyourwords`).

All user data and files are stored in the **platform Drive** (Palette Data Room). Nothing is kept inside the app
itself: there's no app database and no user data in browser storage.

```
Palette Drive (apps.pltt.xyz/drive)
└── 다, 너의 단어 (All your Words)            ← data room, created the first time the app is opened
    ├── State/<time>-records.json           ← saved words, memos, collections, settings (newest = current)
    └── Sessions/<time>-<kind>-<id>/
        ├── input/                          ← what the user gave the app
        └── output/                         ← what the app generated
```

| Action in the app | Session kind | input/ | output/ |
|---|---|---|---|
| Save a word, or write a memo (내 단어장) | `word` | `word.json` | `my-words.csv` |
| 자료와 백업 → 내 기록 백업하기 | `backup` | `records.json` | `all-your-words-backup.json`, `my-words.csv` |
| 업무 도구 → 용어 찾기 | `document` | `document.txt` | `terms.json`, `terms.csv` |
| 자료와 백업 → 백업 가져오기 | `import` | the uploaded file | `merge-result.json` |

---

## Requirements

- **Node.js 18+** (tested with 24)
- **Python 3.12+**, for the backend and the dictionary build scripts
- Palette CLI and SDK: installed by `npm install` (`@palettelab/cli`, `@palettelab/sdk`)
- For staging: a Palette login. `pltt login` saves the URL and token to `~/.palette/config.json`. Never put tokens in `.env`.

## Install

```bash
cd all_your_word
npm install
```

## Run locally

```bash
npx pltt dev
```

- App: http://localhost:7321/ (or the next free port, which is printed in the terminal)
- Backend: http://localhost:8732/api/v1/plugins/allyourwords (or the next free port)

> **Local limitation:** the local simulator has **no platform Drive service**. The app opens, but you'll see
> "Drive에 연결하지 못했어요 — 이번 변경은 저장되지 않아요 (503 · drive_unavailable)", and changes aren't saved.
> Use a staging preview (below) to test real Drive storage.

**Localhost-only extras:** a theme toggle (☀️/🌙), a KO/EN language toggle (switches the whole UI and the
dictionary to English), and the user/org identity line. These are hidden on staging and production.

If the backend fails with `ModuleNotFoundError: No module named 'fastapi'`, install it into the simulator's venv:

```bash
.palette/dev/backend-venv/bin/python -m pip install fastapi pydantic
```

## Test

```bash
# Palette contract checks: manifest, bundle, permission gates, backend import
npx pltt test
npx pltt doctor

# Frontend logic (search, workspace, dictionary coverage): 72 tests
cd backend/tests && node --test *.test.js && cd ../..

# Backend Drive storage (fake Data Room service): 18 tests
PYTHONPATH=node_modules/@palettelab/cli/backend-sdk:backend \
  .palette/dev/backend-venv/bin/python -m unittest backend/tests/test_drive_sessions.py -v

# Dictionary meaning groups
python3 backend/tests/test_meaning_groups.py
```

(The backend tests need `fastapi` and `httpx` in the Python you use:
`.palette/dev/backend-venv/bin/python -m pip install fastapi httpx pydantic`.)

## Publish to staging

Staging is `https://apps-api.pltt.xyz`. Log in once:

```bash
npx pltt login --env staging --url https://apps-api.pltt.xyz --token pltt_xxxxx
```

**First time for a new app id:** publish a preview, then wait for a superadmin to approve it at
https://apps-admin.pltt.xyz/app-preview-reviews

```bash
npx pltt dev --sandbox --env staging      # prints the preview URL
```

**Every release:** bump `version` in `palette-plugin.json` and `package.json` (it must be newer than the last
release), then:

```bash
npx pltt test
npx pltt publish --env staging            # → pending_review
```

Approve it at https://apps-admin.pltt.xyz/app-reviews. Once approved it's live at
https://apps.pltt.xyz/apps/allyourwords

Check a publish, or read the request log:

```bash
npx pltt status <publish-id> --env staging
npx pltt logs allyourwords --env staging --tail 200
```

> Don't run `pltt publish --help`: it runs a real publish instead of printing help.

**Check that Drive works (staging):**
1. Open the app once.
2. https://apps.pltt.xyz/drive should list **다, 너의 단어 (All your Words)**.
3. Save a word. A new `State/…-records.json` file and a `Sessions/…-word-…` folder should appear.

## Project structure

```
palette-plugin.json        app manifest (id allyourwords, data_scope organization, data_rooms permissions)
frontend/
  src/index.tsx            Palette root: mounts the app and connects it to the platform Drive
  src/drive-state.ts       on open: create the data room and load state; on change: save a State/ snapshot
  src/drive-sync.ts        word / backup / document / import → Sessions/ folders
  src/storage-shim.ts      in-memory storage (no user data in the browser)
  src/select-enhance.ts    search filter dropdowns (open downward, scroll inside)
  src/translate.ts         KO↔EN interface text (localhost only)
  app.js core.js workspace-core.js   the dictionary UI and search logic
  data.js / data.en.js     dictionary data (Korean / English)
backend/
  api/main.py              routes: /drive/init, /drive/state, /drive/sessions…
  api/drive_store.py       platform Drive (ctx.data_rooms) access
  tests/                   Node and Python tests
  data/                    dictionary source files
  scripts/                 dictionary build and translation scripts
```

### Backend routes (all need Drive permissions)

| Route | Purpose |
|---|---|
| `POST /drive/init` | create or reuse the data room and its `State/` and `Sessions/` folders; returns the current state |
| `PUT /drive/state` | save the current state as a new `State/<time>-records.json` |
| `POST /drive/sessions` | create a session folder with its input/ and output/ files |
| `GET /drive/sessions[/{session}[/{part}/{file}]]` | list sessions and files, read a file back |

## Update the dictionary data

```bash
cd backend
python3 scripts/build_data.py              # data/*.py, *.tsv → data/dictionary.json + frontend/data.js
python3 scripts/check_editorial_review.py  # every entry must match the review log

# English dictionary (frontend/data.en.js)
python3 scripts/make_en_batches.py         # split into data/en-batches/batch_*.json
python3 scripts/translate_dictionary.py    # needs ANTHROPIC_API_KEY or OPENAI_API_KEY; resumable
python3 scripts/assemble_en.py             # → data/dictionary.en.json + frontend/data.en.js
```

## Notes

- `.env` isn't needed. `pltt` uploads every key in `.env` as an app secret, so never put deploy tokens there
  (see `.env.example`).
- Search works on the bundled dictionary inside the app (no server call). Only user data and files go to the Drive.
