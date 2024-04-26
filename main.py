from lexer import Lexer
from parser_ import Parser
from interpreter import Interpreter

tree = []
text = ""

while True:
    try:
        while True:
            text = input("graph> ")
            if text == "draw":
                break

            lexer = Lexer(text)
            tokens = lexer.generate_tokens()
            parser = Parser(tokens)
            branch = parser.parse()
            print(branch)
            if branch:
                tree.append(branch)
        print(tree)
        interpreter = Interpreter()
        graph, tree = interpreter.visit(tree)
        graph.draw()
    except Exception as e:
        print(e)



