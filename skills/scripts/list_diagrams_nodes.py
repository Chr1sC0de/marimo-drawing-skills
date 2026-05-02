#!/usr/bin/env python3
"""List node classes available in the installed diagrams package."""

from __future__ import annotations

import argparse
import importlib
import inspect
import pkgutil
import sys
from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class NodeClass:
    provider: str
    category: str
    module: str
    name: str


def _load_diagrams():
    try:
        diagrams = importlib.import_module("diagrams")
        node = getattr(diagrams, "Node")
    except ModuleNotFoundError:
        print(
            "The `diagrams` package is not installed. Install it with `pip install diagrams`.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    except AttributeError:
        print(
            "The installed `diagrams` package does not expose `Node` as expected.",
            file=sys.stderr,
        )
        raise SystemExit(2)

    return diagrams, node


def _iter_modules(package_name: str) -> Iterable[str]:
    package = importlib.import_module(package_name)
    package_path = getattr(package, "__path__", None)
    if package_path is None:
        return []

    return (
        module_info.name
        for module_info in pkgutil.walk_packages(package_path, f"{package_name}.")
        if not module_info.ispkg
    )


def _iter_node_classes(provider: str | None) -> Iterable[NodeClass]:
    _, base_node = _load_diagrams()
    root = f"diagrams.{provider}" if provider else "diagrams"

    try:
        module_names = _iter_modules(root)
    except ModuleNotFoundError:
        print(f"No diagrams provider named `{provider}` is installed.", file=sys.stderr)
        raise SystemExit(2)

    for module_name in module_names:
        parts = module_name.split(".")
        if len(parts) < 3:
            continue

        provider_name = parts[1]
        category = parts[2] if len(parts) > 2 else ""

        try:
            module = importlib.import_module(module_name)
        except Exception as exc:  # pragma: no cover - provider imports are third-party code.
            print(f"Skipping {module_name}: {exc}", file=sys.stderr)
            continue

        for class_name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ != module.__name__:
                continue
            if class_name.startswith("_") or class_name == "Node":
                continue
            try:
                is_node = issubclass(obj, base_node)
            except TypeError:
                is_node = False
            if is_node:
                yield NodeClass(provider_name, category, module_name, class_name)


def _matches(node_class: NodeClass, category: str | None, query: str | None) -> bool:
    if category and node_class.category != category:
        return False
    if query is None:
        return True

    haystack = f"{node_class.provider} {node_class.category} {node_class.module} {node_class.name}".lower()
    return query.lower() in haystack


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--provider",
        help="Provider namespace, such as aws, gcp, k8s, onprem, generic, or saas.",
    )
    parser.add_argument(
        "--category",
        help="Category under the provider, such as compute, database, network, or storage.",
    )
    parser.add_argument(
        "--query",
        help="Case-insensitive search term for class name or module path.",
    )
    parser.add_argument("--limit", type=int, default=200, help="Maximum rows to print.")
    args = parser.parse_args()

    rows = [
        node_class
        for node_class in _iter_node_classes(args.provider)
        if _matches(node_class, args.category, args.query)
    ]
    rows.sort(key=lambda row: (row.provider, row.category, row.name))

    if args.limit >= 0:
        rows = rows[: args.limit]

    if not rows:
        print("No matching node classes found.")
        return 1

    for row in rows:
        print(f"{row.module}.{row.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
