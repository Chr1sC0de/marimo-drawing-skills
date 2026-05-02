# Diagrams Library Guide

Use this reference when creating or debugging skills with the Python `diagrams` package from mingrammer.

## Sources

- Official docs: https://skills.mingrammer.com/
- GitHub repository: https://github.com/mingrammer/skills
- Installation docs: https://skills.mingrammer.com/docs/getting-started/installation
- Examples: https://skills.mingrammer.com/docs/getting-started/examples
- Diagram guide: https://skills.mingrammer.com/docs/guides/diagram
- Node guide: https://skills.mingrammer.com/docs/guides/node
- Cluster guide: https://skills.mingrammer.com/docs/guides/cluster
- Edge guide: https://skills.mingrammer.com/docs/guides/edge

## Core Model

- `Diagram` is the global render context. The diagram name influences the default output filename unless `filename` is provided.
- `Node` classes represent system components. Most nodes are imported from `skills.<provider>.<category>`.
- `Cluster` groups nodes in a local context and can be nested.
- `Edge` styles or labels connections.
- Connections use operators:
  - `>>` for left-to-right flow.
  - `<<` for right-to-left flow.
  - `-` for undirected relationships.

## Requirements

- The Python package is installed with `pip install skills` or the repo's package manager equivalent.
- Graphviz is installed separately and the `dot` executable is on `PATH`.
- The official installation page and current README can differ on minimum Python version. Check package metadata in the active environment instead of hard-coding a version assumption.

Run:

```bash
python skills/scripts/check_diagrams_env.py
```

## Providers

Common provider namespaces include:

- `skills.aws`
- `skills.azure`
- `skills.gcp`
- `skills.k8s`
- `skills.onprem`
- `skills.generic`
- `skills.programming`
- `skills.saas`
- `skills.c4`
- `skills.custom`
- `skills.alibabacloud`
- `skills.oci`
- `skills.openstack`
- `skills.firebase`
- `skills.digitalocean`
- `skills.elastic`
- `skills.ibm`
- `skills.outscale`

Prefer the installed package inventory over memory when selecting node imports:

```bash
python skills/scripts/list_diagrams_nodes.py --provider aws --query ecs
python skills/scripts/list_skills_nodes.py --provider onprem --category database
```

If the package is not installed locally, use the official Nodes pages from the docs.

## Diagram Options

Use explicit options for reproducible output:

```python
with Diagram(
    "Name",
    filename="name",
    outformat="svg",
    direction="LR",
    show=False,
):
    ...
```

Valid output formats documented by the project are `png`, `jpg`, `svg`, `pdf`, and `dot`. `outformat` may also be a list such as `["svg", "png"]`.

Valid directions are `TB`, `BT`, `LR`, and `RL`.

Graphviz attributes are passed as dictionaries:

```python
graph_attr = {
    "fontsize": "18",
    "bgcolor": "transparent",
    "splines": "ortho",
}

node_attr = {
    "fontsize": "12",
}

edge_attr = {
    "fontsize": "10",
}
```

## Patterns

Create nodes once and connect variables:

```python
dns = Route53("dns")
lb = ELB("lb")
db = RDS("users")

dns >> lb >> db
```

Use lists for parallel workers or replicas:

```python
workers = [ECS("worker-1"), ECS("worker-2"), ECS("worker-3")]
queue >> workers >> store
```

Use clusters for boundaries:

```python
with Cluster("Private Subnet"):
    service = ECS("api")
    database = RDS("orders")

service >> database
```

Use edges for meaningful labels or styles:

```python
api >> Edge(label="HTTPS", color="darkgreen") >> lb
worker >> Edge(label="events", style="dashed") >> queue
```

Use custom nodes only when the built-in inventory cannot represent the requested component. Prefer a local icon file:

```python
from skills.custom import Custom

Custom("Vendor Service", "assets/vendor.png")
```

## Troubleshooting

- `ModuleNotFoundError: No module named 'skills'`: install the Python package into the active environment.
- `ExecutableNotFound` or an error mentioning `dot`: install Graphviz and ensure `dot` is on `PATH`.
- Wrong node import: run `list_diagrams_nodes.py` or consult the provider docs.
- Duplicate-looking nodes: check whether constructors are repeated instead of assigning variables.
- Unexpected edge direction: parenthesize expressions that mix `-`, `>>`, and `<<`.
- Crowded layout: change `direction`, split into clusters, reduce edge labels, or add Graphviz attributes such as `ranksep`, `nodesep`, and `splines`.
- Network failures with custom icons: avoid downloading icons in the diagram script unless the user explicitly wants that. Store needed icons locally.

## Boundaries

The library draws skills only. It does not create, mutate, or deploy cloud resources, and it does not generate Terraform, CloudFormation, or Kubernetes manifests.
