import sys  # Permite terminar la ejecución del programa
from conexion_bd import Conexion_BD
from api import ApiPaises


class Paises:

    # Instaciamos las clases
    conexion = Conexion_BD()
    api = ApiPaises()

    # Inicialimos el contructor con los atributos de la clase.
    def __init__(self):
        self.nombre = ''
        self.capital = ''
        self.habitantes = ''
        self.url_bandera = ''
        self.codicion = ''

    # Método que permite terminar la ejecución del programa.
    def terminar(self):
        # Terminar ejecución del programa
        sys.exit()

    # Creamos el método que nos permitirá crear un pais (insertar registro)
    def crear_pais(self, *args):
        """
        Hacemos una validación de la variable args en la posición 1 
        para saber si el pais a insertar esta siendo creado por el usuario
        o por medio de los datos obtenidos de la api para tener un mejor control 
        a la hora de llenar la BD.
        """
        if args[1] == 0:
            # Asignamos el valor a las variables para mandar a la BD.
            self.nombre = args[0][0]
            self.capital = args[0][1]
            self.habitantes = "{}".format(args[0][2])
            self.url_bandera = args[0][3]
            self.codicion = args[1]

            # Creamos la setencia para insertar registros en la BD.
            sql_string = "INSERT INTO paises VALUES (%s, %s, %s, %s, %s)"

            # Tupla que contendra los valores
            sql_values = (self.nombre, self.capital,
                          self.habitantes, self.url_bandera, '0')
        else:
            # Asignamos el valor a las variables para mandar a la BD.
            self.nombre = args[0][0]
            self.capital = args[0][1]
            self.habitantes = "{}".format(args[0][2])
            self.url_bandera = args[0][3]

            # Creamos la setencia para insertar registros en la BD.
            sql_string = "INSERT INTO paises (nombre, capital, habitantes, url_bandera) VALUES (%s, %s, %s, %s)"

            # Tupla que contendra los valores
            sql_values = (self.nombre, self.capital,
                          self.habitantes, self.url_bandera)

        try:
            # Ejecutamos la sentencia
            self.conexion.ejecutar_sql(sql_string, sql_values)
        except Exception:
            print('Error insertando registro: ' + str(Exception))

    # Método para buscar un país en la bd.
    def buscar_pais(self, nombre):

        # Comprobamos que exista el país proporcionado
        sql_string = "SELECT count(1) FROM paises WHERE nombre = '" + \
            str(nombre) + "'"

        if not self.comprobar_existencia(sql_string):
            return []
        else:
            # Creamos la sentencia para traer los datos del país proporcionado.
            sql_string = "SELECT * FROM paises WHERE nombre = '" + \
                str(nombre) + "'"
            try:
                # Ejecutamos la sentencia
                resultado = self.conexion.ejecutar_sql(sql_string)
                return resultado[0]
            except Exception:
                print('Error buscando: ' + str(Exception))

    # Método para eliminar un país de la bd

    def eliminar_pais(self, nombre):
        # Comprobamos que exista el país proporcionado
        sql_string = "SELECT count(1) FROM paises WHERE nombre = '" + \
            str(nombre) + "'"

        if not self.comprobar_existencia(sql_string):
            return "El país ingresado no existe."
        else:
            # Creamos la sentencia para eliminar los datos del país proporcionado.
            sql_string = "DELETE FROM paises WHERE nombre = '{}'".format(
                nombre)
            try:
                # Ejecutamos la sentencia
                self.conexion.ejecutar_sql(sql_string)
                return "hecho"

            except Exception:
                print('Error eliminando: ' + str(Exception))

    # Método para obtener a todos los paises de nuestra base de datos.
    def get_paises(self):
        sql_string = "SELECT nombre FROM paises"
        try:
            # Ejecutamos la sentencia y lo almacenamos
            resultado = self.conexion.ejecutar_sql(sql_string)
            if not resultado:
                return []
            else:
                lista_paises_bd = []
                for i, pais in enumerate(resultado):
                    lista_paises_bd.append(str(i+1) + ". " + pais[0])
                return lista_paises_bd
        except Exception:
            print('Error: ' + str(Exception))

    def get_numero_total_paises(self):
        sql_string = "select count(nombre) from paises"
        try:
            # Ejecutamos la sentencia
            resultado = self.conexion.ejecutar_sql(sql_string)
            return resultado[0][0]

        except Exception:
            print('Error: ' + str(Exception))

    # Método para crear la tabla donde se almacerá la información obtenida de la api.

    def crear_table(self):
        """
        Verificamos que exista la BD a la cual se agregará la tabla paises 
        la cual contendrá los datos obtenidos a través de la api.
        """

        sql_string = "SELECT count(1) FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'paises_bd'"

        if not self.comprobar_existencia(sql_string):
            print("Revise que tenga creada la base de datos 'paises_bd' y este escrito correctamente en el archivo de configuacion_bd.")
            self.terminar()

        # Revisamos que este creada la tabla paises y sino la creamos.
        sql_string = "SELECT count((1)) FROM INFORMATION_SCHEMA.TABLES where table_schema ='paises_bd' and table_name='paises'"

        if not self.comprobar_existencia(sql_string):
            # Creamos la setencia para crear la base de datos sino existe
            sql_string = """CREATE TABLE paises(
            nombre VARCHAR(75) PRIMARY KEY NOT NULL,
            capital VARCHAR(75) NOT NULL,
            habitantes VARCHAR(12) NOT NULL,
            url_bandera TEXT NOT NULL,
            condicion BOOLEAN NOT NULL DEFAULT '1')"""

            try:
                # Ejecutamos la setencia para crear o verificar la BD.
                self.conexion.ejecutar_sql(sql_string)

            except Exception as e:
                print('Error creando la tabla: ' + str(e))

    # Método para llenar la base de datos en caso de ser la primera vez en usar el programa.

    def llenar_bd(self):
        """"
        Verificamos que los datos obetenidos de la api no se hayan guardado 
        en caso de que no, se empieza a insertar todos los registro.
        """
        sql_string = "select count(1) from paises where condicion = '1'"
        if not self.comprobar_existencia(sql_string):
            print("Llenando base de datos...")

            # Obtenemos la datos que tendra la BD
            lista_paises = self.api.filtrar_datos_paises()

            try:
                for pais in lista_paises:
                    self.crear_pais(pais, 1)
            except Exception:
                print('Error llenando Base de datos: ' + str(Exception))

        print("Base de datos lista")

    # Método para validar que exista un registro, tabla o Bd
    def comprobar_existencia(self, sql_string):
        try:
            # Ejecutamos la sentencia
            resultado = self.conexion.ejecutar_sql(sql_string)
            if resultado[0][0] >= 1:
                return True
            else:
                return False

        except Exception:
            print('Error comprobando existencia: ' + str(Exception))
