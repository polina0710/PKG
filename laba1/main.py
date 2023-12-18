import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
from colorcontroller import ColorController


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('300x700')
    root.resizable(False, False)

    color_controller = ColorController(root)

    def change_color():
        colors = askcolor(title="Tkinter Color Chooser")
        if colors[1]:
            hex_color = colors[1]
            # Convert hex color to an RGB tuple.
            rgb_color = [int(hex_color[i:i+2], 16) for i in (1, 3, 5)]
            # Inform the controller that the change came from the 'Button', which we can consider as an RGB source.
            color_controller.changeglobalcolor('BUTTON', rgb_color)
            root.configure(bg=hex_color)

    button = ttk.Button(root, text='Select a Color', command=change_color)
    button.pack(expand=True)
    color_controller.changeglobalcolor('BUTTON', [0,0,0])
    root.mainloop()
