import os
import shutil
from tkinter import *
import tkinter as tk
from tkinter import filedialog, messagebox
from utils.excel_utils import ExcelManager
import calendar
from datetime import datetime

class Subir(tk.Frame):

    def __init__(self, padre):
        super().__init__(padre)
        self.file_path = None
        self.current_file = "C:/Users/practicainformatica/Desktop/CarpetaExcel/Minuta_Actual.xlsx"  # Archivo en uso
        self.backup_folder = "C:/Users/practicainformatica/Desktop/CarpetaExcel/archivos_anteriores"  # Carpeta para respaldos
        self.widgets()

    def widgets(self):
        # Título de la ventana
        titulo = tk.Label(self, text="Subir archivo Excel", font=("Arial", 20, "bold"))
        titulo.pack(pady=20)

        # Botón para seleccionar archivo
        boton_seleccionar = tk.Button(self, text="Seleccionar archivo Excel", command=self.seleccionar_archivo, font=("Arial", 14))
        boton_seleccionar.pack(pady=10)

        # Etiqueta para mostrar el archivo seleccionado
        self.label_archivo = tk.Label(self, text="No se ha seleccionado ningún archivo.", font=("Arial", 12), fg="gray")
        self.label_archivo.pack(pady=10)

        # Botón para cargar el archivo
        boton_cargar = tk.Button(self, text="Cargar archivo", command=self.cargar_archivo, font=("Arial", 14))
        boton_cargar.pack(pady=10)

    def seleccionar_archivo(self):
        """Abrir cuadro de diálogo para seleccionar un archivo."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Archivos de Excel", "*.xlsx *.xls")]
        )
        if file_path:
            self.file_path = file_path
            self.label_archivo.config(text=f"Archivo seleccionado: {file_path}", fg="black")
        else:
            self.label_archivo.config(text="No se ha seleccionado ningún archivo.", fg="gray")

    def cargar_archivo(self):
        """Cargar el archivo Excel y gestionar respaldos."""
        if not self.file_path:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo antes de cargarlo.")
            return

        try:
            # Crear carpeta de respaldo si no existe
            os.makedirs(self.backup_folder, exist_ok=True)

            # Respaldar el archivo actual (si existe)
            if os.path.exists(self.current_file):
                backup_path = os.path.join(
                    self.backup_folder, 
                    f"minuta_{self.obtener_mes_actual()}.xlsx"
                )
                shutil.move(self.current_file, backup_path)
                print(f"Archivo actual respaldado en: {backup_path}")

            # Mover el nuevo archivo como el archivo en uso
            shutil.copy(self.file_path, self.current_file)
            print(f"Nuevo archivo en uso: {self.current_file}")

            # Verificar si el archivo se copió correctamente
            if not os.path.exists(self.current_file):
                raise Exception(f"El archivo no se ha copiado correctamente a {self.current_file}")

            # Cargar el nuevo archivo en ExcelManager
            excel_manager = ExcelManager(self.current_file)
            excel_manager.cargar_archivo()  # Asegúrate de que esta función está cargando los datos correctamente

            messagebox.showinfo("Éxito", "El archivo Excel se cargó correctamente y está en uso.")
            self.label_archivo.config(text="Archivo cargado con éxito.", fg="green")
        except Exception as e:
            print(f"Error al cargar el archivo Excel: {e}")
            messagebox.showerror("Error", f"Hubo un problema al cargar el archivo:\n{e}")

    def obtener_mes_actual(self):
        """Obtener el mes actual en español."""
        now = datetime.now()
        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio", 
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        return meses[now.month - 1]
