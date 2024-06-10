import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from interpreter import Interpreter
from lexer import Lexer
from parser_ import Parser
from values import Graph

class GraphEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Editor")

        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=1)

        self.text_area = tk.Text(self.frame, wrap=tk.WORD, height=20, width=40)
        self.text_area.grid(row=0, column=0, padx=10, pady=10, rowspan=4)

        self.update_button = tk.Button(self.frame, text="Update Graph", command=self.update_graph)
        self.update_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.upload_button = tk.Button(self.frame, text="Upload File", command=self.upload_file)
        self.upload_button.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.graph = Graph(self.fig)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=4, padx=10, pady=10)
        self.canvas.draw()

        self.interpreter = Interpreter()
        self.previous_connections = set()

    def update_graph(self):
        text = self.text_area.get("1.0", tk.END).strip()
        lines = text.split('\n')

        current_connections = set()

        for line in lines:
            try:
                lexer = Lexer(line)
                tokens = lexer.generate_tokens()
                parser = Parser(tokens)
                branch = parser.parse()
                if branch:
                    connection = self.interpreter.create_connection(branch)
                    current_connections.add(connection)
            except Exception as e:
                print(f"Error: {e}")

        # Remove connections that are no longer present
        for connection in self.previous_connections - current_connections:
            self.graph.remove_connection(connection)

        # Add new connections
        for connection in current_connections - self.previous_connections:
            self.graph.add_connection(connection)

        self.previous_connections = current_connections
        self.canvas.draw()

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                code = file.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, code)
            self.update_graph()

def main():
    root = tk.Tk()
    app = GraphEditorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
