import tkinter as tk
from control_navegacion import ir_a_vista_almuerzo, ir_a_mantenedor_excel

def mostrar_pantalla_principal():
    root = tk.Tk()
    root.title("Casino App")

    tk.Label(root, text="Casino App", font=("Arial", 24)).grid(pady=20)

    # Crear el frame principal
    main_frame = tk.Frame(root)
    main_frame.grid(padx=20, pady=20)

    # Botón para ingreso al casino
    tk.Button(main_frame, text="Ingreso Casino", font=("Arial", 16), command=lambda: ir_a_vista_almuerzo(main_frame, volver_a_vista_principal)).grid(pady=10)
    
    # Botón para administración
    tk.Button(main_frame, text="Administración", font=("Arial", 16), command=ir_a_mantenedor_excel).grid(pady=10)

    root.mainloop()

def volver_a_vista_principal():
    print("Volver a la vista principal")
    # Aquí puedes agregar el código para volver a la vista principal
    # Crear o actualizar el main_frame y mostrar la pantalla principal nuevamente
    mostrar_pantalla_principal()
