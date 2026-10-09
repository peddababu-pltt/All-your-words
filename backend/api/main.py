"""Backend routes. All app data and files live in the platform Drive (Data Room):

    다, 너의 단어 (All your Words)          (created with ctx.data_rooms.ensure_room)
    ├── State/<ts>-records.json           saved words, memos, settings (newest = current)
    └── Sessions/<time>-<kind>-<id>/{input,output}/

There is no app database; nothing is stored inside the app itself.
"""
from typing import Literal

from fastapi import Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field
from palette_sdk import (
    PluginContext,
    PluginRouter,
    get_plugin_context,
    require_permission,
)
try:
    from .drive_store import DriveSessionError, DriveSessions
except ImportError:  # dev loader imports main.py without a package context
    from drive_store import DriveSessionError, DriveSessions

router = PluginRouter(tags=["all-your-words"])


class StateBody(BaseModel):
    data: dict


# --- Platform Drive: data room + app state ----------------------------------


@router.post("/drive/init", dependencies=[require_permission("data_rooms:write")])
async def drive_init(ctx: PluginContext = Depends(get_plugin_context)):
    """Create (or reuse) the app's data room in the platform Drive and return the current state."""
    try:
        drive = DriveSessions(ctx.data_rooms)
        room = await drive.init_room()
        state = await drive.latest_state()
    except (DriveSessionError, RuntimeError) as exc:
        ctx.logger.warning("drive init failed: %s: %s", type(exc).__name__, exc)
        raise _drive_error(exc)
    ctx.logger.info("drive init room=%r room_id=%s state=%s", room["room"], room["room_id"], "found" if state else "none")
    return {**room, "state": state}


@router.put("/drive/state", dependencies=[require_permission("data_rooms:write")])
async def drive_save_state(body: StateBody, ctx: PluginContext = Depends(get_plugin_context)):
    """Write the current app state as a new snapshot file in Drive › <room> › State/."""
    try:
        saved = await DriveSessions(ctx.data_rooms).save_state(body.data)
    except (DriveSessionError, RuntimeError) as exc:
        ctx.logger.warning("drive state save failed: %s: %s", type(exc).__name__, exc)
        raise _drive_error(exc)
    ctx.logger.info("drive state saved %s saved_words=%d", saved["saved"], len(body.data.get("saved") or []))
    return saved


# --- Drive (Data Room) sessions -------------------------------------------
# Each submission (backup, document scan, backup import) becomes its own
# session folder with separate input/ and output/ subfolders.


class DriveFile(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    content: str
    content_type: str | None = None
    encoding: Literal["utf-8", "base64"] = "utf-8"


class DriveSessionBody(BaseModel):
    kind: Literal["backup", "document", "import", "word"]
    inputs: list[DriveFile] = Field(min_length=1)
    outputs: list[DriveFile] = []


def _drive_error(exc: Exception) -> HTTPException:
    if isinstance(exc, DriveSessionError):
        return HTTPException(status_code=400, detail=str(exc))
    # The local simulator does not inject the Drive service; hosted OS does.
    if isinstance(exc, RuntimeError) and "not available" in str(exc):
        return HTTPException(status_code=503, detail="drive_unavailable")
    raise exc


@router.post("/drive/sessions", dependencies=[require_permission("data_rooms:write")])
async def create_drive_session(body: DriveSessionBody, ctx: PluginContext = Depends(get_plugin_context)):
    ctx.logger.info(
        "drive session requested kind=%s inputs=%s outputs=%s user=%s org=%s",
        body.kind, [f.name for f in body.inputs], [f.name for f in body.outputs],
        ctx.user_id, ctx.organization_id,
    )
    try:
        result = await DriveSessions(ctx.data_rooms).create_session(
            body.kind,
            [f.model_dump() for f in body.inputs],
            [f.model_dump() for f in body.outputs],
        )
    except (DriveSessionError, RuntimeError) as exc:
        ctx.logger.warning("drive session failed kind=%s: %s: %s", body.kind, type(exc).__name__, exc)
        raise _drive_error(exc)
    except Exception:
        ctx.logger.exception("drive session crashed kind=%s", body.kind)
        raise
    ctx.logger.info(
        "drive session saved room=%r room_id=%s path=%s files=%s",
        result["room"], result["room_id"], result["path"],
        {part: [f["name"] for f in files] for part, files in result["files"].items()},
    )
    return result


@router.get("/drive/sessions", dependencies=[require_permission("data_rooms:read")])
async def list_drive_sessions(ctx: PluginContext = Depends(get_plugin_context)):
    try:
        return {"sessions": await DriveSessions(ctx.data_rooms).list_sessions()}
    except (DriveSessionError, RuntimeError) as exc:
        raise _drive_error(exc)


@router.get("/drive/sessions/{session}", dependencies=[require_permission("data_rooms:read")])
async def get_drive_session(session: str, ctx: PluginContext = Depends(get_plugin_context)):
    try:
        return await DriveSessions(ctx.data_rooms).session_files(session)
    except (DriveSessionError, RuntimeError) as exc:
        raise _drive_error(exc)


@router.get(
    "/drive/sessions/{session}/{part}/{filename}",
    dependencies=[require_permission("data_rooms:read")],
)
async def read_drive_file(session: str, part: str, filename: str, ctx: PluginContext = Depends(get_plugin_context)):
    try:
        data = await DriveSessions(ctx.data_rooms).read_file(session, part, filename)
    except (DriveSessionError, RuntimeError) as exc:
        raise _drive_error(exc)
    if data is None:
        raise HTTPException(status_code=404, detail="file not found")
    return Response(content=data, media_type="application/octet-stream")
