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
        self.mode = "default"

    def set_mode(self, mode):
        self.mode = mode

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
        if len(self.G) == 0:
            self.fig.canvas.draw()
            return

        if self.mode == "default":
            pos = nx.kamada_kawai_layout(self.G)  # Using a layout that better handles overlaps
        elif self.mode == "bipartite":
            top_nodes, bottom_nodes = self.get_bipartite_nodes()
            pos = nx.bipartite_layout(self.G, top_nodes)
        elif self.mode == "tree":
            if not nx.is_tree(self.G):
                print("Cannot use tree layout on a graph that is not a tree. Falling back to default layout.")
                pos = nx.kamada_kawai_layout(self.G)
            else:
                pos = self.hierarchy_pos(self.G)

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

    def get_bipartite_nodes(self):
        top_nodes = {n for n in self.G if n.islower()}
        bottom_nodes = {n for n in self.G if n.isupper()}
        return top_nodes, bottom_nodes

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

    def hierarchy_pos(self, G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
        if not nx.is_tree(G):
            raise TypeError('Cannot use hierarchy_pos on a graph that is not a tree')

        if root is None:
            if isinstance(G, nx.DiGraph):
                root = next(iter(nx.topological_sort(G)))  # allows for ordering of DAGs
            else:
                root = next(iter(G.nodes))  # otherwise choose arbitrary node

        def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=[]):
            if pos is None:
                pos = {root: (xcenter, vert_loc)}
            else:
                pos[root] = (xcenter, vert_loc)
            children = list(G.neighbors(root))
            if not isinstance(G, nx.DiGraph) and parent is not None:
                children.remove(parent)
            if len(children) != 0:
                dx = width / len(children)
                nextx = xcenter - width / 2 - dx / 2
                for child in children:
                    nextx += dx
                    pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                         pos=pos, parent=root, parsed=parsed)
            return pos

        return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
