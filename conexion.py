import mysql.connector
from mysql.connector import Error

class Conexion:
    def __init__(self, usar_pool=False):
        self.usar_pool = usar_pool
        self.conexion = None
        self.cursor = None

    def conectar(self):
        """Establece la conexión con la base de datos sin usar pool."""
        try:
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
            try:
                # Consumir todos los resultados pendientes (si los hay)
                self.cursor.fetchall()  # Si hay resultados pendientes, los consume
            except mysql.connector.errors.InterfaceError:
                # Si no hay resultados pendientes, pasamos
                pass
            finally:
                self.cursor.close()
                self.conexion.close()
                self.conexion = None
                print("Conexión cerrada.")


    def obtener_persona_por_rut(self, rut):
        """Obtiene una persona por su RUT."""
        self.conectar()
        query = "SELECT * FROM personas WHERE rut = %s"
        self.cursor.execute(query, (rut,))
        result = self.cursor.fetchone()
        self.desconectar()
        return result

    def obtener_persona_por_clave(self, clave):
        """Obtiene una persona por su clave."""
        self.conectar()
        query = "SELECT * FROM personas WHERE clave = %s"
        self.cursor.execute(query, (clave,))
        result = self.cursor.fetchone()
        self.desconectar()
        return result

    def obtener_menu_por_rut_y_fecha(self, rut, fecha):
        """Obtiene el menú registrado para una persona en una fecha específica."""
        self.conectar()
        query = "SELECT * FROM menus_registrados WHERE rut = %s AND DAY(fecha) = %s"
        self.cursor.execute(query, (rut, fecha))
        result = self.cursor.fetchone()
        self.desconectar()
        return result

    def registrar_boleta(self, rut, menu, nombre_menu, fecha_registro):
        """Registra una nueva boleta para un empleado."""
        self.conectar()
        try:
            # Obtener el último ID registrado en la base de datos
            self.cursor.execute("SELECT MAX(id_boleta) FROM menus_registrados")
            ultimo_id = self.cursor.fetchone()[0]

            # Si no hay ningún ID registrado, comenzamos con 1
            if ultimo_id is None:
                nuevo_id = 1
            else:
                nuevo_id = ultimo_id + 1

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
        finally:
            self.desconectar()

    def obtener_boleta_por_rut_y_fecha(self, rut, fecha):
        """Obtiene una boleta de la base de datos para un rut y fecha específicos."""
        self.conectar()
        query = """
        SELECT * FROM menus_registrados
        WHERE rut = %s AND DATE(fecha_registro) = %s
        """
        self.cursor.execute(query, (rut, fecha.date()))
        boleta = self.cursor.fetchone()
        self.desconectar()
        return boleta
