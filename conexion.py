import mysql.connector
from mysql.connector import pooling, Error

class Conexion:
    def __init__(self, usar_pool=True):
        self.usar_pool = usar_pool
        self.conexion = None
        self.cursor = None
        if self.usar_pool:
            try:
                self.pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name="mypool",
                    pool_size=10,
                    pool_reset_session=True,
                    host='localhost',
                    user='root',
                    password='admin',
                    database='casino'
                )
                print("Pool de conexiones creado exitosamente.")
            except Error as e:
                print(f"Error al crear el pool de conexiones: {e}")

    def conectar(self):
        """Establece la conexión con la base de datos."""
        try:
            if self.usar_pool:
                self.conexion = self.pool.get_connection()
            else:
                self.conexion = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='admin',
                    database='casino',
                    port=3306
                )
            self.cursor = self.conexion.cursor()
            print("Conexión obtenida.")
        except Error as e:
            print(f"Error al obtener conexión: {e}")

    def desconectar(self):
        """Cierra la conexión con la base de datos."""
        if self.conexion and self.cursor:
            self.cursor.close()
            self.conexion.close()
            self.conexion = None
            print("Conexión cerrada.")

    def obtener_persona_por_rut(self, rut):
        self.conectar()
        query = "SELECT * FROM personas WHERE rut = %s"
        self.cursor.execute(query, (rut,))
        result = self.cursor.fetchone()
        self.desconectar()
        return result

    def obtener_persona_por_clave(self, clave):
        self.conectar()
        query = "SELECT * FROM personas WHERE clave = %s"
        self.cursor.execute(query, (clave,))
        result = self.cursor.fetchone()
        self.desconectar()
        return result

    def obtener_menu_por_rut_y_fecha(self, rut, fecha):
        self.conectar()
        query = "SELECT * FROM menus_registrados WHERE rut = %s AND DAY(fecha) = %s"
        self.cursor.execute(query, (rut, fecha))
        result = self.cursor.fetchone()
        self.desconectar()
        return result

    def registrar_boleta(self, rut, menu, nombre_menu, fecha_registro):
        self.conectar()
        query = """
            INSERT INTO menus_registrados (rut, menu, nombre_menu, registrado, estado_dia, fecha_registro)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (rut, menu, nombre_menu, 1, "normal", fecha_registro)
        try:
            print(f"Registrando boleta: {valores}")  # Mensaje de depuración
            self.cursor.execute(query, valores)
            self.conexion.commit()
            print(f"Boleta registrada para RUT {rut} en {fecha_registro}")
            
            # Obtener el último ID insertado
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            id_boleta = self.cursor.fetchone()[0]
            print(f"ID de la boleta registrada: {id_boleta}")
            return id_boleta
        except Error as e:
            print(f"Error al registrar boleta: {e}")
            self.conexion.rollback()
            return None
        finally:
            self.desconectar()