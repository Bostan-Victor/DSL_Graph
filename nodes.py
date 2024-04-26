from dataclasses import dataclass


@dataclass
class NumberNode:
    value: float

    def __repr__(self):
        return f"{self.value}"


@dataclass
class NameNode:
    value: str
    final: bool
    start: bool

    def __repr__(self):
        final_status = "final" if self.final else "not final"
        start_status = "start" if self.start else "not start"
        return f"NameNode(value='{self.value}', status='{final_status, start_status}')"


@dataclass
class ConnectNode:
    name_a: NameNode
    name_b: NameNode
    left_dir: bool
    right_dir: bool
    weight: NumberNode
    destroy: bool

    def __repr__(self):
        return f"ConnectNode({self.name_a} {'<-' if self.left_dir else '-'} {self.weight} " \
               f"{'->' if self.right_dir else '-'} {self.name_b}) {'status:'} {'destroyed' if self.destroy else 'alive'} "
