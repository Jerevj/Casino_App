import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils.excel_utils import excel_manager  # Importar la instancia global de ExcelManager

class Menus(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.data = []  # Datos cargados del Excel
        self.column_names = []  # Para almacenar los nombres de las columnas
        self.widgets()
        self.cargar_excel()  # Llamada a la función para cargar los datos al inicio

    def widgets(self):
        # Título de la ventana
        titulo = tk.Label(self, text="Gestión de Menús", font=("Arial", 20, "bold"))
        titulo.pack(pady=20)

        # Frame principal que contiene el canvas y los scrollbars
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar horizontal (lo colocamos arriba)
        self.scrollbar_horizontal = ttk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL)
        self.scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)

        # Canvas para manejar el desplazamiento
        self.canvas = tk.Canvas(self.main_frame, xscrollcommand=self.scrollbar_horizontal.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame dentro del canvas donde estará la tabla
        self.table_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        # Scrollbar vertical
        self.scrollbar_vertical = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL)
        self.scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind para actualizar la región del canvas
        self.table_frame.bind("<Configure>", self.on_frame_configure)

    def cargar_excel(self):
        """Cargar datos desde el Excel y mostrar en la tabla."""
        try:
            sheet = excel_manager.obtener_sheet()  # Obtener la hoja de empleados
            if not sheet:
                raise Exception("No se pudo obtener la hoja de empleados.")

            self.data = []  # Reiniciar datos
            self.column_names = []  # Reiniciar nombres de columnas

            # Obtener los encabezados (nombres de las columnas) de la primera fila
            headers = next(sheet.iter_rows(min_row=1, max_row=1, values_only=True))
            self.column_names = headers  # Asignar los encabezados a column_names
            self.tree = ttk.Treeview(self.table_frame, show="headings", columns=self.column_names, height=20)

            # Configurar las columnas
            for col in self.column_names:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100, anchor=tk.CENTER)

            # Insertar las filas de datos en la tabla
            for row in sheet.iter_rows(min_row=2, values_only=True):
                self.data.append(row)
                self.tree.insert("", "end", values=row)

            # Mostrar la tabla
            self.tree.pack(fill=tk.BOTH, expand=True)

            # Vincular el scrollbar horizontal con el canvas
            self.scrollbar_horizontal.config(command=self.canvas.xview)

            # Vincular el scrollbar vertical con el Treeview
            self.tree.config(yscrollcommand=self.scrollbar_vertical.set)
            self.scrollbar_vertical.config(command=self.tree.yview)

        except Exception as e:
            print(f"Error al cargar el Excel: {e}")
            messagebox.showerror("Error", f"No se pudo cargar el archivo Excel. {e}")

    def on_frame_configure(self, event):
        """Actualizar la región del canvas cuando el frame cambia de tamaño."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # Vincular el scrollbar horizontal
        self.scrollbar_horizontal.config(command=self.canvas.xview)
