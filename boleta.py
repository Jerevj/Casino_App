import win32print
import win32ui
import win32con
from datetime import datetime
import random
import textwrap

class Boleta:
    def __init__(self, menu_letra, menu_nombre, nombre_persona, rut_persona, id_boleta):
        self.menu_letra = menu_letra
        self.menu_nombre = menu_nombre
        self.nombre_persona = nombre_persona
        self.rut_persona = rut_persona
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.id_boleta = id_boleta

    def __str__(self):
        menu_nombre_wrapped = "\n".join(textwrap.wrap(self.menu_nombre, width=30))
        return (f"==============================\n"
                f"          Knop - Casino          \n"
                f"==============================\n"
                f"Menú: {self.menu_letra}\n"
                f"{menu_nombre_wrapped}\n"
                f"---------------------------------------------\n"
                f"Nombre: {self.nombre_persona}\n"
                f"RUT: {self.rut_persona}\n"
                f"---------------------------------------------\n"
                f"Fecha: {self.fecha}\n"
                f"ID Boleta: {self.id_boleta}\n"
                f"==============================\n")

def imprimir_boleta(menu_letra, menu_nombre, nombre_persona, rut_persona, id_boleta):
    boleta = Boleta(menu_letra, menu_nombre, nombre_persona, rut_persona, id_boleta)
    printer_name = win32print.GetDefaultPrinter()
    hprinter = win32print.OpenPrinter(printer_name)
    try:
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(printer_name)
        
        hdc.StartDoc("Boleta")
        hdc.StartPage()
        
        # Ajustar la posición y el tamaño del texto
        hdc.SetMapMode(win32con.MM_TWIPS)
        hdc.SetTextAlign(win32con.TA_CENTER)
        
        # Configurar la fuente para el menú (más grande)
        font_menu = win32ui.CreateFont({
            "name": "Arial",
            "height": -300,  # Tamaño de la fuente (más grande)
            "weight": win32con.FW_BOLD
        })
        
        # Configurar la fuente para el resto del texto
        font_text = win32ui.CreateFont({
            "name": "Arial",
            "height": -200,  # Tamaño de la fuente (estándar)
            "weight": win32con.FW_BOLD
        })
        
        # Imprimir cada línea de la boleta centrada
        y = -100
        for line in str(boleta).split('\n'):
            if "Menú" in line or boleta.menu_nombre in line:
                hdc.SelectObject(font_menu)
            else:
                hdc.SelectObject(font_text)
            hdc.TextOut(2000, y, line)  # Ajustar la coordenada x para centrar el texto
            y -= 300  # Reducir el espacio entre líneas
        
        hdc.EndPage()
        hdc.EndDoc()
    finally:
        win32print.ClosePrinter(hprinter)