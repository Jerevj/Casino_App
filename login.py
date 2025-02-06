import tkinter as tk
from tkinter import messagebox
import mysql.connector
import bcrypt
from administracion import Administracion

class Login(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
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

    def verificar_login(self):
        """Verifica si el usuario y la clave coinciden en la base de datos."""
        usuario = self.entry_usuario.get()
        clave = self.entry_clave.get()

        # Validar que no estén vacíos
        if not usuario or not clave:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            # Conectar a la base de datos
            conexion = mysql.connector.connect(host="localhost", user="root", password="admin", database="casino")
            cursor = conexion.cursor()

            # Consultar la clave del usuario en la base de datos
            cursor.execute("SELECT clave, usuario FROM usuarios WHERE usuario = %s", (usuario,))
            resultado = cursor.fetchone()
            conexion.close()

            # Si el usuario existe y la clave es correcta
            if resultado and bcrypt.checkpw(clave.encode('utf-8'), resultado[0].encode('utf-8')):
                messagebox.showinfo("Éxito", f"Bienvenido, {resultado[1]}")  # Mostrar nombre del usuario
                self.destroy()  # Cerrar ventana de login
                self.master.destroy()  # Cerrar ventana principal
                app = Administracion()  # Abrir la administración
                app.mainloop()  # Ejecutar la aplicación
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {err}")
