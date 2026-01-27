#!/usr/bin/env python3
"""
Quick runner to invoke the CTO agent for custom audit tasks.
"""
import os
import sys
import asyncio
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from cto_guru.agent import advisor
from cto_guru.custom_tools import get_studio_laws
from google.adk.sessions import Session

async def audit_workflow_test():
    """Run CTO audit on the wan_racehorse_test workflow."""
    
    print("🔧 Evolution CTO - Workflow Test Audit")
    print("=" * 60)
    print()
    
    # Context about the test
    test_context = """
WORKFLOW AUDIT REQUEST:
======================
Location: /mnt/scratch/projects/ComfyUI_Workflows/generated/wan_racehorse_test.json
Scheduled: Tonight

WORKFLOW PIPELINE:
1. Load Video: racehorse.mp4 @ 512x512 (100 frames - test batch)
2. VAE: wan_2.1_vae.safetensors
3. UNET: wan2.1-t2v-14b-Q5_K_M.gguf (GGUF Q5 quality)
4. CLIP: umt5_xxl_fp8_e4m3fn_scaled.safetensors
5. Prompts:
   - Positive: "highly detailed thoroughbred racehorse with jockey, realistic grass 
     texture, natural fabric weave in racing silks, individual horse hair strands, 
     photorealistic skin and muscle definition, professional sports photography, 
     cinematic quality, sharp focus, 4K detail"
   - Negative: "low quality, worst quality, blurry, fuzzy, soft focus, artificial 
     looking, plastic, smooth textures, low detail, motion blur artifacts"
6. Post-Processing:
   - RIFE interpolation (16fps → 32fps @ 512x512)
   - 4x Upscale (512 → 2048) using 4x-UltraSharp.pth
   - Output: H.264 MP4 @ 32fps, CRF 19

HARDWARE REQUIREMENTS:
- RTX 3060 (12GB VRAM)
- Processing on /mnt/scratch for I/O speed
- Model files must be accessible on 990 PRO

AUDIT REQUEST:
Please verify:
1. Hardware readiness (RTX 3060, 990 PRO mount)
2. Model file locations and accessibility
3. VRAM safety (512x512 batch processing)
4. Temp file strategy on /mnt/scratch
5. Any path drift risks
6. Recommended optimizations for tonight's test run
"""
    
    print("📋 Test Context:")
    print(test_context)
    print()
    print("🔍 Invoking CTO Advisor Agent...")
    print("-" * 60)
    print()
    
    try:
        # Create a session
        session = Session(agent=advisor)
        
        # Run the CTO advisor with the workflow context
        print("📊 CTO AUDIT REPORT:")
        print("=" * 60)
        
        response = await session.send_message_async(
            f"{test_context}\n\nProvide a comprehensive audit report for this test run."
        )
        
        print(response.text)
        print()
        print("✅ Audit Complete")
        
    except Exception as e:
        print(f"❌ Error running CTO audit: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(audit_workflow_test())
