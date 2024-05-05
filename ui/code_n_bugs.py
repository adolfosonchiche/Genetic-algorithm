import tkinter as tk
from tkinter import simpledialog, messagebox
from back.file.file_ag import FileAg
from back.file.load_model import LoadModel
from back.node import Node
from tkinter import filedialog


class CodeNBugs(tk.Tk):
    def __init__(self):
        super().__init__()
        self.countNode = 1
        self.title("Code 'n Bugs")
        self.canvas = tk.Canvas(self, width=800, height=600, bg="white")
        self.canvas.pack()
        self.nodes = []
        self.new_node = None
        self.connecting_node = None
        self.connection_input = False
        self.event_input = None

        self.menubar = tk.Menu(self)
        self.node_menu = tk.Menu(self.menubar)
        self.node_menu.add_command(label="Agregar Nodo", command=self.create_new_node)
        self.menubar.add_cascade(label="Nodos", menu=self.node_menu)

        self.file_menu = tk.Menu(self.menubar)
        self.file_menu.add_command(label="Reiniciar", command=self.reset)
        self.file_menu.add_command(label="Guardar", command=self.save_canvas)
        self.file_menu.add_command(label="Cargar", command=self.load_canvas)
        self.file_menu.add_command(label="Cerrar", command=self.quit)
        self.menubar.add_cascade(label="Archivo", menu=self.file_menu)

        self.run_menu = tk.Menu(self.menubar)
        self.run_menu.add_command(label="Ejecutar", command=self.run)
        self.menubar.add_cascade(label="Ejecución", menu=self.run_menu)

        self.config(menu=self.menubar)

        self.canvas.bind("<B1-Motion>", self.move_node)
        self.canvas.bind("<Shift-Button-1>", self.start_connecting_nodes)
        self.canvas.bind("<Shift-Button-3>", self.stop_connecting_nodes)

    def save_canvas(self):
        file_ag = FileAg()
        file_ag.save_model(self.nodes, tk.filedialog)

    def load_canvas(self):
        file_ag = FileAg()
        self.nodes = file_ag.load_model(tk.filedialog)
        if self.nodes:
            self.canvas.delete("all")
            load_model = LoadModel()
            load_model.load(self.nodes, self.canvas, self)
            print(self.nodes)
        else:
            messagebox.showerror("Error en carga de datos", "No se ha podido cargar los datos, intente más tarde.")

    def create_new_node(self):
        self.new_node = Node(0, 0, self.countNode)
        self.canvas.bind("<Button-1>", self.place_new_node)
        self.countNode = self.countNode + 1

    def place_new_node(self, event):
        if self.new_node is not None:
            self.new_node.x, self.new_node.y = event.x, event.y
            self.nodes.append(self.new_node)
            self.new_node.draw(self.canvas, self)
        self.new_node = None

    def move_node(self, event):
        print("mover nodo")
        node_moved = None
        for node in self.nodes:
            if (event.x - node.x) ** 2 + (event.y - node.y) ** 2 <= node.radius ** 2:
                node_moved = node
                break

        if node_moved:
            self.canvas.addtag_overlapping("to_move", node_moved.x - node_moved.radius,
                                           node_moved.y - node_moved.radius,
                                           node_moved.x + node_moved.radius,
                                           node_moved.y + node_moved.radius)
            self.canvas.move("to_move", event.x - node_moved.x, event.y - node_moved.y)
            node_moved.x, node_moved.y = event.x, event.y
            self.canvas.coords(node_moved.label, event.x, event.y)
            self.canvas.dtag("to_move")

    def start_connecting_nodes(self, event):
        for node in self.nodes:
            if (event.x - node.x) ** 2 + (event.y - node.y) ** 2 <= node.radius ** 2:
                self.connecting_node = node
                self.canvas.bind("<B1-Motion>", self.draw_temporary_line)
                break
        if not self.connecting_node:
            self.connection_input = True
            self.event_input = event
            self.canvas.bind("<B1-Motion>", self.draw_temporary_line)

    def draw_temporary_line(self, event):
        if self.connecting_node:
            self.canvas.delete("temp_line")
            line = self.canvas.create_line(self.connecting_node.x, self.connecting_node.y, event.x, event.y, width=2,
                                           arrow="last", tags="temp_line")

    def stop_connecting_nodes(self, event):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.delete("temp_line")
        connection = False
        for node in self.nodes:
            if (event.x - node.x) ** 2 + (event.y - node.y) ** 2 <= node.radius ** 2:
                if self.connection_input:
                    node.connect_in(self.canvas, self.event_input.x, self.event_input.y)
                    self.connection_input = False
                    connection = True
                    self.event_input = None
                elif node != self.connecting_node:
                    self.connecting_node.connect_node(node, self.canvas)
                    connection = True
        if not connection:
            self.connecting_node.connect_out(self.canvas, event.x, event.y)
        self.connecting_node = None

    def show_node_menu(self, event):
        for node in self.nodes:
            if (event.x - node.x) ** 2 + (event.y - node.y) ** 2 <= node.radius ** 2:
                node.edit_properties(self.canvas)

    def show_node_context_menu(self, event):
        node = self.canvas.find_closest(event.x, event.y)[0]
        node_obj = next((n for n in self.nodes if n.oval == node), None)
        if node_obj:
            context_menu = tk.Menu(self, tearoff=0)
            context_menu.add_command(label="Agregar Etiqueta", command=lambda: self.add_node_label(node_obj))
            context_menu.add_separator()
            context_menu.add_command(label="Editar Propiedades", command=lambda: node_obj.edit_properties(self.canvas))
            context_menu.add_separator()
            context_menu.add_command(label="Eliminar Nodo", command=lambda: self.remove_node(node_obj))
            context_menu.tk_popup(event.x_root, event.y_root)

    def add_node_label(self, node):
        label = simpledialog.askstring("Agregar Etiqueta", "Ingrese una etiqueta para el nodo:")
        print(label)
        if label:
            self.canvas.delete(node.label)
            node.label = self.canvas.create_text(node.x, node.y, text=label, font=("Arial", 12))

    def remove_node(self, node):
        node.remove_streets_from_the_node(self.canvas)
        self.canvas.delete(node.oval)
        self.canvas.delete(node.label)
        for other_node in self.nodes:
            if node in other_node.connections:
                other_node.connections.remove(node)
        self.nodes.remove(node)

    def reset(self):
        self.canvas.delete("all")
        self.nodes = []
        self.countNode = 1

    def run(self):
        # Aquí puedes agregar la lógica para ejecutar el programa
        messagebox.showinfo("Ejecución", "Se ha ejecutado el programa.")
