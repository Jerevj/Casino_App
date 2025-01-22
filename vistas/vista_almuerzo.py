import tkinter as tk

def mostrar_vista_almuerzo():
    ventana = tk.Tk()
    ventana.title("Ingreso al Casino")

    tk.Label(ventana, text="Ingrese su clave", font=("Arial", 16)).pack(pady=10)
    # Aquí puedes agregar un panel numérico y lógica para generar boletas.

    tk.Button(ventana, text="Volver", font=("Arial", 12), command=ventana.destroy).pack(pady=10)
    ventana.mainloop()
