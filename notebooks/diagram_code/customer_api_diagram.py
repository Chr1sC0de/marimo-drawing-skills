from __future__ import annotations

from pathlib import Path, PurePath

from skills.aws.compute import ECS
from skills.aws.database import RDS
from skills.aws.network import ELB, Route53

from skills import Cluster, Diagram, Edge

GRAPH_ATTRIBUTES = {
    "bgcolor": "transparent",
    "fontsize": "18",
    "pad": "0.35",
    "splines": "ortho",
}


def build_diagram(
    output_stem: str | Path | PurePath,
    title: str = "Customer API",
    direction: str = "LR",
    outformat: str = "png",
    graph_attributes: dict[str, str] | None = None,
) -> Path:
    output_stem_path = Path(output_stem)
    output_stem_path.parent.mkdir(parents=True, exist_ok=True)
    graph_attributes = graph_attributes or GRAPH_ATTRIBUTES

    with Diagram(
        title or "Architecture Diagram",
        filename=str(output_stem_path),
        outformat=outformat,
        direction=direction,
        show=False,
        graph_attr=graph_attributes,
    ):
        dns = Route53("dns")
        load_balancer = ELB("load balancer")

        with Cluster("Services"):
            services = [ECS("api-1"), ECS("api-2")]

        database = RDS("orders")

        dns >> load_balancer >> services >> Edge(label="read/write") >> database

    return output_stem_path.with_suffix(f".{outformat}")
