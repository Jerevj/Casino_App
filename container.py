from tkinter import *
import tkinter as tk
from vistas_admin.extra import Extra
from vistas_admin.menus import Menus
from vistas_admin.personal import Personal
from vistas_admin.menus_inscritos import Menus_inscritos
from vistas_admin.subir import Subir
from vistas_admin.informes import Informes 
import sys
import os

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0,y=0, width=1100, height=650)
        self.widgets()
        self.frames = {}
        self.buttons = []
        for i in (Menus, Personal, Menus_inscritos, Subir ,Informes, Extra):
            frame = i(self)
            self.frames[i] = frame
            #frame.pack()
            frame.config(bg="#C6D9E3", highlightbackground = "gray", highlightthickness=1)
            frame.place(x=0,y=40, width=1100, height= 650)
        self.show_frames(Menus)
    
    def show_frames(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def menus(self):
        self.show_frames(Menus)

    def menus_inscritos(self):
        self.show_frames(Menus_inscritos)
    
    def personal(self):
        self.show_frames(Personal)
    
    def subir(self):
        self.show_frames(Subir)

    def informes(self):
        self.show_frames(Informes)

    def extra(self):
        self.show_frames(Extra)

    def widgets(self):
        frame2 = tk.Frame(self)
        frame2.place(x=0,y=0,width=1100,height=40)

        self.btn_menus = Button(frame2, fg="black", text="Menus", font="sans 16 bold", command=self.menus)
        self.btn_menus.place(x=0, y=0, width=184, height=40)

        self.btn_personal = Button(frame2, fg="black", text="Personal", font="sans 16 bold", command=self.personal)
        self.btn_personal.place(x=184, y=0, width=184, height=40)

        self.btn_menus_inscritos = Button(frame2, fg="black", text="Menus Inscritos", font="sans 16 bold", command=self.menus_inscritos)
        self.btn_menus_inscritos.place(x=368, y=0, width=184, height=40)

        self.btn_subir = Button(frame2, fg="black", text="Subir", font="sans 16 bold", command=self.subir)
        self.btn_subir.place(x=552, y=0, width=184, height=40)

        self.btn_informes = Button(frame2, fg="black", text="Informes", font="sans 16 bold", command=self.informes)
        self.btn_informes.place(x=736, y=0, width=184, height=40)

        self.btn_extra = Button(frame2, fg="black", text="Extra", font="sans 16 bold", command=self.extra)
        self.btn_extra.place(x=920, y=0, width=184, height=40)

        self.buttons = [self.btn_menus, self.btn_personal, self.btn_menus_inscritos, self.btn_subir, self.btn_informes, self.btn_extra]