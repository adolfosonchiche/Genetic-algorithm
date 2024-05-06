import tkinter as tk


class StreetProperties(tk.Toplevel):
    def __init__(self, node, parent, line, other_node, id_street, line_obj):
        super().__init__(parent.master)
        self.canvas = parent
        self.title("Propiedades de la Calle")
        self.line = line
        self.node = node
        self.other_node = other_node
        self.line_obj = line_obj
        #buscamos si ya existe valores a esta linea
        self.found_street = node.find_street_by_other_line(id_street, line)

        self.frame = tk.Frame(self)
        self.frame.pack(padx=50, pady=60)

        self.label_max_capacity = tk.Label(self.frame, text="Capacidad máxima:")
        self.label_max_capacity.grid(row=0, column=0, sticky="e")
        self.entry_max_capacity = tk.Entry(self.frame)
        self.entry_max_capacity.grid(row=0, column=1)

        self.label_min_capacity = tk.Label(self.frame, text="Capacidad minima:")
        self.label_min_capacity.grid(row=1, column=0, sticky="e")
        self.entry_min_capacity = tk.Entry(self.frame)
        self.entry_min_capacity.grid(row=1, column=1)

        #self.label_traffic_lights = tk.Label(self.frame, text="Porcentaje de semaforo:")
        #self.label_traffic_lights.grid(row=2, column=0, sticky="e")
        #self.entry_traffic_lights = tk.Entry(self.frame)
        #self.entry_traffic_lights.grid(row=2, column=1)

        if not self.found_street.its_connection and self.found_street.its_input:
            self.label_max_cars = tk.Label(self.frame, text="Carros Iniciales:")
            self.label_max_cars.grid(row=3, column=0, sticky="e")
            self.entry_max_cars = tk.Entry(self.frame)
            self.entry_max_cars.grid(row=3, column=1)
            self.entry_max_cars.insert(0, str(self.found_street.cars))

        self.button_save = tk.Button(self, text="Guardar", command=self.save_properties)
        self.button_save.pack(pady=10)

        if self.found_street:
            print(f"Se encontró el Street con other_node: {self.found_street.other_node}")
            self.entry_max_capacity.insert(0, str(self.found_street.max_capacity))
            self.entry_min_capacity.insert(0, str(self.found_street.min_capacity))
            #self.entry_traffic_lights.insert(0, str(self.found_street.traffic_lights))
            # Aquí puedes acceder a los demás atributos del objeto Street encontrado
        else:
            print("No se encontró ningún Street con ese other_node")

        #self.grab_set()

    def save_properties(self):
        if self.found_street:
            print(f"Se encontró el Street con other_node: {self.found_street.other_node}")
            self.found_street.min_capacity = self.entry_min_capacity.get()
            self.found_street.max_capacity = self.entry_max_capacity.get()
            #self.found_street.traffic_lights = self.entry_traffic_lights.get()
            if not self.found_street.its_connection and self.found_street.its_input:
                self.found_street.cars = self.entry_max_cars.get()
            self.line_obj.draw_label_line(self.found_street.min_capacity, self.found_street.max_capacity
                                          , self.found_street, self.canvas, self.line)
        self.destroy()

