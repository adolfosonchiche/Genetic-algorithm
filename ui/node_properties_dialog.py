import tkinter as tk
from tkinter import simpledialog, messagebox


class NodePropertiesDialog(tk.Toplevel):
    def __init__(self, parent, node):
        super().__init__(parent)
        self.title("Propiedades del Nodo")
        self.node = node

        self.frame = tk.Frame(self)
        self.frame.pack(padx=10, pady=10)

        self.label_weight = tk.Label(self.frame, text="Peso:")
        self.label_weight.grid(row=0, column=0, sticky="e")
        self.entry_weight = tk.Entry(self.frame)
        self.entry_weight.grid(row=0, column=1)

        self.label_time_percentage = tk.Label(self.frame, text="Porcentaje de Tiempo:")
        self.label_time_percentage.grid(row=1, column=0, sticky="e")
        self.entry_time_percentage = tk.Entry(self.frame)
        self.entry_time_percentage.grid(row=1, column=1)

        self.label_load = tk.Label(self.frame, text="Carga:")
        self.label_load.grid(row=2, column=0, sticky="e")
        self.entry_load = tk.Entry(self.frame)
        self.entry_load.grid(row=2, column=1)

        self.button_save = tk.Button(self, text="Guardar", command=self.save_properties)
        self.button_save.pack(pady=10)

        self.entry_weight.insert(0, str(node.weight))
        self.entry_time_percentage.insert(0, str(node.time_percentage))
        self.entry_load.insert(0, str(node.load))

        self.grab_set()

    def save_properties(self):
        self.node.weight = int(self.entry_weight.get())
        self.node.time_percentage = int(self.entry_time_percentage.get())
        self.node.load = int(self.entry_load.get())
        self.destroy()
