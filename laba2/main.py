import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image
import threading
import csv
from fractions import Fraction

def get_image_aspect_ratio(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            # Calculate the greatest common divisor and use it for the aspect ratio
            gcd = Fraction(width, height).denominator
            aspect_ratio = f"{width // gcd}:{height // gcd}"
            return aspect_ratio
    except IOError:
        return "Unable to determine aspect ratio; file may not be an image or is corrupted."

def get_image_info(image_path, default_dpi=96):
    aspect_ratio = get_image_aspect_ratio(image_path)
    try:
        with Image.open(image_path) as img:
            dpi = img.info['dpi'][0] if 'dpi' in img.info and img.info['dpi'][0] > 0 else default_dpi
            color_depth = {
                '1': 1, 'L': 8, 'P': 8, 'RGB': 24, 'RGBA': 32, 'CMYK': 32,
                'YCbCr': 24, 'LAB': 24, 'HSV': 24, 'I': 32, 'F': 32
            }.get(img.mode, "Unknown")

            file_size = os.path.getsize(image_path)  # File size in bytes
            uncompressed_size = img.size[0] * img.size[1] * color_depth // 8
            # Adjust the precision to 5 decimal places
            compression_ratio = round(uncompressed_size / file_size, 5) if file_size else "N/A"

            info = {
                "Name": os.path.basename(image_path),
                "Aspect Ratio": aspect_ratio,
                "Size": f"{img.size[0]}x{img.size[1]} pixels",
                "DPI": f"{dpi} dpi",
                "Color Depth": color_depth if color_depth != "Unknown" else "N/A",
                "Compression": compression_ratio,
                "File Size": f"{file_size} bytes"
            }
            return info
    except IOError:
        return {"Name": os.path.basename(image_path), "Aspect Ratio": "N/A", "DPI": "N/A", "Color Depth": "N/A", "Compression": "N/A", "File Size": "N/A"}


# Функция для обновления таблицы с информацией об изображениях
def update_table_with_info(data):
    for info in data:
        tree.insert('', 'end', values=list(info.values()))

# Функция для обработки выбранной папки
def process_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        data = [get_image_info(image) for image in images if get_image_info(image)]
        update_table_with_info(data)

# Функция для обработки выбранных изображений
def process_images():
    image_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.gif *.tif *.bmp *.png *.pcx")])
    if image_paths:
        data = [get_image_info(image_path) for image_path in image_paths if get_image_info(image_path)]
        update_table_with_info(data)

# Функция для удаления выбранного элемента из таблицы
def remove_selected_item():
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)

# Функция для полного очищения таблицы
def clear_table():
    for item in tree.get_children():
        tree.delete(item)

# Функция для сохранения таблицы в файл CSV
def save_table_to_csv():
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if filename:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([tree.heading(col)['text'] for col in tree['columns']])
            for row in tree.get_children():
                writer.writerow([tree.item(row)['values'][col] for col in range(len(tree['columns']))])
        messagebox.showinfo("Save to CSV", "The table has been saved to " + filename)

# Создание основного окна
root = tk.Tk()
root.title("Image Information Viewer")

# Создание и размещение кнопок
folder_button = tk.Button(root, text="Select Folder", command=lambda: threading.Thread(target=process_folder).start())
folder_button.grid(row=0, column=0, sticky="nsew")

images_button = tk.Button(root, text="Select Images", command=lambda: threading.Thread(target=process_images).start())
images_button.grid(row=0, column=1, sticky="nsew")

remove_button = tk.Button(root, text="Remove Selected", command=remove_selected_item)
remove_button.grid(row=0, column=2, sticky="nsew")

clear_button = tk.Button(root, text="Clear Table", command=clear_table)
clear_button.grid(row=0, column=3, sticky="nsew")

save_button = tk.Button(root, text="Save to CSV", command=save_table_to_csv)
save_button.grid(row=0, column=4, sticky="nsew")

# Создание и размещение таблицы
columns = ("Name", "Resolution", "Size", "DPI", "Color Depth", "Compression")  # Add 'Resolution' to the columns
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=1, column=0, columnspan=5, sticky="nsew")

# Настройка разметки окна
for i in range(5):
    root.columnconfigure(i, weight=1)
root.rowconfigure(1, weight=1)

# Запуск главного цикла приложения
root.mainloop()
