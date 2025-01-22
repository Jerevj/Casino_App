'''
import tkinter as tk

def mostrar_vista_almuerzo():
    ventana = tk.Tk()
    ventana.title("Ingreso al Casino")

    tk.Label(ventana, text="Ingrese su clave", font=("Arial", 16)).grid(pady=10)
    # Aquí puedes agregar un panel numérico y lógica para generar boletas.

    tk.Button(ventana, text="Volver", font=("Arial", 12), command=ventana.destroy).grid(pady=10)
    ventana.mainloop()
'''
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from utils import obtener_sheet, obtener_menu_sheet
from boleta import crear_boleta  # Función para generar la boleta

# Variable global para el campo activo
campo_activo = None

def set_campo_activo(campo):
    """Establecer el campo activo al que tiene el foco."""
    global campo_activo
    campo_activo = campo

def agregar_digit(digit):
    """Agrega un dígito al campo activo."""
    if campo_activo:  # Si hay un campo activo
        campo_actual = campo_activo.get()
        if len(campo_actual) < 8:  # Limitar a 8 dígitos para el RUT
            campo_activo.insert(tk.END, digit)

def borrar_digit():
    """Borra un dígito del campo activo."""
    if campo_activo:
        campo_activo.delete(len(campo_activo.get()) - 1, tk.END)

def borrar_todo():
    """Borra todo el texto en el campo activo."""
    if campo_activo:
        campo_activo.delete(0, tk.END)

def validar_rut(entry_rut):
    """Valida el RUT ingresado."""
    rut = entry_rut.get()
    if len(rut) != 8:
        messagebox.showerror("Error", "El RUT debe ser de 8 dígitos.")
        return None
    return rut

def obtener_almuerzo(entry_rut):
    """Obtener el almuerzo de acuerdo al RUT ingresado."""
    rut = validar_rut(entry_rut)
    if not rut:
        return

    # Obtener las hojas de datos y menús
    sheet = obtener_sheet()
    menu_sheet = obtener_menu_sheet()
    empleado_encontrado = False

    # Obtener la fecha actual
    fecha_actual = datetime.now()
    dia_actual = fecha_actual.day  # Día actual del mes

    # Buscar en la hoja de empleados
    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
        if str(row[0].value).startswith(rut):
            nombre = row[1].value  # Obtener el nombre del empleado

            menu = row[dia_actual].value  # Obtener el menú del día actual

            # Obtener la descripción del menú desde la hoja de menús
            menu_a = menu_sheet.cell(row=2, column=dia_actual + 1).value
            menu_b = menu_sheet.cell(row=3, column=dia_actual + 1).value
            menu_c = menu_sheet.cell(row=4, column=dia_actual + 1).value

            if menu == 'A':
                menu_descripcion = menu_a
            elif menu == 'B':
                menu_descripcion = menu_b
            elif menu == 'C':
                menu_descripcion = menu_c
            else:
                menu_descripcion = "Menú no asignado"

            # Llamada a la función para crear la boleta
            crear_boleta(menu, nombre, rut, dia_actual, menu_descripcion)
            empleado_encontrado = True
            break

    if not empleado_encontrado:
        messagebox.showerror("Error", "RUT no encontrado o no tiene menú para este día.")

def mostrar_vista_almuerzo(main_frame, volver_callback):
    """Mostrar la vista para ingresar al casino y obtener el almuerzo."""
    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="Ingrese su RUT:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
    entry_rut = tk.Entry(main_frame, font=("Arial", 12), width=15)
    entry_rut.grid(row=0, column=1, padx=5, pady=5)
    entry_rut.bind("<FocusIn>", lambda event: set_campo_activo(entry_rut))

    botones_frame = tk.Frame(main_frame)
    botones_frame.grid(row=1, column=0, columnspan=2)

    botones = [
        ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
        ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
        ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
        ('0', 3, 0), ('C', 3, 1), ('<-', 3, 2)
    ]

    for (text, row, col) in botones:
        if text == 'C':
            tk.Button(botones_frame, text=text, font=("Arial", 12), command=borrar_todo).grid(row=row, column=col, padx=5, pady=5)
        elif text == '<-':
            tk.Button(botones_frame, text=text, font=("Arial", 12), command=borrar_digit).grid(row=row, column=col, padx=5, pady=5)
        else:
            tk.Button(botones_frame, text=text, font=("Arial", 12), command=lambda t=text: agregar_digit(t)).grid(row=row, column=col, padx=5, pady=5)

    tk.Button(main_frame, text="Obtener Boleta", font=("Arial", 12), bg="lightblue", command=lambda: obtener_almuerzo(entry_rut)).grid(row=2, column=0, columnspan=2, pady=10)

    tk.Button(main_frame, text="Volver", font=("Arial", 12), bg="lightgreen", command=volver_callback).grid(row=3, column=0, columnspan=2, pady=10)
