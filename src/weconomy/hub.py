"""Versioned run bundles on private Hugging Face dataset repositories."""
import hashlib
import json
import re
import tempfile
import zipfile
from pathlib import Path

from .pipeline import read_table
from .quality import validate
from .schema import SCHEMAS

FORMAT = "weconomy-hf-run-v1"
MAX_BYTES = 1024 ** 3
MAX_METADATA_BYTES = 1024 ** 2
BASE_FILES = {"manifest.json", "config.yaml", "sources.yaml", "aliases.yaml"}
for _table in SCHEMAS:
    _layer = "bronze" if _table == "bronze" else "gold" if _table in {
        "entities", "events", "relations"} else "silver"
    BASE_FILES.add(f"{_layer}/{_table}.parquet")


def _run_id(value):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,99}", value):
        raise ValueError("Invalid run ID: use letters, digits, hyphens or underscores")
    return value


def _repo_id(value):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*", value):
        raise ValueError("Dataset repository must be namespace/name")
    return value


def _allowed(path):
    return path in BASE_FILES or bool(re.fullmatch(r"bronze/html/[0-9a-f]{24}\.html", path))


def _digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def _pack(run, folder):
    run = Path(run).resolve()
    rid = _run_id(run.name)
    result = validate(run)
    if not result["valid"]:
        raise ValueError(f"Invalid run: {result['failures']}")
    manifest = json.loads((run / "manifest.json").read_text("utf-8"))
    if manifest.get("counts") != result["counts"]:
        raise ValueError("Run manifest counts do not match the dataset")
    if manifest["status"] != "completed" or not result["counts"]["articles"]:
        raise ValueError("Only nonempty completed runs can be shared; reprocess/merge partial runs first")
    paths = BASE_FILES | {r["raw_path"] for r in read_table(run, "bronze")}
    if any(not _allowed(path) for path in paths):
        raise ValueError("Run contains an unsupported raw snapshot path")
    sizes = {}
    for name in sorted(paths):
        path = run / name
        if path.is_symlink() or not path.resolve().is_relative_to(run):
            raise ValueError("Symlinks or paths outside the run cannot be shared")
        sizes[name] = path.stat().st_size
    if sum(sizes.values()) > MAX_BYTES:
        raise ValueError("Run exceeds the 1 GiB bundle limit")
    archive = folder / f"{rid}.zip"
    files = {}
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name in sorted(paths):
            # A fixed timestamp makes retrying an unchanged run produce the same archive hash.
            payload = (run / name).read_bytes()
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, payload)
            files[name] = {"bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}
    if archive.stat().st_size > MAX_BYTES:
        raise ValueError("Compressed archive exceeds the 1 GiB limit")
    metadata = {"format": FORMAT, "run_id": rid, "schema_version": manifest["schema_version"],
                "counts": result["counts"], "files": files,
                "archive_bytes": archive.stat().st_size, "archive_sha256": _digest(archive)}
    sidecar = folder / f"{rid}.json"
    sidecar.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), "utf-8")
    if sidecar.stat().st_size > MAX_METADATA_BYTES:
        raise ValueError("Bundle metadata exceeds the 1 MiB limit; split the corpus into smaller runs")
    return archive, sidecar, metadata


def _client():
    try:
        from huggingface_hub import HfApi, get_token
    except ImportError:
        raise RuntimeError("Install the hub extra: uv sync --locked --extra hub (retain other extras)") from None
    token = get_token()
    if not token:
        raise ValueError("Authenticate with hf auth login or set HF_TOKEN locally; never paste it into chat")
    return HfApi(token=token)


def push_run(run, repo_id, *, dry_run=False):
    repo_id = _repo_id(repo_id)
    with tempfile.TemporaryDirectory(prefix="weconomy-hf-") as temp:
        archive, sidecar, metadata = _pack(run, Path(temp))
        result = {"repo_id": repo_id, "run_id": metadata["run_id"], "private_required": True,
                  "dry_run": dry_run, "counts": metadata["counts"], "files": sorted(metadata["files"]),
                  "archive_bytes": metadata["archive_bytes"], "archive_sha256": metadata["archive_sha256"]}
        if dry_run:
            return result  # No SDK, credentials or network required to review the exact bundle contents.
        api = _client()
        from huggingface_hub import CommitOperationAdd
        from huggingface_hub.errors import RepositoryNotFoundError
        try:
            info = api.repo_info(repo_id, repo_type="dataset")
        except RepositoryNotFoundError:
            api.create_repo(repo_id, repo_type="dataset", private=True, exist_ok=True)
            info = api.repo_info(repo_id, repo_type="dataset")
        if not info.private:
            raise ValueError("Refusing upload: dataset repository is public; use a private repository")
        paths = [f"runs/{path.name}" for path in (archive, sidecar)]
        if info.sha and api.get_paths_info(repo_id, paths, repo_type="dataset", revision=info.sha):
            raise FileExistsError("Run ID already exists remotely; publish a new run instead of overwriting")
        commit = api.create_commit(repo_id, repo_type="dataset", parent_commit=info.sha,
            commit_message=f"Add Weconomy run {metadata['run_id']}", operations=[
                CommitOperationAdd(path_in_repo=name, path_or_fileobj=path)
                for name, path in zip(paths, (archive, sidecar))])
        result.update(commit=commit.oid, url=commit.commit_url)
        return result


def _unpack(archive, metadata, destination, run_id):
    if metadata.get("format") != FORMAT or metadata.get("run_id") != run_id:
        raise ValueError("Unsupported bundle format or mismatched run ID")
    files = metadata.get("files")
    if not isinstance(files, dict) or not BASE_FILES.issubset(files) or len(files) > 100000:
        raise ValueError("Missing required files or invalid file inventory")
    if any(not _allowed(name) for name in files):
        raise ValueError("Unsafe or unsupported path in bundle inventory")
    for item in files.values():
        if (not isinstance(item, dict) or type(item.get("bytes")) is not int or item["bytes"] < 0
                or not re.fullmatch(r"[0-9a-f]{64}", str(item.get("sha256", "")))):
            raise ValueError("Invalid file size or checksum")
    if sum(item["bytes"] for item in files.values()) > MAX_BYTES:
        raise ValueError("Unpacked bundle exceeds the 1 GiB limit")
    if archive.stat().st_size != metadata.get("archive_bytes") or _digest(archive) != metadata.get("archive_sha256"):
        raise ValueError("Archive checksum/size mismatch")
    with zipfile.ZipFile(archive) as bundle:
        members = bundle.infolist()
        if len(members) != len(files) or {m.filename for m in members} != set(files):
            raise ValueError("Archive file inventory mismatch or duplicate entries")
        for member in members:
            if member.file_size != files[member.filename]["bytes"] or member.external_attr >> 28 == 10:
                raise ValueError("Invalid member size or symlink")
            target = destination / member.filename
            target.parent.mkdir(parents=True, exist_ok=True)
            digest = hashlib.sha256()
            with bundle.open(member) as source, target.open("xb") as output:
                while chunk := source.read(1024 * 1024):
                    output.write(chunk)
                    digest.update(chunk)
            if digest.hexdigest() != files[member.filename]["sha256"]:
                raise ValueError(f"File checksum mismatch: {member.filename}")
    result = validate(destination)
    manifest = json.loads((destination / "manifest.json").read_text("utf-8"))
    if (not result["valid"] or result["counts"] != metadata.get("counts")
            or manifest.get("counts") != result["counts"]
            or manifest.get("schema_version") != metadata.get("schema_version")
            or manifest.get("status") != "completed" or not result["counts"]["articles"]):
        raise ValueError("Downloaded run failed dataset validation/count checks")
    return result


def pull_run(repo_id, run_id, output, *, revision="main"):
    repo_id, run_id = _repo_id(repo_id), _run_id(run_id)
    root = Path(output).resolve()
    target = root / run_id
    if target.exists():
        raise FileExistsError("Local run already exists; choose another output directory")
    api = _client()
    info = api.repo_info(repo_id, repo_type="dataset", revision=revision)
    # Resolve a branch once: both files must come from the same immutable commit.
    names = [f"runs/{run_id}.json", f"runs/{run_id}.zip"]
    remote = {p.path: p for p in api.get_paths_info(repo_id, names, repo_type="dataset", revision=info.sha)}
    if set(remote) != set(names):
        raise ValueError("Run bundle not found at the requested revision")
    if any(type(getattr(item, "size", None)) is not int or item.size < 0 for item in remote.values()):
        raise ValueError("Expected regular bundle files with known sizes")
    if remote[names[0]].size > MAX_METADATA_BYTES or remote[names[1]].size > MAX_BYTES:
        raise ValueError("Remote bundle or metadata exceeds the download size limit")
    root.mkdir(parents=True, exist_ok=True)
    from huggingface_hub import hf_hub_download
    with tempfile.TemporaryDirectory(prefix=".hf-download-", dir=root) as temp:
        temp = Path(temp)
        # local_dir avoids Windows symlink privileges and keeps cache files outside the published run.
        local = [Path(hf_hub_download(repo_id, name, repo_type="dataset", revision=info.sha,
                                     token=api.token, local_dir=temp / "download")) for name in names]
        metadata = json.loads(local[0].read_text("utf-8"))
        staging = temp / "run"
        staging.mkdir()
        result = _unpack(local[1], metadata, staging, run_id)
        if target.exists():
            raise FileExistsError("Local run was created during download; refusing to overwrite")
        staging.rename(target)
    return {"repo_id": repo_id, "commit": info.sha, "run": str(target), **result}
