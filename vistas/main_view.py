import tkinter as tk
from control_navegacion import ir_a_vista_almuerzo, ir_a_mantenedor_excel

def mostrar_pantalla_principal(root, main_frame):
    # Limpiar el frame actual
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Título de la pantalla principal
    tk.Label(main_frame, text="Casino App", font=("Arial", 24)).grid(row=0, column=0, columnspan=2, pady=20)

    # Botón para ingreso al casino
    tk.Button(main_frame, text="Ingreso Casino", font=("Arial", 16),
              command=lambda: ir_a_vista_almuerzo(main_frame, lambda: mostrar_pantalla_principal(root, main_frame))
              ).grid(row=1, column=0, columnspan=2, pady=10)

    # Botón para administración
    tk.Button(main_frame, text="Administración", font=("Arial", 16), command=ir_a_mantenedor_excel
              ).grid(row=2, column=0, columnspan=2, pady=10)


def iniciar_aplicacion():
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Casino App")

    # Crear un frame principal para gestionar las vistas
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Mostrar la pantalla principal
    mostrar_pantalla_principal(root, main_frame)

    # Iniciar el loop principal de la aplicación
    root.mainloop()
