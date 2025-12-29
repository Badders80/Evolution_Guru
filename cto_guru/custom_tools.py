import os
import json
from pathlib import Path

from dotenv import load_dotenv


def _load_env():
    env_path = os.getenv("EVO_ENV_FILE")
    if env_path:
        load_dotenv(dotenv_path=env_path, override=True)
        return

    base_dir = Path(__file__).resolve().parent
    candidates = (
        base_dir / "central_keys.env",
        base_dir.parent / "central_keys.env",
        base_dir / ".env",
        base_dir.parent / ".env",
    )
    for candidate in candidates:
        if candidate.is_file():
            load_dotenv(dotenv_path=candidate, override=True)
            return

    load_dotenv()


_load_env()


def scan_studio_projects():
    """
    CTO Tool: Scans the /mnt/scratch/projects/ directory.
    Identifies existing tech stack and saves a manifest to the vault.
    """
    projects_path = os.getenv("EVO_PROJECTS_PATH", "/mnt/scratch/projects")
    vault_path = os.getenv("EVO_VAULT_PATH", "/mnt/scratch/vault")

    path = Path(projects_path)
    mount_root = path if os.path.ismount(path) else path.parent
    if not os.path.ismount(mount_root):
        return (
            f"ERROR: {mount_root} is not mounted. Ensure 990 PRO is attached "
            "and /mnt/scratch is available."
        )
    if not path.exists():
        return f"ERROR: {projects_path} not found. Ensure 990 PRO is mounted."

    vault_dir = Path(vault_path)
    if not vault_dir.exists():
        return f"ERROR: {vault_path} not found. Ensure 990 PRO is mounted."

    # List directories (excluding hidden ones)
    projects = [
        d.name for d in path.iterdir() if d.is_dir() and not d.name.startswith(".")
    ]

    # Save the 'Institutional Memory'
    manifest = {"timestamp": os.popen("date").read().strip(), "inventory": projects}
    with open(vault_dir / "studio_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)

    return f"Scan complete. Found: {', '.join(projects)}. Manifest updated in vault."


def get_studio_laws():
    """
    CTO Tool: Loads the hardware_specs.md guide from the vault.
    Returns ERROR on missing vault or guide.
    """
    vault_path = os.getenv("EVO_VAULT_PATH", "/mnt/scratch/vault")
    vault_dir = Path(vault_path)
    mount_root = vault_dir if os.path.ismount(vault_dir) else vault_dir.parent
    if not os.path.ismount(mount_root):
        return (
            f"ERROR: {mount_root} is not mounted. Ensure 990 PRO is attached "
            "and /mnt/scratch is available."
        )

    laws_path = vault_dir / "hardware_specs.md"
    if not laws_path.exists():
        return f"ERROR: {laws_path} not found. Create the hardware guide first."

    return laws_path.read_text(encoding="utf-8")
