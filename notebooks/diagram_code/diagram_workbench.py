from __future__ import annotations

from pathlib import Path

from . import customer_api_diagram

DIAGRAM_CODE_DIR = Path(__file__).resolve().parent
NOTEBOOK_DIR = DIAGRAM_CODE_DIR.parent
DIAGRAM_OUTPUT_DIR = NOTEBOOK_DIR / "rendered_diagrams"


def render_aws_diagram(
    output_dir: str | Path = DIAGRAM_OUTPUT_DIR,
) -> Path:
    output_directory = Path(output_dir)
    output_stem = output_directory / "customer_api"
    return customer_api_diagram.build_diagram(output_stem)
