import tkinter as tk
from inicio import Inicio
from conexion import Conexion

def main():
    # Crear la conexión a la base de datos
    db_connection = Conexion()
    db_connection.conectar()

    # Iniciar la aplicación
    app = Inicio(db_connection)
    app.mainloop()

    # Desconectar la base de datos al cerrar la aplicación
    if db_connection.conexion:
        print("Desconectando la base de datos desde index.py...")
        db_connection.desconectar()
        print("Base de datos desconectada desde index.py.")

    # Forzar el cierre de la aplicación
    print("Forzando el cierre de la aplicación...")
    app.quit()
    print("Aplicación cerrada.")

if __name__ == "__main__":
    main()