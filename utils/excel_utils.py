import openpyxl
from tkinter import messagebox
import pandas as pd

class ExcelManager:
    def __init__(self, minuta_file_path, menus_file_path):
        self.minuta_file_path = minuta_file_path
        self.menus_file_path = menus_file_path
        self.minuta_wb = None
        self.menus_wb = None
        self.minuta_sheet = None
        self.menus_sheet = None
        self.cargar_archivos()

    def cargar_archivos(self):
        """Cargar ambos archivos de Excel."""
        try:
            # Cargar el archivo 'Minuta_Actual'
            self.minuta_wb = openpyxl.load_workbook(self.minuta_file_path)
            self.minuta_sheet = self.minuta_wb.active  # Suposición: la hoja activa contiene los datos de minuta

            # Cargar el archivo 'Menus'
            self.menus_wb = openpyxl.load_workbook(self.menus_file_path)
            self.menus_sheet = self.menus_wb.active  # Suposición: la hoja activa contiene los menús

        except Exception as e:
            print(f"Error al cargar los archivos de Excel: {e}")
            messagebox.showerror("Error", "Hubo un problema al cargar los archivos de Excel.")

    def obtener_minuta_wb(self):
        """Retorna el libro de trabajo de Minuta."""
        return self.minuta_wb

    def obtener_menus_wb(self):
        """Retorna el libro de trabajo de Menús."""
        return self.menus_wb

    def obtener_minuta_sheet(self):
        """Retorna la hoja de datos de empleados y menús seleccionados."""
        return self.minuta_sheet

    def obtener_menus_sheet(self):
        """Retorna la hoja de menús disponibles."""
        return self.menus_sheet

    '''def obtener_menu_desde_excel(self, rut, dia):
        """Obtiene el menú de un empleado según el RUT y el día del mes desde 'Minuta_Actual.xlsx'."""
        try:
            df = pd.read_excel(self.minuta_file_path, dtype=str)

            fila = df[df.iloc[:, 0] == rut]  # Asumiendo que la primera columna es RUT
            if fila.empty:
                print(f"RUT {rut} no encontrado en el Excel.")
                return None
            
            columna_dia = str(dia)
            if columna_dia not in df.columns:
                print(f"No se encontró la columna para el día {dia}.")
                return None

            menu = fila[columna_dia].values[0]
            return menu

        except Exception as e:
            print(f"Error al leer el Excel: {e}")
            return None'''
    def obtener_menu_desde_excel(self, rut, dia):
        """Obtiene el menú de un empleado según el RUT y el día del mes desde 'Minuta_Actual.xlsx'."""
        try:
            df = pd.read_excel(self.minuta_file_path, header=0, dtype=str)
            
            # Imprimir todo el dataframe para inspección
            print(df)

            # Limpiar posibles espacios en los nombres de las columnas
            df.columns = df.columns.str.strip()

            print("Encabezados de columnas:", df.columns.tolist())  # Imprime las columnas para depuración

            fila = df[df['Rut'] == rut]  # Asegúrate de que 'Rut' esté presente en las columnas
            if fila.empty:
                print(f"RUT {rut} no encontrado en el Excel.")
                return None
            
            # Asegurarse de que el día esté presente como columna
            columna_dia = str(dia)  # Asegúrate de que sea un string
            if columna_dia not in df.columns:
                print(f"No se encontró la columna para el día {dia}.")
                return None

            menu = fila[columna_dia].values[0]
            return menu

        except Exception as e:
            print(f"Error al leer el Excel: {e}")
            return None







# Instanciamos el objeto global
excel_manager = ExcelManager(
    "C:/Users/practicainformatica/Desktop/CarpetaExcel/Minuta_Actual.xlsx", 
    "C:/Users/practicainformatica/Desktop/CarpetaExcel/Menus_Actual.xlsx"
)
