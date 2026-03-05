# /// script
# requires-python = ">=3.12"
# dependencies = ["python-dotenv"]
# ///
"""Local dev server — starts session container, orchestrator, and frontend."""

import os
import signal
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).parent

if not (ROOT / ".env").exists():
    print("Error: .env not found. Copy .env.example to .env and fill in values.")
    sys.exit(1)

load_dotenv(ROOT / ".env")
os.environ["POOL_MANAGEMENT_ENDPOINT"] = "http://localhost:8080"
os.environ["WORKSPACE"] = str(ROOT / "workspace")
workspace = ROOT / "workspace"
# Clean workspace on startup so sessions don't see stale files
if workspace.exists():
    import shutil
    shutil.rmtree(workspace)
workspace.mkdir(exist_ok=True)

procs: list[subprocess.Popen] = []


def cleanup(*_):
    print("\nShutting down...")
    for p in procs:
        p.terminate()
    for p in procs:
        p.wait()
    sys.exit(0)


signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

print("Starting session container on :8080...")
procs.append(subprocess.Popen(
    ["uv", "run", "uvicorn", "server:app", "--port", "8080", "--reload"],
    cwd=ROOT / "session-container",
))

print("Starting orchestrator on :8000...")
procs.append(subprocess.Popen(
    ["uv", "run", "uvicorn", "app:app", "--port", "8000", "--reload"],
    cwd=ROOT,
))

print("Starting frontend on :3000...")
procs.append(subprocess.Popen(
    ["npm", "run", "dev"],
    cwd=ROOT / "frontend",
))

print()
print("  Frontend:  http://localhost:3000")
print("  API:       http://localhost:8000")
print("  Session:   http://localhost:8080")
print()

for p in procs:
    p.wait()
