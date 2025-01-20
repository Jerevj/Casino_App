import tkinter as tk
from tkinter import messagebox
from utils import obtener_wb, obtener_sheet, obtener_menu_sheet, file_path

# Variable global para almacenar la etiqueta del menú actual
label_menu_actual = None

def iniciar_mantenedor(contraseña, main_frame):
    if contraseña == "12345":
        mostrar_mantenedor(main_frame)  # Llamada sin el segundo argumento
    else:
        messagebox.showerror("Error", "Contraseña incorrecta")

def mostrar_mantenedor(main_frame, mostrar_vista_almuerzos):
    """Mostrar la ventana de mantenimiento de menús."""
    # Limpiar la pantalla anterior
    for widget in main_frame.winfo_children():
        widget.grid_forget()

    # Título del mantenedor
    tk.Label(main_frame, text="Mantenedor de Selección de Menús", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=3, pady=10)

    # Campos de entrada para RUT y Día
    tk.Label(main_frame, text="Ingrese el RUT del empleado:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky='e')
    entry_rut_mantenedor = tk.Entry(main_frame, font=("Arial", 12))
    entry_rut_mantenedor.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    tk.Label(main_frame, text="Ingrese el día (1-31):", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky='e')
    entry_dia_mantenedor = tk.Entry(main_frame, font=("Arial", 12))
    entry_dia_mantenedor.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    def buscar_menu():
        rut = entry_rut_mantenedor.get()
        try:
            dia = int(entry_dia_mantenedor.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un número válido para el día.")
            return

        if dia < 1 or dia > 31:
            messagebox.showerror("Error", "El día debe estar entre 1 y 31.")
            return

        empleado_encontrado = False
        sheet = obtener_sheet()  # Obtener la hoja de empleados
        menu_sheet = obtener_menu_sheet()  # Obtener la hoja de menús

        # Aquí vamos a mostrar los resultados debajo de los campos de entrada
        # Mostramos la información del empleado si se encuentra
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
            if str(row[0].value).startswith(rut):  # Verifica si el RUT coincide
                nombre = row[-2].value
                # Ajuste para obtener el menú según el día
                menu = row[dia].value  # Asegúrate de que `dia+1` sea la columna correcta para el día
                menu_a = menu_sheet.cell(row=2, column=dia+1).value
                menu_b = menu_sheet.cell(row=3, column=dia+1).value
                menu_c = menu_sheet.cell(row=4, column=dia+1).value

                # Eliminar la etiqueta anterior (si existe)
                global label_menu_actual
                if label_menu_actual:
                    label_menu_actual.grid_forget()

                # Mostrar el nombre del empleado y el menú actual en una fila separada
                tk.Label(main_frame, text=f"Empleado: {nombre} ({rut})", font=("Arial", 12)).grid(row=4, column=0, columnspan=3, pady=10)

                # Aquí guardamos la nueva etiqueta para el menú
                label_menu_actual = tk.Label(main_frame, text=f"Menú Actual: {menu}", font=("Arial", 12))
                label_menu_actual.grid(row=5, column=0, columnspan=3, pady=5)

                def cambiar_menu(menu_seleccionado):
                    # Asegúrate de que estamos modificando la celda correcta
                    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
                        if str(row[0].value).startswith(rut):
                            row[dia].value = menu_seleccionado 
                            break
                    obtener_wb().save(file_path)  # Guardar el archivo Excel
                    messagebox.showinfo("Guardado", f"El menú ha sido cambiado a {menu_seleccionado} para {nombre}.")

                botones_menu_frame = tk.Frame(main_frame)
                botones_menu_frame.grid(row=6, column=0, columnspan=3, pady=5)

                tk.Button(botones_menu_frame, text="A", width=10, height=2, font=("Arial", 12),
                          command=lambda menu_seleccionado="A": cambiar_menu(menu_seleccionado)).grid(row=0, column=0, padx=5)
                tk.Button(botones_menu_frame, text="B", width=10, height=2, font=("Arial", 12),
                          command=lambda menu_seleccionado="B": cambiar_menu(menu_seleccionado)).grid(row=0, column=1, padx=5)
                tk.Button(botones_menu_frame, text="C", width=10, height=2, font=("Arial", 12),
                          command=lambda menu_seleccionado="C": cambiar_menu(menu_seleccionado)).grid(row=0, column=2, padx=5)

                empleado_encontrado = True
                break

        if not empleado_encontrado:
            messagebox.showerror("Error", "RUT no encontrado o no tiene menú para este día.")

    # Botón para buscar el menú del empleado
    tk.Button(main_frame, text="Buscar Menú", font=("Arial", 12), command=buscar_menu).grid(row=3, column=0, columnspan=3, pady=10)

    # Botón para volver a la vista de almuerzos
    # Este botón siempre se coloca al final
    tk.Button(main_frame, text="Volver", font=("Arial", 12), command=lambda: mostrar_vista_almuerzos(main_frame)).grid(row=7, column=0, columnspan=3, pady=10)
