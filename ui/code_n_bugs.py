import tkinter as tk
from os import fork
from tkinter import simpledialog, messagebox
from back.node import Node
import pickle
import json
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
        self.file_menu.add_command(label="Guardar como JSON", command=self.save_canvas_to_json)
        self.file_menu.add_command(label="Cargar desde JSON", command=self.load_canvas_from_json)
        self.file_menu.add_command(label="Cerrar", command=self.quit)
        self.menubar.add_cascade(label="Archivo", menu=self.file_menu)

        self.run_menu = tk.Menu(self.menubar)
        self.run_menu.add_command(label="Ejecutar", command=self.run)
        self.menubar.add_cascade(label="Ejecución", menu=self.run_menu)

        self.config(menu=self.menubar)

        self.canvas.bind("<B1-Motion>", self.move_node)
        self.canvas.bind("<Shift-Button-1>", self.start_connecting_nodes)
        self.canvas.bind("<Shift-Button-3>", self.stop_connecting_nodes)

    def save_canvas_to_json(self):
        file_name = tk.filedialog.asksaveasfilename(defaultextension=".json")
        if file_name:
            canvas_data = self.canvas.find_all()
            canvas_json = []
            for item in canvas_data:
                item_type = self.canvas.type(item)
                item_coords = self.canvas.coords(item)
                item_json = {
                    "type": item_type,
                    "coords": list(item_coords)
                }
                canvas_json.append(item_json)

            with open(file_name, "w") as file:
                json.dump(canvas_json, file)

    def load_canvas_from_json(self):
        file_name = tk.filedialog.askopenfilename(defaultextension=".json")
        if file_name:
            self.canvas.delete("all")
            with open(file_name, "r") as file:
                canvas_json = json.load(file)
                for item_json in canvas_json:
                    item_type = item_json["type"]
                    item_coords = item_json["coords"]
                    if item_type == "line":
                        self.canvas.create_line(*item_coords)
                    elif item_type == "oval":
                        self.canvas.create_oval(*item_coords)

    def save_canvas(self):
        file_name = tk.filedialog.asksaveasfilename(defaultextension=".pkl")
        if file_name:
            data = {
                "nodes": self.nodes,
                "canvas_data": self.canvas.find_all()
            }
            with open(file_name, "wb") as file:
                pickle.dump(self.nodes, file)

    def load_canvas(self):
        file_name = tk.filedialog.askopenfilename(defaultextension=".pkl")
        if file_name:
            with open(file_name, "rb") as file:
                data = pickle.load(file)
                self.nodes = data
                self.canvas.delete("all")
                print(self.nodes)
                for node in self.nodes:
                    print(isinstance(node, Node))
                    node.oval = self.canvas.create_oval(node.x - node.radius, node.y - node.radius,
                                                        node.x + node.radius, node.y + node.radius,
                                                        fill="white", outline="black", tags="node")
                    node.label = self.canvas.create_text(node.x, node.y, text="nodo " + str(node.id), tags="node_label")
                    self.canvas.tag_bind(node.oval, "<Button-3>", self.show_node_context_menu)
                    self.canvas.bind("<B1-Motion>", self.move_node)
                for node in self.nodes:
                    self.filter_connection(node, node.connections)

    def filter_connection(self, node, connections):
        """Filtra las calles de la lista 'connections' según las condiciones."""
        for street in connections:
            #node.connect(street.other_node, self.canvas)
            if not street.its_input and street.its_output and street.its_connection:
                print(street.line)
                line = self.canvas.create_line(street.x1, street.y1, street.x2, street.y2, width=4,
                                               arrow="last", tags=("connection_line",))
                street.line = line
                self.canvas.tag_bind(line, "<Button-1>", lambda e: node.remove_line(line, self.canvas))
                self.canvas.tag_bind(line, "<Button-3>",
                                     lambda e: node.show_connection_properties(node, self.canvas, line,
                                                                               street.other_node))

    def create_new_node(self):
        self.new_node = Node(0, 0, self.countNode)
        self.canvas.bind("<Button-1>", self.place_new_node)
        self.countNode = self.countNode + 1

    def place_new_node(self, event):
        if self.new_node is not None:
            self.new_node.x, self.new_node.y = event.x, event.y
            self.nodes.append(self.new_node)
            self.new_node.draw(self.canvas)
            self.canvas.tag_bind(self.new_node.oval, "<Button-3>", self.show_node_context_menu)
            self.canvas.bind("<B1-Motion>", self.move_node)
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
            #self.connecting_node.connect_out(self.canvas, event.x, event.y)

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
                    self.connecting_node.connect(node, self.canvas)
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
