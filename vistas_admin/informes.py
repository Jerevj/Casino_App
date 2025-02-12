import tkinter as tk
from tkinter import ttk, filedialog
import datetime
from conexion import Conexion
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from fpdf import FPDF
import os

class Informes(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)

        # Crear Canvas para agregar scroll
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.db = Conexion()
        self.db.conectar()
        self.widgets()
        self.cargar_datos()

    def widgets(self):
        self.frame_filtros = tk.Frame(self.scrollable_frame)
        self.frame_filtros.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Año
        self.label_anio = tk.Label(self.frame_filtros, text="Año:")
        self.label_anio.grid(row=0, column=0, padx=5, sticky="w")
        self.combo_anio = ttk.Combobox(self.frame_filtros, values=[str(i) for i in range(2020, 2031)], state="readonly")
        self.combo_anio.grid(row=0, column=1, padx=5)
        self.combo_anio.set(str(datetime.date.today().year))

        # Mes en español
        meses_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        self.label_mes = tk.Label(self.frame_filtros, text="Mes:")
        self.label_mes.grid(row=0, column=2, padx=5, sticky="w")
        self.combo_mes = ttk.Combobox(self.frame_filtros, values=meses_es + ["Todo el mes"], state="readonly")
        self.combo_mes.grid(row=0, column=3, padx=5)
        self.combo_mes.set(meses_es[datetime.date.today().month - 1])

        # Día
        self.label_dia = tk.Label(self.frame_filtros, text="Día:")
        self.label_dia.grid(row=0, column=4, padx=5, sticky="w")
        self.combo_dia = ttk.Combobox(self.frame_filtros, values=[str(i) for i in range(1, 32)] + ["Todo el mes"], state="readonly")
        self.combo_dia.grid(row=0, column=5, padx=5)
        self.combo_dia.set(str(datetime.date.today().day))

        # Botón para filtrar
        self.boton_filtrar_fecha = tk.Button(self.frame_filtros, text="Aplicar Filtro", command=self.aplicar_filtro_fecha)
        self.boton_filtrar_fecha.grid(row=0, column=6, padx=5)

        # Tabla
        self.tree = ttk.Treeview(self.scrollable_frame, columns=("RUT", "Fecha", "Menú"), show="headings")
        self.tree.heading("RUT", text="RUT")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Menú", text="Menú")
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Frame para gráfico
        self.frame_grafico = tk.Frame(self.scrollable_frame)
        self.frame_grafico.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Botones para exportar
        self.boton_exportar_excel = tk.Button(self.frame_filtros, text="Exportar a Excel", command=self.exportar_a_excel)
        self.boton_exportar_excel.grid(row=0, column=7, padx=5)

        self.boton_exportar_pdf = tk.Button(self.frame_filtros, text="Exportar a PDF", command=self.exportar_a_pdf)
        self.boton_exportar_pdf.grid(row=0, column=8, padx=5)

    def cargar_datos(self, anio=None, mes=None, dia=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        datos = self.obtener_datos(anio, mes, dia)

        for dato in datos:
            self.tree.insert("", "end", values=dato)

        self.mostrar_grafico(datos)

    def obtener_datos(self, anio, mes, dia):
        self.db.conectar()

        query = "SELECT rut, fecha_registro, menu FROM menus_registrados WHERE YEAR(fecha_registro) = %s"
        parametros = [anio]

        if mes != "Todo el mes":
            query += " AND MONTH(fecha_registro) = %s"
            parametros.append(mes)

        if dia != "Todo el mes":
            query += " AND DAY(fecha_registro) = %s"
            parametros.append(dia)

        self.db.cursor.execute(query, parametros)
        datos = self.db.cursor.fetchall()
        self.db.desconectar()
        return datos

    def mostrar_grafico(self, datos):
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        conteo_menus = {"A": 0, "B": 0, "C": 0}
        for dato in datos:
            menu = dato[2]
            if menu in conteo_menus:
                conteo_menus[menu] += 1

        # Ordenar C después de B
        orden_correcto = ["A", "B", "C"]
        categorias = [m for m in orden_correcto if conteo_menus[m] > 0]
        valores = [conteo_menus[m] for m in categorias]

        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(categorias, valores)
        ax.set_title("Menús por Fecha")

        # Agregar los números sobre las barras
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + 0.2, str(int(yval)), ha="center", fontsize=12)

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def aplicar_filtro_fecha(self):
        anio = int(self.combo_anio.get())
        mes = self.combo_mes.current() + 1 if self.combo_mes.get() != "Todo el mes" else "Todo el mes"
        dia = int(self.combo_dia.get()) if self.combo_dia.get() != "Todo el mes" else "Todo el mes"

        self.cargar_datos(anio, mes, dia)

    def exportar_a_excel(self):
        # Abrir cuadro de diálogo para seleccionar el archivo
        archivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if archivo:
            datos = self.obtener_datos(self.combo_anio.get(), self.combo_mes.get(), self.combo_dia.get())
            if datos:  # Verificamos que haya datos
                df = pd.DataFrame(datos, columns=["RUT", "Fecha", "Menú"])
                df.to_excel(archivo, index=False)

    def exportar_a_pdf(self):
        # Abrir cuadro de diálogo para seleccionar el archivo
        archivo = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if archivo:
            # Crear PDF
            pdf = FPDF()
            pdf.add_page()

            # Título
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, "Informe de Menús", ln=True, align="C")

            # Tabla de datos
            pdf.set_font("Arial", '', 10)
            pdf.ln(10)

            # Columnas de la tabla
            pdf.cell(60, 10, "RUT", border=1)
            pdf.cell(60, 10, "Fecha", border=1)
            pdf.cell(60, 10, "Menú", border=1)
            pdf.ln()

            # Agregar filas
            datos = self.obtener_datos(self.combo_anio.get(), self.combo_mes.get(), self.combo_dia.get())
            if datos:  # Verificamos que haya datos
                for dato in datos:
                    pdf.cell(60, 10, str(dato[0]), border=1)
                    pdf.cell(60, 10, str(dato[1]), border=1)
                    pdf.cell(60, 10, str(dato[2]), border=1)
                    pdf.ln()

            # Gráfico
            fig, ax = plt.subplots(figsize=(6, 4))
            conteo_menus = {"A": 0, "B": 0, "C": 0}
            for dato in datos:
                menu = dato[2]
                if menu in conteo_menus:
                    conteo_menus[menu] += 1

            # Ordenar C después de B
            orden_correcto = ["A", "B", "C"]
            categorias = [m for m in orden_correcto if conteo_menus[m] > 0]
            valores = [conteo_menus[m] for m in categorias]

            bars = ax.bar(categorias, valores)
            ax.set_title("Menús por Fecha")

            # Guardar gráfico como imagen
            grafico_img = "grafico.png"
            fig.savefig(grafico_img)

            # Insertar la imagen del gráfico en el PDF
            pdf.ln(10)
            pdf.image(grafico_img, x=50, w=100)

            # Guardar PDF
            pdf.output(archivo)

            # Eliminar la imagen del gráfico
            os.remove(grafico_img)

