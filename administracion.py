from tkinter import *
from tkinter import ttk
#from login import Login
#from login import Registro
from container import Container
import sys
import os

class Administracion(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Administracion Casino")
        self.geometry("1100x650+120+20")
        self.resizable(True, True)

        container = Frame(self)
        container.pack(side=TOP, fill=BOTH, expand=True)
        container.configure(bg="lightblue")

        self.frames = {}
        frame = Container(container, self)
        self.frames[Container] = frame
        frame.pack(fill=BOTH, expand=True)

        self.show_frame(Container)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        '''self.frames = {}
        for i in (Login, Registro, Container):
            frame = i(container, self)
            self.frames[i]= frame'''

        # Manejo del cierre de la ventana de administración
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Método para manejar el cierre de la ventana de administración."""
        self.quit()  # Termina el mainloop y cierra la aplicación

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

def main():
    app = Administracion()
    app.mainloop()

if __name__ == "__main__":
    main()