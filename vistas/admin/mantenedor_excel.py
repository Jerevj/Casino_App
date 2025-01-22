import tkinter as tk
from tkinter import filedialog, messagebox
from utils.excel_utils import cargar_archivo, obtener_sheet, obtener_menu_sheet


def mostrar_mantenedor_excel():
    """Ventana para el mantenedor de Excel."""
    ventana = tk.Toplevel()  # Usamos Toplevel si esta ventana es secundaria
    ventana.title("Mantenedor de Excel")
    ventana.geometry("400x300")

    tk.Label(ventana, text="Cargar Menú desde Excel", font=("Arial", 16)).pack(pady=10)

    def cargar():
        """Función para cargar el archivo Excel."""
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=(("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*"))
        )
        if ruta:
            try:
                wb, sheet, menu_sheet = cargar_archivo()
                if wb and sheet and menu_sheet:
                    messagebox.showinfo("Éxito", "Archivo Excel cargado exitosamente")
                    print("Datos de la hoja de empleados:")
                    for row in sheet.iter_rows(values_only=True):
                        print(row)
                    print("Datos de la hoja de menús:")
                    for row in menu_sheet.iter_rows(values_only=True):
                        print(row)
                else:
                    messagebox.showerror("Error", "No se pudo cargar el archivo Excel.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo: {e}")

    tk.Button(ventana, text="Cargar Excel", font=("Arial", 12), command=cargar).pack(pady=10)
    tk.Button(ventana, text="Volver", font=("Arial", 12), command=ventana.destroy).pack(pady=10)
