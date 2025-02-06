import mysql.connector
import bcrypt

def registrar_usuario(usuario, clave):
    conexion = mysql.connector.connect(host="localhost", user="root", password="admin", database="casino")
    cursor = conexion.cursor()

    clave_encriptada = bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO usuarios (usuario, clave) VALUES (%s, %s)", (usuario, clave_encriptada.decode('utf-8')))
        conexion.commit()
        print("Usuario registrado correctamente")
    except mysql.connector.Error as e:
        print("Error:", e)
    finally:
        cursor.close()
        conexion.close()

registrar_usuario("admin", "1234")  # Cambia "admin" y "1234" por los datos deseados
