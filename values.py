import os
from dataclasses import dataclass
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

    def draw(self):
        dot = Digraph()

        script_dir = os.path.dirname(os.path.realpath(__file__))
        output_path = os.path.join(script_dir, 'connection_graph')

        if self.name_a.final:
            dot.node(self.name_a.value, label=self.name_a.value, shape='doublecircle')
        else:
            dot.node(self.name_a.value, label=self.name_a.value, shape='circle')

        if self.name_b.final:
            dot.node(self.name_b.value, label=self.name_b.value, shape='doublecircle')
        else:
            dot.node(self.name_b.value, label=self.name_b.value, shape='circle')

        if self.left_dir:
            if self.weight.value != 0:
                dot.edge(self.name_a.value, self.name_b.value, label=str(self.weight.value))
            else:
                dot.edge(self.name_a.value, self.name_b.value)
        if self.right_dir:
            if self.weight.value != 0:
                dot.edge(self.name_b.value, self.name_a.value, label=str(self.weight.value))
            else:
                dot.edge(self.name_b.value, self.name_a.value)
        if not (self.right_dir and self.left_dir):
            if self.weight.value != 0:
                dot.edge(self.name_a.value, self.name_b.value, label=str(self.weight.value), dir='none')
            else:
                dot.edge(self.name_a.value, self.name_b.value, dir='none')

        dot.render(output_path, format='png', cleanup=True, view=True)

    def __repr__(self):
        return f"ConnectNode({self.name_a} {'<-' if self.left_dir else '-'} {self.weight} " \
               f"{'->' if self.right_dir else '-'} {self.name_b})"
