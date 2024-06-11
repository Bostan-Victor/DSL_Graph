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
        self.root.title("GraphExpress")

        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=1)

        # Configure grid to allow resizing
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)

        self.default_mode_button = tk.Button(self.frame, text="Default Mode", command=self.set_default_mode, width=15)
        self.default_mode_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.upload_button = tk.Button(self.frame, text="Upload File", command=self.upload_file, width=15)
        self.upload_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.download_button = tk.Button(self.frame, text="Save Graph", command=self.download_graph, width=15)
        self.download_button.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.bipartite_mode_button = tk.Button(self.frame, text="Bipartite Mode", command=self.set_bipartite_mode, width=15)
        self.bipartite_mode_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.tree_mode_button = tk.Button(self.frame, text="Tree Mode", command=self.set_tree_mode, width=15)
        self.tree_mode_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

        self.text_area = tk.Text(self.frame, wrap=tk.WORD, height=20, width=40)
        self.text_area.grid(row=2, column=0, padx=10, pady=10, rowspan=4, columnspan=2, sticky="nsew")
        self.text_area.bind('<<Modified>>', self.on_text_change)

        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.graph = Graph(self.fig)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=2, column=3, rowspan=4, padx=10, pady=10, sticky="nsew")
        self.canvas.draw()

        self.interpreter = Interpreter()
        self.previous_connections = set()
        self.set_default_mode()

    def set_default_mode(self):
        self.graph.set_mode("default")
        self.update_graph()
        self.default_mode_button.config(relief=tk.SUNKEN, bg='lightblue')
        self.bipartite_mode_button.config(relief=tk.RAISED, bg='SystemButtonFace')
        self.tree_mode_button.config(relief=tk.RAISED, bg='SystemButtonFace')

    def set_bipartite_mode(self):
        self.graph.set_mode("bipartite")
        self.update_graph()
        self.bipartite_mode_button.config(relief=tk.SUNKEN, bg='lightblue')
        self.default_mode_button.config(relief=tk.RAISED, bg='SystemButtonFace')
        self.tree_mode_button.config(relief=tk.RAISED, bg='SystemButtonFace')

    def set_tree_mode(self):
        self.graph.set_mode("tree")
        self.update_graph()
        self.tree_mode_button.config(relief=tk.SUNKEN, bg='lightblue')
        self.default_mode_button.config(relief=tk.RAISED, bg='SystemButtonFace')
        self.bipartite_mode_button.config(relief=tk.RAISED, bg='SystemButtonFace')

    def on_text_change(self, event):
        self.text_area.edit_modified(0)  # Reset the modified flag
        self.update_graph()

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

    def download_graph(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if file_path:
            self.fig.savefig(file_path)

def main():
    root = tk.Tk()
    root.iconbitmap('icon.ico')  # Set the path to your icon file here
    app = GraphEditorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
