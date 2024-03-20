from nodes import ConnectNode
from values import Number, Name, Connection


class Interpreter:
    def __init__(self):
        pass

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node)

    @staticmethod
    def visit_ConnectNode(node):
        node_a = Name(node.name_a.value, node.name_a.final)
        node_b = Name(node.name_b.value, node.name_b.final)
        weight = Number(node.weight.value)
        return Connection(name_a=node_a, name_b=node_b, weight=weight, left_dir=node.left_dir, right_dir=node.right_dir)
