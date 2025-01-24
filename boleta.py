import tkinter as tk
from tkinter import Canvas
from tkinter.font import Font
from random import randint

def crear_boleta(menu, nombre, rut, fecha, menu_descripcion, id_boleta):
    """Crear la ventana de la boleta de almuerzo con el formato proporcionado."""
    if " " in nombre:  # Reordena si hay más de una palabra
        nombre_parts = nombre.split()
        nombre = f"{nombre_parts[2]} {nombre_parts[0]}" if len(nombre_parts) >= 2 else nombre_parts[0]
    else:
        nombre = nombre  # Deja el nombre tal cual si tiene una sola palabra

    root = tk.Tk()
    root.title("Boleta de Almuerzo")
    root.geometry("300x500")
    root.configure(bg="white")

    canvas = Canvas(root, width=300, height=500, bg="white", highlightthickness=0)
    canvas.pack()

    title_font = Font(family="Helvetica", size=16, weight="bold")
    text_font = Font(family="Helvetica", size=12)
    name_font = Font(family="Helvetica", size=10)

    canvas.create_text(150, 50, text="MENU", font=title_font)
    canvas.create_text(150, 80, text=menu, font=title_font)
    canvas.create_text(150, 110, text=f"{fecha}", font=text_font)

    canvas.create_line(20, 130, 280, 130, dash=(3, 2))
    canvas.create_text(150, 160, text=menu_descripcion, font=text_font)
    canvas.create_line(20, 200, 280, 200, dash=(3, 2))

    canvas.create_text(40, 230, text="NOMBRE: ", font=text_font, anchor="w")
    canvas.create_text(250, 230, text=nombre, font=name_font, anchor="e")
    canvas.create_text(40, 260, text="RUT: ", font=text_font, anchor="w")
    canvas.create_text(230, 260, text=rut, font=text_font)

    canvas.create_text(150, 290, text="Boleta para retiro de almuerzo", font=text_font)
    canvas.create_text(150, 320, text=f"ID BOLETA: {id_boleta}", font=text_font)

    barcode_y = 360
    for i in range(20, 280, 10):
        altura = randint(20, 40)
        canvas.create_line(i, barcode_y, i, barcode_y + altura, width=2)
    root.mainloop()
