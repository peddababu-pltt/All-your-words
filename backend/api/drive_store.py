"""Per-session storage in the Palette Drive (Data Rooms).

Every processing session gets its own folder, with the user's inputs and the
app's generated outputs kept apart:

    다, 너의 단어 (All your Words)   (Drive / Data Room)
    └── Sessions/
        └── 20261009-170512-backup-a1b2c3/
            ├── input/
            └── output/

A new submission always creates a new session folder, so files from different
sessions are never mixed. All Drive access goes through ``ctx.data_rooms``
(the platform-injected service); this module never talks to storage directly.
"""

from __future__ import annotations

import base64
import mimetypes
import re
import secrets
from datetime import datetime, timezone
from typing import Any, Iterable

ROOM_NAME = "다, 너의 단어 (All your Words)"
ROOM_DESCRIPTION = "Inputs and outputs from 다, 너의 단어 (All your Words) — one folder per session."
ROOT_FOLDER = "Sessions"
STATE_FOLDER = "State"
STATE_SUFFIX = "-records.json"
# State snapshots: 20261009T150102123456Z-records.json (sortable by name = by time)
STATE_RE = re.compile(r"^\d{8}T\d{12}Z-records\.json$")
PARTS = ("input", "output")
KINDS = ("backup", "document", "import", "word")

MAX_FILES_PER_PART = 10
MAX_FILE_BYTES = 20 * 1024 * 1024

# Session folder names this module creates: 20261009-170512-backup-a1b2c3
SESSION_RE = re.compile(r"^\d{8}-\d{6}-(?:backup|document|import|word)-[0-9a-f]{6}$")
_UNSAFE = re.compile(r"[\x00-\x1f/\\]+")


class DriveSessionError(ValueError):
    """Invalid request for a Drive session (bad kind, name, or payload)."""


def safe_filename(name: str) -> str:
    """Strip path separators and control characters; keep Unicode (e.g. Korean)."""
    cleaned = _UNSAFE.sub("_", (name or "").strip()).strip(" .")
    return cleaned[:150] or "file"


def new_session_name(kind: str, now: datetime | None = None) -> str:
    if kind not in KINDS:
        raise DriveSessionError(f"unknown session kind: {kind}")
    now = now or datetime.now(timezone.utc)
    return f"{now:%Y%m%d-%H%M%S}-{kind}-{secrets.token_hex(3)}"


def _payload_bytes(item: dict[str, Any]) -> bytes:
    content = item.get("content", "")
    if item.get("encoding") == "base64":
        try:
            data = base64.b64decode(content, validate=True)
        except Exception as exc:  # noqa: BLE001 - surface as a request error
            raise DriveSessionError(f"invalid base64 for {item.get('name')!r}") from exc
    elif isinstance(content, bytes):
        data = content
    else:
        data = str(content).encode("utf-8")
    if len(data) > MAX_FILE_BYTES:
        raise DriveSessionError(f"{item.get('name')!r} exceeds {MAX_FILE_BYTES} bytes")
    return data


def _content_type(name: str, given: str | None) -> str:
    if given:
        return given
    guessed, _ = mimetypes.guess_type(name)
    return guessed or "application/octet-stream"


def _split_contents(contents: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Normalize ``contents()`` into (folders, files); tolerant of response shapes."""
    if not isinstance(contents, dict):
        return [], []
    folders = list(contents.get("folders") or [])
    files = list(contents.get("files") or [])
    for item in contents.get("items") or []:
        kind = (item.get("type") or item.get("kind") or "").lower()
        (folders if kind == "folder" else files).append(item)
    return folders, files


def _fname(item: dict[str, Any]) -> str:
    """File/folder display name (the platform's DataRoomFile uses `original_filename`)."""
    return item.get("name") or item.get("original_filename") or ""


class DriveSessions:
    """Session-folder operations on top of a ``DataRoomsClient``."""

    def __init__(self, data_rooms: Any):
        self.dr = data_rooms

    async def _room(self) -> dict[str, Any]:
        return await self.dr.ensure_room(ROOM_NAME, ROOM_DESCRIPTION)

    async def _existing_room(self) -> dict[str, Any] | None:
        return await self.dr.find_room_by_name(ROOM_NAME)

    async def create_session(
        self,
        kind: str,
        inputs: Iterable[dict[str, Any]],
        outputs: Iterable[dict[str, Any]] = (),
    ) -> dict[str, Any]:
        inputs, outputs = list(inputs), list(outputs)
        if not inputs:
            raise DriveSessionError("a session needs at least one input file")
        if len(inputs) > MAX_FILES_PER_PART or len(outputs) > MAX_FILES_PER_PART:
            raise DriveSessionError(f"at most {MAX_FILES_PER_PART} files per folder")
        # validate every payload before touching the Drive
        prepared = {
            part: [(safe_filename(f.get("name", "")), _payload_bytes(f), f.get("content_type")) for f in files]
            for part, files in (("input", inputs), ("output", outputs))
        }

        name = new_session_name(kind)
        room = await self._room()
        folders = {
            part: await self.dr.resolve_folder_path(room["id"], [ROOT_FOLDER, name, part], create=True)
            for part in PARTS
        }

        uploaded: dict[str, list[dict[str, Any]]] = {part: [] for part in PARTS}
        for part in PARTS:
            for filename, data, ctype in prepared[part]:
                saved = await self.dr.upload_file(
                    room["id"],
                    filename,
                    data,
                    folder_id=folders[part]["id"],
                    content_type=_content_type(filename, ctype),
                )
                uploaded[part].append({"name": filename, "id": (saved or {}).get("id"), "bytes": len(data)})

        return {
            "session": name,
            "kind": kind,
            "room": ROOM_NAME,
            "room_id": room["id"],
            "path": f"{ROOT_FOLDER}/{name}",
            "folders": {part: folders[part]["id"] for part in PARTS},
            "files": uploaded,
        }

    async def list_sessions(self) -> list[str]:
        room = await self._existing_room()
        if room is None:
            return []
        root = await self.dr.resolve_folder_path(room["id"], [ROOT_FOLDER])
        if root is None:
            return []
        folders, _ = _split_contents(await self.dr.contents(room["id"], root["id"]))
        names = [f.get("name", "") for f in folders if SESSION_RE.match(f.get("name", ""))]
        return sorted(names, reverse=True)  # names start with a timestamp: newest first

    async def session_files(self, session: str) -> dict[str, Any]:
        self._check_session(session)
        room = await self._existing_room()
        result: dict[str, Any] = {"session": session, "input": [], "output": []}
        if room is None:
            return result
        for part in PARTS:
            folder = await self.dr.resolve_folder_path(room["id"], [ROOT_FOLDER, session, part])
            if folder is None:
                continue
            _, files = _split_contents(await self.dr.contents(room["id"], folder["id"]))
            result[part] = sorted(_fname(f) for f in files)
        return result

    async def read_file(self, session: str, part: str, filename: str) -> bytes | None:
        self._check_session(session)
        if part not in PARTS:
            raise DriveSessionError(f"part must be one of {PARTS}")
        room = await self._existing_room()
        if room is None:
            return None
        folder = await self.dr.resolve_folder_path(room["id"], [ROOT_FOLDER, session, part])
        if folder is None:
            return None
        found = await self.dr.find_file_by_name(room["id"], safe_filename(filename), folder_id=folder["id"])
        if found is None:
            return None
        return await self.dr.read_file_bytes(found["id"])

    # --- app state in the platform Drive ---------------------------------
    # The Drive API has no update/delete, so the current state (saved words,
    # memos, settings, …) is written as timestamped snapshot files under
    # State/ and the newest one is the current state.

    async def init_room(self) -> dict[str, Any]:
        """Create (or reuse) the app's data room and its State/ + Sessions/ folders."""
        room = await self._room()
        state = await self.dr.resolve_folder_path(room["id"], [STATE_FOLDER], create=True)
        sessions = await self.dr.resolve_folder_path(room["id"], [ROOT_FOLDER], create=True)
        return {"room": ROOM_NAME, "room_id": room["id"], "state_folder": state["id"], "sessions_folder": sessions["id"]}

    async def save_state(self, data: dict[str, Any], now: datetime | None = None) -> dict[str, Any]:
        import json

        now = now or datetime.now(timezone.utc)
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        if len(payload) > MAX_FILE_BYTES:
            raise DriveSessionError(f"state exceeds {MAX_FILE_BYTES} bytes")
        room = await self._room()
        folder = await self.dr.resolve_folder_path(room["id"], [STATE_FOLDER], create=True)
        name = f"{now:%Y%m%dT%H%M%S%f}Z{STATE_SUFFIX}"
        saved = await self.dr.upload_file(room["id"], name, payload, folder_id=folder["id"], content_type="application/json")
        return {"saved": name, "id": (saved or {}).get("id"), "bytes": len(payload)}

    async def latest_state(self) -> dict[str, Any] | None:
        import json

        room = await self._existing_room()
        if room is None:
            return None
        folder = await self.dr.resolve_folder_path(room["id"], [STATE_FOLDER])
        if folder is None:
            return None
        _, files = _split_contents(await self.dr.contents(room["id"], folder["id"]))
        snaps = sorted((f for f in files if STATE_RE.match(_fname(f))), key=_fname)
        if not snaps:
            return None
        newest = snaps[-1]
        raw = await self.dr.read_file_bytes(newest["id"])
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return None

    @staticmethod
    def _check_session(session: str) -> None:
        if not SESSION_RE.match(session or ""):
            raise DriveSessionError("invalid session name")
