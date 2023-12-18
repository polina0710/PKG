import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.colorchooser import askcolor

# Assuming ColorController is implemented in a separate module
# from colorcontroller import ColorController

class ColorPanel:
    def __init__(self, format: str, root: tk.Tk, controller) -> None:
        self.format = format
        self.panels = []
        self.strings = []
        self.scales = []
        self.controller = controller
        self.updating = False  # Flag to prevent update loops

        label = ttk.Label(root, text=format)
        label.pack(anchor=tk.N)

        n = 4 if format == 'CMYK' else 3

        # Define the ranges for each color space
        scale_ranges = {
            'RGB': [(0, 255), (0, 255), (0, 255)],
            'CMYK': [(0, 100), (0, 100), (0, 100), (0, 100)],
            'HLS': [(0, 100), (0, 100), (0, 100)]
        }

        # Initialize StringVars, Entries and Scales for each component
        for i in range(n):
            string_var = tk.StringVar()
            self.strings.append(string_var)
            string_var.trace("w", lambda name, index, mode, i=i: self.entry_to_slider(i))

            entry = ttk.Entry(root, textvariable=string_var)
            self.panels.append(entry)
            entry.pack(anchor=tk.N, padx=1, pady=1)

            scale_from, scale_to = scale_ranges[self.format][i]
            scale = ttk.Scale(root, orient='horizontal', length=200, from_=scale_from, to_=scale_to,
                              command=lambda value, i=i: self.slider_to_entry(i))
            self.scales.append(scale)
            
            scale.pack(anchor=tk.N, padx=1, pady=1)

            default_value = 0
            scale.set(default_value)
            string_var.set(str(default_value))

    def changecolor(self, color: list, global_change: bool = False):
        if not self.updating or global_change:
            self.updating = True
            for i, value in enumerate(color[:len(self.strings)]):
                rounded_value = round(value)
                self.strings[i].set(str(rounded_value))
                self.scales[i].set(rounded_value)
            self.updating = False

    def entry_to_slider(self, index: int):
        if not self.updating:
            try:
                value = round(float(self.strings[index].get()))
                self.scales[index].set(value)
            except ValueError:
                if self.strings[index].get() != "":
                    messagebox.showerror(title='Error', message='Please enter a valid numeric value.')
                self.strings[index].set("")

    def slider_to_entry(self, index: int):
        if not self.updating:
            self.updating = True
            value = round(self.scales[index].get())
            self.strings[index].set(str(value))
            if self.controller:
                self.controller.changeglobalcolor(self.format, self.getcolorvalues())
            self.updating = False

    def getcolorvalues(self) -> list:
        color_values = []
        for string_var in self.strings:
            try:
                color_value = round(float(string_var.get()))
                color_values.append(color_value)
            except ValueError:
                color_values.append(0)
        return color_values
