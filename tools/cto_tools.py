import os
import json
from pathlib import Path

def get_studio_laws():
    """
    CTO Tool: Loads the hardware_specs.md guide from the vault.
    Returns ERROR on missing vault or guide.
    """
    vault_path = os.getenv("EVO_VAULT_PATH", "/mnt/scratch/vault")
    vault_dir = Path(vault_path)
    mount_root = vault_dir if vault_dir.is_mount() else vault_dir.parent

    # Check mount point
    if not mount_root.is_mount():
        return (
            f"ERROR: {mount_root} is not mounted. Ensure 990 PRO is attached "
            "and /mnt/scratch is available."
        )

    # Load hardware guide
    laws_path = vault_dir / "hardware_specs.md"
    if not laws_path.exists():
        return f"ERROR: {laws_path} not found. Create the hardware guide first."

    return laws_path.read_text(encoding="utf-8")

def scan_studio_projects():
    """
    CTO Tool: Scans the /mnt/scratch/projects/ directory.
    Identifies existing tech stack and saves a manifest to the vault.
    """
    projects_path_str = os.getenv("EVO_PROJECTS_PATH", "/mnt/scratch/projects")
    vault_path_str = os.getenv("EVO_VAULT_PATH", "/mnt/scratch/vault")

    projects_path = Path(projects_path_str)
    mount_root = projects_path if projects_path.is_mount() else projects_path.parent

    # Validate mount
    if not mount_root.is_mount():
        return (
            f"ERROR: {mount_root} is not mounted. Ensure 990 PRO is attached "
            "and /mnt/scratch is available."
        )

    # Scan projects directory
    if not projects_path.exists():
        return f"ERROR: {projects_path_str} not found."

    vault_dir = Path(vault_path_str)
    if not vault_dir.exists():
        return f"ERROR: {vault_path_str} not found."

    # Create institutional memory
    projects = [
        d.name for d in projects_path.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    ]

    manifest = {
        "timestamp": os.popen("date").read().strip(),
        "inventory": projects
    }

    manifest_path = vault_dir / "studio_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)

    return f"Scan complete. Found: {', '.join(projects)}. Manifest updated in vault at {manifest_path}"
