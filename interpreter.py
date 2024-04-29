from values import Number, Name, Connection, Graph


class Interpreter:
    def __init__(self):
        pass

    def visit(self, tree, graph):
        # Assuming this method updates the graph based on the parsed tree
        tree = self.clear_tree(tree)
        for node in tree:
            method_name = f'visit_{type(node).__name__}'
            method = getattr(self, method_name, None)
            if method:
                method(node, graph)  # Pass the graph to the specific visit method

        return graph

    def visit_ConnectNode(self, node, graph):
        # Create instances of Name and Number from the node information
        node_a = Name(node.name_a.value, node.name_a.final, node.name_a.start)
        node_b = Name(node.name_b.value, node.name_b.final, node.name_b.start)
        weight = Number(node.weight.value)
        # Create a Connection object with directional attributes
        connection = Connection(name_a=node_a, name_b=node_b, weight=weight, destroy=node.destroy,
                                left_dir=node.left_dir, right_dir=node.right_dir)
        graph.add_connection(connection)


    @staticmethod
    def clear_tree(tree):
        seen = set()
        new_tree = []

        for node in reversed(tree):
            key = tuple(sorted((node.name_a.value, node.name_b.value)))

            if key not in seen:
                seen.add(key)
                new_tree.append(node)

        new_tree = [node for node in new_tree if not getattr(node, 'destroy', False)]

        return new_tree
