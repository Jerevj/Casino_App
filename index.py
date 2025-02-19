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
    db_connection.desconectar()

if __name__ == "__main__":
    main()