#!/usr/bin/env python3
"""Run the ANI validation API with uvicorn."""

from __future__ import annotations

import argparse
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Run FastAPI ANI validation service")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", default="8080")
    args = parser.parse_args()
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "antispam_robocall_toolkit.api:app",
        "--app-dir",
        "src",
        "--host",
        args.host,
        "--port",
        args.port,
        "--reload",
    ]
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
