"""Local fixtures and mocked Hub calls: tests never upload news or use real credentials."""
import copy
import hashlib
import json
import zipfile
from pathlib import Path
from types import SimpleNamespace

import pytest

from weconomy import hub
from weconomy.pipeline import load_config, process, read_table
from weconomy.quality import validate

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def run(tmp_path):
    config = load_config(ROOT / "config/pipeline.yaml")
    config.update(output=str(tmp_path / "source"), allow_excerpts=True)
    run, _ = process(config, manifest=ROOT / "samples/excerpts/manifest.json")
    return run


def test_pack_roundtrip_whitelist_checksums_and_determinism(run, tmp_path):
    (run / ".env").write_text("SECRET=not-a-real-token")
    (run / "notes.jsonl").write_text("not part of the corpus")
    (tmp_path / "one").mkdir()
    archive, _, metadata = hub._pack(run, tmp_path / "one")
    (tmp_path / "two").mkdir()
    _, _, other = hub._pack(run, tmp_path / "two")
    assert metadata == other
    assert ".env" not in metadata["files"] and "notes.jsonl" not in metadata["files"]
    restored = tmp_path / "restored"
    restored.mkdir()
    result = hub._unpack(archive, metadata, restored, run.name)
    assert result["valid"] and validate(restored)["valid"]
    for table in ("bronze", "articles", "mentions", "entities", "relations", "events"):
        assert read_table(restored, table) == read_table(run, table)


def test_dry_run_has_no_client_or_credentials(run, monkeypatch):
    monkeypatch.setattr(hub, "_client", lambda: pytest.fail("dry-run must never contact Hub"))
    result = hub.push_run(run, "team/corpus", dry_run=True)
    assert result["dry_run"] and result["private_required"]
    assert result["counts"]["articles"] == 4


@pytest.mark.parametrize("case", ["path", "archive_hash", "file_hash", "missing_member", "size", "run_id"])
def test_rejects_unsafe_or_corrupt_bundles(run, tmp_path, case):
    archive, _, metadata = hub._pack(run, tmp_path)
    if case == "path":
        metadata["files"]["../escaped.txt"] = {"bytes": 0, "sha256": "0" * 64}
    elif case == "archive_hash":
        metadata["archive_sha256"] = "0" * 64
    elif case == "file_hash":
        metadata["files"]["aliases.yaml"]["sha256"] = "0" * 64
    elif case == "size":
        metadata["files"]["aliases.yaml"]["bytes"] = hub.MAX_BYTES + 1
    elif case == "run_id":
        metadata["run_id"] = "other"
    else:
        with zipfile.ZipFile(archive) as bundle:
            rows = {n: bundle.read(n) for n in bundle.namelist() if n != "aliases.yaml"}
        archive.unlink()
        with zipfile.ZipFile(archive, "w") as bundle:
            for name, content in rows.items():
                bundle.writestr(name, content)
        metadata.update(archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
                        archive_bytes=archive.stat().st_size)
    restored = tmp_path / "restored"
    restored.mkdir()
    with pytest.raises(ValueError):
        hub._unpack(archive, metadata, restored, run.name)
    assert not (tmp_path / "escaped.txt").exists()


def test_invalid_input_before_network_and_existing_local_target(run, tmp_path, monkeypatch):
    monkeypatch.setattr(hub, "_client", lambda: pytest.fail("must fail before credentials/network"))
    with pytest.raises(ValueError, match="namespace/name"):
        hub.push_run(run, "https://huggingface.co/datasets/team/data", dry_run=True)
    with pytest.raises(ValueError, match="run ID"):
        hub.pull_run("team/data", "../escape", tmp_path)
    with pytest.raises(FileExistsError):
        hub.pull_run("team/data", run.name, run.parent)
    manifest = json.loads((run / "manifest.json").read_text("utf-8"))
    manifest["status"] = "partial"
    (run / "manifest.json").write_text(json.dumps(manifest), "utf-8")
    with pytest.raises(ValueError, match="completed"):
        hub.push_run(run, "team/data", dry_run=True)


@pytest.fixture
def remote(monkeypatch):
    sdk = pytest.importorskip("huggingface_hub")

    class Remote:
        private = True
        token = "unit-test-not-a-real-token"
        sha = "a" * 40
        calls = []

        def __init__(self):
            self.files = {}
            self.calls = []

        def create_repo(self, *args, **kwargs):
            assert kwargs["private"] is True and kwargs["repo_type"] == "dataset"

        def repo_info(self, *args, **kwargs):
            return SimpleNamespace(private=self.private, sha=self.sha)

        def get_paths_info(self, repo, paths, **kwargs):
            assert kwargs["revision"] == self.sha
            return [SimpleNamespace(path=n, size=len(self.files[n])) for n in paths if n in self.files]

        def create_commit(self, repo, operations, **kwargs):
            assert kwargs["parent_commit"] == self.sha
            self.calls.append(kwargs)
            for operation in operations:
                self.files[operation.path_in_repo] = Path(operation.path_or_fileobj).read_bytes()
            return SimpleNamespace(oid=self.sha, commit_url="https://huggingface.co/test-commit")

        def download(self, repo, name, **kwargs):
            assert kwargs["revision"] == self.sha and kwargs["token"] == self.token
            path = Path(kwargs["local_dir"]) / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(self.files[name])
            return str(path)

    remote = Remote()
    monkeypatch.setattr(hub, "_client", lambda: remote)
    monkeypatch.setattr(sdk, "hf_hub_download", remote.download)
    return remote


def test_mocked_push_pull_private_immutable_commit_and_dataset_validation(run, tmp_path, remote):
    sent = hub.push_run(run, "team/data")
    assert sent["commit"] == remote.sha and len(remote.files) == 2
    with pytest.raises(FileExistsError):
        hub.push_run(run, "team/data")
    received = hub.pull_run("team/data", run.name, tmp_path / "received", revision=remote.sha)
    assert received["valid"] and received["commit"] == remote.sha
    assert read_table(received["run"], "articles") == read_table(run, "articles")


def test_public_repo_rejected_before_upload(run, remote):
    remote.private = False
    with pytest.raises(ValueError, match="public"):
        hub.push_run(run, "team/data")
    assert remote.files == {} and remote.calls == []


def test_new_empty_repository_is_created_private_without_existing_head(run, remote, monkeypatch):
    import httpx
    from huggingface_hub.errors import RepositoryNotFoundError
    created = []
    remote.sha = None

    def info(*args, **kwargs):
        if not created:
            raise RepositoryNotFoundError("Test repository not created yet", response=httpx.Response(
                404, request=httpx.Request("GET", "https://huggingface.co/api/datasets/team/new-data")))
        return SimpleNamespace(private=True, sha=None)

    monkeypatch.setattr(remote, "repo_info", info)
    monkeypatch.setattr(remote, "create_repo", lambda *args, **kwargs: created.append(kwargs))
    hub.push_run(run, "team/new-data")
    assert created[0]["private"] is True and created[0]["repo_type"] == "dataset"
    assert len(remote.files) == 2


def test_pull_corruption_cleans_staging_without_publishing_partial_run(run, tmp_path, remote):
    hub.push_run(run, "team/data")
    sidecar = f"runs/{run.name}.json"
    metadata = copy.deepcopy(json.loads(remote.files[sidecar]))
    metadata["files"]["aliases.yaml"]["sha256"] = "0" * 64
    remote.files[sidecar] = json.dumps(metadata).encode()
    output = tmp_path / "received"
    with pytest.raises(ValueError, match="checksum"):
        hub.pull_run("team/data", run.name, output)
    assert list(output.iterdir()) == []
