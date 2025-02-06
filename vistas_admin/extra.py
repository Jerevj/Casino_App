import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import bcrypt

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

        # Botón para agregar un nuevo usuario
        btn_agregar_usuario = tk.Button(self, text="Agregar Nuevo Usuario", command=self.agregar_usuario, font=("Arial", 12))
        btn_agregar_usuario.pack(pady=10)

    def mostrar_menus(self):
        # Lógica para mostrar los menús (igual a lo que tienes actualmente)
        pass

    def agregar_usuario(self):
        # Crear una nueva ventana para agregar el usuario
        ventana_usuario = tk.Toplevel(self)
        ventana_usuario.title("Agregar Nuevo Usuario")
        ventana_usuario.geometry("400x300")

        # Campos de entrada para nombre de usuario y contraseña

        tk.Label(ventana_usuario, text="Nombre Usuario:", font=("Arial", 12)).pack(pady=5)
        entry_usuario = tk.Entry(ventana_usuario, font=("Arial", 12))
        entry_usuario.pack(pady=5)

        tk.Label(ventana_usuario, text="Contraseña:", font=("Arial", 12)).pack(pady=5)
        entry_clave = tk.Entry(ventana_usuario, font=("Arial", 12), show="*")
        entry_clave.pack(pady=5)

        # Botón para guardar el nuevo usuario
        btn_guardar = tk.Button(ventana_usuario, text="Guardar Usuario", command=lambda: self.guardar_usuario(entry_usuario, entry_clave, ventana_usuario), font=("Arial", 12))
        btn_guardar.pack(pady=10)

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

            # Conectar a la base de datos
            conexion = mysql.connector.connect(host="localhost", user="root", password="admin", database="casino")
            cursor = conexion.cursor()

            # Insertar el nuevo usuario en la base de datos
            cursor.execute("INSERT INTO usuarios (usuario, clave) VALUES (%s, %s)", (usuario, hashed_clave))
            conexion.commit()

            # Cerrar la conexión y la ventana
            conexion.close()
            ventana_usuario.destroy()

            messagebox.showinfo("Éxito", "Nuevo usuario agregado correctamente")

        except mysql.connector.Error as err:
            messagebox.showerror("Error de Conexión", f"No se pudo agregar el usuario: {err}")
