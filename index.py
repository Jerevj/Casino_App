import sys
import tkinter as tk
from inicio import Inicio
from conexion import Conexion

def cerrar_app(app, db_connection):
    """Cierra la aplicación y desconecta la base de datos correctamente."""
    if db_connection.conexion:
        print("Desconectando la base de datos desde index.py...")
        db_connection.desconectar()
        print("Base de datos desconectada desde index.py.")

    app.quit()  # Detiene el loop de tkinter
    app.destroy()  # Destruye la ventana
    sys.exit(0)  # Cierra el proceso completamente

def main():
    # Crear la conexión a la base de datos
    db_connection = Conexion()
    db_connection.conectar()

    # Iniciar la aplicación
    app = Inicio(db_connection)

    # Asegurar que la aplicación cierre correctamente al presionar la "X"
    app.protocol("WM_DELETE_WINDOW", lambda: cerrar_app(app, db_connection))

    app.mainloop()

if __name__ == "__main__":
    main()