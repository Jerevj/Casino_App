import tkinter as tk
import pandas as pd
from utils.excel_utils import excel_manager  # Importamos la instancia de ExcelManager
from tkinter import messagebox
from datetime import datetime
from boleta import crear_boleta
from conexion import Conexion  # Importa la clase Conexion
from PIL import Image, ImageTk

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
        if len(campo_actual) < 4:  # Limitar a 4 dígitos para la clave
            campo_activo.insert(tk.END, digit)

def borrar_digit():
    """Borra un dígito del campo activo."""
    if campo_activo:
        campo_activo.delete(len(campo_activo.get()) - 1, tk.END)

def borrar_todo():
    """Borra todo el texto en el campo activo."""
    if campo_activo:
        campo_activo.delete(0, tk.END)

def validar_clave(validar_clave):
    """Valida la clave de 4 dígitos ingresada, que es parte del RUT."""
    clave = validar_clave.get()
    if len(clave) != 4 or not clave.isdigit():  # Validamos que tenga 4 dígitos y que sean numéricos
        messagebox.showerror("Error", "La clave debe ser de 4 dígitos numéricos.")
        return None
    return clave

class VistaUsuario(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        
        # Crear una instancia de la clase Conexion
        self.db = Conexion()
        self.db.conectar()  # Conectar a la base de datos
        self.widgets()

         # Manejar el cierre de la ventana
        self.master.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

    def widgets(self):
        """Crea los widgets para la vista de usuario."""
        # Cambiamos el tamaño de fuente
        fuente_grande = ("Arial", 20)

        # Etiqueta para el RUT
        tk.Label(self, text="Ingrese su RUT:", font=fuente_grande).grid(row=0, column=0, padx=10, pady=10)
        
        # Campo de entrada
        self.validar_clave = tk.Entry(self, font=fuente_grande, width=15)
        self.validar_clave.grid(row=0, column=1, padx=10, pady=10)
        self.validar_clave.bind("<FocusIn>", lambda event: set_campo_activo(self.validar_clave))
        self.validar_clave.focus_set()  # Seleccionar automáticamente el Entry

        # Botones numéricos
        botones_frame = tk.Frame(self)
        botones_frame.grid(row=1, column=0, columnspan=2, pady=20)

        botones = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('0', 3, 0), ('C', 3, 1), ('<-', 3, 2)
        ]

        # Cargar la imagen para el botón de retroceder
        imagen_retroceder = Image.open("images/borrar2.jpg")
        imagen_retroceder = imagen_retroceder.resize((50, 50), Image.Resampling.LANCZOS)  # Usar LANCZOS en lugar de ANTIALIAS
        self.imagen_retroceder = ImageTk.PhotoImage(imagen_retroceder)

        # Configurar columnas y filas para asegurar que los botones tengan el mismo tamaño
        botones_frame.grid_columnconfigure(0, weight=1, uniform="equal")
        botones_frame.grid_columnconfigure(1, weight=1, uniform="equal")
        botones_frame.grid_columnconfigure(2, weight=1, uniform="equal")
        botones_frame.grid_rowconfigure(0, weight=1, uniform="equal")
        botones_frame.grid_rowconfigure(1, weight=1, uniform="equal")
        botones_frame.grid_rowconfigure(2, weight=1, uniform="equal")
        botones_frame.grid_rowconfigure(3, weight=1, uniform="equal")

        for (text, row, col) in botones:
            if text == 'C':
                # Botón de borrar todo (con texto)
                tk.Button(botones_frame, text=text, font=fuente_grande, command=borrar_todo, width=5, height=2).grid(row=row, column=col, padx=10, pady=10)
            elif text == '<-':
                # Botón de retroceder (con imagen)
                tk.Button(botones_frame, image=self.imagen_retroceder, command=borrar_digit, width=87, height=87).grid(row=row, column=col, padx=10, pady=10)
            else:
                # Botón con texto normal
                tk.Button(botones_frame, text=text, font=fuente_grande, command=lambda t=text: agregar_digit(t), width=5, height=2).grid(row=row, column=col, padx=10, pady=10)

        # Botón para obtener la boleta
        tk.Button(self, text="Obtener Boleta", font=fuente_grande, bg="lightblue", 
                  command=self.obtener_almuerzo).grid(row=2, column=0, columnspan=2, pady=20)

    def obtener_almuerzo(self):
        """Obtener el almuerzo de acuerdo al RUT ingresado."""
        clave = validar_clave(self.validar_clave)
        if not clave:
            return

        # Imprimir la clave para depurar
        print(f"Clave ingresada: {clave}")

        # Obtener la fecha actual
        fecha_actual = datetime.now()
        dia_actual = fecha_actual.day

        # Buscar el RUT en la base de datos
        persona = self.db.obtener_persona_por_clave(clave)
        
        if persona:
            print(f"Empleado encontrado: {persona[1]}")  # Persona[1] es el nombre del empleado
            
            # Buscar el menú en el Excel
            menu_data = excel_manager.obtener_menu_desde_excel(persona[0], dia_actual)  # persona[0] es el RUT
            
            if menu_data:
                # Aquí puedes obtener los datos del menú y pasarlos a la función para generar la boleta
                menu = menu_data[2]  # Menu (campo de la tabla menus_registrados)
                nombre_menu = menu_data[3]  # Nombre del menú
                
                # Generar boleta
                id_boleta = f"{fecha_actual.strftime('%Y%m%d')}{clave}"
                crear_boleta(menu, persona[1], persona[0], fecha_actual.strftime('%d/%m/%Y'), nombre_menu, id_boleta)
                print("Boleta generada.")
            else:
                messagebox.showerror("Error", "No hay menú asignado para este día.")
        else:
            messagebox.showerror("Error", "RUT no encontrado.")
    
    def cerrar_ventana(self):
        """Llamar al método para cerrar la conexión antes de cerrar la ventana."""
        print("Cerrando la ventana...")
        self.db.desconectar()  # Cerrar la conexión de la base de datos
        self.master.destroy()  # Cerrar la ventana
