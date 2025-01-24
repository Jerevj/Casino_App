from tkinter import *
import tkinter as tk

class Extra(tk.Frame):

    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()

    def widgets(self):
        # Agregar una etiqueta para confirmar que la ventana se muestra
        mensaje = tk.Label(self, text="¡Ventana Extra cargada correctamente!", font=("Arial", 16))
        mensaje.pack(pady=20)  # Añadir un poco de espacio alrededor del texto
