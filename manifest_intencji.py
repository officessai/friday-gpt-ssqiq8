#!/usr/bin/env python3
"""Codex Launcher: validates access and runs helper scripts sequentially."""

import subprocess
from datetime import datetime

ACCESS_CODE = "RUN-CODEX-888"
PYTHON_FILES = ["one.py", "two.py", "three.py"]


def validate_access(code: str) -> bool:
    """Return True when the provided access code matches the expected value."""
    return code == ACCESS_CODE


def log_launch(log_path: str = "launch.log") -> None:
    """Append the current launch timestamp to the log file."""
    with open(log_path, "a", encoding="utf-8") as log:
        log.write(f"Launch at {datetime.now().isoformat()}\n")


def run_scripts(files: list[str]) -> None:
    """Execute each Python helper script sequentially and print their output."""
    print("Starting sequential execution:\n")
    for script in files:
        print(f"\nRunning {script}...")
        result = subprocess.run(["python3", script], capture_output=True, text=True, check=False)
        print(f"Output of {script}:")
        print(result.stdout, end="")
        if result.stderr:
            print(f"Errors from {script}:\n{result.stderr}")


def main() -> None:
    """Prompt for access, log the launch, and run configured helper scripts."""
    print("--- Codex Launcher ---")
    access = input("Enter access code: ")

    if not validate_access(access):
        print("Invalid access code. Access denied.")
        return

    log_launch()
    run_scripts(PYTHON_FILES)
    print("\n--- All scripts executed. ---")


if __name__ == "__main__":
    main()
