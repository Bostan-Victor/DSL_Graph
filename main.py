from interpreter import Interpreter
from lexer import Lexer
from parser_ import Parser
from values import Graph

def main():
    graph = Graph()
    interpreter = Interpreter()

    while True:
        try:
            text = input("graph> ")
            if text.lower() == "exit":
                break

            lexer = Lexer(text)
            tokens = lexer.generate_tokens()
            parser = Parser(tokens)
            branch = parser.parse()
            if branch:
                # Pass both the branch and the graph to the visit method
                graph = interpreter.visit([branch], graph)  # ensure the visit method updates and returns the graph
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
