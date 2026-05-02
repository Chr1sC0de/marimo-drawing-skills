from __future__ import annotations

import subprocess
import sys
from pathlib import Path

DIAGRAM_CODE_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = DIAGRAM_CODE_DIR.parent
PROJECT_PYTHON = WORKSPACE_ROOT / ".venv" / "bin" / "python"
AWS_DIAGRAM_FILE = DIAGRAM_CODE_DIR / "customer_api_diagram.py"
DIAGRAM_OUTPUT_DIR = WORKSPACE_ROOT / "rendered_diagrams"


def render_aws_diagram(
    diagram_file_path: str | Path = AWS_DIAGRAM_FILE,
    output_dir: str | Path = DIAGRAM_OUTPUT_DIR,
) -> Path:
    diagram_path = Path(diagram_file_path)
    output_directory = Path(output_dir)
    output_directory.mkdir(parents=True, exist_ok=True)

    output_stem = output_directory / "customer_api"
    image_path = output_stem.with_suffix(".png")
    python_executable = (
        PROJECT_PYTHON if PROJECT_PYTHON.is_file() else Path(sys.executable)
    )
    command = [
        str(python_executable),
        str(diagram_path),
        "--output-stem",
        str(output_stem),
        "--outformat",
        "png",
    ]

    completed_process = subprocess.run(
        command,
        cwd=diagram_path.parent,
        capture_output=True,
        check=False,
        text=True,
    )
    if completed_process.returncode != 0:
        command_text = " ".join(command)
        raise RuntimeError(
            "Diagram render failed.\n"
            f"Command: {command_text}\n"
            f"stdout:\n{completed_process.stdout}\n"
            f"stderr:\n{completed_process.stderr}"
        )

    if not image_path.is_file() or image_path.stat().st_size == 0:
        raise FileNotFoundError(f"Expected diagram was not created: {image_path}")

    return image_path
