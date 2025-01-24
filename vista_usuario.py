import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from utils.excel_utils import excel_manager
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

class VistaUsuario(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.widgets()

    def widgets(self):
        """Crea los widgets para la vista de usuario."""
        tk.Label(self, text="Ingrese su RUT:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.entry_rut = tk.Entry(self, font=("Arial", 12), width=15)
        self.entry_rut.grid(row=0, column=1, padx=5, pady=5)
        self.entry_rut.bind("<FocusIn>", lambda event: set_campo_activo(self.entry_rut))

        botones_frame = tk.Frame(self)
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

        tk.Button(self, text="Obtener Boleta", font=("Arial", 12), bg="lightblue", 
                  command=self.obtener_almuerzo).grid(row=2, column=0, columnspan=2, pady=10)

    def obtener_almuerzo(self):
        """Obtener el almuerzo de acuerdo al RUT ingresado."""
        rut = validar_rut(self.entry_rut)
        if not rut:
            return

        sheet = excel_manager.obtener_sheet()
        menu_sheet = excel_manager.obtener_menu_sheet()
        empleado_encontrado = False

        fecha_actual = datetime.now()
        dia_actual = fecha_actual.day

        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
            if str(row[0].value).startswith(rut):
                nombre = row[1].value
                menu = row[dia_actual].value

                menu_descripcion = menu_sheet.cell(row=2 if menu == 'A' else 3 if menu == 'B' else 4, column=dia_actual + 1).value
                if not menu_descripcion:
                    menu_descripcion = "Menú no asignado"

                id_boleta = f"{fecha_actual.strftime('%Y%m%d')}{rut}"
                crear_boleta(menu, nombre, rut, fecha_actual.strftime('%d/%m/%Y'), menu_descripcion, id_boleta)
                empleado_encontrado = True
                break

        if not empleado_encontrado:
            messagebox.showerror("Error", "RUT no encontrado o no tiene menú para este día.")