'''import tkinter as tk
from tkinter import messagebox
from utils import obtener_sheet, obtener_menu_sheet

def mostrar_panel_numerico(main_frame):
    """Mostrar toda la vista de inicio de la aplicación."""
    for widget in main_frame.winfo_children():
        widget.grid_forget()

    # Ingreso de la contraseña del administrador
    tk.Label(main_frame, text="Ingrese su RUT:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
    entry_rut = tk.Entry(main_frame, font=("Arial", 12), width=15)
    entry_rut.grid(row=0, column=1, padx=5, pady=5)

    # Ingreso del Día
    tk.Label(main_frame, text="Ingrese el día (1-31):", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
    entry_dia = tk.Entry(main_frame, font=("Arial", 12), width=15)
    entry_dia.grid(row=2, column=1, padx=5, pady=5)

    def agregar_digit(digit):
        rut_actual = entry_rut.get()
        if len(rut_actual) < 8:  # Limitar a 8 dígitos
            entry_rut.insert(tk.END, digit)

    def borrar_digit():
        entry_rut.delete(len(entry_rut.get()) - 1, tk.END)

    def borrar_todo():
        entry_rut.delete(0, tk.END)

    def obtener_almuerzo():
        rut = entry_rut.get()
        if len(rut) != 8:
            messagebox.showerror("Error", "El RUT debe ser de 8 dígitos.")
            return

        try:
            dia = int(entry_dia.get())  # Obtener el día
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un número válido para el día.")
            return

        if dia < 1 or dia > 31:
            messagebox.showerror("Error", "El día debe estar entre 1 y 31.")
            return

        # Obtener las hojas de datos y menús
        sheet = obtener_sheet()  # Obtener la hoja de empleados
        menu_sheet = obtener_menu_sheet()  # Obtener la hoja de menús
        empleado_encontrado = False

        # Buscar en la hoja de empleados
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
            if str(row[0].value).startswith(rut):  # Verifica si el RUT coincide (compara solo los primeros 8 dígitos)
                nombre = row[1].value  # Obtener el nombre del empleado
                menu = row[dia].value  # Obtener el menú para el día seleccionado

                # Obtener la descripción del menú desde la hoja de menús
                menu_a = menu_sheet.cell(row=2, column=dia+1).value  # Menú A
                menu_b = menu_sheet.cell(row=3, column=dia+1).value  # Menú B
                menu_c = menu_sheet.cell(row=4, column=dia+1).value  # Menú C

                # Determinar la descripción del menú seleccionado
                if menu == 'A':
                    menu_descripcion = menu_a
                elif menu == 'B':
                    menu_descripcion = menu_b
                elif menu == 'C':
                    menu_descripcion = menu_c
                else:
                    menu_descripcion = "Menú no asignado"

                # Mostrar la boleta con la descripción del menú
                mensaje = f"Boleta para {nombre} ({rut}):\nAlmuerzo: {menu_descripcion}\nDía: {dia}"
                messagebox.showinfo("Boleta", mensaje)
                empleado_encontrado = True
                break

        if not empleado_encontrado:
            messagebox.showerror("Error", "RUT no encontrado o no tiene menú para este día.")

    # Crear los botones numéricos y las opciones
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
            tk.Button(botones_frame, text=text, width=5, height=2, font=("Arial", 12), command=borrar_todo).grid(row=row, column=col, padx=5, pady=5)
        elif text == '<-':
            tk.Button(botones_frame, text=text, width=5, height=2, font=("Arial", 12), command=borrar_digit).grid(row=row, column=col, padx=5, pady=5)
        else:
            tk.Button(botones_frame, text=text, width=5, height=2, font=("Arial", 12), command=lambda t=text: agregar_digit(t)).grid(row=row, column=col, padx=5, pady=5)

    boton_obtener_almuerzo = tk.Button(main_frame, text="Obtener Almuerzo", font=("Arial", 12), command=obtener_almuerzo)
    boton_obtener_almuerzo.grid(row=4, column=0, columnspan=2, pady=10)
'''