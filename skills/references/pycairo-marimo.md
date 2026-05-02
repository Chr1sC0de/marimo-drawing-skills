# Pycairo Marimo Pattern

Use this reference when a marimo notebook needs lower-level custom drawing than the `diagrams` library provides.

`diagrams` remains the default drawing tool for architecture diagrams. Use pycairo when the user needs manual control over cairo surfaces, paths, fills, strokes, gradients, transforms, or custom composition.

## Requirements

Pycairo installs as the Python module `cairo`. It also depends on the native cairo library. Building from source requires cairo headers and `pkg-config`.

Common native dependency examples from the pycairo docs:

- Ubuntu/Debian: `sudo apt install libcairo2-dev pkg-config python3-dev`
- macOS/Homebrew: `brew install cairo pkg-config`
- Fedora: `sudo dnf install cairo-devel pkg-config python3-devel`

Verify the local environment before relying on a pycairo notebook:

```bash
python skills/scripts/check_pycairo_env.py
```

## Recommended Shape

Use direct import rendering:

1. Put pycairo drawing code in an importable drawing module.
2. Expose a `draw_surface(output_stem, ...) -> Path` function.
3. Accept an extensionless output stem and default to `outformat="png"`.
4. Draw to a `cairo.ImageSurface`.
5. Use an aspect-aware design coordinate system instead of `context.scale(width, height)`, which distorts circles, text, and rounded corners.
6. Write the PNG with `surface.write_to_png(...)`.
7. Return the final rendered artifact path.
8. In marimo, call `draw_surface(...)` from a cell and display the path with `mo.image`.

## Drawing Module

```python
from __future__ import annotations

import math
from pathlib import Path

import cairo

DESIGN_WIDTH = 16.0
DESIGN_HEIGHT = 9.0


def draw_surface(
    output_stem: str | Path,
    width: int = 960,
    height: int = 540,
    outformat: str = "png",
) -> Path:
    if outformat != "png":
        raise ValueError("Only PNG output is supported for this pycairo pattern.")

    output_stem_path = Path(output_stem)
    if output_stem_path.suffix:
        raise ValueError(
            "output_stem must not include a file extension; set outformat instead."
        )

    output_stem_path.parent.mkdir(parents=True, exist_ok=True)
    output_path = output_stem_path.with_suffix(".png")

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context(surface)
    scale = min(width / DESIGN_WIDTH, height / DESIGN_HEIGHT)
    context.translate(
        (width - DESIGN_WIDTH * scale) / 2,
        (height - DESIGN_HEIGHT * scale) / 2,
    )
    context.scale(scale, scale)

    context.set_source_rgb(1, 1, 1)
    context.paint()

    context.set_line_width(0.08)
    context.set_source_rgb(0.12, 0.16, 0.22)
    context.arc(8, 4.5, 2.4, 0, 2 * math.pi)
    context.stroke()

    surface.write_to_png(str(output_path))
    surface.finish()
    return output_path
```

## Marimo Notebook Cells

```python
import marimo

__generated_with = "0.23.4"
app = marimo.App(width="medium")

with app.setup:
    import sys
    from pathlib import Path

    import marimo as mo

    notebook_dir = Path(__file__).parent
    if str(notebook_dir) not in sys.path:
        sys.path.insert(0, str(notebook_dir))

    from drawing_code import cairo_interface

    drawing_output_dir = notebook_dir / "rendered_diagrams"


@app.cell
def _():
    mo.md("## Pycairo Custom Drawing Interface")
    return


@app.cell
def _():
    cairo_artifact_path = cairo_interface.draw_surface(
        drawing_output_dir / "pycairo_interface"
    )
    return (cairo_artifact_path,)


@app.cell
def _(cairo_artifact_path):
    mo.image(cairo_artifact_path, alt="Pycairo custom drawing interface", width="100%")
    return


if __name__ == "__main__":
    app.run()
```

## Path Rules

- Use the same notebook-local generated output directory as diagram examples.
- Treat pycairo PNGs as rendered artifacts, not source.
- Pass an extensionless output stem such as `drawing_output_dir / "pycairo_interface"`.
- Do not pass a `.png` path; the draw function appends the extension from `outformat`.

## Sources

- Pycairo docs: https://pycairo.readthedocs.io/
- Getting Started: https://pycairo.readthedocs.io/en/latest/getting_started.html
- GitHub: https://github.com/pygobject/pycairo/tree/main
