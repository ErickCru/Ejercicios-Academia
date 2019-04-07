import pymysql
from configuracion_bd import DATABASE


class Conexion_BD:

    def __init__(self):

        # Iniciamos una variables para saber el estado de la conexión.
        self.conexion_estado = False

        # Inciamos la conexión con el valor None
        self.conexion = None

        '''
        Obtenemos los parametros necesarios para posteriormente 
        relalizar la conexión con la BD.
        '''
        self.db_name = DATABASE["db_name"]
        self.host = DATABASE["host"]
        self.user = DATABASE["user"]
        self.password = DATABASE["password"]

    # Definimos el método que permitirá la conexión con la BD.
    def establecer_conexion(self):

        self.conexion = pymysql.connect(host=self.host,
                                        user=self.user,
                                        password=self.password,
                                        db=self.db_name)

    # Declaramos el método que permitirá realizar las operaciones con la BD
    def ejecutar_sql(self, sql_string, values=()):
        # Establecemos la conexión
        self.establecer_conexion()

        try:
            cursor = self.conexion.cursor()
            # Ejecutamos las sentencias
            if values:
                cursor.execute(sql_string, values)
            else:
                cursor.execute(sql_string)

            # Realizamos el commit para guardar los cambios en la BD
            self.conexion.commit()

            # Obtenemos el resultado del commit
            result = cursor.fetchall()

            # Devolvemos el resultado
            return result

        finally:
            # Cerramos la conexion
            self.conexion.close()
