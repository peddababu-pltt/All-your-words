"""Drive (Data Room) session storage: layout, separation, upload/retrieve, routes.

The Palette runtime injects the real Data Room service; here a fake in-memory
service is injected instead, as the SDK recommends for tests.

Run (from daneoword/):
  PYTHONPATH=node_modules/@palettelab/cli/backend-sdk:backend \
    .palette/dev/backend-venv/bin/python -m unittest backend/tests/test_drive_sessions.py -v
"""

import base64
import itertools
import unittest

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from palette_sdk import PluginContext, get_plugin_context
from palette_sdk.data_rooms import DataRoomsClient
from palette_sdk.testing import route_permission_issues

from api import drive_store
from api.drive_store import ROOM_NAME, ROOT_FOLDER, DriveSessionError, DriveSessions
from api.main import router


class FakeDataRoomService:
    """In-memory stand-in for the platform Data Room ("Drive") service."""

    def __init__(self, shape="split"):
        self.shape = shape
        self.ids = itertools.count(1)
        self.rooms = {}    # id -> {id, name}
        self.folders = {}  # id -> {id, name, room_id, parent_id}
        self.files = {}    # id -> {id, name, room_id, folder_id, content, content_type}

    async def list_rooms(self):
        return list(self.rooms.values())

    async def create_room(self, name, description=None):
        rid = next(self.ids)
        self.rooms[rid] = {"id": rid, "name": name, "description": description}
        return self.rooms[rid]

    async def find_room_by_name(self, name, case_sensitive=False):
        return next((r for r in self.rooms.values() if r["name"] == name), None)

    async def ensure_room(self, name, description=None):
        return await self.find_room_by_name(name) or await self.create_room(name, description)

    def _children(self, room_id, parent_id):
        return [f for f in self.folders.values() if f["room_id"] == room_id and f["parent_id"] == parent_id]

    async def contents(self, room_id, folder_id=None):
        folders = self._children(room_id, folder_id)
        files = [f for f in self.files.values() if f["room_id"] == room_id and f["folder_id"] == folder_id]
        if self.shape == "items":
            return {"items": [{**f, "type": "folder"} for f in folders] + [{**f, "type": "file"} for f in files]}
        return {"folders": folders, "files": files}

    async def create_folder(self, room_id, name, parent_folder_id=None):
        fid = next(self.ids)
        self.folders[fid] = {"id": fid, "name": name, "room_id": room_id, "parent_id": parent_folder_id}
        return self.folders[fid]

    async def find_folder_by_name(self, room_id, name, parent_folder_id=None, case_sensitive=False):
        return next((f for f in self._children(room_id, parent_folder_id) if f["name"] == name), None)

    async def ensure_folder(self, room_id, name, parent_folder_id=None):
        return await self.find_folder_by_name(room_id, name, parent_folder_id) or await self.create_folder(
            room_id, name, parent_folder_id
        )

    async def resolve_folder_path(self, room_id, path, create=False, case_sensitive=False):
        parts = path.split("/") if isinstance(path, str) else list(path)
        parent = None
        for part in parts:
            found = await self.find_folder_by_name(room_id, part, parent)
            if found is None:
                if not create:
                    return None
                found = await self.create_folder(room_id, part, parent)
            parent = found["id"]
        return self.folders[parent]

    async def find_file_by_name(self, room_id, name, folder_id=None, case_sensitive=False):
        return next(
            (f for f in self.files.values() if f["room_id"] == room_id and f["folder_id"] == folder_id and f["name"] == name),
            None,
        )

    async def read_file_bytes(self, file_id):
        return self.files[file_id]["content"]

    async def upload_file(self, room_id, filename, content, folder_id=None, content_type=None):
        fid = next(self.ids)
        self.files[fid] = {
            "id": fid, "name": filename, "room_id": room_id, "folder_id": folder_id,
            "content": content, "content_type": content_type,
        }
        return {"id": fid, "name": filename}

    # helpers for assertions
    def path_of(self, folder_id):
        names = []
        while folder_id is not None:
            folder = self.folders[folder_id]
            names.append(folder["name"])
            folder_id = folder["parent_id"]
        return "/".join(reversed(names))


def store(shape="split"):
    fake = FakeDataRoomService(shape)
    return fake, DriveSessions(DataRoomsClient(fake))


BACKUP_INPUTS = [{"name": "records.json", "content": '{"saved":["dev-001"]}', "content_type": "application/json"}]
BACKUP_OUTPUTS = [
    {"name": "all-your-words-backup.json", "content": '{"app":"daneoword","saved":["dev-001"]}'},
    {"name": "my-words.csv", "content": "term,field\nCommit,Dev & IT\n", "content_type": "text/csv"},
]


class DriveStoreTest(unittest.IsolatedAsyncioTestCase):
    async def test_session_has_separate_input_and_output_folders(self):
        fake, drive = store()
        res = await drive.create_session("backup", BACKUP_INPUTS, BACKUP_OUTPUTS)

        self.assertRegex(res["session"], drive_store.SESSION_RE)
        self.assertEqual(res["path"], f"{ROOT_FOLDER}/{res['session']}")
        self.assertEqual(fake.path_of(res["folders"]["input"]), f"{ROOT_FOLDER}/{res['session']}/input")
        self.assertEqual(fake.path_of(res["folders"]["output"]), f"{ROOT_FOLDER}/{res['session']}/output")
        self.assertEqual([r["name"] for r in fake.rooms.values()], [ROOM_NAME])

        files = await drive.session_files(res["session"])
        self.assertEqual(files["input"], ["records.json"])
        self.assertEqual(files["output"], ["all-your-words-backup.json", "my-words.csv"])
        csv = next(f for f in fake.files.values() if f["name"] == "my-words.csv")
        self.assertEqual(csv["content_type"], "text/csv")

    async def test_each_submission_gets_its_own_session_and_never_mixes(self):
        fake, drive = store()
        a = await drive.create_session("backup", BACKUP_INPUTS, BACKUP_OUTPUTS)
        b = await drive.create_session(
            "document",
            [{"name": "document.txt", "content": "We commit the code."}],
            [{"name": "terms.json", "content": '[{"term":"Commit"}]'}],
        )
        self.assertNotEqual(a["session"], b["session"])
        self.assertNotEqual(a["folders"]["input"], b["folders"]["input"])
        self.assertNotEqual(a["folders"]["output"], b["folders"]["output"])

        files_a = await drive.session_files(a["session"])
        files_b = await drive.session_files(b["session"])
        self.assertEqual(files_a["input"], ["records.json"])
        self.assertEqual(files_b["input"], ["document.txt"])
        self.assertEqual(files_b["output"], ["terms.json"])
        self.assertTrue(set(files_a["output"]).isdisjoint(files_b["output"]))
        # every uploaded file sits inside exactly its own session folder
        for f in fake.files.values():
            session = fake.path_of(f["folder_id"]).split("/")[1]
            self.assertIn(session, (a["session"], b["session"]))
        self.assertEqual(sorted(await drive.list_sessions(), reverse=True), await drive.list_sessions())
        self.assertEqual(set(await drive.list_sessions()), {a["session"], b["session"]})

    async def test_upload_then_retrieve_returns_identical_bytes(self):
        _, drive = store()
        korean = "회의록: 시안 컨펌 부탁드려요. CPC 확인."
        binary = bytes(range(256))
        res = await drive.create_session(
            "import",
            [
                {"name": "다너의단어-내기록.json", "content": korean},
                {"name": "raw.bin", "content": base64.b64encode(binary).decode(), "encoding": "base64"},
            ],
            [{"name": "merge-result.json", "content": '{"merged":1}'}],
        )
        s = res["session"]
        self.assertEqual(await drive.read_file(s, "input", "다너의단어-내기록.json"), korean.encode("utf-8"))
        self.assertEqual(await drive.read_file(s, "input", "raw.bin"), binary)
        self.assertEqual(await drive.read_file(s, "output", "merge-result.json"), b'{"merged":1}')
        # input files are not visible from output and vice versa
        self.assertIsNone(await drive.read_file(s, "output", "raw.bin"))
        self.assertIsNone(await drive.read_file(s, "input", "merge-result.json"))

    async def test_list_sessions_newest_first(self):
        _, drive = store()
        names = iter(["20261009-100000-backup-aaaaaa", "20261009-120000-document-bbbbbb", "20261009-110000-import-cccccc"])
        original = drive_store.new_session_name
        drive_store.new_session_name = lambda kind, now=None: next(names)
        try:
            for kind in ("backup", "document", "import"):
                await drive.create_session(kind, [{"name": "in.txt", "content": "x"}])
        finally:
            drive_store.new_session_name = original
        self.assertEqual(
            await drive.list_sessions(),
            ["20261009-120000-document-bbbbbb", "20261009-110000-import-cccccc", "20261009-100000-backup-aaaaaa"],
        )

    async def test_saved_word_session(self):
        _, drive = store()
        res = await drive.create_session(
            "word",
            [{"name": "word.json", "content": '{"id":"dev-001","term":"커밋","action":"saved"}'}],
            [{"name": "my-words.csv", "content": "단어,분야\n커밋,개발·IT\n", "content_type": "text/csv"}],
        )
        self.assertRegex(res["session"], r"-word-")
        files = await drive.session_files(res["session"])
        self.assertEqual(files, {"session": res["session"], "input": ["word.json"], "output": ["my-words.csv"]})
        self.assertIn(res["session"], await drive.list_sessions())

    async def test_init_room_creates_room_with_state_and_sessions_folders(self):
        fake, drive = store()
        res = await drive.init_room()
        self.assertEqual([r["name"] for r in fake.rooms.values()], [ROOM_NAME])
        self.assertEqual(fake.path_of(res["state_folder"]), "State")
        self.assertEqual(fake.path_of(res["sessions_folder"]), ROOT_FOLDER)
        again = await drive.init_room()  # idempotent
        self.assertEqual(again["room_id"], res["room_id"])
        self.assertEqual(len(fake.rooms), 1)

    async def test_state_snapshots_newest_wins(self):
        from datetime import datetime, timezone
        fake, drive = store()
        self.assertIsNone(await drive.latest_state())
        await drive.save_state({"saved": ["a"]}, now=datetime(2026, 10, 9, 15, 0, 0, tzinfo=timezone.utc))
        await drive.save_state({"saved": ["a", "b"], "notes": {"a": {"text": "메모"}}}, now=datetime(2026, 10, 9, 15, 0, 5, tzinfo=timezone.utc))
        self.assertEqual(await drive.latest_state(), {"saved": ["a", "b"], "notes": {"a": {"text": "메모"}}})
        names = sorted(f["name"] for f in fake.files.values())
        self.assertTrue(all(fake.path_of(f["folder_id"]) == "State" for f in fake.files.values()))
        self.assertTrue(all(n.endswith("-records.json") for n in names), names)

    async def test_state_with_platform_original_filename_field(self):
        fake, drive = store()
        await drive.save_state({"saved": ["x"]})
        for f in fake.files.values():  # the platform's DataRoomFile uses original_filename
            f["original_filename"] = f.pop("name")
        self.assertEqual(await drive.latest_state(), {"saved": ["x"]})

    async def test_alternate_contents_shape_is_supported(self):
        _, drive = store(shape="items")
        res = await drive.create_session("backup", BACKUP_INPUTS, BACKUP_OUTPUTS)
        self.assertEqual(await drive.list_sessions(), [res["session"]])
        files = await drive.session_files(res["session"])
        self.assertEqual(files["output"], ["all-your-words-backup.json", "my-words.csv"])

    async def test_validation_and_unsafe_names(self):
        fake, drive = store()
        with self.assertRaises(DriveSessionError):
            await drive.create_session("unknown", BACKUP_INPUTS)
        with self.assertRaises(DriveSessionError):
            await drive.create_session("backup", [])
        with self.assertRaises(DriveSessionError):
            await drive.session_files("../../etc")
        with self.assertRaises(DriveSessionError):
            await drive.read_file("20261009-100000-backup-aaaaaa", "secrets", "x")
        self.assertEqual(fake.files, {})  # nothing uploaded by rejected requests

        res = await drive.create_session("document", [{"name": "../../evil.txt", "content": "x"}])
        (stored,) = fake.files.values()
        self.assertNotIn("/", stored["name"])
        self.assertEqual(fake.path_of(stored["folder_id"]), f"{ROOT_FOLDER}/{res['session']}/input")

    async def test_unavailable_drive_service_raises_runtime_error(self):
        drive = DriveSessions(DataRoomsClient(None))
        with self.assertRaises(RuntimeError):
            await drive.create_session("backup", BACKUP_INPUTS)


PERMISSIONS = ["resources:read", "resources:write", "data_rooms:read", "data_rooms:write"]


def client(service, permissions=PERMISSIONS):
    app = FastAPI()

    @app.middleware("http")
    async def grant(request: Request, call_next):
        request.state.plugin_permissions = permissions
        return await call_next(request)

    app.include_router(router)
    ctx = PluginContext(
        db=None, user_id="u1", organization_id=1, permissions=list(permissions), data_rooms=DataRoomsClient(service)
    )
    app.dependency_overrides[get_plugin_context] = lambda: ctx
    return TestClient(app)


class DriveRoutesTest(unittest.TestCase):
    def test_every_route_is_permission_gated(self):
        self.assertEqual(route_permission_issues(router), [])

    def test_upload_list_and_retrieve_over_http(self):
        http = client(FakeDataRoomService())
        body = {
            "kind": "document",
            "inputs": [{"name": "document.txt", "content": "We commit the code, then drop the feature."}],
            "outputs": [{"name": "terms.json", "content": '[{"term":"Commit"},{"term":"Drop"}]', "content_type": "application/json"}],
        }
        created = http.post("/drive/sessions", json=body)
        self.assertEqual(created.status_code, 200, created.text)
        session = created.json()["session"]

        self.assertEqual(http.get("/drive/sessions").json(), {"sessions": [session]})
        self.assertEqual(
            http.get(f"/drive/sessions/{session}").json(),
            {"session": session, "input": ["document.txt"], "output": ["terms.json"]},
        )
        got = http.get(f"/drive/sessions/{session}/input/document.txt")
        self.assertEqual(got.status_code, 200)
        self.assertEqual(got.content, b"We commit the code, then drop the feature.")
        self.assertEqual(http.get(f"/drive/sessions/{session}/output/nope.json").status_code, 404)

    def test_bad_requests_are_rejected(self):
        http = client(FakeDataRoomService())
        self.assertEqual(http.post("/drive/sessions", json={"kind": "backup", "inputs": []}).status_code, 422)
        self.assertEqual(http.post("/drive/sessions", json={"kind": "x", "inputs": BACKUP_INPUTS}).status_code, 422)
        self.assertEqual(http.get("/drive/sessions/not-a-session").status_code, 400)

    def test_init_and_state_routes(self):
        http = client(FakeDataRoomService())
        first = http.post("/drive/init")
        self.assertEqual(first.status_code, 200, first.text)
        self.assertEqual(first.json()["room"], ROOM_NAME)
        self.assertIsNone(first.json()["state"])
        put = http.put("/drive/state", json={"data": {"saved": ["dev-001"], "onboarded": True}})
        self.assertEqual(put.status_code, 200, put.text)
        self.assertTrue(put.json()["saved"].endswith("-records.json"))
        self.assertEqual(http.post("/drive/init").json()["state"], {"saved": ["dev-001"], "onboarded": True})

    def test_init_without_drive_service_returns_503(self):
        self.assertEqual(client(None).post("/drive/init").status_code, 503)

    def test_simulator_without_drive_returns_503(self):
        http = client(None)
        res = http.post("/drive/sessions", json={"kind": "backup", "inputs": BACKUP_INPUTS})
        self.assertEqual(res.status_code, 503)
        self.assertEqual(res.json()["detail"], "drive_unavailable")

    def test_missing_permission_is_forbidden(self):
        http = client(FakeDataRoomService(), permissions=["data_rooms:read"])
        res = http.post("/drive/sessions", json={"kind": "backup", "inputs": BACKUP_INPUTS})
        self.assertEqual(res.status_code, 403)


if __name__ == "__main__":
    unittest.main()
