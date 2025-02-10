import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
from utils.excel_utils import ExcelManager
from config import MINUTA_FILE_PATH, MENUS_FILE_PATH, BACKUP_FOLDER

class Subir(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.minuta_file_path = None
        self.menus_file_path = None
        self.current_minuta_file = MINUTA_FILE_PATH
        self.current_menus_file = MENUS_FILE_PATH
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
        file_path = filedialog.askopenfilename(title="Seleccionar archivo Minuta", filetypes=[("Archivos de Excel", "*.xlsx *.xls")])
        if file_path:
            self.minuta_file_path = file_path
        self.actualizar_label_archivos()

    def seleccionar_archivo_menus(self):
        file_path = filedialog.askopenfilename(title="Seleccionar archivo Menús", filetypes=[("Archivos de Excel", "*.xlsx *.xls")])
        if file_path:
            self.menus_file_path = file_path
        self.actualizar_label_archivos()

    def actualizar_label_archivos(self):
        minuta_text = f"Minuta: {self.minuta_file_path}" if self.minuta_file_path else "Minuta no seleccionada"
        menus_text = f"Menús: {self.menus_file_path}" if self.menus_file_path else "Menús no seleccionado"
        self.label_archivos.config(text=f"{minuta_text}\n{menus_text}", fg="black")

    def cargar_minuta(self):
        if not self.minuta_file_path:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo de Minuta antes de subirlo.")
            return
        self.procesar_archivo(self.minuta_file_path, self.current_minuta_file, "minuta")

    def cargar_menus(self):
        if not self.menus_file_path:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un archivo de Menús antes de subirlo.")
            return
        self.procesar_archivo(self.menus_file_path, self.current_menus_file, "menus")

    def procesar_archivo(self, nuevo_archivo, archivo_actual, tipo):
        try:
            os.makedirs(self.backup_folder, exist_ok=True)
            if os.path.exists(archivo_actual):
                backup_path = os.path.join(self.backup_folder, f"{tipo}_{self.obtener_mes_actual()}.xlsx")
                shutil.move(archivo_actual, backup_path)

            shutil.copy(nuevo_archivo, archivo_actual)
            messagebox.showinfo("Éxito", f"El archivo {tipo} se ha cargado correctamente.")
            
            excel_manager = ExcelManager()
            excel_manager.cargar_archivos()
            self.label_archivos.config(text=f"Archivo {tipo} cargado con éxito.", fg="green")
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un problema al cargar el archivo {tipo}:\n{e}")

    def guardar_respaldo_minuta(self):
        self.guardar_respaldo(self.current_minuta_file, "Minuta")

    def guardar_respaldo_menus(self):
        self.guardar_respaldo(self.current_menus_file, "Menús")

    def guardar_respaldo(self, archivo_actual, tipo):
        file_path = filedialog.asksaveasfilename(title=f"Guardar Respaldo {tipo}", defaultextension=".xlsx", filetypes=[("Archivos de Excel", "*.xlsx *.xls")])
        if file_path:
            try:
                os.makedirs(self.backup_folder, exist_ok=True)
                shutil.copy(archivo_actual, file_path)
                messagebox.showinfo("Éxito", f"El respaldo de {tipo} se ha guardado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Hubo un problema al guardar el respaldo de {tipo}:\n{e}")

    def obtener_mes_actual(self):
        now = datetime.now()
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        return meses[now.month - 1]