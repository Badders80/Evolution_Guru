import os
import re
import json
import datetime
from pathlib import Path

def get_file_type(filename: str) -> str:
    """Classifies file type based on extension for the 'Local Meat Grinder'."""
    if filename.endswith('.mp4'):
        return 'video'
    if filename.endswith('.json'):
        return 'data'
    if filename.endswith(('.mp3', '.wav')):
        return 'voice'
    return 'unknown'

def create_manifest(studio_audit_report: str) -> str:
    """
    Analyzes the CTO's audit report, scans the physical 01_raw_intake directory,
    filters files by the mandatory naming convention [DATE]_[VENUE]_[TYPE],
    captures physical metadata, and creates a comprehensive input manifest.

    Args:
        studio_audit_report: The audit report from the Evolution_CTO agent.

    Returns:
        A JSON string representing the input manifest.
    """
    print("FileWatcher Tool: Switching to production mode. Scanning physical intake directory.")
    
    # 1. Path Targeting: Look specifically at the 01_raw_intake folder.
    intake_path_str = "/mnt/scratch/projects/01_raw_intake"
    base_path_str = "/mnt/scratch" # Base for creating relative paths
    intake_path = Path(intake_path_str)
    
    # Mandatory naming convention from The Evolution Bible.
    naming_convention = re.compile(r"^\d{4}-\d{2}-\d{2}_[a-zA-Z0-9]+_[a-zA-Z0-9]+_v\d+\..+$")
    
    manifest_entries = []

    if not intake_path.is_dir():
        print(f"Warning: Intake directory '{intake_path_str}' not found. Returning an empty manifest.")
    else:
        # Scan the physical directory structure.
        for root, _, files in os.walk(intake_path_str):
            for filename in files:
                if naming_convention.match(filename):
                    full_path = os.path.join(root, filename)
                    
                    try:
                        # 2. Physical Metadata: Get the actual file size.
                        file_size = os.path.getsize(full_path)
                        
                        # 3. Dual Path Integrity: Create relative path for agent reasoning.
                        relative_path = os.path.relpath(full_path, base_path_str)

                        file_type = get_file_type(filename)
                        parts = filename.split('_')
                        project_name = f"{parts[0]}_{parts[1]}"

                        entry = {
                            "project_name": project_name,
                            "file_path": full_path, # Absolute path for tools
                            "relative_path": str(Path(relative_path)), # Relative path for agent logic
                            "file_type": file_type,
                            "size_bytes": file_size,
                            "processing_queue": "transcription"
                        }
                        manifest_entries.append(entry)
                    except FileNotFoundError:
                        print(f"Warning: File '{full_path}' found during scan but could not be accessed.")

    print(f"Found {len(manifest_entries)} compliant files to add to the manifest.")

    final_manifest = {
      "manifest_id": f"manifest-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
      "timestamp": datetime.datetime.now().isoformat(),
      "entries": manifest_entries
    }
    
    return json.dumps(final_manifest, indent=2)
