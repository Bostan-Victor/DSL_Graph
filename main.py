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
                # Check if it's a destruction command
                if branch.destroy:
                    graph.remove_connection(interpreter.create_connection(branch))
                else:
                    graph.add_connection(interpreter.create_connection(branch))
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

