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
        btn_usuario = tk.Button(self, text="Modo Usuario", font=("Arial", 12), command=self.modo_usuario, width=20)
        btn_usuario.pack(pady=10)

        # Botón para modo administrador
        btn_admin = tk.Button(self, text="Modo Administrador", font=("Arial", 12), command=self.modo_administrador, width=20)
        btn_admin.pack(pady=10)

    def modo_usuario(self):
        """Lógica para abrir el modo usuario (panel numérico)."""
        self.destroy()  # Cierra la ventana actual
        app = tk.Tk()  # Crea una nueva ventana principal para el modo usuario
        vista_usuario = VistaUsuario(app, self)  # Pasa la nueva ventana y el controlador (self)
        vista_usuario.pack(fill="both", expand=True)  # Empaqueta el frame
        app.mainloop()
        
        """#Abrir una nueva ventana para el modo usuario sin destruir la ventana principal.
        nueva_ventana = tk.Toplevel(self)  # Crea una nueva ventana secundaria
        vista_usuario = VistaUsuario(nueva_ventana, self)  # Pasa la nueva ventana y el controlador (self)
        vista_usuario.pack()
        nueva_ventana.mainloop()"""

    def modo_administrador(self):
        """Lógica para abrir el modo administrador."""
        self.destroy()  # Cerramos la ventana actual
        app = Administracion()
        app.mainloop()


'''
import tkinter as tk
from tkinter import messagebox
#from administracion import Administracion
from login import Login
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
        btn_usuario = tk.Button(self, text="Modo Usuario", font=("Arial", 12), command=self.modo_usuario, width=20)
        btn_usuario.pack(pady=10)

        # Botón para modo administrador
        btn_admin = tk.Button(self, text="Modo Administrador", font=("Arial", 12), command=self.modo_administrador, width=20)
        btn_admin.pack(pady=10)

    def modo_usuario(self):
        """Lógica para abrir el modo usuario (panel numérico). Manteniendo la conexion"""
        self.destroy()  # Cierra la ventana actual
        app = tk.Tk()  # Crea una nueva ventana principal para el modo usuario
        vista_usuario = VistaUsuario(app, self)  # Pasa la nueva ventana y el controlador (self)
        vista_usuario.pack(fill="both", expand=True)  # Empaqueta el frame
        app.protocol("WM_DELETE_WINDOW", vista_usuario.cerrar_conexion)  # Cerrar conexión al salir
        app.mainloop()
        
        """#Abrir una nueva ventana para el modo usuario sin destruir la ventana principal.
        nueva_ventana = tk.Toplevel(self)  # Crea una nueva ventana secundaria
        vista_usuario = VistaUsuario(nueva_ventana, self)  # Pasa la nueva ventana y el controlador (self)
        vista_usuario.pack()
        nueva_ventana.mainloop()"""

    def modo_administrador(self):
        """Abrir la ventana de login antes de ir a Administración."""
        login_window = Login(self)
        login_window.grab_set()  # Bloquea la ventana principal hasta cerrar el login

'''