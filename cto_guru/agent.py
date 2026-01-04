import os
from pathlib import Path

from dotenv import load_dotenv

_env_file = os.getenv("EVO_ENV_FILE")
if _env_file:
    load_dotenv(dotenv_path=_env_file, override=True)
else:
    load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env", override=True)

from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import FunctionTool

from tools.scan_tool import scan_studio_projects
from tools.postmortem import record_first_success
from .custom_tools import get_studio_laws


cto_tool = FunctionTool(scan_studio_projects)
postmortem_tool = FunctionTool(record_first_success)

# 1. The CTO Advisor (Strategy & Audit)
advisor = Agent(
    name="Evolution_CTO",
    model="gemini-2.0-flash",  # High-speed reasoning
    instruction=(
        "You are the CTO. Always run 'get_studio_laws' first. "
        "If it returns an ERROR, reply 'Hardware Error: <error>' and stop. "
        "Then run 'scan_studio_projects' and include the hardware laws in your audit. "
        "Use tool outputs for absolute paths, and keep internal logic on "
        "relative paths. Audit the /mnt/scratch paths for compliance."
    ),
    tools=[FunctionTool(get_studio_laws), cto_tool],
    output_key="studio_audit_report",
)

# 2. File Watcher (Detect)
file_watcher = Agent(
    name="FileWatcher",
    model="gemini-2.0-flash",
    instruction=(
        "Use {{studio_audit_report}} as the grounding law. "
        "Create an input manifest anchored to /mnt/scratch projects and data. "
        "Keep internal logic on relative paths and output only the manifest."
    ),
    output_key="input_manifest",
)

# 3. Transcriber (Process)
transcriber = Agent(
    name="Transcriber",
    model="gemini-2.0-flash",
    instruction=(
        "Use {{input_manifest}} to produce raw transcription output. "
        "Keep temporary files on /mnt/scratch and return only the raw result."
    ),
    output_key="transcription_raw",
)

# 4. Extractor (Extract)
extractor = Agent(
    name="Extractor",
    model="gemini-2.0-flash",
    instruction=(
        "Use {{transcription_raw}} to extract structured metadata. "
        "Assume GPU/LM Studio for compute and return only metadata payload."
    ),
    output_key="metadata_payload",
)

# 5. Organiser (Commit)
organiser = Agent(
    name="Organiser",
    model="gemini-2.0-flash",
    instruction=(
        "Use {{metadata_payload}} to generate the final sync log. "
        "Confirm all outputs remain on /mnt/scratch before syncing to the library. "
        "After a successful audit, call 'record_first_success' with a brief "
        "summary from {{studio_audit_report}}."
    ),
    tools=[postmortem_tool],
    output_key="final_sync_log",
)

# Optional: Builder for implementation tasks (not in main chain yet).
builder = Agent(
    name="Evolution_Builder",
    model="gemini-2.0-flash",
    instruction=(
        "Use the {{studio_audit_report}} to ensure no path drift. "
        "Use relative paths for internal logic and rely on tools for "
        "/mnt/scratch access. Generate rigging for systemd and venv on the "
        "990 PRO."
    ),
)

# 2. The Final Orchestrator
root_agent = SequentialAgent(
    name="Evolution_Guru_v1",
    sub_agents=[advisor, file_watcher, transcriber, extractor, organiser],
)
