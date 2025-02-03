import tkinter as tk
from tkinter import ttk, messagebox
from utils.excel_utils import excel_manager
from openpyxl import load_workbook
from conexion import Conexion

class Minutas(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.data = []
        self.column_names = ['Día', 'Menú A', 'Menú B', 'Menú C']
        self.db = Conexion()
        self.db.conectar()
        self.widgets()
        #self.sincronizar_empleados_con_excel()
        self.cargar_minutas()

    def widgets(self):
        titulo = tk.Label(self, text="Gestión de Menús seleccionados", font=("Arial", 20, "bold"))
        titulo.pack(pady=10)
        
        self.btn_actualizar = tk.Button(self, text="Actualizar", command=self.sincronizar_empleados_con_excel)
        self.btn_actualizar.pack(pady=5)
        
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.scrollbar_vertical = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL)
        self.scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.scrollbar_horizontal = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.table_frame = tk.Frame(self.main_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

    def sincronizar_empleados_con_excel(self):
        try:
            minuta_path = excel_manager.obtener_ruta_minuta()
            wb = load_workbook(minuta_path)
            sheet = wb.active
            
            # Obtener lista de RUTs en Excel
            ruts_excel = {sheet.cell(row=i, column=1).value for i in range(2, sheet.max_row + 1)}
            
            # Obtener lista de empleados desde la BD
            self.db.cursor.execute("SELECT rut, nombre FROM personas")
            empleados = self.db.cursor.fetchall()
            
            fila_actual = sheet.max_row + 1
            for rut, nombre in empleados:
                if rut not in ruts_excel:
                    sheet.cell(row=fila_actual, column=1, value=rut)  # Columna 0 (RUT)
                    sheet.cell(row=fila_actual, column=33, value=nombre)  # Columna 32 (Nombre Funcionario)
                    fila_actual += 1
            
            wb.save(minuta_path)
        
            messagebox.showinfo("Éxito", "Los empleados fueron sincronizados con el Excel.")
            self.cargar_minutas()
        except Exception as e:
            messagebox.showerror("Error", f"Error al sincronizar empleados con el Excel: {e}")

    def cargar_minutas(self):
        try:
            sheet = excel_manager.obtener_minuta_sheet()
            if not sheet:
                raise Exception("No se pudo obtener la hoja de minutas.")

            rows = list(sheet.iter_rows(values_only=True))
            if not rows:
                raise Exception("El archivo está vacío o mal estructurado.")

            self.data = []
            self.column_names = rows[0]

            for widget in self.table_frame.winfo_children():
                widget.destroy()

            self.tree = ttk.Treeview(self.table_frame, show="headings", columns=self.column_names, height=25)
            self.tree.pack(fill=tk.BOTH, expand=True)

            self.scrollbar_vertical.config(command=self.tree.yview)
            self.scrollbar_horizontal.config(command=self.tree.xview)
            self.tree.configure(yscrollcommand=self.scrollbar_vertical.set, xscrollcommand=self.scrollbar_horizontal.set)

            for col in self.column_names:
                self.tree.heading(col, text=col)
                self.tree.column(col, anchor="center", width=130)
                
            for row in rows[1:]:
                self.tree.insert('', 'end', values=row)
            
            self.tree.bind("<Double-1>", self.editar_celda)

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar las minutas desde el archivo: {e}")

    def editar_celda(self, event):
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        col_index = int(column[1:]) - 1  # Convertir el índice a entero

        # Bloquear edición en la primera columna (RUT) y la columna 32 (Nombre Funcionario)
        if col_index == 0 or col_index == 32:
            return  # No permitir edición en estas columnas
    
        if item:
            valores = list(self.tree.item(item, "values"))
            valor_actual = valores[col_index]

            entrada = tk.Entry(self.tree)
            entrada.insert(0, valor_actual)
            entrada.bind("<Return>", lambda e: self.guardar_edicion(item, col_index, entrada.get()))
            entrada.bind("<FocusOut>", lambda e: entrada.destroy())

            x, y, width, height = self.tree.bbox(item, column)
            entrada.place(x=x, y=y, width=width, height=height)
            entrada.focus()

    def guardar_edicion(self, item, col_index, nuevo_valor):
        valores = list(self.tree.item(item, "values"))
        valores[col_index] = nuevo_valor
        self.tree.item(item, values=valores)
        
        self.actualizar_excel()
    
    def actualizar_excel(self):
        try:
            minuta_path = excel_manager.obtener_ruta_minuta()
            wb = load_workbook(minuta_path)
            sheet = wb.active
            for i, item in enumerate(self.tree.get_children(), start=2):
                valores = self.tree.item(item, "values")
                for j, valor in enumerate(valores):
                    sheet.cell(row=i, column=j+1, value=valor)
            wb.save(minuta_path)
            messagebox.showinfo("Éxito", "Datos actualizados en Excel.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el Excel: {e}")
