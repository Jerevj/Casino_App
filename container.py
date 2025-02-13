from tkinter import *
import tkinter as tk
from vistas_admin.extra import Extra
from vistas_admin.minutas import Minutas
from vistas_admin.personal import Personal
from vistas_admin.menus_inscritos import MenusInscritos
from vistas_admin.subir import Subir
from vistas_admin.informes import Informes 
import sys
import os

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.grid(row=0, column=0, sticky="nsew")  # Usamos grid para el contenedor principal

        self.frames = {}
        self.buttons = []

        # Crea el navbar usando un Frame
        frame_navbar = tk.Frame(self, bg="lightblue")
        frame_navbar.grid(row=0, column=0, sticky="ew")  # Coloca el navbar en la primera fila

        # Aquí vamos a colocar los botones en una sola fila en el navbar
        self.btn_Minutas = Button(frame_navbar, fg="black", text="Minutas", font="sans 16 bold", command=self.Minutas)
        self.btn_Minutas.grid(row=0, column=0, sticky="ew")  # Usamos grid para cada botón

        self.btn_personal = Button(frame_navbar, fg="black", text="Personal", font="sans 16 bold", command=self.personal)
        self.btn_personal.grid(row=0, column=1, sticky="ew")

        self.btn_menus_inscritos = Button(frame_navbar, fg="black", text="Menus Inscritos", font="sans 16 bold", command=self.menus_inscritos)
        self.btn_menus_inscritos.grid(row=0, column=2, sticky="ew")

        self.btn_subir = Button(frame_navbar, fg="black", text="Subir", font="sans 16 bold", command=self.subir)
        self.btn_subir.grid(row=0, column=3, sticky="ew")

        self.btn_informes = Button(frame_navbar, fg="black", text="Informes", font="sans 16 bold", command=self.informes)
        self.btn_informes.grid(row=0, column=4, sticky="ew")
        self.btn_extra = Button(frame_navbar, fg="black", text="Extra", font="sans 16 bold", command=self.extra)
        self.btn_extra.grid(row=0, column=5, sticky="ew")

        # Ahora configuramos el contenedor principal para que los frames (contenido) se ajusten correctamente
        self.frames = {}
        for i in (Minutas, Personal, MenusInscritos, Subir, Informes, Extra):
            frame = i(self)
            self.frames[i] = frame
            frame.grid(row=1, column=0, sticky="nsew")  # Contenido debajo del navbar
        self.show_frames(Minutas)

        # Hacemos que las filas y columnas se expandan
        self.grid_rowconfigure(0, weight=0)  # La primera fila (navbar) no se expande
        self.grid_rowconfigure(1, weight=1)  # La segunda fila (contenido) se expande
        self.grid_columnconfigure(0, weight=1)  # Columna 0 (todo el ancho)

        # Configuramos las columnas del navbar para que se expandan
        for i in range(6):  # Se asume que hay 6 botones
            frame_navbar.grid_columnconfigure(i, weight=1)  # Asignamos el mismo peso a cada columna del navbar

    def show_frames(self, container):
        frame = self.frames[container]
        frame.tkraise()
        # Asegurarse de recargar los datos cuando se muestra el frame
        '''if hasattr(frame, 'cargar_minutas'):
            frame.cargar_minutas()
        elif hasattr(frame, 'cargar_personal'):
            frame.cargar_personal()'''

    def Minutas(self):
        self.show_frames(Minutas)

    def menus_inscritos(self):
        self.show_frames(MenusInscritos)

    def personal(self):
        self.show_frames(Personal)

    def subir(self):
        self.show_frames(Subir)

    def informes(self):
        self.show_frames(Informes)

    def extra(self):
        self.show_frames(Extra)

'''    def widgets(self):
        navbar = Frame(self, bg="#ddd")
        navbar.grid(row=0, column=0, sticky="ew")

        buttons = [
            ("Menus", Menus),
            ("Personal", Personal),
            ("Menus Inscritos", MenusInscritos),
            ("Subir", Subir),
            ("Informes", Informes),
            ("Extra", Extra),
        ]

        for idx, (text, frame) in enumerate(buttons):
            btn = Button(navbar, text=text, command=lambda f=frame: self.show_frame(f))
            btn.grid(row=0, column=idx, padx=2, pady=2)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)'''