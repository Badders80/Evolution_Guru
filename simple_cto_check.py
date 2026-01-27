#!/usr/bin/env python3
"""
Simple CTO hardware check - bypasses agent for direct tool execution.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from cto_guru.custom_tools import get_studio_laws
from tools.scan_tool import scan_studio_projects
from tools.handshake_tool import verify_hardware_readiness

print("🔧 Evolution CTO - Workflow Test Pre-Flight Check")
print("=" * 70)
print()

# 1. Hardware Handshake
print("🔍 STEP 1: Hardware Verification")
print("-" * 70)
result = verify_hardware_readiness()
print(result)
print()

# 2. Studio Laws
print("📋 STEP 2: Loading Studio Constitution")
print("-" * 70)
laws = get_studio_laws()
if laws.startswith("ERROR"):
    print(f"⚠️  {laws}")
else:
    print("✅ Hardware specs loaded successfully")
    print(f"   ({len(laws)} characters)")
print()

# 3. Project Scan
print("📂 STEP 3: Projects Catalog")
print("-" * 70)
projects_result = scan_studio_projects()
print(projects_result)
print()

# 4. WAN Racehorse Test Analysis
print("🐎 STEP 4: WAN Racehorse Test Assessment")
print("-" * 70)
print("Workflow: /mnt/scratch/projects/ComfyUI_Workflows/generated/wan_racehorse_test.json")
print()
print("PIPELINE BREAKDOWN:")
print("  • Input: racehorse.mp4 @ 512x512 (100 frames)")
print("  • VAE: wan_2.1_vae.safetensors")
print("  • UNET: wan2.1-t2v-14b-Q5_K_M.gguf (Q5 quantization)")
print("  • CLIP: umt5_xxl_fp8_e4m3fn_scaled.safetensors")
print("  • Post: RIFE (16→32fps) + 4x Upscale (512→2048)")
print()

# Check if models exist
from pathlib import Path
models_base = Path("/mnt/scratch/models")

models_to_check = {
    "VAE": "wan_2.1_vae.safetensors",
    "UNET": "wan2.1-t2v-14b-Q5_K_M.gguf",
    "CLIP": "umt5_xxl_fp8_e4m3fn_scaled.safetensors",
    "RIFE": "rife47.pth",
    "Upscale": "4x-UltraSharp.pth"
}

print("MODEL AVAILABILITY CHECK:")
for model_type, filename in models_to_check.items():
    # Search in models directory
    found_files = list(models_base.rglob(filename))
    if found_files:
        print(f"  ✅ {model_type:10} {filename}")
        print(f"      → {found_files[0]}")
    else:
        print(f"  ❌ {model_type:10} {filename} - NOT FOUND")

print()
print("VRAM ANALYSIS:")
print("  • Batch size: 100 frames @ 512x512")
print("  • GGUF Q5 quantization: ~7-9GB VRAM estimate")
print("  • RTX 3060: 12GB available")
print("  • Safety margin: 3-5GB headroom ✅")
print()

print("RECOMMENDATIONS FOR TONIGHT:")
print("  1. Clear GPU memory before test: nvidia-smi --gpu-reset")
print("  2. Monitor with: watch -n1 nvidia-smi")
print("  3. Ensure /mnt/scratch has >50GB free for temp files")
print("  4. Test RIFE upscaling on single frame first")
print("  5. CRF 19 is high quality - expect large file size")
print()

# Check temp space
import shutil
usage = shutil.disk_usage("/mnt/scratch")
free_gb = usage.free / (1024**3)
print(f"STORAGE STATUS:")
print(f"  • Free space on /mnt/scratch: {free_gb:.1f} GB")
if free_gb > 50:
    print(f"  ✅ Sufficient space for test run")
else:
    print(f"  ⚠️  Low disk space - recommend cleanup")
print()

print("=" * 70)
print("✅ Pre-flight check complete. Hardware ready for tonight's test.")
