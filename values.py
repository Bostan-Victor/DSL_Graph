import os
from dataclasses import dataclass
from typing import List

from graphviz import Digraph


@dataclass
class Number:
    value: float

    def __repr__(self):
        return f"{self.value}"


@dataclass
class Name:
    value: str
    final: bool

    def __repr__(self):
        final_status = "final" if self.final else "not final"
        return f"NameNode(value='{self.value}', status='{final_status}')"


@dataclass
class Connection:
    name_a: Name
    name_b: Name
    left_dir: bool
    right_dir: bool
    weight: Number

    def draw(self, dot):

        self.isFinal(self.name_a, dot)

        self.isFinal(self.name_b, dot)

        if self.right_dir:
            if self.weight.value != 0:
                dot.edge(self.name_a.value, self.name_b.value, label=str(self.weight.value))
            else:
                dot.edge(self.name_a.value, self.name_b.value)
        if self.left_dir:
            if self.weight.value != 0:
                dot.edge(self.name_b.value, self.name_a.value, label=str(self.weight.value))
            else:
                dot.edge(self.name_b.value, self.name_a.value)
        if not (self.right_dir or self.left_dir):
            if self.weight.value != 0:
                dot.edge(self.name_a.value, self.name_b.value, label=str(self.weight.value), dir='none')
            else:
                dot.edge(self.name_a.value, self.name_b.value, dir='none')

    def __repr__(self):
        return f"ConnectNode({self.name_a} {'<-' if self.left_dir else '-'} {self.weight} " \
               f"{'->' if self.right_dir else '-'} {self.name_b})"

    @staticmethod
    def isFinal(node, dot):
        if node.final:
            dot.node(node.value, label=node.value, shape='doublecircle')
        else:
            dot.node(node.value, label=node.value, shape='circle')


class Graph:
    def __init__(self):
        self.connections: List[Connection] = []
        self.dot = Digraph()

    def add_connection(self, connection: Connection):
        self.connections.append(connection)

    def draw(self):
        for connection in self.connections:
            connection.draw(self.dot)

        script_dir = os.path.dirname(os.path.realpath(__file__))
        output_path = os.path.join(script_dir, 'connection_graph')

        self.dot.render(output_path, format='png', cleanup=True, view=True)
