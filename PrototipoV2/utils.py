'''
import openpyxl
from tkinter import messagebox

file_path = 'Minuta_Diciembre_24.xlsx'

def cargar_archivo():
    """Cargar el archivo de Excel y devolver las hojas."""
    try:
        wb = openpyxl.load_workbook(file_path)
        sheet = wb['Hoja1']
        menu_sheet = wb['Hoja2']
        return wb, sheet, menu_sheet
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        messagebox.showerror("Error", "Hubo un problema al cargar el archivo de Excel.")
        return None, None, None

def obtener_wb():
    """Retorna el libro de trabajo cargado."""
    wb, _, _ = cargar_archivo()
    return wb

def obtener_sheet():
    """Retorna la hoja de empleados."""
    _, sheet, _ = cargar_archivo()
    return sheet

def obtener_menu_sheet():
    """Retorna la hoja de menús."""
    _, _, menu_sheet = cargar_archivo()
    return menu_sheet

'''
import openpyxl
from tkinter import messagebox

file_path = 'Minuta_Diciembre_24.xlsx'

def cargar_archivo():
    """Cargar el archivo de Excel y devolver las hojas."""
    try:
        wb = openpyxl.load_workbook(file_path)
        sheet = wb['Hoja1']
        menu_sheet = wb['Hoja2']
        return wb, sheet, menu_sheet
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        messagebox.showerror("Error", "Hubo un problema al cargar el archivo de Excel.")
        return None, None, None

# Guardar el libro de trabajo y las hojas en variables globales
wb, sheet, menu_sheet = cargar_archivo()

def obtener_wb():
    """Retorna el libro de trabajo cargado."""
    return wb

def obtener_sheet():
    """Retorna la hoja de empleados."""
    return sheet

def obtener_menu_sheet():
    """Retorna la hoja de menús."""
    return menu_sheet
