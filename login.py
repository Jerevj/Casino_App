import tkinter as tk
from tkinter import messagebox
import bcrypt
import mysql.connector
from administracion import Administracion

class Login(tk.Toplevel):
    def __init__(self, parent, db_connection):
        super().__init__(parent)
        self.db_connection = db_connection  # Guardar la conexión
        self.title("Login Administrador")
        self.geometry("350x200")
        self.resizable(False, False)
        self.config(bg="lightgray")

        # Campos de entrada para usuario y clave
        tk.Label(self, text="Usuario:", font=("Arial", 12), bg="lightgray").pack(pady=5)
        self.entry_usuario = tk.Entry(self, font=("Arial", 12))
        self.entry_usuario.pack(pady=5)

        tk.Label(self, text="Contraseña:", font=("Arial", 12), bg="lightgray").pack(pady=5)
        self.entry_clave = tk.Entry(self, font=("Arial", 12), show="*")
        self.entry_clave.pack(pady=5)

        # Botón de login
        btn_login = tk.Button(self, text="Ingresar", font=("Arial", 12), command=self.verificar_login)
        btn_login.pack(pady=10)

        # Asegurarse de que el cierre de la ventana no cause errores
        self.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)

    def verificar_login(self):
        """Verifica si el usuario y la clave coinciden en la base de datos."""
        usuario = self.entry_usuario.get()
        clave = self.entry_clave.get()

        # Validar que no estén vacíos
        if not usuario or not clave:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            # Usar la conexión pasada desde inicio.py
            cursor = self.db_connection.cursor  # No usar paréntesis aquí
            if cursor is None:
                messagebox.showerror("Error de Conexión", "El cursor de la base de datos no está disponible.")
                return

            cursor.execute("SELECT clave, usuario FROM usuarios WHERE usuario = %s", (usuario,))
            resultado = cursor.fetchone()

            # Si el usuario existe y la clave es correcta
            if resultado and bcrypt.checkpw(clave.encode('utf-8'), resultado[0].encode('utf-8')):
                messagebox.showinfo("Éxito", f"Bienvenido, {resultado[1]}")  # Mostrar nombre del usuario
                self.destroy()  # Cerrar ventana de login

                # Abrir la ventana de administración
                app = Administracion(self.db_connection)  # Pasar la conexión a la administración
                app.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_ventana(app))  # Controlar el cierre de la ventana de administración
                app.deiconify()  # Mostrar la ventana de administración
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {err}")

    def cerrar_ventana(self, app=None):
        """Cierra la ventana sin cerrar la conexión a la base de datos."""
        if app:
            app.destroy()  # Cerrar la ventana de administración si está abierta
        self.destroy()  # Cerrar la ventana de login