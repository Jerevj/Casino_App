import filecmp
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import pandas as pd
import openpyxl
from config import BACKUP_FOLDER
from utils.excel_utils import excel_manager

class Subir(tk.Frame):
    def __init__(self, parent, db_connection):
        super().__init__(parent)
        self.db_connection = db_connection  # Guardar la conexión
        self.minuta_file_path = None
        self.menus_file_path = None
        self.current_minuta_file = excel_manager.obtener_ruta_minuta()
        self.current_menus_file = excel_manager.obtener_ruta_menus()
        self.backup_folder = BACKUP_FOLDER
        self.widgets()

    def widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        titulo = tk.Label(self, text="Subir archivos Excel", font=("Arial", 20, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=20)

        # Botones para seleccionar archivos
        boton_seleccionar_minuta = tk.Button(self, text="📂 Seleccionar Minuta", command=self.seleccionar_archivo_minuta, font=("Arial", 12))
        boton_seleccionar_minuta.grid(row=1, column=0, padx=20, pady=10, sticky="e")

        boton_seleccionar_menus = tk.Button(self, text="📂 Seleccionar Menús", command=self.seleccionar_archivo_menus, font=("Arial", 12))
        boton_seleccionar_menus.grid(row=2, column=0, padx=20, pady=10, sticky="e")

        # Botones para subir archivos
        boton_subir_minuta = tk.Button(self, text="⬆ Subir Minuta", command=self.cargar_minuta, font=("Arial", 12), bg="#4CAF50", fg="white")
        boton_subir_minuta.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        boton_subir_menus = tk.Button(self, text="⬆ Subir Menús", command=self.cargar_menus, font=("Arial", 12), bg="#4CAF50", fg="white")
        boton_subir_menus.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        # Botones para guardar respaldo
        boton_guardar_respaldo_minuta = tk.Button(self, text="💾 Guardar Respaldo Minuta", command=self.guardar_respaldo_minuta, font=("Arial", 12), bg="#2196F3", fg="white")
        boton_guardar_respaldo_minuta.grid(row=3, column=0, pady=10, sticky="e")

        boton_guardar_respaldo_menus = tk.Button(self, text="💾 Guardar Respaldo Menús", command=self.guardar_respaldo_menus, font=("Arial", 12), bg="#2196F3", fg="white")
        boton_guardar_respaldo_menus.grid(row=3, column=1, pady=10, sticky="w")

        # Etiqueta para mostrar el estado de los archivos
        self.label_archivos = tk.Label(self, text="No se han seleccionado archivos.", font=("Arial", 12), fg="gray")
        self.label_archivos.grid(row=4, column=0, columnspan=2, pady=15)

    def seleccionar_archivo_minuta(self):
        """Selecciona el archivo de Minuta y actualiza la ruta."""
        file_path = filedialog.askopenfilename(title="Seleccionar archivo Minuta", filetypes=[("Archivos de Excel", "*.xlsx *.xls")])
        if file_path:
            self.minuta_file_path = file_path
        self.actualizar_label_archivos()

    def seleccionar_archivo_menus(self):
        """Selecciona el archivo de Menús y actualiza la ruta."""
        file_path = filedialog.askopenfilename(title="Seleccionar archivo Menús", filetypes=[("Archivos de Excel", "*.xlsx *.xls")])
        if file_path:
            self.menus_file_path = file_path
        self.actualizar_label_archivos()

    def actualizar_label_archivos(self):
        """Actualiza la etiqueta de estado con las rutas de los archivos seleccionados."""
        minuta_text = f"Minuta: {self.minuta_file_path}" if self.minuta_file_path else "Minuta no seleccionada"
        menus_text = f"Menús: {self.menus_file_path}" if self.menus_file_path else "Menús no seleccionado"
        self.label_archivos.config(text=f"{minuta_text}\n{menus_text}", fg="black")

    def cargar_minuta(self):
        """Carga el archivo de Minuta seleccionado."""
        if not self.minuta_file_path:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo de Minuta antes de subirlo.")
            return
        self.procesar_archivo(self.minuta_file_path, self.current_minuta_file, "minuta")

    def cargar_menus(self):
        """Carga el archivo de Menús seleccionado."""
        if not self.menus_file_path:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo de Menús antes de subirlo.")
            return
        self.procesar_archivo(self.menus_file_path, self.current_menus_file, "menus")

    def validar_columnas(archivo, tipo):
        if tipo == "minuta":
            columnas_esperadas = ["RUT"] + [f"Día {i}" for i in range(1, 32)] + ["Nombre", "Mes"]
        elif tipo == "menus":
            columnas_esperadas = ["Fecha", "A", "B", "C"]
        else:
            messagebox.showerror("Error", "Tipo de archivo no reconocido.")
            return False

        try:
            wb = openpyxl.load_workbook(archivo)
            hoja = wb.active
            columnas_archivo = [col.value for col in hoja[1] if col.value]  # Leer los nombres de las columnas

            # Verificar si faltan columnas
            columnas_faltantes = [col for col in columnas_esperadas if col not in columnas_archivo]

            if columnas_faltantes:
                messagebox.showerror("Error", f"Faltan columnas en el Excel: {', '.join(columnas_faltantes)}")
                return False

            return True  # Si todas las columnas están correctas

        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo: {str(e)}")
            return False

    def es_excel_valido(self, archivo):
        """Verifica si el archivo es un Excel válido y no está corrupto."""
        try:
            wb = openpyxl.load_workbook(archivo)
            wb.close()
            return True
        except Exception:
            return False

    def procesar_archivo(self, nuevo_archivo, archivo_actual, tipo):
        """Procesa el archivo seleccionado, realiza el respaldo y lo carga."""
        try:
            # Verificar el formato de las columnas antes de procesar el archivo
            '''if not self.validar_columnas(nuevo_archivo, tipo):
                return '''
            # Verificar si el archivo es un Excel válido
            if not nuevo_archivo.endswith('.xlsx') and not nuevo_archivo.endswith('.xls'):
                messagebox.showerror("Error", "El archivo seleccionado no es un archivo Excel válido.")
                return
            
            if not self.es_excel_valido(nuevo_archivo):
                messagebox.showerror("Error", "El archivo Excel está dañado o no tiene un formato válido.")
                return

            # Convertir archivo .xls a .xlsx si es necesario
            if nuevo_archivo.endswith('.xls'):
                nuevo_archivo = self.convertir_xls_a_xlsx(nuevo_archivo)

            # Verificar si el nuevo archivo es idéntico al actual
            if os.path.exists(archivo_actual) and filecmp.cmp(nuevo_archivo, archivo_actual, shallow=False):
                messagebox.showinfo("Información", f"El archivo {tipo} es idéntico al existente. No se realizaron cambios.")
                return  # No hacemos nada porque es el mismo archivo

            # Crear carpeta de respaldo si no existe
            os.makedirs(self.backup_folder, exist_ok=True)

            # Mover el archivo actual al respaldo antes de reemplazarlo
            if os.path.exists(archivo_actual):
                backup_path = os.path.join(self.backup_folder, f"{tipo}_{self.obtener_mes_actual()}.xlsx")
                shutil.move(archivo_actual, backup_path)

            # Copiar el nuevo archivo a la ubicación del archivo actual
            shutil.copy(nuevo_archivo, archivo_actual)
            messagebox.showinfo("Éxito", f"El archivo {tipo} se ha cargado correctamente.")

            # Actualizar rutas en ExcelManager
            if tipo == "minuta":
                excel_manager.minuta_file_path = archivo_actual
            elif tipo == "menus":
                excel_manager.menus_file_path = archivo_actual

            excel_manager.cargar_archivos()
            self.label_archivos.config(text=f"Archivo {tipo} cargado con éxito.", fg="green")

        except Exception as e:
            messagebox.showerror("Error", f"Hubo un problema al cargar el archivo {tipo}:\n{e}")

    def convertir_xls_a_xlsx(self, ruta_xls):
        """Convierte un archivo .xls a .xlsx y devuelve la nueva ruta."""
        try:
            df = pd.read_excel(ruta_xls, engine='xlrd')
            ruta_xlsx = ruta_xls.replace('.xls', '.xlsx')
            df.to_excel(ruta_xlsx, index=False, engine='openpyxl')
            return ruta_xlsx
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un problema al convertir el archivo {ruta_xls} a .xlsx:\n{e}")
            return ruta_xls

    def guardar_respaldo_minuta(self):
        """Guarda un respaldo del archivo de Minuta."""
        self.guardar_respaldo(self.current_minuta_file, "Minuta")

    def guardar_respaldo_menus(self):
        """Guarda un respaldo del archivo de Menús."""
        self.guardar_respaldo(self.current_menus_file, "Menús")

    def guardar_respaldo(self, archivo_actual, tipo):
        """Guarda un respaldo del archivo especificado."""
        file_path = filedialog.asksaveasfilename(title=f"Guardar Respaldo {tipo}", defaultextension=".xlsx", filetypes=[("Archivos de Excel", "*.xlsx *.xls")])
        if file_path:
            try:
                os.makedirs(self.backup_folder, exist_ok=True)
                shutil.copy(archivo_actual, file_path)
                messagebox.showinfo("Éxito", f"El respaldo de {tipo} se ha guardado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Hubo un problema al guardar el respaldo de {tipo}:\n{e}")

    def obtener_mes_actual(self):
        """Obtiene el nombre del mes actual."""
        now = datetime.now()
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        return meses[now.month - 1]