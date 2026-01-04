import os
import subprocess
from datetime import datetime
from pathlib import Path

FIRST_SUCCESS_MARKER = "First Successful Audit"


def _repo_root(repo_path=None):
    if repo_path:
        return Path(repo_path)
    env_path = os.getenv("EVO_GURU_REPO")
    if env_path:
        return Path(env_path)
    return Path(__file__).resolve().parents[1]


def _git_run(repo_root, args):
    return subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def _changed_paths(status_output):
    paths = set()
    for line in status_output.splitlines():
        if not line:
            continue
        path_part = line[3:] if len(line) > 3 else ""
        if " -> " in path_part:
            path_part = path_part.split(" -> ", 1)[1]
        path_part = path_part.strip()
        if path_part:
            paths.add(path_part)
    return paths


def record_first_success(
    audit_summary="",
    repo_path=None,
    log_relative_path="run_log.md",
    allow_commit=True,
):
    """
    Records the first successful audit run and commits it if the repo is clean.
    """
    repo_root = _repo_root(repo_path)
    if not repo_root.exists():
        return f"ERROR: Repo path not found: {repo_root}"
    if not (repo_root / ".git").exists():
        return f"ERROR: {repo_root} is not a git repo."

    log_path = repo_root / log_relative_path
    log_rel = Path(log_relative_path).as_posix()
    if log_path.is_absolute():
        try:
            log_rel = log_path.relative_to(repo_root).as_posix()
        except ValueError:
            log_rel = log_path.name

    if log_path.exists():
        content = log_path.read_text(encoding="utf-8")
        if FIRST_SUCCESS_MARKER in content:
            return "Post-mortem already recorded; no changes made."

    timestamp = datetime.now().isoformat(timespec="seconds")
    summary = (audit_summary or "").strip()
    if summary:
        summary = " ".join(summary.splitlines()).strip()

    if not log_path.exists():
        log_path.write_text("# Evolution Guru Run Log\n\n", encoding="utf-8")

    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"- {FIRST_SUCCESS_MARKER}: {timestamp}\n")
        if summary:
            handle.write(f"  - Audit Summary: {summary}\n")
        handle.write("\n")

    if not allow_commit:
        return f"Recorded post-mortem in {log_rel}; commit skipped."

    staged = _git_run(repo_root, ["diff", "--name-only", "--cached"])
    if staged.returncode != 0:
        return f"ERROR: git diff failed: {staged.stderr.strip()}"
    if staged.stdout.strip():
        return "Post-mortem recorded, but staged changes detected; commit skipped."

    status = _git_run(repo_root, ["status", "--porcelain"])
    if status.returncode != 0:
        return f"ERROR: git status failed: {status.stderr.strip()}"
    changed = _changed_paths(status.stdout)
    if changed and changed != {log_rel}:
        return "Post-mortem recorded, but other changes exist; commit skipped."

    added = _git_run(repo_root, ["add", log_rel])
    if added.returncode != 0:
        return f"ERROR: git add failed: {added.stderr.strip()}"

    committed = _git_run(
        repo_root,
        ["commit", "-m", "chore: log first successful audit"],
    )
    if committed.returncode != 0:
        msg = (committed.stderr or committed.stdout).strip()
        return f"Post-mortem recorded; git commit skipped: {msg}"

    return "Post-mortem recorded and committed."
