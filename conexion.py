import mysql.connector
from mysql.connector import Error

class Conexion:
    def __init__(self):
        self.conexion = None
        self.cursor = None

    def conectar(self):
        """Establece la conexión con la base de datos."""
        try:
            self.conexion = mysql.connector.connect(
                host='localhost',
                user='root',  # Cambia esto si tienes un usuario diferente
                password='admin',  # Contraseña de MySQL
                database='casino',
                port=3306
            )
            self.cursor = self.conexion.cursor()
            print("Conexión exitosa a la base de datos.")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def asegurarse_conectado(self):
        """Verifica si la conexión está activa antes de ejecutar una consulta."""
        if self.conexion is None or not self.conexion.is_connected():
            self.conectar()  # Conecta si no está conectado

    def desconectar(self):
        """Cierra la conexión con la base de datos."""
        if self.conexion and self.cursor:
            self.cursor.close()
            self.conexion.close()
            self.conexion = None  # Asegurarse de que la conexión quede como None
            print("Conexión cerrada.")

    def obtener_persona_por_rut(self, rut):
        """Obtiene los datos de la persona según el RUT."""
        self.asegurarse_conectado()  # Verificar si la conexión está activa
        query = "SELECT * FROM personas WHERE rut = %s"
        self.cursor.execute(query, (rut,))
        return self.cursor.fetchone()

    def obtener_persona_por_clave(self, clave):
        """Obtiene los datos de la persona según la clave de 4 dígitos."""
        self.asegurarse_conectado()  # Verificar si la conexión está activa
        query = "SELECT * FROM personas WHERE clave = %s"
        self.cursor.execute(query, (clave,))
        return self.cursor.fetchone()

    def obtener_menu_por_rut_y_fecha(self, rut, fecha):
        """Obtiene el menú de la persona según el RUT y solo el día del mes."""
        self.asegurarse_conectado()  # Verificar si la conexión está activa
        print(f"Buscando menú para RUT: {rut}, Día: {fecha}")  # Verifica el día
        query = "SELECT * FROM menus_registrados WHERE rut = %s AND DAY(fecha) = %s"
        self.cursor.execute(query, (rut, fecha))  # Cambiamos a solo usar el día
        resultado = self.cursor.fetchone()
        print(f"Resultado de la consulta: {resultado}")  # Verifica el resultado
        return resultado

'''    def registrar_boleta(self, rut, fecha, opcion_menu, nombre_menu):
        """Registra la boleta en la base de datos."""
        try:
            with self.conexion.cursor() as cursor:
                query = """
                    INSERT INTO menus_registrados (rut, fecha, menu, nombre_menu, registrado, estado_dia)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                valores = (rut, fecha, opcion_menu, nombre_menu, 1, "normal")
                cursor.execute(query, valores)
                self.conexion.commit()  # Cambié self.conn.commit() por self.conexion.commit()
                print(f"Boleta registrada para RUT {rut} en {fecha}")
        except Exception as e:
            print(f"Error al registrar boleta: {e}")
            self.conexion.rollback()  # Revertir cambios si ocurre un error


'''
# Instancia global de la clase (si es necesario)
# db = Conexion()
