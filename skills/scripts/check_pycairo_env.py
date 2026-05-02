#!/usr/bin/env python3
"""Check whether the local environment can render pycairo artifacts."""

from __future__ import annotations

import tempfile
from pathlib import Path


def main() -> int:
    try:
        import cairo
    except ModuleNotFoundError:
        print("MISSING: pycairo package: install with `pip install pycairo`")
        print(
            "Native requirements include cairo, cairo headers, and pkg-config "
            "when building from source."
        )
        return 1

    print(f"OK: pycairo package: {cairo.version}")
    print(f"OK: native cairo: {cairo.cairo_version_string()}")

    output_path = Path(tempfile.gettempdir()) / "pycairo-env-check.png"
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 16, 16)
    context = cairo.Context(surface)
    context.set_source_rgb(1, 1, 1)
    context.paint()
    context.set_source_rgb(0.1, 0.45, 0.85)
    context.rectangle(2, 2, 12, 12)
    context.fill()
    surface.write_to_png(str(output_path))
    surface.finish()

    if not output_path.is_file() or output_path.stat().st_size == 0:
        print(f"MISSING: pycairo artifact: expected {output_path}")
        return 1

    print(f"OK: pycairo artifact: {output_path}")
    print("\nEnvironment is ready to render pycairo artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
