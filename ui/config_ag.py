import tkinter as tk
from tkinter import ttk


class ConfigAg(tk.Toplevel):
    def __init__(self, parent, model_ag):
        super().__init__(parent)
        print("sstt")
        self.canvas = parent
        self.model_ag = model_ag
        self.title("Propiedades para iniciar el Algoritmo")
        self.options = ['Número de generaciones', 'Porcentaje de eficiencia']
        self.value_completion = 1
        self.label_generations = None
        self.entry_generations = None
        self.label_efficiency = None
        self.entry_efficiency = None

        self.frame = tk.Frame(self)
        self.frame.pack(padx=50, pady=60)

        self.label_town_size = tk.Label(self.frame, text="Tamaño de la población:")
        self.label_town_size.grid(row=0, column=0, sticky="e")
        self.entry_town_size = tk.Entry(self.frame)
        self.entry_town_size.grid(row=0, column=1)
        self.entry_town_size.insert(0, str(self.model_ag.population_size))

        self.label_num_mutation = tk.Label(self.frame, text="Cantidad de mutación:")
        self.label_num_mutation.grid(row=1, column=0, sticky="e")
        self.entry_num_mutation = tk.Entry(self.frame)
        self.entry_num_mutation.grid(row=1, column=1)
        self.entry_num_mutation.insert(0, str(self.model_ag.num_mutations))

        self.label_completion_criteria = tk.Label(self.frame, text="Criterio de finalización:")
        self.label_completion_criteria.grid(row=2, column=0, sticky="e")
        self.entry_completion_criteria = ttk.Combobox(self.frame, values=self.options)
        self.entry_completion_criteria.grid(row=2, column=1)
        self.entry_completion_criteria.bind('<<ComboboxSelected>>', self.get_selected_value)

        self.button_save = tk.Button(self, text="Guardar", command=self.save_properties)
        self.button_save.pack(pady=10)

    def save_properties(self):
        self.model_ag.population_size = self.entry_town_size.get()
        self.model_ag.num_mutations = self.entry_num_mutation.get()
        if self.entry_generations is not None and self.value_completion == 1:
            self.model_ag.generations = self.entry_generations.get()
            self.model_ag.mutation_rate = float(self.model_ag.num_mutations) / float(self.model_ag.generations)
        elif self.entry_efficiency is not None and self.value_completion == 2:
            self.model_ag.efficiency = self.entry_efficiency.get()
        self.destroy()

    def get_selected_value(self, event):
        if self.entry_generations is not None:
            self.label_generations.destroy()
            self.entry_generations.destroy()
        if self.entry_efficiency is not None and self.label_efficiency is not None:
            self.label_efficiency.destroy()
            self.entry_efficiency.destroy()

        value = self.entry_completion_criteria.get()
        if value == 'Número de generaciones':
            self.value_completion = 1
            self.model_ag.efficiency = None
        else:
            self.value_completion = 2
            self.model_ag.generations = 1000000
        if self.value_completion == 1:
            self.model_ag.completion_criteria = self.value_completion
            self.label_generations = tk.Label(self.frame, text="Número de generaciones:")
            self.label_generations.grid(row=3, column=0, sticky="e")
            self.entry_generations = tk.Entry(self.frame)
            self.entry_generations.grid(row=3, column=1)
            self.entry_generations.insert(0, str(self.model_ag.generations))
        else:
            self.model_ag.completion_criteria = self.value_completion
            self.label_efficiency = tk.Label(self.frame, text="Porcentaje de eficiencia:")
            self.label_efficiency.grid(row=4, column=0, sticky="e")
            self.entry_efficiency = tk.Entry(self.frame)
            self.entry_efficiency.grid(row=4, column=1)
            self.entry_efficiency.insert(0, str(self.model_ag.efficiency))
