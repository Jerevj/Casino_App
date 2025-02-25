from tkinter import *
from tkinter import ttk
from container import Container

class Administracion(Tk):
    def __init__(self, db_connection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_connection = db_connection  # Guardar la conexión
        self.title("Administracion Casino")
        self.geometry("1100x650+120+20")
        self.resizable(True, True)

        container = Frame(self)
        container.pack(side=TOP, fill=BOTH, expand=True)
        container.configure(bg="lightblue")

        self.frames = {}
        frame = Container(container, self, self.db_connection)
        self.frames[Container] = frame
        frame.pack(fill=BOTH, expand=True)

        self.show_frame(Container)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Manejo del cierre de la ventana de administración
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Método para manejar el cierre de la ventana de administración."""
        self.destroy()  # solo cierra la ventana

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()