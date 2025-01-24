# utils/excel_utils.py
import openpyxl
from tkinter import messagebox

class ExcelManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.wb = None
        self.sheet = None
        self.menu_sheet = None
        self.cargar_archivo()

    def cargar_archivo(self):
        """Cargar el archivo de Excel y devolver las hojas."""
        try:
            self.wb = openpyxl.load_workbook(self.file_path)
            self.sheet = self.wb['Hoja1']
            self.menu_sheet = self.wb['Hoja2']
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            messagebox.showerror("Error", "Hubo un problema al cargar el archivo de Excel.")

    def obtener_wb(self):
        """Retorna el libro de trabajo cargado."""
        return self.wb

    def obtener_sheet(self):
        """Retorna la hoja de empleados."""
        return self.sheet

    def obtener_menu_sheet(self):
        """Retorna la hoja de menús."""
        return self.menu_sheet

# Crear una instancia global para reutilizarla
file_path = "C:/Users/practicainformatica/Desktop/CarpetaExcel/Minuta_Diciembre_24.xlsx"
excel_manager = ExcelManager(file_path)
