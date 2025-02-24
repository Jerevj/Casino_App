import tkinter as tk
from tkinter import messagebox
from administracion import Administracion
from vista_usuario import VistaUsuario
from login import Login

class Inicio(tk.Tk):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection  # Guardar la conexión
        self.title("Casino - Selección de Modo")
        self.geometry("400x300+400+200")
        self.resizable(True, True)
        self.config(bg="lightblue")

        # Inicializar la variable para evitar múltiples cierres
        self.cerrando = False
        
        # Título
        titulo = tk.Label(self, text="Seleccione el modo de operación", font=("Arial", 14, "bold"), bg="lightblue")
        titulo.pack(pady=20)

        # Botón para modo usuario
        self.btn_usuario = tk.Button(self, text="Modo Usuario", font=("Arial", 12), command=self.modo_usuario, width=20)
        self.btn_usuario.pack(pady=10)

        # Botón para modo administrador
        self.btn_admin = tk.Button(self, text="Modo Administrador", font=("Arial", 12), command=self.modo_administrador, width=20)
        self.btn_admin.pack(pady=10)

        # Variables para controlar si las ventanas están abiertas
        self.ventana_usuario_abierta = False
        self.ventana_admin_abierta = False

        # Manejo del cierre de la ventana principal
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Método para manejar el cierre de la ventana principal."""
        if not self.cerrando:
            self.cerrando = True
            self.db_connection.desconectar()  # Desconectar la base de datos al cerrar la aplicación
            self.quit()  # Termina el mainloop y cierra la aplicación

    def modo_usuario(self):
        """Lógica para abrir el modo usuario (panel numérico)."""
        if not self.ventana_usuario_abierta:
            self.ventana_usuario_abierta = True  # Marca que la ventana está abierta
            self.btn_usuario.config(state="disabled")  # Deshabilita el botón mientras la ventana está abierta

            nueva_ventana = tk.Toplevel(self)  # Crea una nueva ventana secundaria
            vista_usuario = VistaUsuario(nueva_ventana, self, self.db_connection)  # Pasa la nueva ventana, el controlador (self) y la conexión
            vista_usuario.pack(fill="both", expand=True)  # Empaqueta el frame

            nueva_ventana.protocol("WM_DELETE_WINDOW", lambda: self.on_close_usuario(nueva_ventana))  # Controlar el cierre de la ventana

    def on_close_usuario(self, ventana):
        """Método para manejar el cierre de la ventana usuario."""
        ventana.destroy()  # Destruye la ventana
        self.ventana_usuario_abierta = False  # Marca que la ventana ya se ha cerrado
        self.btn_usuario.config(state="normal")  # Habilita el botón nuevamente

    def modo_administrador(self):
        """Lógica para abrir el modo administrador."""
        if not self.ventana_admin_abierta:
            self.ventana_admin_abierta = True  # Marca que la ventana está abierta
            self.btn_admin.config(state="disabled")  # Deshabilita el botón mientras la ventana está abierta

            nueva_ventana = Login(self, self.db_connection)  # Crea una nueva ventana de login
            nueva_ventana.protocol("WM_DELETE_WINDOW", lambda: self.on_close_admin(nueva_ventana))  # Controlar el cierre de la ventana

    def on_close_admin(self, ventana):
        """Método para manejar el cierre de la ventana administrador."""
        ventana.destroy()  # Destruye la ventana
        self.ventana_admin_abierta = False  # Marca que la ventana ya se ha cerrado
        self.btn_admin.config(state="normal")  # Habilita el botón nuevamente