# utils/excel_utils.py

from openpyxl import load_workbook
from tkinter import messagebox

class ExcelManager:
    def __init__(self, minuta_file_path, menus_file_path):
        self.minuta_file_path = minuta_file_path
        self.menus_file_path = menus_file_path
        self.minuta_wb = None
        self.menus_wb = None
        self.minuta_ws = None
        self.menus_ws = None
        self.cargar_archivos()

    def cargar_archivos(self):
        """Carga los archivos de Excel usando openpyxl."""
        try:
            self.minuta_wb = load_workbook(self.minuta_file_path)
            self.minuta_ws = self.minuta_wb.active  # Asumimos que los datos están en la primera hoja
        except Exception as e:
            print(f"Error al cargar 'Minuta_Actual.xlsx': {e}")
            messagebox.showerror("Error", "No se pudo cargar el archivo 'Minuta_Actual.xlsx'.")
            self.minuta_wb = None
        
        try:
            self.menus_wb = load_workbook(self.menus_file_path)
            self.menus_ws = self.menus_wb.active  # Asumimos que los menús están en la primera hoja
        except Exception as e:
            print(f"Error al cargar 'Menus_Actual.xlsx': {e}")
            messagebox.showerror("Error", "No se pudo cargar el archivo 'Menus_Actual.xlsx'.")
            self.menus_wb = None

    def obtener_menu_desde_excel(self, rut, dia):
        """Obtiene la opción de menú (A, B, C) de un empleado según el RUT y el día del mes desde 'Minuta_Actual.xlsx'."""
        if self.minuta_ws is None:
            print("El archivo 'Minuta_Actual.xlsx' no está cargado correctamente.")
            return None
        
        # Buscar la fila con el RUT correspondiente
        for row in self.minuta_ws.iter_rows(min_row=2, values_only=True):  # Asumimos que la primera fila es el encabezado
            if str(row[0]) == str(rut):  # Comparar el RUT
                columna_dia = str(dia)  # Asegurar que el día sea string
                # Buscar el día en los encabezados
                for col_num, cell in enumerate(list(self.minuta_ws.iter_rows(min_row=1, max_row=1, values_only=True))[0]):
                    if str(cell) == columna_dia:  # Buscar el día en los encabezados
                        menu = row[col_num]  # Obtener la opción A, B o C
                        if menu:
                            return menu
                        else:
                            print(f"No hay menú asignado para el RUT {rut} el día {dia}.")
                            return None
        print(f"RUT {rut} no encontrado en el Excel.")
        return None

    def obtener_nombre_menu(self, dia, opcion_menu):
        """Obtiene el nombre del menú a partir de la opción (A, B o C) desde 'Menus_Actual.xlsx'."""
        if self.menus_ws is None:
            print("El archivo 'Menus_Actual.xlsx' no está cargado correctamente.")
            return None
        
        # Buscar la opción (A, B o C) en las filas y devolver el nombre del menú
        for row in self.menus_ws.iter_rows(min_row=2, values_only=True):  # Asumimos que la primera fila es el encabezado
            fecha = str(row[0])  # Convertir la fecha a string para evitar problemas de formato
            print(f"Fecha en la fila: {fecha}")  # Depuración de la fecha
            
            # Verificar que la fecha tenga al menos 2 caracteres antes de intentar extraer el día
            if len(fecha) < 2:
                print(f"Fecha inválida en la fila: {fecha}. Saltando esta fila.")
                continue  # Saltar filas con fechas inválidas
            
            try:
                dia_mes_menu = int(fecha[-2:])  # Extraer los dos últimos dígitos (día del mes)
            except ValueError:
                print(f"Fecha no válida en la fila: {fecha}. No se puede extraer el día.")
                continue  # Si no se puede convertir los últimos dos dígitos a entero, saltamos la fila
            
            # Comparar el día del mes con el día actual (dia_mes)
            if dia_mes_menu == dia:
                # Buscar la opción A, B o C
                if opcion_menu == 'A':
                    return row[2]  # El nombre del menú A está en la tercera columna
                elif opcion_menu == 'B':
                    return row[3]  # El nombre del menú B está en la cuarta columna
                elif opcion_menu == 'C':
                    return row[4]  # El nombre del menú C está en la quinta columna
                else:
                    print(f"Opción de menú {opcion_menu} no válida.")
                    return None  # Si la opción no es A, B o C
        print(f"Menú con opción {opcion_menu} no encontrado para el día {dia}.")
        return None



# Crear la instancia global de ExcelManager
excel_manager = ExcelManager(
    "C:/Users/practicainformatica/Desktop/CarpetaExcel/Minuta_Actual.xlsx", 
    "C:/Users/practicainformatica/Desktop/CarpetaExcel/Menus_Actual.xlsx"
)
