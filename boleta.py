import tkinter as tk
from tkinter import Canvas
from tkinter.font import Font

def crear_boleta(menu, nombre, rut, dia, menu_descripcion):
    """Crear la ventana de la boleta de almuerzo con el formato proporcionado."""
    # Convertir el nombre completo a solo el primer nombre y el primer apellido
    nombre_parts = nombre.split()  # Dividir el nombre completo en partes
    if len(nombre_parts) >= 2:
        nombre = f"{nombre_parts[2]} {nombre_parts[0]}"  # Tomar el primer nombre y apellido
    else:
        nombre = nombre_parts[0]  # Si solo tiene un nombre, usarlo

    # Crear ventana principal
    root = tk.Tk()
    root.title("Boleta de Almuerzo")
    root.geometry("300x500")
    root.configure(bg="white")

    # Crear un canvas para dibujar la boleta
    canvas = Canvas(root, width=300, height=500, bg="white", highlightthickness=0)
    canvas.pack()

    # Fuente personalizada
    title_font = Font(family="Helvetica", size=16, weight="bold")
    text_font = Font(family="Helvetica", size=12)
    name_font = Font(family="Helvetica", size=10)  # Ajustamos el tamaño de la fuente para el nombre

    # Agregar textos al canvas
    canvas.create_text(150, 50, text="MENU", font=title_font)
    canvas.create_text(150, 80, text=menu, font=title_font)
    canvas.create_text(150, 110, text=f"{dia}/01/2025 - 13:36PM", font=text_font)
    
    # Líneas divisorias
    canvas.create_line(20, 130, 280, 130, dash=(3, 2))
    canvas.create_text(150, 160, text=menu_descripcion, font=text_font)
    canvas.create_line(20, 200, 280, 200, dash=(3, 2))
    
    # Información del usuario
    canvas.create_text(40, 230, text="NOMBRE: ", font=text_font, anchor="w")  # Mover a la izquierda
    canvas.create_text(250, 230, text=nombre, font=name_font, anchor="e")  # Usar font ajustado
    canvas.create_text(40, 260, text="RUT: ", font=text_font, anchor="w")  # Mover a la izquierda
    canvas.create_text(230, 260, text=rut, font=text_font, anchor="e")

    canvas.create_text(150, 290, text="Boleta para retiro de almuerzo", font=text_font)
    canvas.create_text(150, 320, text="ID BOLETA: 10009", font=text_font)

    # Simular un código de barras
    barcode_y = 360
    for i in range(20, 280, 10):
        canvas.create_line(i, barcode_y, i, barcode_y + 30, width=2)

    root.mainloop()
