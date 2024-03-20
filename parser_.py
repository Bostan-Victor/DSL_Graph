from tokens import TokenType
from nodes import *


class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.advance()

    def raise_error(self):
        raise Exception("Invalid syntax")

    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def parse(self):
        if self.current_token is None:
            return None

        result = self.expr()

        if self.current_token is not None:
            self.raise_error()

        return result

    def expr(self):
        start_node = self.node()
        weight = NumberNode(value=0)
        l_direction = False
        r_direction = False

        while self.current_token is not None:

            if self.current_token.type == TokenType.LEFT:
                self.advance()
                l_direction = True

            self.dash()

            if self.current_token.type == TokenType.WEIGHT:
                weight = self.weight()

            self.dash()

            if self.current_token.type == TokenType.RIGHT:
                self.advance()
                r_direction = True

            end_node = self.node()

            return ConnectNode(name_a=start_node, name_b=end_node, left_dir=l_direction, right_dir=r_direction,
                               weight=weight)

    def node(self):
        token = self.current_token

        if token.type == TokenType.FINAL:
            self.advance()
            token = self.current_token
            if token.type == TokenType.NAME:
                self.advance()
                return NameNode(value=token.value, final=True)
            else:
                self.raise_error()
        elif token.type == TokenType.NAME:
            self.advance()
            return NameNode(value=token.value, final=False)

        self.raise_error()

    def weight(self):
        token = self.current_token

        if token.type == TokenType.WEIGHT:
            self.advance()
            return NumberNode(value=token.value)

        self.raise_error()

    def dash(self):
        token = self.current_token

        if token.type == TokenType.DASH:
            self.advance()
            return

        self.raise_error()