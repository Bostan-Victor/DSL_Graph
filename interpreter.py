from nodes import ConnectNode
from values import Number, Name, Connection, Graph


class Interpreter:
    def __init__(self):
        pass

    def visit(self, tree):
        graph = Graph()
        tree = self.clear_tree(tree)
        for node in tree:
            method_name = f'visit_{type(node).__name__}'
            method = getattr(self, method_name)
            graph.add_connection(method(node))
        return graph, tree

    @staticmethod
    def visit_ConnectNode(node):
        node_a = Name(node.name_a.value, node.name_a.final)
        node_b = Name(node.name_b.value, node.name_b.final)
        weight = Number(node.weight.value)
        return Connection(name_a=node_a, name_b=node_b, weight=weight, left_dir=node.left_dir, right_dir=node.right_dir)

    @staticmethod
    def clear_tree(tree):
        seen = set()
        new_tree = []

        for node in reversed(tree):
            key = tuple(sorted((node.name_a.value, node.name_b.value)))

            if key not in seen:
                seen.add(key)
                new_tree.append(node)
        return new_tree
