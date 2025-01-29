# vistas_admin/subir.py
import os
import shutil
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from utils.excel_utils import ExcelManager
from datetime import datetime

class Subir(tk.Frame):

    def __init__(self, padre):
        super().__init__(padre)
        self.minuta_file_path = None
        self.menus_file_path = None
        self.current_minuta_file = "C:/Users/practicainformatica/Desktop/CarpetaExcel/Minuta_Actual.xlsx"  # Archivo en uso
        self.current_menus_file = "C:/Users/practicainformatica/Desktop/CarpetaExcel/Menus_Actual.xlsx"  # Archivo de menús
        self.backup_folder = "C:/Users/practicainformatica/Desktop/CarpetaExcel/archivos_anteriores"  # Carpeta para respaldos
        self.widgets()

    def widgets(self):
        # Título de la ventana
        titulo = tk.Label(self, text="Subir archivos Excel", font=("Arial", 20, "bold"))
        titulo.pack(pady=20)

        # Botón para seleccionar el archivo de minutas
        boton_seleccionar_minuta = tk.Button(self, text="Seleccionar archivo Minuta", command=self.seleccionar_archivo_minuta, font=("Arial", 14))
        boton_seleccionar_minuta.pack(pady=10)

        # Botón para seleccionar el archivo de menús
        boton_seleccionar_menus = tk.Button(self, text="Seleccionar archivo Menús", command=self.seleccionar_archivo_menus, font=("Arial", 14))
        boton_seleccionar_menus.pack(pady=10)

        # Etiqueta para mostrar el archivo seleccionado
        self.label_archivos = tk.Label(self, text="No se han seleccionado archivos.", font=("Arial", 12), fg="gray")
        self.label_archivos.pack(pady=10)

        # Botón para cargar los archivos
        boton_cargar = tk.Button(self, text="Cargar archivos", command=self.cargar_archivos, font=("Arial", 14))
        boton_cargar.pack(pady=10)

    def seleccionar_archivo_minuta(self):
        """Abrir cuadro de diálogo para seleccionar el archivo de minutas."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo Minuta",
            filetypes=[("Archivos de Excel", "*.xlsx *.xls")]
        )
        if file_path:
            self.minuta_file_path = file_path
        self.actualizar_label_archivos()

    def seleccionar_archivo_menus(self):
        """Abrir cuadro de diálogo para seleccionar el archivo de menús."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo Menús",
            filetypes=[("Archivos de Excel", "*.xlsx *.xls")]
        )
        if file_path:
            self.menus_file_path = file_path
        self.actualizar_label_archivos()

    def actualizar_label_archivos(self):
        """Actualizar el texto de la etiqueta con los archivos seleccionados."""
        if self.minuta_file_path and self.menus_file_path:
            self.label_archivos.config(text=f"Minuta: {self.minuta_file_path}\nMenús: {self.menus_file_path}", fg="black")
        else:
            self.label_archivos.config(text="No se han seleccionado ambos archivos.", fg="red")

    def cargar_archivos(self):
        """Cargar ambos archivos Excel y gestionar respaldos."""
        if not self.minuta_file_path or not self.menus_file_path:
            messagebox.showwarning("Advertencia", "Por favor, selecciona ambos archivos antes de cargarlos.")
            return

        try:
            # Respaldar los archivos actuales
            os.makedirs(self.backup_folder, exist_ok=True)

            # Respaldar el archivo de minutas
            if os.path.exists(self.current_minuta_file):
                backup_minuta_path = os.path.join(self.backup_folder, f"minuta_{self.obtener_mes_actual()}.xlsx")
                shutil.move(self.current_minuta_file, backup_minuta_path)

            # Respaldar el archivo de menús
            if os.path.exists(self.current_menus_file):
                backup_menus_path = os.path.join(self.backup_folder, f"menus_{self.obtener_mes_actual()}.xlsx")
                shutil.move(self.current_menus_file, backup_menus_path)

            # Mover los nuevos archivos como los archivos en uso
            shutil.copy(self.minuta_file_path, self.current_minuta_file)
            shutil.copy(self.menus_file_path, self.current_menus_file)

            # Cargar los archivos en ExcelManager
            excel_manager = ExcelManager(self.current_minuta_file, self.current_menus_file)
            excel_manager.cargar_archivos()

            messagebox.showinfo("Éxito", "Los archivos Excel se cargaron correctamente y están en uso.")
            self.label_archivos.config(text="Archivos cargados con éxito.", fg="green")
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un problema al cargar los archivos:\n{e}")

    def obtener_mes_actual(self):
        """Obtener el mes actual en español."""
        now = datetime.now()
        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio", 
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        return meses[now.month - 1]
