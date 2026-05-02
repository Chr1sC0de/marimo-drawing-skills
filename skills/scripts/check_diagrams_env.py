#!/usr/bin/env python3
"""Check whether the local environment can render diagrams."""

from __future__ import annotations

import importlib.metadata
import shutil
import subprocess
import sys
from pathlib import Path


def _print_status(label: str, ok: bool, detail: str) -> None:
    prefix = "OK" if ok else "MISSING"
    print(f"{prefix}: {label}: {detail}")


def _check_diagrams() -> bool:
    try:
        version = importlib.metadata.version("diagrams")
    except importlib.metadata.PackageNotFoundError:
        _print_status("diagrams package", False, "install with `pip install diagrams`")
        return False

    _print_status("diagrams package", True, version)
    return True


def _check_graphviz() -> bool:
    dot = shutil.which("dot")
    if dot is None:
        _print_status(
            "Graphviz dot",
            False,
            "install Graphviz and ensure `dot` is on PATH",
        )
        return False

    try:
        result = subprocess.run(
            [dot, "-V"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except OSError as exc:
        _print_status("Graphviz dot", False, str(exc))
        return False

    version = (result.stderr or result.stdout).strip() or "version unavailable"
    _print_status("Graphviz dot", result.returncode == 0, f"{Path(dot)} ({version})")
    return result.returncode == 0


def main() -> int:
    print(f"Python: {sys.version.split()[0]} ({Path(sys.executable)})")
    ok = _check_diagrams()
    ok = _check_graphviz() and ok
    if not ok:
        print("\nRendering will fail until the missing dependency is available.")
        return 1

    print("\nEnvironment is ready to render diagrams.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
