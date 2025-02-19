import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import bcrypt
from utils.excel_utils import excel_manager

class Extra(tk.Frame):

    def __init__(self, padre, db_connection):
        super().__init__(padre)
        self.padre = padre
        self.db_connection = db_connection  # Guardar la conexión
        self.menus_ventana_abierta = None  # Variable para controlar la ventana de menús abierta
        self.widgets()

    def widgets(self):
        # Título de la ventana
        mensaje = tk.Label(self, text="¡Ventana Extra cargada correctamente!", font=("Arial", 16))
        mensaje.grid(row=0, column=0, pady=20)

        # Botón para mostrar el Excel ordenado
        btn_mostrar_excel = tk.Button(self, text="Mostrar Menú Actual", command=self.mostrar_menus, font=("Arial", 12))
        btn_mostrar_excel.grid(row=1, column=0, pady=10)

        # Botón para agregar un nuevo usuario
        btn_agregar_usuario = tk.Button(self, text="Agregar Nuevo Usuario", command=self.agregar_usuario, font=("Arial", 12))
        btn_agregar_usuario.grid(row=2, column=0, pady=10)

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
                    # Agregar '/' para separar año, mes y día
                    fecha_str = str(fecha)
                    fecha_formateada = f"{fecha_str[:4]}/{fecha_str[4:6]}/{fecha_str[6:]}"
                    menus_data.append([fecha_formateada, menu_a, menu_b, menu_c])

            if not menus_data:
                raise Exception("No se encontraron menús válidos en el archivo.")

            # Crear una nueva ventana para mostrar la tabla de menús
            ventana_menus = tk.Toplevel(self)
            ventana_menus.title("Menú Actual")
            ventana_menus.geometry("800x600")  # Establecemos el tamaño de la ventana (más grande)

            # Crear el Treeview para mostrar los menús
            tree = ttk.Treeview(ventana_menus, columns=("Fecha", "Menú A", "Menú B", "Menú C"), show="headings", height=15)
            tree.grid(padx=20, pady=20, fill=tk.BOTH, expand=True)

            # Configurar las columnas
            tree.heading("Fecha", text="Fecha (año/mes/dia)", anchor=tk.W)
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
            btn_cerrar.grid(row=0, column=0, pady=10)

            # Guardamos la referencia de la ventana abierta
            self.menus_ventana_abierta = ventana_menus

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar el menú: {e}")

    def agregar_usuario(self):
        # Crear una nueva ventana para agregar el usuario
        ventana_usuario = tk.Toplevel(self)
        ventana_usuario.title("Agregar Nuevo Usuario")
        ventana_usuario.geometry("400x300")

        # Campos de entrada para nombre de usuario y contraseña
        tk.Label(ventana_usuario, text="Nombre Usuario:", font=("Arial", 12)).grid(row=0, column=0, pady=5)
        entry_usuario = tk.Entry(ventana_usuario, font=("Arial", 12))
        entry_usuario.grid(row=0, column=1, pady=5)

        tk.Label(ventana_usuario, text="Contraseña:", font=("Arial", 12)).grid(row=1, column=0, pady=5)
        entry_clave = tk.Entry(ventana_usuario, font=("Arial", 12), show="*")
        entry_clave.grid(row=1, column=1, pady=5)

        # Botón para guardar el nuevo usuario
        btn_guardar = tk.Button(ventana_usuario, text="Guardar Usuario", command=lambda: self.guardar_usuario(entry_usuario, entry_clave, ventana_usuario), font=("Arial", 12))
        btn_guardar.grid(row=2, column=0, columnspan=2, pady=10)

    def guardar_usuario(self, entry_usuario, entry_clave, ventana_usuario):
        # Obtener los valores de los campos
        usuario = entry_usuario.get()
        clave = entry_clave.get()

        # Validar que los campos no estén vacíos
        if not usuario or not clave:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            # Encriptar la contraseña
            hashed_clave = bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt())

            # Insertar el nuevo usuario en la base de datos
            self.db_connection.cursor.execute("INSERT INTO usuarios (usuario, clave) VALUES (%s, %s)", (usuario, hashed_clave))
            self.db_connection.commit()

            # Cerrar la ventana
            ventana_usuario.destroy()

            messagebox.showinfo("Éxito", "Nuevo usuario agregado correctamente")

        except mysql.connector.Error as err:
            messagebox.showerror("Error de Conexión", f"No se pudo agregar el usuario: {err}")