import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from conexion import Conexion  # Para conexión a la base de datos
from boleta import crear_boleta  # Para la generación de boletas
from utils.excel_utils import excel_manager  # Para obtener los menús desde el Excel

class VistaUsuario(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)

        # Crear instancia de conexión a la base de datos
        self.db = Conexion()
        self.db.conectar()  # Conectar a la base de datos
        self.widgets()

        # Manejar el cierre de la ventana
        self.master.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

        self.boleta_generada = False  # Asegura que solo se genere una boleta por clave
        self.ventana_abierta = True  # Estado de la ventana, si está abierta

    def widgets(self):
        """Crear los widgets para la vista de usuario."""
        fuente_grande = ("Arial", 20)

        # Etiqueta para la clave
        tk.Label(self, text="Ingrese su clave:", font=fuente_grande).grid(row=0, column=0, padx=10, pady=10)

        # Campo de entrada para la clave
        self.entry_clave = tk.Entry(self, font=fuente_grande, width=15, show='*')
        self.entry_clave.grid(row=0, column=1, padx=10, pady=10)
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

        # Crear los botones
        for (text, row, col) in botones:
            if text == 'C':
                tk.Button(botones_frame, text=text, font=fuente_grande, command=self.borrar_todo, width=5, height=2).grid(row=row, column=col, padx=10, pady=10)
            elif text == '<-':
                tk.Button(botones_frame, text=text, font=fuente_grande, command=self.borrar_digit, width=5, height=2).grid(row=row, column=col, padx=10, pady=10)
            else:
                tk.Button(botones_frame, text=text, font=fuente_grande, command=lambda t=text: self.agregar_digit(t), width=5, height=2).grid(row=row, column=col, padx=10, pady=10)

        # Botón para obtener boleta
        self.boton_generar = tk.Button(self, text="Obtener Boleta", font=fuente_grande, bg="lightblue", command=self.obtener_almuerzo)
        self.boton_generar.grid(row=2, column=0, columnspan=2, pady=20)

    def agregar_digit(self, digit):
        """Agrega un dígito al campo de la clave."""
        if len(self.entry_clave.get()) < 4:  # Limitar a 4 dígitos
            self.entry_clave.insert(tk.END, digit)

    def borrar_digit(self):
        """Borra un dígito del campo de la clave."""
        self.entry_clave.delete(len(self.entry_clave.get()) - 1, tk.END)

    def borrar_todo(self):
        """Borra todo el texto en el campo de la clave."""
        self.entry_clave.delete(0, tk.END)

    def validar_clave(self):
        """Valida la clave de 4 dígitos ingresada."""
        clave = self.entry_clave.get()
        if not clave.isdigit() or len(clave) != 4:
            messagebox.showerror("Error", "La clave debe ser de 4 dígitos numéricos.")
            return None
        return clave

    def obtener_almuerzo(self):
        """Obtiene el almuerzo del usuario según su clave."""
        clave = self.validar_clave()
        if not clave:
            self.boton_generar.config(state="normal")  # Habilitar el botón si la clave no es válida
            self.limpiar_campo_clave()  # Limpiar el campo de clave para el siguiente usuario
            return

        # Limpiar el campo de clave antes de cualquier operación
        self.limpiar_campo_clave()

        # Obtener la fecha actual
        fecha_actual = datetime.now()
        dia_mes = fecha_actual.day  # Extrae solo el día

        try:
            # Buscar la persona en la base de datos
            persona = self.db.obtener_persona_por_clave(clave)
            if persona:
                rut = persona[0]
                nombre = persona[1]

                # Verificar si ya existe una boleta registrada para ese día
                boleta_existente = self.db.obtener_boleta_por_rut_y_fecha(rut, fecha_actual)
                if boleta_existente:
                    messagebox.showwarning("Advertencia", "Ya se ha generado una boleta para hoy.")
                    self.boton_generar.config(state="normal")  # Habilitar el botón
                    return  # Si ya existe, no generamos otra boleta

                # Buscar la opción de menú en el Excel
                opcion_menu = excel_manager.obtener_menu_desde_excel(rut, dia_mes)
                if opcion_menu:
                    # Obtener el nombre del menú
                    nombre_menu = excel_manager.obtener_nombre_menu(dia_mes, opcion_menu)
                    if nombre_menu:
                        # Registrar boleta en la base de datos
                        id_boleta = self.db.registrar_boleta(rut, opcion_menu, nombre_menu, fecha_actual)

                        if id_boleta:
                            # Generar boleta
                            crear_boleta(opcion_menu, nombre, rut, fecha_actual.strftime('%d/%m/%Y'), nombre_menu, id_boleta)
                            print("Boleta generada, llamando a mostrar_boleta_generada...")
                            # Usar `after()` para asegurarse de que el ciclo de eventos se actualice
                            self.after(0, self.mostrar_boleta_generada) 

                        else:
                            messagebox.showerror("Error", "No se pudo registrar la boleta.")
                            self.boton_generar.config(state="normal")  # Habilitar el botón
                    else:
                        messagebox.showerror("Error", "No se encontró el nombre del menú.")
                        self.boton_generar.config(state="normal")  # Habilitar el botón
                else:
                    messagebox.showerror("Error", "No hay menú asignado para este día.")
                    self.boton_generar.config(state="normal")  # Habilitar el botón
            else:
                messagebox.showerror("Error", "Clave no encontrada.")
                self.boton_generar.config(state="normal")  # Habilitar el botón
            
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al obtener el almuerzo: {e}")
            self.boton_generar.config(state="normal")  # Habilitar el botón
        
    def mostrar_boleta_generada(self):
        """Muestra el mensaje de éxito y habilita el botón nuevamente."""
        self.update_idletasks()  # Forzar actualización de la UI
        messagebox.showinfo("Éxito", "Boleta generada.")
        self.boton_generar.config(state="normal")  # Habilitar el botón nuevamente

    def limpiar_campo_clave(self):
        """Limpia el campo de entrada después de generar la boleta."""        
        self.entry_clave.delete(0, tk.END)
        self.entry_clave.update_idletasks()  # Asegurarse de que el campo se actualice
        self.entry_clave.focus_set()  # Enfocar el campo de clave nuevamente

    def cerrar_ventana(self):
        """Cierra la conexión antes de cerrar la ventana."""
        self.ventana_abierta = False  # Marca que la ventana está cerrada
        print("Cerrando la ventana...")
        self.db.desconectar()
        self.master.destroy()

    def __del__(self):
        """Asegurarse de que la conexión se cierre si no se llama a cerrar_ventana explícitamente."""
        self.db.desconectar()
        print("Base de datos desconectada")