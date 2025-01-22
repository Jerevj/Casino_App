import mysql.connector

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="tu_password",
            database="casino_db"
        )
        return conexion
    except mysql.connector.Error as e:
        print(f"Error al conectar: {e}")
        return None
