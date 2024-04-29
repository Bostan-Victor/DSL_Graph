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
    left_dir: bool  # Direction towards A
    right_dir: bool  # Direction towards B

class Graph:
    def __init__(self):
        self.G = nx.DiGraph()
        plt.ion()  # Turn on interactive mode
        self.fig, self.ax = plt.subplots()

    def add_connection(self, connection):
        if not connection.destroy:
            # Add the edge with the appropriate direction
            if connection.left_dir and connection.right_dir:
                style = 'double_arrow'  # bidirectional
            elif connection.left_dir:
                style = 'left_arrow'  # arrow pointing to A
            elif connection.right_dir:
                style = 'right_arrow'  # arrow pointing to B
            else:
                style = 'line'  # straight line

            self.G.add_edge(connection.name_a.value, connection.name_b.value,
                            weight=connection.weight.value, style=style)
        self.draw()

    def draw(self):
        self.ax.clear()
        pos = nx.kamada_kawai_layout(self.G)  # Using a layout that better handles overlaps
        nx.draw_networkx_nodes(self.G, pos, node_color='skyblue', node_size=700, ax=self.ax)
        nx.draw_networkx_labels(self.G, pos, font_weight='bold', ax=self.ax)

        edge_labels = {}
        for edge in self.G.edges(data=True):
            style = edge[2].get('style', 'line')
            weight = edge[2]['weight']
            if weight > 0:
                edge_labels[(edge[0], edge[1])] = f"{weight}"

            if style == 'double_arrow':
                nx.draw_networkx_edges(self.G, pos, edgelist=[(edge[0], edge[1])],
                                       arrowstyle='<->', arrowsize=20, ax=self.ax)
            elif style == 'left_arrow':
                nx.draw_networkx_edges(self.G, pos, edgelist=[(edge[0], edge[1])],
                                       arrowstyle='<-', arrowsize=20, ax=self.ax)
            elif style == 'right_arrow':
                nx.draw_networkx_edges(self.G, pos, edgelist=[(edge[0], edge[1])],
                                       arrowstyle='->', arrowsize=20, ax=self.ax)
            else:
                nx.draw_networkx_edges(self.G, pos, edgelist=[(edge[0], edge[1])],
                                       arrowstyle='-', ax=self.ax)

        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, ax=self.ax)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def remove_connection(self, connection):
        if self.G.has_edge(connection.name_a.value, connection.name_b.value):
            self.G.remove_edge(connection.name_a.value, connection.name_b.value)
        self.draw()
