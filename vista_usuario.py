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
    if campo_activo and len(campo_activo.get()) < 4:  # Limitar a 4 dígitos
        campo_activo.insert(tk.END, digit)

def borrar_digit():
    """Borra un dígito del campo activo."""
    if campo_activo:
        campo_activo.delete(len(campo_activo.get()) - 1, tk.END)

def borrar_todo():
    """Borra todo el texto en el campo activo."""
    if campo_activo:
        campo_activo.delete(0, tk.END)

def validar_clave_entry(entry):
    """Valida la clave de 4 dígitos ingresada."""
    clave = entry.get()
    if not clave.isdigit() or len(clave) != 4:
        messagebox.showerror("Error", "La clave debe ser de 4 dígitos numéricos.")
        return None
    return clave

class VistaUsuario(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        
        # Crear una instancia de la clase Conexion con pool
        self.db = Conexion(usar_pool=True)
        self.db.conectar()  # Conectar a la base de datos
        self.widgets()

        # Manejar el cierre de la ventana
        self.master.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

    def widgets(self):
        """Crea los widgets para la vista de usuario."""
        fuente_grande = ("Arial", 20)

        # Etiqueta para la clave
        tk.Label(self, text="Ingrese su clave:", font=fuente_grande).grid(row=0, column=0, padx=10, pady=10)

        # Campo de entrada
        self.entry_clave = tk.Entry(self, font=fuente_grande, width=15, show='*')
        self.entry_clave.grid(row=0, column=1, padx=10, pady=10)
        self.entry_clave.bind("<FocusIn>", lambda event: set_campo_activo(self.entry_clave))
        self.entry_clave.focus_set()  

        # Panel de botones numéricos
        botones_frame = tk.Frame(self)
        botones_frame.grid(row=1, column=0, columnspan=2, pady=20)

        botones = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('0', 3, 0), ('C', 3, 1), ('<-', 3, 2)
        ]

        # Cargar imagen para el botón de retroceso
        imagen_retroceder = Image.open("images/borrar2.jpg").resize((50, 50), Image.Resampling.LANCZOS)
        self.imagen_retroceder = ImageTk.PhotoImage(imagen_retroceder)

        # Configurar tamaño de los botones
        for (text, row, col) in botones:
            if text == 'C':
                tk.Button(botones_frame, text=text, font=fuente_grande, command=borrar_todo, width=5, height=2).grid(row=row, column=col, padx=10, pady=10)
            elif text == '<-':
                tk.Button(botones_frame, image=self.imagen_retroceder, command=borrar_digit, width=87, height=87).grid(row=row, column=col, padx=10, pady=10)
            else:
                tk.Button(botones_frame, text=text, font=fuente_grande, command=lambda t=text: agregar_digit(t), width=5, height=2).grid(row=row, column=col, padx=10, pady=10)

        # Botón para obtener la boleta
        tk.Button(self, text="Obtener Boleta", font=fuente_grande, bg="lightblue", command=self.obtener_almuerzo).grid(row=2, column=0, columnspan=2, pady=20)

    def obtener_almuerzo(self):
        """Obtener el almuerzo del usuario según su clave."""
        clave = validar_clave_entry(self.entry_clave)
        if not clave:
            return

        # Obtener la fecha actual
        fecha_actual = datetime.now()
        dia_mes = fecha_actual.day  # Extrae solo el día

        try:
            # Buscar la persona en la base de datos
            persona = self.db.obtener_persona_por_clave(clave)
            
            if persona:
                rut = persona[0]
                nombre = persona[1]
                print(f"Empleado encontrado: {nombre} (RUT: {rut})")

                # Buscar la opción de menú en el Excel
                opcion_menu = excel_manager.obtener_menu_desde_excel(rut, dia_mes)
                if opcion_menu:
                    # Obtener el nombre del menú
                    nombre_menu = excel_manager.obtener_nombre_menu(dia_mes, opcion_menu)
                    if nombre_menu:
                        # Registrar boleta en la base de datos
                        print("Registrando boleta en la base de datos...")  # Mensaje de depuración
                        id_boleta = self.db.registrar_boleta(rut, opcion_menu, nombre_menu, fecha_actual)
                        
                        if id_boleta:
                            # Generar boleta
                            crear_boleta(opcion_menu, nombre, rut, fecha_actual.strftime('%d/%m/%Y'), nombre_menu, id_boleta)
                            print("Boleta generada.")
                        else:
                            messagebox.showerror("Error", "No se pudo registrar la boleta.")
                    else:
                        messagebox.showerror("Error", "No se encontró el nombre del menú.")
                else:
                    messagebox.showerror("Error", "No hay menú asignado para este día.")
            else:
                messagebox.showerror("Error", "Clave no encontrada.")
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al obtener el almuerzo: {e}")
        finally:
            self.db.desconectar()  # Aseguramos que la conexión se cierre después de la operación
        
    def cerrar_ventana(self):
        """Cierra la conexión antes de cerrar la ventana."""
        print("Cerrando la ventana...")
        self.db.desconectar()
        self.master.destroy()

    def __del__(self):
        """Asegurarse de que la conexión se cierre si no se llama a cerrar_ventana explícitamente."""
        self.db.desconectar()
        print("Base de datos desconectada")
