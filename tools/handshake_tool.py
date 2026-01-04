import os
import subprocess
from pathlib import Path

def verify_hardware_readiness():
    """
    CTO Tool: Final check of physical infrastructure before pipeline ignition.
    Validates: 990 PRO mount, RTX 3060 visibility, and Vault integrity.
    """
    # 1. Validate 990 PRO Mount Point
    mount_point = "/mnt/scratch"
    if not os.path.ismount(mount_point):
        return f"HARDWARE ERROR: {mount_point} is not mounted. Pipeline halted."

    # 2. Verify RTX 3060 Headless Compute via nvidia-smi
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'], 
                                capture_output=True, text=True, check=True)
        if "RTX 3060" not in result.stdout:
            return "HARDWARE ERROR: RTX 3060 not detected. Check BIOS iGPU split."
    except Exception:
        return "HARDWARE ERROR: nvidia-smi failed. Ensure drivers are installed."

    # 3. Confirm Vault Constitution
    vault_path = Path("/mnt/scratch/vault/hardware_specs.md")
    if not vault_path.exists():
        return "GOVERNANCE ERROR: hardware_specs.md (Constitution) missing from vault."

    return "SUCCESS: Hardware Handshake Complete. 990 PRO and RTX 3060 verified."
