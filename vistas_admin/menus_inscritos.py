import tkinter as tk
from tkinter import ttk, messagebox
import traceback

class MenusInscritos(tk.Frame):
    def __init__(self, padre, db_connection):
        super().__init__(padre)
        self.db_connection = db_connection  # Guardar la conexión
        self.grid(row=0, column=0, sticky="nsew")

        self.widgets()
        
        # Asegurar cierre de conexión al cerrar la ventana
        self.winfo_toplevel().protocol("WM_DELETE_WINDOW", self.cerrar_conexion)

    def widgets(self):
        frame_tree = tk.Frame(self)
        frame_tree.grid(row=0, column=0, sticky="nsew")

        self.tree = ttk.Treeview(
            frame_tree, 
            columns=("id_boleta", "rut", "menu", "nombre_menu", "registrado", "estado_dia", "fecha_registro"), 
            show="headings"
        )

        columnas = {
            "id_boleta": "ID Boleta",
            "rut": "RUT",
            "menu": "Menú",
            "nombre_menu": "Nombre Menú",
            "registrado": "Registrado",
            "estado_dia": "Estado Día",
            "fecha_registro": "Fecha Registro"
        }

        for col, texto in columnas.items():
            self.tree.heading(col, text=texto)
            self.tree.column(col, anchor="center", width=120)

        scrollbar_vertical = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        scrollbar_horizontal = ttk.Scrollbar(frame_tree, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=scrollbar_vertical.set, xscroll=scrollbar_horizontal.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_vertical.grid(row=0, column=1, sticky="ns")
        scrollbar_horizontal.grid(row=1, column=0, sticky="ew")

        frame_tree.grid_rowconfigure(0, weight=1)
        frame_tree.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.btn_actualizar_estado = tk.Button(self, text="Actualizar Estado", command=self.actualizar_estado)
        self.btn_actualizar_estado.grid(row=1, column=0, pady=10, sticky="w", padx=10)

        self.btn_actualizar_datos = tk.Button(self, text="Actualizar Datos", command=self.cargar_datos)
        self.btn_actualizar_datos.grid(row=1, column=0, pady=10, sticky="e", padx=10)

        self.cargar_datos()

    def cargar_datos(self):
        """Carga los datos de la base de datos en el Treeview"""
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Asegurar que la base de datos refleje los cambios antes de cargar
            self.db_connection.conexion.commit()

            query = "SELECT id_boleta, rut, menu, nombre_menu, registrado, estado_dia, fecha_registro FROM menus_registrados ORDER BY fecha_registro DESC"
            self.db_connection.cursor.execute(query)
            rows = self.db_connection.cursor.fetchall()

            if rows:
                for row in rows:
                    self.tree.insert("", "end", values=row)
            else:
                messagebox.showinfo("Información", "No se encontraron registros.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la tabla.\n{e}")
            print(traceback.format_exc())

    def actualizar_estado(self):
        """Abre una ventana emergente para modificar el estado del día"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un registro para actualizar.")
            return

        item = self.tree.item(selected_item)
        values = item["values"]
        self.id_boleta_seleccionada = values[0]  # Guardar el id_boleta seleccionado

        # Crear ventana emergente para actualizar el estado
        self.ventana_estado = tk.Toplevel(self)
        self.ventana_estado.title("Actualizar Estado")
        self.ventana_estado.geometry("300x200")

        tk.Label(self.ventana_estado, text="Estado Día:").pack(pady=10)

        # Estado actual del día
        estado_actual = values[5]

        # Crear Combobox con valores posibles para el estado
        self.estado_menu = ttk.Combobox(self.ventana_estado, values=["normal", "vacaciones", "licencia", "otro"])
        self.estado_menu.set(estado_actual)  # Establecer el valor actual en el combobox
        self.estado_menu.pack(pady=10)

        tk.Button(self.ventana_estado, text="Guardar", command=self.guardar_estado).pack(pady=10)

    def guardar_estado(self):
        """Guarda el nuevo estado en la base de datos y actualiza solo la fila correspondiente"""
        try:
            # Obtener el valor del Combobox directamente
            nuevo_estado = self.estado_menu.get()

            if not nuevo_estado:
                messagebox.showerror("Error", "Debe seleccionar un estado válido.")
                return

            # Verificar que se haya seleccionado un ID de boleta
            if not hasattr(self, 'id_boleta_seleccionada') or not self.id_boleta_seleccionada:
                messagebox.showerror("Error", "No se ha seleccionado un registro válido para actualizar.")
                return

            print(f"ID Boleta Seleccionada para actualizar: {self.id_boleta_seleccionada}")  # Depuración
            print(f"Nuevo estado seleccionado: {nuevo_estado}")  # Depuración

            if not messagebox.askyesno("Confirmar", "¿Seguro que deseas actualizar el estado?"):
                return

            # Determinar si el estado es distinto de "normal" y cambiar el valor de "registrado"
            if nuevo_estado != "normal":
                registrado = 0
            else:
                registrado = 1  # Si el estado es "normal", dejamos el valor de registrado en 1

            # Actualización en la base de datos
            query = "UPDATE menus_registrados SET estado_dia = %s, registrado = %s WHERE id_boleta = %s"
            self.db_connection.cursor.execute(query, (nuevo_estado, registrado, self.id_boleta_seleccionada))
            filas_afectadas = self.db_connection.cursor.rowcount  # Número de filas afectadas
            self.db_connection.conexion.commit()

            print(f"Filas afectadas por la actualización: {filas_afectadas}")  # Depuración

            if filas_afectadas == 0:
                messagebox.showwarning("Advertencia", "No se encontró el registro a actualizar.")
                return

            # Actualizar solo la fila en el Treeview en lugar de recargar todo
            selected_item = self.tree.selection()[0]
            valores_actualizados = list(self.tree.item(selected_item, "values"))
            valores_actualizados[5] = nuevo_estado  # Modificar el estado en la lista
            valores_actualizados[4] = registrado  # Actualizar el valor de 'registrado'
            self.tree.item(selected_item, values=valores_actualizados)

            self.ventana_estado.destroy()
            messagebox.showinfo("Éxito", "Estado actualizado correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el estado.\n{e}")
            print(traceback.format_exc())

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos al salir"""
        try:
            self.db_connection.desconectar()
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")
        finally:
            self.winfo_toplevel().destroy()