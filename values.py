import matplotlib.pyplot as plt
import networkx as nx
from dataclasses import dataclass

@dataclass
class Number:
    value: float

@dataclass
class Name:
    value: str
    final: bool
    start: bool

@dataclass
class Connection:
    name_a: Name
    name_b: Name
    weight: Number
    destroy: bool

class Graph:
    def __init__(self):
        self.G = nx.DiGraph()
        plt.ion()  # Turn on interactive mode
        self.fig, self.ax = plt.subplots()

    def add_connection(self, connection):
        if not connection.destroy:
            self.G.add_edge(connection.name_a.value, connection.name_b.value, weight=connection.weight.value)
        self.draw()

    def draw(self):
        self.ax.clear()
        pos = nx.kamada_kawai_layout(self.G)  # Using a layout that better handles overlaps
        nx.draw(self.G, pos, with_labels=True, font_weight='bold', node_color='skyblue', edge_color='k', node_size=700, ax=self.ax)

        # Omit zero weights from the edge labels
        edge_weights = {edge: data['weight'] for edge, data in self.G.edges.items() if data['weight'] > 0}
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_weights, ax=self.ax)

        # Custom handling for loopback connections and bidirectional edges can be added here

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def remove_connection(self, connection):
        if self.G.has_edge(connection.name_a.value, connection.name_b.value):
            self.G.remove_edge(connection.name_a.value, connection.name_b.value)
        self.draw()
