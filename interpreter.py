from values import Name, Number, Connection

class Interpreter:
    def __init__(self):
        pass

    def visit(self, tree, graph):
        # This method updates the graph based on the parsed tree
        tree = self.clear_tree(tree)  # Clear redundant or conflicting commands
        for node in tree:
            if node.destroy:
                graph.remove_connection(self.create_connection(node))
            else:
                graph.add_connection(self.create_connection(node))
        return graph

    def create_connection(self, node):
        # Helper method to create a Connection object from a node
        node_a = Name(node.name_a.value, node.name_a.final, node.name_a.start)
        node_b = Name(node.name_b.value, node.name_b.final, node.name_b.start)
        weight = Number(node.weight.value)
        return Connection(
            name_a=node_a, name_b=node_b, weight=weight, destroy=node.destroy,
            left_dir=node.left_dir, right_dir=node.right_dir
        )

    def visit_ConnectNode(self, node, graph):
        # This is now handled in visit by calling add_connection or remove_connection directly
        pass

    @staticmethod
    def clear_tree(tree):
        # Clears redundant or conflicting commands from the tree, ensuring each connection is unique
        seen = set()
        new_tree = []
        for node in reversed(tree):
            key = tuple(sorted((node.name_a.value, node.name_b.value)))
            if key not in seen:
                seen.add(key)
                new_tree.append(node)
        new_tree = [node for node in new_tree if not getattr(node, 'destroy', False)]
        return new_tree
