from __future__ import annotations

from pathlib import Path, PurePath

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
    output_stem: str | Path | PurePath,
    title: str = "Customer API",
    direction: str = "LR",
    outformat: str = "png",
    graph_attributes: dict[str, str] | None = None,
) -> Path:
    output_stem_path = Path(output_stem)
    if output_stem_path.suffix:
        raise ValueError(
            "output_stem must not include a file extension; set outformat instead."
        )

    output_stem_path.parent.mkdir(parents=True, exist_ok=True)
    graph_attributes = (
        GRAPH_ATTRIBUTES if graph_attributes is None else graph_attributes
    )

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
