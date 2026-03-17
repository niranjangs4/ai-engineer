from __future__ import annotations

from pathlib import Path

import networkx as nx

from utils.helpers import ensure_directory


class NavigationGraph:
    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    def add_edge(self, source: str, target: str, action_label: str) -> None:
        self.graph.add_node(source)
        self.graph.add_node(target)
        self.graph.add_edge(source, target, action=action_label)

    def get_neighbors(self, node: str) -> list[str]:
        if node not in self.graph:
            return []
        return list(self.graph.successors(node))

    def nodes(self) -> list[str]:
        return list(self.graph.nodes)

    def visualize(self, output_path: str | Path | None = None) -> str:
        lines: list[str] = []
        for node in self.graph.nodes:
            neighbors = self.get_neighbors(node)
            if neighbors:
                lines.append(f"{node} -> {', '.join(neighbors)}")
            else:
                lines.append(node)
        visualization = "\n".join(lines)
        if output_path:
            output_file = Path(output_path)
            ensure_directory(output_file.parent)
            output_file.write_text(visualization, encoding="utf-8")
        return visualization

    def shortest_path(self, source: str, target: str) -> list[str]:
        try:
            return nx.shortest_path(self.graph, source=source, target=target)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []
