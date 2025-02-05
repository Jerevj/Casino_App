import tkinter as tk
from tkinter import messagebox, ttk
from utils.excel_utils import excel_manager  # Importamos el ExcelManager

class Extra(tk.Frame):

    def __init__(self, padre):
        super().__init__(padre)
        self.padre = padre
        self.menus_ventana_abierta = None  # Variable para controlar la ventana de menús abierta
        self.widgets()

    def widgets(self):
        # Título de la ventana
        mensaje = tk.Label(self, text="¡Ventana Extra cargada correctamente!", font=("Arial", 16))
        mensaje.pack(pady=20)

        # Botón para mostrar el Excel ordenado
        btn_mostrar_excel = tk.Button(self, text="Mostrar Menú Actual", command=self.mostrar_menus, font=("Arial", 12))
        btn_mostrar_excel.pack(pady=10)


    def mostrar_menus(self):
        # Verificar si la ventana de menús ya está abierta
        if self.menus_ventana_abierta and self.menus_ventana_abierta.winfo_exists():
            # Si la ventana ya está abierta, traerla al frente
            self.menus_ventana_abierta.lift()
            return

        try:
            # Cargar el archivo de Excel usando ExcelManager
            menus_ws = excel_manager.menus_ws
            if menus_ws is None:
                raise Exception("No se pudo cargar el archivo 'Menus_Actual.xlsx'.")

            # Obtener los datos de los menús
            menus_data = []
            for row in menus_ws.iter_rows(min_row=2, values_only=True):  # Comenzamos desde la segunda fila
                fecha = row[0]
                menu_a = row[1] if row[1] else 'N/A'
                menu_b = row[2] if row[2] else 'N/A'
                menu_c = row[3] if row[3] else 'N/A'

                # Solo agregar filas que tengan al menos un menú válido
                if menu_a != 'N/A' or menu_b != 'N/A' or menu_c != 'N/A':
                    menus_data.append([fecha, menu_a, menu_b, menu_c])

            if not menus_data:
                raise Exception("No se encontraron menús válidos en el archivo.")

            # Crear una nueva ventana para mostrar la tabla de menús
            ventana_menus = tk.Toplevel(self)
            ventana_menus.title("Menú Actual")
            ventana_menus.geometry("800x600")  # Establecemos el tamaño de la ventana (más grande)

            # Crear el Treeview para mostrar los menús
            tree = ttk.Treeview(ventana_menus, columns=("Fecha", "Menú A", "Menú B", "Menú C"), show="headings", height=15)
            tree.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

            # Configurar las columnas
            tree.heading("Fecha", text="Fecha", anchor=tk.W)
            tree.heading("Menú A", text="Menú A", anchor=tk.W)
            tree.heading("Menú B", text="Menú B", anchor=tk.W)
            tree.heading("Menú C", text="Menú C", anchor=tk.W)

            # Configurar el ancho de las columnas y la alineación
            tree.column("Fecha", width=150, anchor=tk.W)
            tree.column("Menú A", width=100, anchor=tk.W)
            tree.column("Menú B", width=100, anchor=tk.W)
            tree.column("Menú C", width=100, anchor=tk.W)

            # Aumentar el tamaño de la fuente en el Treeview
            style = ttk.Style()
            style.configure("Treeview", font=("Arial", 12))  # Fuente más grande para la tabla

            # Insertar los datos en el Treeview
            for menu in menus_data:
                tree.insert("", "end", values=menu)

            # Añadir un botón para cerrar la ventana de la tabla
            btn_cerrar = tk.Button(ventana_menus, text="Cerrar", command=ventana_menus.destroy, font=("Arial", 12))
            btn_cerrar.pack(pady=10)

            # Guardamos la referencia de la ventana abierta
            self.menus_ventana_abierta = ventana_menus

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar el menú: {e}")
