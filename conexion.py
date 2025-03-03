import mysql.connector
from mysql.connector import Error
from config import CHARSET, DB_HOST, DB_NAME, DB_PASSWORD, DB_USER, PORT

class Conexion:
    def __init__(self):
        self.conexion = None
        self.cursor = None
        self.conectar()

    def conectar(self):
        """Establece la conexión con la base de datos."""
        try:
            if not self.conexion or not self.conexion.is_connected():
                self.conexion = mysql.connector.connect(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    database=DB_NAME,
                    port=PORT,
                    charset=CHARSET 
                )
                self.cursor = self.conexion.cursor()
                print("Conexión obtenida.")
        except Error as e:
            print(f"Error al obtener conexión: {e}")
            self.conexion = None
            self.cursor = None

    def desconectar(self):
        """Cierra la conexión con la base de datos."""
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()
        print("Conexión cerrada.")

    def obtener_persona_por_rut(self, rut):
        """Obtiene una persona por su RUT."""
        self.conectar()
        if self.cursor:
            query = "SELECT * FROM personas WHERE rut = %s"
            self.cursor.execute(query, (rut,))
            result = self.cursor.fetchone()
            return result
        else:
            print("Error: El cursor no está disponible.")
            return None

    def obtener_persona_por_clave(self, clave):
        """Obtiene una persona por su clave."""
        self.conectar()
        if self.cursor:
            query = "SELECT * FROM personas WHERE clave = %s"
            self.cursor.execute(query, (clave,))
            result = self.cursor.fetchone()
            return result
        else:
            print("Error: El cursor no está disponible.")
            return None

    def obtener_menu_por_rut_y_fecha(self, rut, fecha):
        """Obtiene el menú registrado para una persona en una fecha específica."""
        self.conectar()
        if self.cursor:
            query = "SELECT * FROM menus_registrados WHERE rut = %s AND DAY(fecha) = %s"
            self.cursor.execute(query, (rut, fecha))
            result = self.cursor.fetchone()
            return result
        else:
            print("Error: El cursor no está disponible.")
            return None

    def registrar_boleta(self, rut, menu, nombre_menu, fecha_registro):
        """Registra una nueva boleta para un empleado."""
        self.conectar()
        if self.cursor:
            try:
                # Obtener el último ID registrado en la base de datos
                self.cursor.execute("SELECT MAX(id_boleta) FROM menus_registrados")
                ultimo_id = self.cursor.fetchone()[0]

                # Si no hay ningún ID registrado, comenzamos con 1
                nuevo_id = 1 if ultimo_id is None else ultimo_id + 1

                # Insertar la nueva boleta con el ID calculado
                query = """
                    INSERT INTO menus_registrados (id_boleta, rut, menu, nombre_menu, registrado, estado_dia, fecha_registro)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                valores = (nuevo_id, rut, menu, nombre_menu, 1, "normal", fecha_registro)
                print(f"Registrando boleta: {valores}")  # Mensaje de depuración
                self.cursor.execute(query, valores)
                self.conexion.commit()
                print(f"Boleta registrada para RUT {rut} con ID {nuevo_id} en {fecha_registro}")
                
                return nuevo_id  # Retornar el nuevo ID generado

            except Error as e:
                print(f"Error al registrar boleta: {e}")
                self.conexion.rollback()
                return None
        else:
            print("Error: El cursor no está disponible.")
            return None

    def obtener_boleta_por_rut_y_fecha(self, rut, fecha):
        """Obtiene una boleta de la base de datos para un rut y fecha específicos."""
        self.conectar()
        if self.cursor:
            query = """
            SELECT * FROM menus_registrados
            WHERE rut = %s AND DATE(fecha_registro) = %s
            """
            self.cursor.execute(query, (rut, fecha.date()))
            boleta = self.cursor.fetchone()
            return boleta
        else:
            print("Error: El cursor no está disponible.")
            return None