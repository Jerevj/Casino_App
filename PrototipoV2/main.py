import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from utils import cargar_archivo, obtener_sheet, obtener_menu_sheet
from boleta import crear_boleta  # Importamos la función para mostrar la boleta
# Variable para guardar el campo activo
campo_activo = None

def crear_campos_ingreso(main_frame):
    """Crea los campos de ingreso de RUT, Día y Contraseña, y devuelve los widgets creados."""
    # Ingreso del RUT
    tk.Label(main_frame, text="Ingrese su RUT:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
    entry_rut = tk.Entry(main_frame, font=("Arial", 12), width=15)
    entry_rut.grid(row=0, column=1, padx=5, pady=5)
    entry_rut.bind("<FocusIn>", lambda event: set_campo_activo(entry_rut))  # Asignar el campo activo

    # Ingreso del Día
    tk.Label(main_frame, text="Ingrese el día (1-31):", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
    entry_dia = tk.Entry(main_frame, font=("Arial", 12), width=15)
    entry_dia.grid(row=1, column=1, padx=5, pady=5)
    entry_dia.bind("<FocusIn>", lambda event: set_campo_activo(entry_dia))  # Asignar el campo activo

    return entry_rut, entry_dia

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

def validar_rut_y_dia(entry_rut, entry_dia):
    """Valida el RUT y el día."""
    rut = entry_rut.get()
    if len(rut) != 8:
        messagebox.showerror("Error", "El RUT debe ser de 8 dígitos.")
        return False

    try:
        dia = int(entry_dia.get())  # Obtener el día
    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese un número válido para el día.")
        return False

    if dia < 1 or dia > 31:
        messagebox.showerror("Error", "El día debe estar entre 1 y 31.")
        return False

    return rut, dia

def obtener_almuerzo(entry_rut, entry_dia):
    """Obtener el almuerzo de acuerdo al RUT y al día seleccionado."""
    rut, dia = validar_rut_y_dia(entry_rut, entry_dia)
    if not rut or not dia:
        return

    # Obtener las hojas de datos y menús
    sheet = obtener_sheet()  # Obtener la hoja de empleados
    menu_sheet = obtener_menu_sheet()  # Obtener la hoja de menús
    empleado_encontrado = False

    # Buscar en la hoja de empleados
    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
        if str(row[0].value).startswith(rut):  # Verifica si el RUT coincide (compara solo los primeros 8 dígitos)
            nombre = row[32].value  # Obtener el nombre del empleado
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

            # Llamar a la función para crear la boleta con los valores correctos
            crear_boleta(menu, nombre, rut, dia, menu_descripcion)
            empleado_encontrado = True
            break

    if not empleado_encontrado:
        messagebox.showerror("Error", "RUT no encontrado o no tiene menú para este día.")


    if not empleado_encontrado:
        messagebox.showerror("Error", "RUT no encontrado o no tiene menú para este día.")

def verificar_contraseña(contraseña, main_frame):
    """Verificar la contraseña y mostrar el mantenedor."""
    if contraseña == "12345":
        from mantenedor import mostrar_mantenedor
        mostrar_mantenedor(main_frame, mostrar_vista_almuerzos)  # Mostrar la ventana de mantenimiento
    else:
        messagebox.showerror("Error", "Contraseña incorrecta")

def mostrar_vista_almuerzos(main_frame):
    """Mostrar toda la vista de inicio de la aplicación."""
    for widget in main_frame.winfo_children():
        widget.grid_forget()

    # Crear campos de ingreso (RUT y Día)
    entry_rut, entry_dia = crear_campos_ingreso(main_frame)

    # Crear los botones numéricos y las opciones
    botones_frame = tk.Frame(main_frame)
    botones_frame.grid(row=3, column=0, columnspan=2)

     # Cargar la imagen para el botón de borrar
    image_borrar = Image.open('PrototipoV2/images/borrar2.jpg')
    image_borrar = image_borrar.resize((40, 40), Image.Resampling.LANCZOS)  # Usar LANCZOS en lugar de ANTIALIAS
    photo_borrar = ImageTk.PhotoImage(image_borrar)

    botones = [
        ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
        ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
        ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
        ('0', 3, 0), ('C', 3, 1), ('<-', 3, 2)
    ]
    
    # Configuración de las columnas y filas para mantener la consistencia del tamaño de los botones
    botones_frame.grid_columnconfigure(0, weight=1, uniform="equal")
    botones_frame.grid_columnconfigure(1, weight=1, uniform="equal")
    botones_frame.grid_columnconfigure(2, weight=1, uniform="equal")
    botones_frame.grid_rowconfigure(0, weight=1, uniform="equal")
    botones_frame.grid_rowconfigure(1, weight=1, uniform="equal")
    botones_frame.grid_rowconfigure(2, weight=1, uniform="equal")
    botones_frame.grid_rowconfigure(3, weight=1, uniform="equal")

    for (text, row, col) in botones:
        if text == 'C':
            tk.Button(botones_frame, text=text, width=5, height=2, font=("Arial", 12), command=borrar_todo ).grid(row=row, column=col, padx=5, pady=5)
        elif text == '<-':
            tk.Button(botones_frame, image=photo_borrar, width=49, height=45, command=borrar_digit).grid(row=row, column=col, padx=5, pady=5)
        else:
            tk.Button(botones_frame, text=text, width=5, height=2, font=("Arial", 12), command=lambda t=text: agregar_digit(t)).grid(row=row, column=col, padx=5, pady=5)

    boton_obtener_almuerzo = tk.Button(main_frame,bg="lightblue", text="Obtener Boleta", font=("Arial", 12), command=lambda: obtener_almuerzo(entry_rut, entry_dia))
    boton_obtener_almuerzo.grid(row=4, column=0, columnspan=2, pady=10)

    # Agregar los campos de Contraseña y Botón Mantenedor al final
    tk.Label(main_frame, text="Ingrese la contraseña del administrador:", font=("Arial", 12)).grid(row=5, column=0, padx=5, pady=5)
    entry_contraseña_admin = tk.Entry(main_frame, font=("Arial", 12), show="*")
    entry_contraseña_admin.grid(row=5, column=1, padx=5, pady=5)

    # Botón para ingresar al mantenedor
    boton_mantenedor = tk.Button(main_frame, text="Mantenedor",bg="lightgreen", font=("Arial", 12), command=lambda: verificar_contraseña(entry_contraseña_admin.get(), main_frame))
    boton_mantenedor.grid(row=6, column=0, columnspan=2, pady=10)
    
    # Mantener referencia a la imagen para evitar que sea eliminada por el recolector de basura
    botones_frame.image = photo_borrar

def main():
    root = tk.Tk()
    root.title("Sistema de Almuerzos del Casino")
    root.iconbitmap('PrototipoV2/images/logoKnop.ico')
    

    main_frame = tk.Frame(root)
    main_frame.grid(row=0, column=0, padx=20, pady=20)

    # Mostrar la vista principal de almuerzos
    mostrar_vista_almuerzos(main_frame)

    root.mainloop()

if __name__ == "__main__":
    main()
