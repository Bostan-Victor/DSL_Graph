from lexer import Lexer
from parser_ import Parser
from interpreter import Interpreter

while True:
    try:
        text = input("graph> ")
        lexer = Lexer(text)
        tokens = lexer.generate_tokens()
        parser = Parser(tokens)
        tree = parser.parse()
        print(tree)
        if not tree:
            continue
        interpreter = Interpreter()
        graph = interpreter.visit(tree)
        graph.draw()
    except Exception as e:
        print(e)
