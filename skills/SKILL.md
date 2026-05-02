---
name: marimo-drawing
description: "Create, render, and troubleshoot drawings in marimo notebooks. Use when Codex needs to make or modify marimo notebook drawings, choose between the diagrams backend for architecture diagrams and pycairo for custom drawing, generate importable drawing modules, display rendered artifacts with mo.image, or verify Graphviz/pycairo rendering environments."
---

# Marimo Drawing

## Overview

Use this skill to create drawing workflows in marimo notebooks. The notebook should call importable drawing modules, write rendered artifacts to a notebook-local output directory, and display them with `mo.image`.

Use `diagrams` as the default backend for cloud, Kubernetes, on-prem, SaaS, C4, generic infrastructure, and programming-framework architecture diagrams. Use pycairo only when the user needs lower-level custom drawing control over paths, fills, strokes, gradients, transforms, or cairo surfaces.

## Reference Selection

- Architecture diagrams in marimo: read [marimo-auto-render.md](references/marimo-auto-render.md).
- `diagrams` providers, nodes, clusters, edges, or Graphviz troubleshooting: read [library-guide.md](references/library-guide.md).
- Custom drawing in marimo with cairo surfaces, paths, gradients, or aspect-aware geometry: read [pycairo-marimo.md](references/pycairo-marimo.md).

## Workflow

1. Clarify the notebook output: drawing purpose, backend, dimensions/aspect ratio, output format, destination slide, and rendered artifact name.
2. Choose the backend. Use `diagrams` by default for architecture diagrams. Use pycairo for custom drawing that needs manual geometry or surface-level control.
3. Check only the relevant local environment before rendering:

```bash
# For diagrams:
python skills/scripts/check_diagrams_env.py

# For pycairo:
python skills/scripts/check_pycairo_env.py
```

4. For `diagrams`, choose node classes by inspecting the installed package when possible:

```bash
python skills/scripts/list_diagrams_nodes.py --provider aws --query lambda
python skills/scripts/list_diagrams_nodes.py --provider k8s --category compute
```

5. Put drawing construction in an importable module. Use `build_diagram(output_stem) -> Path` for diagrams and `draw_surface(output_stem) -> Path` for pycairo.
6. Pass an extensionless output stem, create parent directories in the drawing module, and return the final rendered artifact path.
7. Keep marimo cells focused on presentation: call the drawing module function and display the returned path with `mo.image`.
8. Configure local imports from the CLI before iterating, for example `PYTHONPATH="$PWD/notebooks:$PYTHONPATH"`; do not mutate `sys.path` inside notebooks.
9. Treat notebook `rendered_diagrams/` directories as generated output unless the repo intentionally keeps a small example artifact.
10. Verify by rendering the drawing module directly and embedding or exporting the marimo notebook.

## Backend Patterns

For architecture diagrams, prefer readable variables and explicit imports. Assign nodes once and connect the variables; repeated constructor calls create repeated diagram nodes.

```python
from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import ECS
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB, Route53

graph_attr = {
    "fontsize": "18",
    "pad": "0.35",
    "splines": "ortho",
}

with Diagram(
    "Customer API",
    filename="customer_api",
    outformat="svg",
    direction="LR",
    show=False,
    graph_attr=graph_attr,
):
    dns = Route53("dns")
    lb = ELB("load balancer")

    with Cluster("Services"):
        api = [ECS("api-1"), ECS("api-2")]

    db = RDS("orders")

    dns >> lb >> api >> Edge(label="read/write") >> db
```

For custom drawing, read [pycairo-marimo.md](references/pycairo-marimo.md). Use an aspect-aware design coordinate system instead of scaling x and y independently, because `context.scale(width, height)` distorts circles, text, and rounded corners on non-square canvases.

## Guidance

- Use `Diagram(..., direction="LR")` by default for service flows; use `TB` for layered or top-down architecture. Other valid directions are `BT` and `RL`.
- Use `Cluster` for deployment boundaries, security zones, subnets, teams, or logical tiers. Avoid deep nesting unless the user needs it.
- Use `Edge(label=..., color=..., style=...)` sparingly for important protocols, trust boundaries, or asynchronous flows.
- Use list fanout for replicas or parallel consumers: `lb >> [ECS("api-1"), ECS("api-2")]`.
- Parenthesize mixed `-`, `>>`, and `<<` expressions when chaining undirected and directed edges.
- Prefer `png` for marimo display and chat previews unless the user requests another format.
- Prefer `svg` for version-controlled architecture diagram source outputs.
- Use pycairo as an alternative for custom drawing; do not make it the default architecture diagram path.
- Keep notebook import setup outside the notebook. Agents should prepend module paths from the CLI before iterating.
- Preserve the user's surrounding notebook structure. Add only the drawing cells/modules needed for the request.

## Resources

- `scripts/check_diagrams_env.py`: verify Python, `diagrams`, and Graphviz `dot`.
- `scripts/check_pycairo_env.py`: verify pycairo, native cairo, and PNG output.
- `scripts/list_diagrams_nodes.py`: list node classes from the installed `diagrams` package.
- `references/marimo-auto-render.md`: direct-import marimo rendering pattern.
- `references/pycairo-marimo.md`: direct-import pycairo drawing pattern for marimo.
- `references/library-guide.md`: detailed diagrams backend patterns, provider notes, examples, and troubleshooting.
