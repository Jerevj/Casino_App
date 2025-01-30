from tkinter import *
from tkinter import ttk
import tkinter as tk
from conexion import Conexion  # Importar la clase Conexion

class Personal(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.db = Conexion()  # Instanciamos la clase de conexión
        self.db.conectar()  # Establecemos la conexión a la base de datos
        self.widgets()
        self.cargar_personal()  # Cargar los datos automáticamente al entrar

    def widgets(self):
        # Agregar una etiqueta para confirmar que la ventana se muestra
        mensaje = tk.Label(self, text="¡Ventana Personal cargada correctamente!", font=("Arial", 16))
        mensaje.grid(row=0, column=0, pady=20, padx=20, sticky="n")

        # Crear un botón para actualizar la tabla de personas
        actualizar_button = tk.Button(self, text="Actualizar Personal", command=self.cargar_personal)
        actualizar_button.grid(row=1, column=0, pady=10, padx=20, sticky="n")

        # Crear un frame para la tabla
        self.tabla_frame = Frame(self)
        self.tabla_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        # Crear el Treeview (tabla)
        self.treeview = ttk.Treeview(self.tabla_frame, columns=("RUT", "Nombre", "Clave", "Estado"), show="headings")
        self.treeview.grid(row=0, column=0, sticky="nsew")

        # Configurar las columnas
        self.treeview.heading("RUT", text="RUT")
        self.treeview.heading("Nombre", text="Nombre")
        self.treeview.heading("Clave", text="Clave")
        self.treeview.heading("Estado", text="Estado")

        # Crear el scrollbar para el Treeview
        self.scrollbar = Scrollbar(self.tabla_frame, orient=VERTICAL, command=self.treeview.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Asociar el scrollbar al Treeview
        self.treeview.config(yscrollcommand=self.scrollbar.set)

        # Agregar la funcionalidad de desplazamiento con la rueda del mouse
        self.treeview.bind_all("<MouseWheel>", self._on_mouse_wheel)

        # Configurar el grid para expandir la tabla
        self.tabla_frame.grid_rowconfigure(0, weight=1)
        self.tabla_frame.grid_columnconfigure(0, weight=1)

        # Hacer que todo el contenido sea responsivo
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _on_mouse_wheel(self, event):
        """Permitir que el Treeview se desplace con la rueda del mouse"""
        self.treeview.yview_scroll(-1*(event.delta//120), "units")

    def cargar_personal(self):
        # Si ya hay una tabla, eliminarla antes de crear una nueva
        for widget in self.treeview.get_children():
            self.treeview.delete(widget)

        # Obtener todas las personas desde la base de datos
        query = "SELECT rut, nombre, clave, estado FROM personas"
        self.db.cursor.execute(query)
        personas = self.db.cursor.fetchall()

        # Insertar las filas en el Treeview
        for persona in personas:
            self.treeview.insert("", "end", values=persona)

    def on_closing(self):
        self.db.desconectar()  # Cerrar la conexión cuando la ventana se cierre
        self.master.destroy()

# Ejemplo de uso
if __name__ == "__main__":
    root = Tk()
    root.title("Mantenedor de Personal")
    root.geometry("1000x600")  # Establecemos un tamaño inicial más grande para la ventana
    personal_frame = Personal(root)
    personal_frame.pack(fill=BOTH, expand=True)
    root.protocol("WM_DELETE_WINDOW", personal_frame.on_closing)  # Asegurar el cierre de la conexión
    root.mainloop()
