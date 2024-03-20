from tokens import Token, TokenType

WHITESPACE = ' \n\t'
DIGITS = '0123456789'
ALPHA = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Lexer:
    def __init__(self, text):
        self.text = iter(text)
        self.advance()

    def advance(self):
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def generate_tokens(self):
        while self.current_char is not None:
            if self.current_char in WHITESPACE:
                self.advance()
            elif self.current_char == '-':
                self.advance()
                yield Token(TokenType.DASH)
            elif self.current_char in ALPHA:
                yield self.generate_name()
            elif self.current_char == '<':
                self.advance()
                yield Token(TokenType.LEFT)
            elif self.current_char == '>':
                self.advance()
                yield Token(TokenType.RIGHT)
            elif self.current_char == '.' or self.current_char in DIGITS:
                yield self.generate_number()
            elif self.current_char == '*':
                self.advance()
                yield Token(TokenType.FINAL)
            else:
                raise Exception(f"Illegal character '{self.current_char}'")

    def generate_number(self):
        decimal_point_count = 0
        number_str = self.current_char
        self.advance()

        while self.current_char is not None and (self.current_char == '.' or self.current_char in DIGITS):
            if self.current_char == '.':
                decimal_point_count += 1
                if decimal_point_count > 1:
                    break

            number_str += self.current_char
            self.advance()

        if number_str.startswith('.'):
            number_str = '0' + number_str
        if number_str.endswith('.'):
            number_str += '0'

        return Token(TokenType.WEIGHT, float(number_str))

    def generate_name(self):
        name_str = self.current_char
        self.advance()

        while self.current_char is not None and self.current_char in ALPHA:
            name_str += self.current_char
            self.advance()

        return Token(TokenType.NAME, str(name_str))
