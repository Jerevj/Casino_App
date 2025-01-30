import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils.excel_utils import excel_manager  # Instancia global para manejar Excel

class Minutas(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.data = []  # Datos cargados del Excel
        self.column_names = ['Día', 'Menú A', 'Menú B', 'Menú C']  # Definir los nombres de las columnas
        self.widgets()
        self.cargar_minutas()  # Llamada a la función para cargar los datos al inicio

    def widgets(self):
        # Título de la ventana
        titulo = tk.Label(self, text="Gestión de Minutas", font=("Arial", 20, "bold"))
        titulo.pack(pady=20)

        # Frame principal que contiene la tabla y los Scrollbars
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar vertical (directamente vinculado al Treeview)
        self.scrollbar_vertical = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL)
        self.scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)

        # Scrollbar horizontal (también vinculado directamente al Treeview)
        self.scrollbar_horizontal = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)

        # Frame que contendrá la tabla
        self.table_frame = tk.Frame(self.main_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

    def cargar_minutas(self):
        """Cargar las minutas desde el archivo Excel y mostrar en la tabla."""
        try:
            sheet = excel_manager.obtener_minuta_sheet()  # Obtener la hoja de minutas
            if not sheet:
                raise Exception("No se pudo obtener la hoja de minutas.")

            rows = list(sheet.iter_rows(values_only=True))  # Obtener todas las filas
            if not rows:
                raise Exception("El archivo está vacío o mal estructurado.")

            self.data = []  # Reiniciar datos

            # Obtener los encabezados
            self.column_names = rows[0]  # Primera fila como encabezado

            # Si ya existe un Treeview, eliminarlo antes de crear uno nuevo
            for widget in self.table_frame.winfo_children():
                widget.destroy()

            # Crear el nuevo Treeview
            self.tree = ttk.Treeview(
                self.table_frame, 
                show="headings", 
                columns=self.column_names, 
                height=25
            )
            self.tree.pack(fill=tk.BOTH, expand=True)

            # Conectar los scrollbars al Treeview
            self.scrollbar_vertical.config(command=self.tree.yview)
            self.scrollbar_horizontal.config(command=self.tree.xview)
            self.tree.configure(yscrollcommand=self.scrollbar_vertical.set, xscrollcommand=self.scrollbar_horizontal.set)

            # Crear las columnas con los encabezados
            for col in self.column_names:
                self.tree.heading(col, text=col)
                self.tree.column(col, anchor="center", width=130)  # Ancho de columnas

            # Insertar filas
            for row in rows[1:]:  # Saltar la primera fila (encabezados)
                self.tree.insert('', 'end', values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar las minutas desde el archivo: {e}")

    '''def cargar_minutas(self):
        """Cargar las minutas desde el archivo Excel y mostrar en la tabla."""
        try:
            sheet = excel_manager.obtener_minuta_sheet()  # Obtener la hoja de minutas
            if not sheet:
                raise Exception("No se pudo obtener la hoja de minutas.")

            self.data = []  # Reiniciar datos

            # Obtener los encabezados (nombres de las columnas) de la primera fila
            headers = next(sheet.iter_rows(min_row=1, max_row=1, values_only=True))
            self.column_names = headers  # Asignar los encabezados a column_names

            # Si ya existe un Treeview, eliminarlo antes de crear uno nuevo
            for widget in self.table_frame.winfo_children():
                widget.destroy()

            # Crear el nuevo Treeview
            self.tree = ttk.Treeview(
                self.table_frame, 
                show="headings", 
                columns=self.column_names, 
                height=25
            )
            self.tree.pack(fill=tk.BOTH, expand=True)

            # Conectar los scrollbars al Treeview
            self.scrollbar_vertical.config(command=self.tree.yview)
            self.scrollbar_horizontal.config(command=self.tree.xview)

            self.tree.configure(
                yscrollcommand=self.scrollbar_vertical.set, 
                xscrollcommand=self.scrollbar_horizontal.set
            )

            # Crear las columnas con los encabezados
            for col in self.column_names:
                self.tree.heading(col, text=col)
                self.tree.column(col, anchor="center", width=130)  # Aumentamos el ancho de columnas

            # Cargar las filas con las minutas
            for row in sheet.iter_rows(min_row=2, values_only=True):
                self.tree.insert('', 'end', values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar las minutas desde el archivo: {e}")
'''