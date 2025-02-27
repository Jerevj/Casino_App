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
        self.ventanas_abiertas = []  # Lista para rastrear ventanas secundarias

        # Manejo del cierre de la ventana principal
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Método para manejar el cierre de la ventana principal y asegurarse de que todo se cierra bien."""
        if not self.cerrando:
            self.cerrando = True  # Evita múltiples ejecuciones de este método
            print("Cerrando la aplicación...")

            # Cerrar todas las ventanas abiertas antes de salir
            for ventana in self.ventanas_abiertas:
                if ventana.winfo_exists():
                    ventana.destroy()

            # Intentar desconectar la base de datos
            try:
                if self.db_connection.conexion:
                    print("Desconectando la base de datos...")
                    self.db_connection.desconectar()
                    print("Base de datos desconectada.")
            except Exception as e:
                print(f"Error al desconectar la base de datos: {e}")

            # Cerrar la ventana principal y detener el bucle de eventos
            self.destroy()
            print("Ventana principal destruida.")
            self.quit()  # Detiene el bucle de eventos de Tkinter
            print("Aplicación cerrada completamente.")

    def modo_usuario(self):
        """Lógica para abrir el modo usuario (panel numérico)."""
        if not any(isinstance(v, VistaUsuario) for v in self.ventanas_abiertas):
            nueva_ventana = tk.Toplevel(self)
            vista_usuario = VistaUsuario(nueva_ventana, self, self.db_connection)
            vista_usuario.pack(fill="both", expand=True)

            self.ventanas_abiertas.append(nueva_ventana)  # Agregar a la lista

            nueva_ventana.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_ventana(nueva_ventana))

    def modo_administrador(self):
        """Lógica para abrir el modo administrador."""
        nueva_ventana = Login(self, self.db_connection)
        self.ventanas_abiertas.append(nueva_ventana)

        nueva_ventana.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_ventana(nueva_ventana))

    def abrir_administracion(self):
        """Lógica para abrir la ventana de administración después de un login exitoso."""
        nueva_ventana = tk.Toplevel(self)
        admin = Administracion(nueva_ventana, self.db_connection)
        admin.pack(fill="both", expand=True)

        self.ventanas_abiertas.append(nueva_ventana)  # Agregar a la lista

        nueva_ventana.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_ventana(nueva_ventana))

    def cerrar_ventana(self, ventana):
        """Método para manejar el cierre de cualquier ventana secundaria."""
        if ventana in self.ventanas_abiertas:
            self.ventanas_abiertas.remove(ventana)
        ventana.destroy()