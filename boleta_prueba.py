import win32print
import win32ui
import win32con
from datetime import datetime
import random

class Boleta:
    def __init__(self, menu_letra, menu_nombre, nombre_persona, rut_persona):
        self.menu_letra = menu_letra
        self.menu_nombre = menu_nombre
        self.nombre_persona = nombre_persona
        self.rut_persona = rut_persona
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.id_boleta = random.randint(1000, 9999)

    def __str__(self):
        return (f"==============================\n"
                f"          Knop - Casino          \n"
                f"==============================\n"
                f"ID Boleta: {self.id_boleta}\n"
                f"Fecha: {self.fecha}\n"
                f"---------------------------------------------\n"
                f"Nombre: {self.nombre_persona}\n"
                f"RUT: {self.rut_persona}\n"
                f"---------------------------------------------\n"
                f"Menú ({self.menu_letra}): {self.menu_nombre}\n"
                f"==============================\n")

def imprimir_boleta(boleta):
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
        
        # Configurar la fuente
        font = win32ui.CreateFont({
            "name": "Arial",
            "height": -200,  # Tamaño de la fuente (más grande)
            "weight": win32con.FW_BOLD
        })
        hdc.SelectObject(font)
        
        # Imprimir cada línea de la boleta centrada
        y = -100
        for line in str(boleta).split('\n'):
            hdc.TextOut(2000, y, line)  # Ajustar la coordenada x para centrar el texto
            y -= 300  # Reducir el espacio entre líneas
        
        hdc.EndPage()
        hdc.EndDoc()
    finally:
        win32print.ClosePrinter(hprinter)

# Datos de ejemplo
menu_letra = "A"
menu_nombre = "Pollo al horno con ensalada"
nombre_persona = "Juan Pérez"
rut_persona = "12.345.678-9"

# Crear la boleta con los datos de ejemplo
boleta = Boleta(menu_letra, menu_nombre, nombre_persona, rut_persona)

# Imprimir la boleta
imprimir_boleta(boleta)