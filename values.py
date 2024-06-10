import matplotlib.pyplot as plt
import networkx as nx
from dataclasses import dataclass
from matplotlib.figure import Figure

@dataclass(frozen=True)
class Number:
    value: float

@dataclass(frozen=True)
class Name:
    value: str
    final: bool
    start: bool

@dataclass(frozen=True)
class Connection:
    name_a: Name
    name_b: Name
    weight: Number
    destroy: bool
    left_dir: bool  
    right_dir: bool  

class Graph:
    def __init__(self, fig: Figure):
        self.G = nx.DiGraph()
        self.fig = fig
        self.ax = self.fig.add_subplot(111)

    def add_connection(self, connection):
        if not connection.destroy:
            # Add the edge with the appropriate direction
            if connection.left_dir and connection.right_dir:
                style = 'double_arrow'  
            elif connection.left_dir:
                style = 'left_arrow'  
            elif connection.right_dir:
                style = 'right_arrow'  
            else:
                style = 'line'  

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
        # This method checks if an edge between name_a and name_b exists and removes it.
        if self.G.has_edge(connection.name_a.value, connection.name_b.value):
            self.G.remove_edge(connection.name_a.value, connection.name_b.value)
            print(f"Removed edge from {connection.name_a.value} to {connection.name_b.value}")
        elif self.G.has_edge(connection.name_b.value, connection.name_a.value):
            # Check the other direction as well, in case the edge is bidirectional or reversed
            self.G.remove_edge(connection.name_b.value, connection.name_a.value)
            print(f"Removed edge from {connection.name_b.value} to {connection.name_a.value}")

        # Check if either node is now isolated and remove it if so
        if self.G.degree(connection.name_a.value) == 0:
            self.G.remove_node(connection.name_a.value)
            print(f"Removed isolated node: {connection.name_a.value}")

        if self.G.degree(connection.name_b.value) == 0:
            self.G.remove_node(connection.name_b.value)
            print(f"Removed isolated node: {connection.name_b.value}")

        self.draw()
