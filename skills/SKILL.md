---
name: diagrams
description: "Create, edit, and troubleshoot Python architecture diagrams with the mingrammer/diagrams library. Use when Codex needs to generate diagram-as-code scripts, render cloud/system architecture diagrams, select provider node classes, use Diagram/Cluster/Edge patterns, debug Graphviz rendering issues, embed rendered diagrams in marimo notebooks, or use pycairo for lower-level custom drawing."
---

# Diagrams

## Overview

Use the `diagrams` Python library to create architecture diagrams as code. The library renders through Graphviz and is best for cloud, Kubernetes, on-prem, SaaS, C4, generic infrastructure, and programming-framework diagrams.

## Workflow

1. Clarify the target output: providers, major systems, grouping boundaries, data flow direction, output format, and destination file.
2. Check the local environment before rendering:

```bash
python skills/scripts/check_diagrams_env.py
```

3. Choose node classes by inspecting the installed package when possible:

```bash
python skills/scripts/list_diagrams_nodes.py --provider aws --query lambda
python skills/scripts/list_diagrams_nodes.py --provider k8s --category compute
```

4. Write a normal Python script near the requested output. Use `show=False`, an explicit `filename` without an extension, and the requested `outformat` (`png`, `jpg`, `svg`, `pdf`, or `dot`).
5. For marimo notebooks, put diagram construction in an importable module and call a `build_diagram(output_stem) -> Path` function from the notebook; read [marimo-auto-render.md](references/marimo-auto-render.md) for the full pattern.
6. Use `diagrams` by default for architecture diagrams; use pycairo only when the user needs lower-level custom drawing control. For pycairo in marimo, expose `draw_surface(output_stem) -> Path`; read [pycairo-marimo.md](references/pycairo-marimo.md).
7. Render by running the diagram script, then verify that the expected output file exists and is non-empty.
8. If rendering fails, use the troubleshooting section in [library-guide.md](references/library-guide.md).

## Coding Pattern

Prefer readable variables and explicit imports. Assign nodes once and connect the variables; repeated constructor calls create repeated diagram nodes.

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

## Guidance

- Read [library-guide.md](references/library-guide.md) when selecting providers, using clusters/edges, working with custom nodes, or debugging errors.
- Use `Diagram(..., direction="LR")` by default for service flows; use `TB` for layered or top-down architecture. Other valid directions are `BT` and `RL`.
- Use `Cluster` for deployment boundaries, security zones, subnets, teams, or logical tiers. Avoid deep nesting unless the user needs it.
- Use `Edge(label=..., color=..., style=...)` sparingly for important protocols, trust boundaries, or asynchronous flows.
- Use list fanout for replicas or parallel consumers: `lb >> [ECS("api-1"), ECS("api-2")]`.
- Parenthesize mixed `-`, `>>`, and `<<` expressions when chaining undirected and directed edges.
- Prefer `svg` for version-controlled diagrams and `png` for documents, notebook display, or chat previews unless the user specifies otherwise.
- Treat notebook `rendered_diagrams/` directories as generated output unless the repo intentionally keeps a small example artifact.
- Use pycairo as an alternative for custom drawing with manual paths, fills, strokes, transforms, and cairo surfaces; do not make it the default architecture diagram path.

## Resources

- `scripts/check_diagrams_env.py`: verify Python, `diagrams`, and Graphviz `dot`.
- `scripts/check_pycairo_env.py`: verify pycairo, native cairo, and PNG output.
- `scripts/list_diagrams_nodes.py`: list node classes from the installed `diagrams` package.
- `references/library-guide.md`: detailed patterns, provider notes, examples, and troubleshooting.
- `references/marimo-auto-render.md`: direct-import marimo rendering pattern.
- `references/pycairo-marimo.md`: direct-import pycairo drawing pattern for marimo.
