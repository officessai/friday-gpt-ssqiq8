#!/usr/bin/env python3
"""Utility to run a sequence of Python scripts in order."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run_script(script: Path) -> None:
    """Execute a Python script using the current interpreter."""
    print(f"Running {script}...")
    result = subprocess.run([sys.executable, str(script)], check=False)
    if result.returncode != 0:
        raise RuntimeError(
            f"Script {script} exited with status {result.returncode}."
        )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run one or more Python scripts sequentially."
    )
    parser.add_argument(
        "scripts",
        nargs="*",
        help="Paths to Python files that should be executed in order.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    scripts = args.scripts or ["one.py", "two.py", "three.py"]

    for script_name in scripts:
        script_path = Path(script_name)
        if not script_path.is_file():
            print(f"Error: script '{script_name}' does not exist.", file=sys.stderr)
            return 1

        try:
            run_script(script_path)
        except RuntimeError as exc:
            print(str(exc), file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
