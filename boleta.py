import tkinter as tk
from tkinter import Canvas
from tkinter.font import Font
from random import randint
import win32print
import win32ui
from PIL import ImageWin

def crear_boleta(menu, nombre, rut, fecha, menu_descripcion, id_boleta):
    """Crear la ventana de la boleta de almuerzo con el formato proporcionado y la opción de imprimirla."""
    if " " in nombre:  # Reordena si hay más de una palabra
        nombre_parts = nombre.split()
        nombre = f"{nombre_parts[1]} {nombre_parts[0]}" if len(nombre_parts) >= 2 else nombre_parts[0]
    else:
        nombre = nombre  # Deja el nombre tal cual si tiene una sola palabra

    # Crear la interfaz gráfica de la boleta (pantalla)
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
    canvas.create_text(270, 230, text=nombre, font=name_font, anchor="e")
    canvas.create_text(40, 260, text="RUT: ", font=text_font, anchor="w")
    canvas.create_text(230, 260, text=rut, font=text_font)

    canvas.create_text(150, 290, text="Boleta para retiro de almuerzo", font=text_font)
    canvas.create_text(150, 320, text=f"ID BOLETA: {id_boleta}", font=text_font)

    barcode_y = 360
    for i in range(20, 280, 10):
        altura = randint(20, 40)
        canvas.create_line(i, barcode_y, i, barcode_y + altura, width=2)

    # Función para imprimir la boleta
    def imprimir_boleta():
        try:
            printer_name = win32print.GetDefaultPrinter()  # Obtener impresora predeterminada
            hprinter = win32print.OpenPrinter(printer_name)  # Abrir la impresora
            printer_info = win32print.GetPrinter(hprinter, 2)  # Obtener información de la impresora

            # Crear el contexto de la impresora
            hdc = win32ui.CreateDC()
            hdc.CreatePrinterDC(printer_name)
            hdc.StartDoc("Boleta de Almuerzo")
            hdc.StartPage()

            # Dibujar el texto en la impresora
            hdc.TextOut(100, 100, f"MENU: {menu}")
            hdc.TextOut(100, 150, f"Fecha: {fecha}")
            hdc.TextOut(100, 200, f"Nombre: {nombre}")
            hdc.TextOut(100, 250, f"RUT: {rut}")
            hdc.TextOut(100, 300, f"ID BOLETA: {id_boleta}")
            hdc.TextOut(100, 350, f"Descripción: {menu_descripcion}")

            hdc.EndPage()
            hdc.EndDoc()
            hdc.DeleteDC()
        except Exception as e:
            print(f"Error al imprimir la boleta: {e}")

    # Botón para imprimir la boleta
    tk.Button(root, text="Imprimir Boleta", command=imprimir_boleta).pack(pady=20)

    root.mainloop()