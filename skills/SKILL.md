---
name: skills
description: "Create, edit, and troubleshoot Python architecture skills with the mingrammer/skills library. Use when Codex needs to generate diagram-as-code scripts, render cloud/system architecture diagrams, select provider node classes, use Diagram/Cluster/Edge patterns, or debug Graphviz and diagrams rendering issues."
---

# Diagrams

## Overview

Use the `skills` Python library to create architecture diagrams as code. The library renders through Graphviz and is best for cloud, Kubernetes, on-prem, SaaS, C4, generic infrastructure, and programming-framework diagrams.

## Workflow

1. Clarify the target output: providers, major systems, grouping boundaries, data flow direction, output format, and destination file.
2. Check the local environment before rendering:

```bash
python skills/scripts/check_diagrams_env.py
```

3. Choose node classes by inspecting the installed package when possible:

```bash
python skills/scripts/list_diagrams_nodes.py --provider aws --query lambda
python skills/scripts/list_skills_nodes.py --provider k8s --category compute
```

4. Write a normal Python script near the requested output. Use `show=False`, an explicit `filename` without an extension, and the requested `outformat` (`png`, `jpg`, `svg`, `pdf`, or `dot`).
5. Render by running the diagram script or the `skills` CLI, then verify that the expected output file exists and is non-empty.
6. If rendering fails, use the troubleshooting section in [library-guide.md](references/library-guide.md).

## Coding Pattern

Prefer readable variables and explicit imports. Assign nodes once and connect the variables; repeated constructor calls create repeated diagram nodes.

```python
from skills import Cluster, Diagram, Edge
from skills.aws.compute import ECS
from skills.aws.database import RDS
from skills.aws.network import ELB, Route53

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
- Prefer `svg` for version-controlled skills and `png` for documents or chat previews unless the user specifies otherwise.

## Resources

- `scripts/check_skills_env.py`: verify Python, `diagrams`, and Graphviz `dot`.
- `scripts/list_skills_nodes.py`: list node classes from the installed `skills` package.
- `references/library-guide.md`: detailed patterns, provider notes, examples, and troubleshooting.
