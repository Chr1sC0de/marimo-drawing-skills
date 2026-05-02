# Marimo Drawing Skill

This repository contains a Codex skill for helping agents create, render, and troubleshoot drawings in marimo notebooks.

Skill name: `marimo-drawing`.

The skill supports two drawing backends:

- `diagrams`: the default backend for architecture diagrams as code.
- `pycairo`: an alternative backend for custom lower-level drawing with paths, fills, strokes, gradients, transforms, and cairo surfaces.

The common workflow is the same for both backends: put drawing code in an importable Python module, render an image artifact to a notebook-local output directory, and display the result in marimo with `mo.image`.

## Repository Layout

- `skills/SKILL.md`: main skill instructions.
- `skills/references/marimo-auto-render.md`: `diagrams` backend pattern for marimo.
- `skills/references/pycairo-marimo.md`: pycairo backend pattern for marimo.
- `skills/references/library-guide.md`: detailed `diagrams` library reference.
- `skills/scripts/check_diagrams_env.py`: verifies `diagrams` and Graphviz.
- `skills/scripts/check_pycairo_env.py`: verifies pycairo and native cairo.
- `skills/scripts/list_diagrams_nodes.py`: lists installed `diagrams` node classes.
- `notebooks/slide_2.py`: executable `diagrams` marimo example.
- `notebooks/slide_3.py`: executable pycairo marimo example.
- `notebooks/diagram_code/`: drawing modules for `diagrams`.
- `notebooks/drawing_code/`: drawing modules for pycairo.

## Usage

Install dependencies:

```bash
uv sync
```

Check the drawing environments:

```bash
uv run python skills/scripts/check_diagrams_env.py
uv run python skills/scripts/check_pycairo_env.py
```

Run the example notebook with notebook-local modules on `PYTHONPATH`:

```bash
PYTHONPATH="$PWD/notebooks:$PYTHONPATH" uv run marimo run notebooks/main.py
```

When working outside this repository, replace `$PWD/notebooks` with the directory that contains the notebook-local drawing packages.

Export the example notebook:

```bash
PYTHONPATH="$PWD/notebooks:$PYTHONPATH" uv run marimo export html notebooks/main.py -o /tmp/marimo-drawing.html -f --no-include-code
```

## Agent Conventions

- Use `diagrams` by default for architecture diagrams.
- Use pycairo only when custom drawing control is required.
- Keep drawing construction outside marimo cells in importable modules.
- Use `build_diagram(output_stem) -> Path` for `diagrams` modules.
- Use `draw_surface(output_stem) -> Path` for pycairo modules.
- Pass extensionless output stems and let the backend append the output format.
- Do not mutate `sys.path` inside notebooks; prepend `PYTHONPATH` from the CLI.
- Treat `notebooks/rendered_diagrams/` as generated output.

## Verification

Render the `diagrams` example directly:

```bash
PYTHONPATH="$PWD/notebooks:$PYTHONPATH" uv run python -c "from diagram_code.customer_api_diagram import build_diagram; print(build_diagram('/tmp/customer_api_diagram'))"
```

Render the pycairo example directly:

```bash
PYTHONPATH="$PWD/notebooks:$PYTHONPATH" uv run python -c "from drawing_code.cairo_interface import draw_surface; print(draw_surface('/tmp/pycairo_interface'))"
```

Run Python compilation checks:

```bash
uv run python -m compileall notebooks skills/scripts
```
