# Marimo Auto-Render Pattern

Use this reference when a marimo notebook should render a `diagrams` diagram and display the generated image automatically.

## Recommended Shape

Use direct import rendering:

1. Put diagram construction in an importable diagram module.
2. Expose a `build_diagram(output_stem, ...) -> Path` function.
3. Pass an extensionless output stem to `Diagram(filename=...)`.
4. Set `show=False`.
5. Return the final rendered artifact path.
6. In the marimo notebook, call `build_diagram(...)` from a cell and display the returned path with `mo.image`.

Do not shell out from the notebook by default. A subprocess wrapper is only useful when a diagram script needs process isolation or has an existing CLI contract.

## Diagram Module

```python
from __future__ import annotations

from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import ECS
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB, Route53

GRAPH_ATTRIBUTES = {
    "bgcolor": "transparent",
    "fontsize": "18",
    "pad": "0.35",
    "splines": "ortho",
}


def build_diagram(
    output_stem: str | Path,
    title: str = "Customer API",
    outformat: str = "png",
) -> Path:
    output_stem_path = Path(output_stem)
    if output_stem_path.suffix:
        raise ValueError(
            "output_stem must not include a file extension; set outformat instead."
        )

    output_stem_path.parent.mkdir(parents=True, exist_ok=True)

    with Diagram(
        title,
        filename=str(output_stem_path),
        outformat=outformat,
        direction="LR",
        show=False,
        graph_attr=GRAPH_ATTRIBUTES,
    ):
        dns = Route53("dns")
        load_balancer = ELB("load balancer")

        with Cluster("Services"):
            services = [ECS("api-1"), ECS("api-2")]

        database = RDS("orders")

        dns >> load_balancer >> services >> Edge(label="read/write") >> database

    return output_stem_path.with_suffix(f".{outformat}")
```

## Marimo Notebook Cells

```python
import marimo

__generated_with = "0.23.4"
app = marimo.App(width="medium")

with app.setup:
    from pathlib import Path

    import marimo as mo

    from notebooks.diagram_code import customer_api_diagram

    notebook_dir = Path(__file__).parent
    diagram_output_dir = notebook_dir / "rendered_diagrams"


@app.cell
def _():
    mo.md("## Customer API Architecture")
    return


@app.cell
def _():
    customer_api_diagram_path = customer_api_diagram.build_diagram(
        diagram_output_dir / "customer_api_diagram"
    )
    return (customer_api_diagram_path,)


@app.cell
def _(customer_api_diagram_path):
    mo.image(
        customer_api_diagram_path,
        alt="Customer API architecture diagram",
        width="100%",
    )
    return


if __name__ == "__main__":
    app.run()
```

## Path Rules

- Use a notebook-local output directory such as `notebooks/rendered_diagrams/`.
- Treat that directory as generated output unless the repo intentionally keeps an example artifact.
- Pass an extensionless output stem such as `diagram_output_dir / "customer_api_diagram"`.
- Do not pass `diagram_output_dir / "customer_api_diagram.png"`; `diagrams` will append the format extension and create names such as `customer_api_diagram.png.png`.

## Verification

Render outside marimo first when debugging:

```bash
python -c "from notebooks.diagram_code.customer_api_diagram import build_diagram; print(build_diagram('/tmp/customer_api_diagram'))"
```

Then run the notebook:

```bash
marimo run notebooks/slide_2.py
```

If rendering fails, check Graphviz and the `diagrams` package with:

```bash
python skills/scripts/check_diagrams_env.py
```
