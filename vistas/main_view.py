import tkinter as tk
from control_navegacion import ir_a_vista_almuerzo, ir_a_mantenedor_excel

def mostrar_pantalla_principal():
    root = tk.Tk()
    root.title("Casino App")

    tk.Label(root, text="Casino App", font=("Arial", 24)).pack(pady=20)

    tk.Button(root, text="Ingreso Casino", font=("Arial", 16), command=ir_a_vista_almuerzo).pack(pady=10)
    tk.Button(root, text="Administración", font=("Arial", 16), command=ir_a_mantenedor_excel).pack(pady=10)

    root.mainloop()
