import tkinter as tk
from tkinter import simpledialog, messagebox

from back.street import Street


class StreetProperties(tk.Toplevel):
    def __init__(self, node, parent, line, other_node):
        super().__init__(parent.master)
        self.canvas = parent
        self.title("Propiedades de la Calle")
        self.line = line
        self.node = node
        self.other_node = other_node
        #buscamos si ya existe valores a esta linea
        self.found_street = node.find_street_by_other_node(other_node)

        self.frame = tk.Frame(self)
        self.frame.pack(padx=50, pady=50)

        self.label_max_capacity = tk.Label(self.frame, text="Capacidad máxima:")
        self.label_max_capacity.grid(row=0, column=0, sticky="e")
        self.entry_max_capacity = tk.Entry(self.frame)
        self.entry_max_capacity.grid(row=0, column=1)

        self.label_min_capacity = tk.Label(self.frame, text="Capacidad minima:")
        self.label_min_capacity.grid(row=1, column=0, sticky="e")
        self.entry_min_capacity = tk.Entry(self.frame)
        self.entry_min_capacity.grid(row=1, column=1)

        self.label_traffic_lights = tk.Label(self.frame, text="Porcentaje de semaforo:")
        self.label_traffic_lights.grid(row=2, column=0, sticky="e")
        self.entry_traffic_lights = tk.Entry(self.frame)
        self.entry_traffic_lights.grid(row=2, column=1)

        self.button_save = tk.Button(self, text="Guardar", command=self.save_properties)
        self.button_save.pack(pady=10)

        if self.found_street:
            print(f"Se encontró el Street con other_node: {self.found_street.other_node}")
            self.entry_max_capacity.insert(0, str(self.found_street.max_capacity))
            self.entry_min_capacity.insert(0, str(self.found_street.min_capacity))
            self.entry_traffic_lights.insert(0, str(self.found_street.traffic_lights))
            # Aquí puedes acceder a los demás atributos del objeto Street encontrado
        else:
            print("No se encontró ningún Street con ese other_node")

        #self.grab_set()

    def save_properties(self):
        if self.found_street:
            print(f"Se encontró el Street con other_node: {self.found_street.other_node}")
            self.found_street.min_capacity = self.entry_min_capacity.get()
            self.found_street.max_capacity = self.entry_traffic_lights.get()
            self.found_street.traffic_lights = self.entry_max_capacity.get()
            self.draw_label(self.found_street.min_capacity, self.found_street.max_capacity)
        else:
            min_capacity = self.entry_min_capacity.get()
            max_capacity = self.entry_traffic_lights.get()
            traffic_lights = self.entry_max_capacity.get()
            print("No se encontró ningún Street con ese other_node")
            self.found_street = Street(self.other_node, False, False, True,
                                       min_capacity, max_capacity, traffic_lights, self.line
                                       )
            self.node.connections.append(self.found_street)
            self.draw_label(min_capacity, max_capacity)
        self.destroy()

    def draw_label(self, min_capacity, max_capacity):
        x1, y1, x2, y2 = self.canvas.coords(self.line)
        x_center = (x1 + x2) / 2
        y_center = (y1 + y2) / 2
        label_text = f"Capacidad mínima: {min_capacity}\n\nCapacidad máxima: {max_capacity}"

        if self.found_street.label_text:
            self.canvas.delete(self.found_street.label_text)
        self.canvas.label = self.canvas.create_text(x_center, y_center, text=label_text, font=("Arial", 10))
        self.found_street.label_text = self.canvas.label
