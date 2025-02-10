import tkinter as tk
from tkinter import ttk
from conexion import Conexion

class Menus_inscritos(tk.Frame):

    def __init__(self, padre):
        super().__init__(padre)
        self.grid(row=0, column=0, sticky="nsew")
        self.widgets()

    def widgets(self):
        # Crear una instancia de la clase Conexion
        self.db = Conexion(usar_pool=True)
        self.db.conectar()

        # Crear un Frame para contener el Treeview y los Scrollbars
        frame_tree = tk.Frame(self)
        frame_tree.grid(row=0, column=0, sticky="nsew")

        # Crear el Treeview
        self.tree = ttk.Treeview(frame_tree, columns=("id_boleta", "rut", "menu", "nombre_menu", "registrado", "estado_dia", "fecha_registro"), show="headings")
        self.tree.heading("id_boleta", text="ID Boleta")
        self.tree.heading("rut", text="RUT")
        self.tree.heading("menu", text="Menú")
        self.tree.heading("nombre_menu", text="Nombre Menú")
        self.tree.heading("registrado", text="Registrado")
        self.tree.heading("estado_dia", text="Estado Día")
        self.tree.heading("fecha_registro", text="Fecha Registro")

        # Crear Scrollbars
        scrollbar_vertical = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        scrollbar_horizontal = ttk.Scrollbar(frame_tree, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=scrollbar_vertical.set, xscroll=scrollbar_horizontal.set)

        # Empaquetar el Treeview y los Scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_vertical.grid(row=0, column=1, sticky="ns")
        scrollbar_horizontal.grid(row=1, column=0, sticky="ew")

        # Configurar el Frame para expandirse
        frame_tree.grid_rowconfigure(0, weight=1)
        frame_tree.grid_columnconfigure(0, weight=1)

        # Configurar el Frame principal para expandirse
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Obtener los datos de la base de datos
        self.cargar_datos()

        # Botón para actualizar el estado
        self.btn_actualizar = tk.Button(self, text="Actualizar Estado", command=self.actualizar_estado)
        self.btn_actualizar.grid(row=2, column=0, pady=10)

    def cargar_datos(self):
        # Limpiar la tabla
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Obtener los datos de la base de datos
        self.db.conectar()  # Asegurarse de que la conexión esté abierta
        query = "SELECT * FROM menus_registrados"
        self.db.cursor.execute(query)
        rows = self.db.cursor.fetchall()
        self.db.desconectar()  # Cerrar la conexión después de obtener los datos

        # Insertar los datos en el Treeview
        for row in rows:
            self.tree.insert("", "end", values=row)

    def actualizar_estado(self):
        # Obtener el elemento seleccionado
        selected_item = self.tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("Advertencia", "Seleccione un registro para actualizar.")
            return

        # Obtener los valores del elemento seleccionado
        item = self.tree.item(selected_item)
        values = item["values"]

        # Crear una ventana para actualizar el estado
        self.ventana_estado = tk.Toplevel(self)
        self.ventana_estado.title("Actualizar Estado")
        self.ventana_estado.geometry("300x200")

        # Etiqueta y menú desplegable para el estado
        tk.Label(self.ventana_estado, text="Estado Día:").pack(pady=10)
        self.estado_var = tk.StringVar(value=values[5])
        self.estado_menu = ttk.Combobox(self.ventana_estado, textvariable=self.estado_var, values=["normal", "vacaciones", "licencia", "otro"])
        self.estado_menu.pack(pady=10)

        # Botón para guardar el estado
        tk.Button(self.ventana_estado, text="Guardar", command=lambda: self.guardar_estado(values[0])).pack(pady=10)

    def guardar_estado(self, id_boleta):
        # Obtener el nuevo estado
        nuevo_estado = self.estado_var.get()

        # Actualizar el estado en la base de datos
        self.db.conectar()  # Asegurarse de que la conexión esté abierta
        query = "UPDATE menus_registrados SET estado_dia = %s WHERE id_boleta = %s"
        self.db.cursor.execute(query, (nuevo_estado, id_boleta))
        self.db.conexion.commit()
        self.db.desconectar()  # Cerrar la conexión después de actualizar

        # Cerrar la ventana de actualización
        self.ventana_estado.destroy()

        # Recargar los datos en la tabla
        self.cargar_datos()