import pandas as pd
import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import filedialog, messagebox


# Función para obtener los 4 últimos números antes del guion
def obtener_clave(rut):
    partes = rut.split('-')
    if len(partes) > 1:
        clave = partes[0][-4:]
    else:
        clave = partes[0][-4:]
    return clave


# Función para cargar los datos desde el Excel a la base de datos
def cargar_datos_excel_a_bd(ruta_excel, nombre_hoja):
    connection = None
    try:
        df = pd.read_excel(ruta_excel, sheet_name=nombre_hoja)
        df['Rut'] = df['Rut'].astype(str).str.strip()
        df['Nombre Funcionario'] = df['Nombre Funcionario'].fillna('Desconocido')

        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin',
            database='casino'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("DELETE FROM personas")
            for _, row in df.iterrows():
                rut = row['Rut']
                nombre = row['Nombre Funcionario']
                clave = obtener_clave(rut)
                estado = True
                cursor.execute("SELECT COUNT(*) FROM personas WHERE rut = %s", (rut,))
                if cursor.fetchone()[0] == 0:
                    cursor.execute(
                        "INSERT INTO personas (rut, nombre, clave, estado) VALUES (%s, %s, %s, %s)",
                        (rut, nombre, clave, estado)
                    )
            connection.commit()
            messagebox.showinfo("Éxito", "Datos insertados con éxito")
    except Error as e:
        messagebox.showerror("Error", f"Error al conectar a MySQL o insertar datos: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def seleccionar_archivo():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Archivos Excel", "*.xlsx;*.xls")])
    if archivo:
        entry_ruta_excel.delete(0, tk.END)
        entry_ruta_excel.insert(0, archivo)


def borrar_todo():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin',
            database='casino'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("DELETE FROM personas")
            connection.commit()
            messagebox.showinfo("Éxito", "Datos eliminados con éxito")
    except Error as e:
        messagebox.showerror("Error", f"Error al borrar los datos: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def cargar_datos():
    ruta_excel = entry_ruta_excel.get()
    if ruta_excel:
        nombre_hoja = 'Hoja1'
        cargar_datos_excel_a_bd(ruta_excel, nombre_hoja)
    else:
        messagebox.showerror("Error", "Debe seleccionar un archivo Excel")


def buscar_empleado():
    rut = entry_buscar_rut.get().strip()
    if not rut:
        messagebox.showerror("Error", "Debe ingresar un RUT para buscar")
        return

    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin',
            database='casino'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT nombre, clave, estado FROM personas WHERE rut = %s", (rut,))
            resultado = cursor.fetchone()
            if resultado:
                entry_nombre.delete(0, tk.END)
                entry_nombre.insert(0, resultado[0])

                entry_clave.delete(0, tk.END)
                entry_clave.insert(0, resultado[1])

                var_estado.set(resultado[2])
                entry_buscar_rut.config(state=tk.DISABLED)
                btn_guardar.config(state=tk.NORMAL)
            else:
                messagebox.showinfo("Información", "Empleado no encontrado")
    except Error as e:
        messagebox.showerror("Error", f"Error al buscar empleado: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def guardar_cambios():
    rut = entry_buscar_rut.get().strip()
    nombre = entry_nombre.get().strip()
    clave = entry_clave.get().strip()
    estado = var_estado.get()

    if not rut or not nombre or not clave:
        messagebox.showerror("Error", "Debe completar todos los campos")
        return

    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin',
            database='casino'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE personas SET nombre = %s, clave = %s, estado = %s WHERE rut = %s",
                (nombre, clave, estado, rut)
            )
            connection.commit()
            messagebox.showinfo("Éxito", "Datos actualizados con éxito")
            entry_buscar_rut.config(state=tk.NORMAL)
            btn_guardar.config(state=tk.DISABLED)
            limpiar_campos_edicion()
    except Error as e:
        messagebox.showerror("Error", f"Error al actualizar empleado: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def limpiar_campos_edicion():
    entry_buscar_rut.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_clave.delete(0, tk.END)
    var_estado.set(True)


# Crear la interfaz gráfica
root = tk.Tk()
root.title("Cargar Datos a Base de Datos")

label_ruta_excel = tk.Label(root, text="Seleccionar archivo Excel:")
label_ruta_excel.pack(padx=10, pady=5)

entry_ruta_excel = tk.Entry(root, width=50)
entry_ruta_excel.pack(padx=10, pady=5)

boton_seleccionar = tk.Button(root, text="Seleccionar Excel", command=seleccionar_archivo)
boton_seleccionar.pack(padx=10, pady=5)

boton_borrar = tk.Button(root, text="Borrar Todo", command=borrar_todo)
boton_borrar.pack(padx=10, pady=5)

boton_cargar = tk.Button(root, text="Subir Datos a la Base de Datos", command=cargar_datos)
boton_cargar.pack(padx=10, pady=5)

# Sección de edición
label_buscar_rut = tk.Label(root, text="Buscar empleado por RUT:")
label_buscar_rut.pack(padx=10, pady=5)

entry_buscar_rut = tk.Entry(root, width=50)
entry_buscar_rut.pack(padx=10, pady=5)

boton_buscar = tk.Button(root, text="Buscar", command=buscar_empleado)
boton_buscar.pack(padx=10, pady=5)

label_nombre = tk.Label(root, text="Nombre:")
label_nombre.pack(padx=10, pady=5)

entry_nombre = tk.Entry(root, width=50)
entry_nombre.pack(padx=10, pady=5)

label_clave = tk.Label(root, text="Clave:")
label_clave.pack(padx=10, pady=5)

entry_clave = tk.Entry(root, width=50)
entry_clave.pack(padx=10, pady=5)

label_estado = tk.Label(root, text="Estado:")
label_estado.pack(padx=10, pady=5)

var_estado = tk.BooleanVar(value=True)
check_estado = tk.Checkbutton(root, text="Activo", variable=var_estado)
check_estado.pack(padx=10, pady=5)

btn_guardar = tk.Button(root, text="Guardar Cambios", command=guardar_cambios, state=tk.DISABLED)
btn_guardar.pack(padx=10, pady=5)

root.mainloop()
