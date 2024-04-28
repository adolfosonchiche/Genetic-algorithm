import tkinter as tk
from tkinter import simpledialog, messagebox

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Nodos y Conexiones")
        self.canvas = tk.Canvas(self, width=800, height=600, bg="white")
        self.canvas.pack()
        self.nodes = []
        self.new_node = None
        self.connecting_node = None

        self.menubar = tk.Menu(self)
        self.nodemenu = tk.Menu(self.menubar)
        self.nodemenu.add_command(label="Agregar Nodo", command=self.create_new_node)
        self.menubar.add_cascade(label="Nodos", menu=self.nodemenu)

        self.filemenu = tk.Menu(self.menubar)
        self.filemenu.add_command(label="Reiniciar", command=self.reset)
        self.filemenu.add_command(label="Cerrar", command=self.quit)
        self.menubar.add_cascade(label="Archivo", menu=self.filemenu)

        self.runmenu = tk.Menu(self.menubar)
        self.runmenu.add_command(label="Ejecutar", command=self.run)
        self.menubar.add_cascade(label="Ejecución", menu=self.runmenu)

        self.config(menu=self.menubar)

        self.canvas.bind("<B1-Motion>", self.move_node)
        #self.canvas.bind("<Button-3>", self.show_node_menu)
        self.canvas.bind("<Shift-Button-1>", self.start_connecting_nodes)
        self.canvas.bind("<Shift-Button-3>", self.stop_connecting_nodes)

    def create_new_node(self):
        self.new_node = Node(0, 0)
        self.canvas.bind("<Button-1>", self.place_new_node)

    def place_new_node(self, event):
        self.new_node.x, self.new_node.y = event.x, event.y
        self.nodes.append(self.new_node)
        self.new_node.draw(self.canvas)
        #self.canvas.tag_bind(self.new_node.oval, "<Button-1>", lambda e: self.new_node.edit_properties(self.canvas))
        self.canvas.tag_bind(self.new_node.oval, "<Button-3>", self.show_node_context_menu)
        self.canvas.unbind("<Button-1>")
        self.new_node = None

    def move_node(self, event):
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

    def draw_temporary_line(self, event):
        if self.connecting_node:
            self.canvas.delete("temp_line")
            line = self.canvas.create_line(self.connecting_node.x, self.connecting_node.y, event.x, event.y, width=2, arrow="last", tags="temp_line")

    def stop_connecting_nodes(self, event):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.delete("temp_line")
        for node in self.nodes:
            if (event.x - node.x) ** 2 + (event.y - node.y) ** 2 <= node.radius ** 2:
                if node != self.connecting_node:
                    self.connecting_node.connect(node, self.canvas)
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
            #canvas.create_text(self.x, self.y, text="fatima", tags="node_label")
            #self.label = canvas.create_text(self.x, self.y, text="fatima", tags="node_label")
            node.label = self.canvas.create_text(node.x, node.y, text=label, font=("Arial", 12))

    def remove_node(self, node):
        self.canvas.delete(node.oval)
        self.canvas.delete(node.label)
        for other_node in self.nodes:
            if node in other_node.connections:
                other_node.connections.remove(node)
        self.nodes.remove(node)

    def reset(self):
        self.canvas.delete("all")
        self.nodes = []

    def run(self):
        # Aquí puedes agregar la lógica para ejecutar el programa
        messagebox.showinfo("Ejecución", "Se ha ejecutado el programa.")
