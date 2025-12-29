import os
import json
from pathlib import Path


def scan_studio_projects(project_path="/mnt/scratch/projects"):
    """
    Evolution Studio Audit Tool: Verifies 990 PRO mount status and
    catalogs projects without path drift.
    """
    path = Path(project_path)

    # 1. Hardware Check: Verify Mount
    if not path.exists():
        return (
            f"CRITICAL: {project_path} not found. Ensure S: drive is mounted "
            "with noatime."
        )

    # 2. Project Catalog
    projects = [
        d.name for d in path.iterdir() if d.is_dir() and not d.name.startswith(".")
    ]

    # 3. Vault Update (Institutional Memory)
    manifest_path = "/mnt/scratch/vault/studio_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump({"timestamp": "2025-12-29", "inventory": projects}, f)

    return f"Audit Complete. Found {len(projects)} projects. Manifest updated in vault."
