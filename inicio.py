import tkinter as tk
from tkinter import messagebox
from administracion import Administracion
from vista_usuario import VistaUsuario

class Inicio(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Casino - Selección de Modo")
        self.geometry("400x300+400+200")
        self.resizable(True, True)
        self.config(bg="lightblue")

        # Título
        titulo = tk.Label(self, text="Seleccione el modo de operación", font=("Arial", 14, "bold"), bg="lightblue")
        titulo.pack(pady=20)

        # Botón para modo usuario
        self.btn_usuario = tk.Button(self, text="Modo Usuario", font=("Arial", 12), command=self.modo_usuario, width=20)
        self.btn_usuario.pack(pady=10)

        # Botón para modo administrador
        self.btn_admin = tk.Button(self, text="Modo Administrador", font=("Arial", 12), command=self.modo_administrador, width=20)
        self.btn_admin.pack(pady=10)

        # Variable para controlar si la ventana de modo usuario está abierta
        self.ventana_usuario_abierta = False

    def modo_usuario(self):
        """Lógica para abrir el modo usuario (panel numérico)."""
        if not self.ventana_usuario_abierta:
            self.ventana_usuario_abierta = True  # Marca que la ventana está abierta
            self.btn_usuario.config(state="disabled")  # Deshabilita el botón mientras la ventana está abierta

            nueva_ventana = tk.Toplevel(self)  # Crea una nueva ventana secundaria
            vista_usuario = VistaUsuario(nueva_ventana, self)  # Pasa la nueva ventana y el controlador (self)
            vista_usuario.pack(fill="both", expand=True)  # Empaqueta el frame

            nueva_ventana.protocol("WM_DELETE_WINDOW", self.on_close_usuario)  # Controlar el cierre de la ventana
            nueva_ventana.mainloop()

    def on_close_usuario(self):
        """Método para manejar el cierre de la ventana usuario."""
        self.ventana_usuario_abierta = False  # Marca que la ventana ya se ha cerrado
        self.btn_usuario.config(state="normal")  # Habilita el botón nuevamente

    def modo_administrador(self):
        """Lógica para abrir el modo administrador."""
        self.destroy()  # Cerramos la ventana principal
        app = Administracion()
        app.mainloop()
