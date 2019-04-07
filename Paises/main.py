
import os  # Permite limpiar la terminal (CLI)
import platform  # Permite conocer el S.O. utilizado
import columnize

from paises import Paises

# Instanciamos la clase Paises.

pais = Paises()

# Método que permite limpiar la terminal.


def limpiar():
    # Permite saber el S.O que se utiliza
    if platform.system() == 'Windows':
        # Limpiar terminal en windows
        os.system('cls')
    else:
        # Limpiar terminal en Linux o Mac
        os.system('clear')


# Método que contiene las opciones que se pueden realizar dentro del programa.


def menu_opciones():

    menu = input('''
        \tPaíses\n
        Ingrese el número correspondiente a su opción:\n
        1). Listar países.
        2). Agregar un pais
        3). Buscar un país.
        4). Eliminar un país
        5). Salir
        > ''')

    if menu == '1':
        limpiar()
        if not pais.get_paises():
            print("No hay países en la BD.")
        else:
            print('{:^180}\n'.format('Lista de países'))
            print(columnize.columnize(pais.get_paises(), displaywidth=200))
            menu_opciones()
    elif menu == '2':
        # Limpiarmos la consola
        limpiar()

        # Mostramos el número actual de los paíse antes de crear uno.
        print("\tInsertando un País.\nPaíses actualmente: {}\n".format(
            pais.get_numero_total_paises()))

        # Solicitamos los datos que tendrá el nuevo país.
        nombre = input("Ingrese el nombre del país\n> ")
        while nombre == '':
            nombre = input("Ingrese el nombre del país\n> ")

        while pais.comprobar_existencia("SELECT count(1) FROM paises WHERE nombre = '{}'".format(nombre)):
            nombre = input(
                "El país ya existe.\nIngrese el nombre del país\n> ")

        capital = input("Ingrese el nombre de la capital del país\n> ")
        while capital == '':
            input("Ingrese el nombre de la capital del país\n> ")

        habitantes = input("Ingrese el total de habitantes del país\n> ")
        while not habitantes.isdigit() or '.' in habitantes or int(habitantes) < 0:
            habitantes = input(
                "Ingrese el total de habitantes del país (número entero positivo)\n> ")

        url_bandera = input(
            "Ingrese la dirección url de la bandera del país\n> ")
        while url_bandera == '':
            input(
                "Ingrese la dirección url de la bandera del país\n> ")

        # Llamamos al método para crear el país.
        pais.crear_pais([nombre, capital, habitantes, url_bandera], 0)
        print("País creado\n")

        # Mostramos el número actual de los paíse después de crear uno.
        print("Países actualmente: {}".format(pais.get_numero_total_paises()))

        # Volemos a mostrar las opcions del menú.
        menu_opciones()
    elif menu == '3':
        # Limpiarmos la consola
        limpiar()
        print("\t\nBuscando un país.\n")
        # Solicitamos el nombre del país a buscar
        nombre = input("Ingrese el nombre del país\n> ")
        while nombre == '':
            nombre = input("Ingrese el nombre del país\n> ")

        # Llamos al método buscar_pais()
        datos_pais = pais.buscar_pais(nombre)
        # Mostramos los datos del país
        if datos_pais:
            print("\t\nDatos del país.\n\nNombre: " + datos_pais[0])
            print("capital: " + datos_pais[1])
            print("población: " + datos_pais[2])
            print("url de la bandera: " + datos_pais[3])
        else:
            print("El país ingresado no existe.")
        menu_opciones()
    elif menu == '4':
        # Limpiarmos la consola
        limpiar()

        # Mostramos el número actual de los paíse antes de eliminar uno.
        print("\tEliminado un país.\nPaíses actualmente: {}".format(
            pais.get_numero_total_paises()))

        # Solicitamos el nombre del país a buscar
        nombre = input("Ingrese el nombre del país\n> ")
        while nombre == '':
            nombre = input("Ingrese el nombre del país\n> ")

        if pais.eliminar_pais(nombre) == "hecho":
            print("País eliminado.")
            # Mostramos el número actual de los paíse antes de eliminar uno.
            print("Países actualmente: {}".format(
                pais.get_numero_total_paises()))
        else:
            print(pais.eliminar_pais(nombre))
        menu_opciones()
    elif menu == '5':
        limpiar()
        pais.terminar()
    else:
        limpiar()
        print('Ingrese el número correspondiente a su opción.')
        menu_opciones()


def iniciar():

    # Verificamos que este la BD creada y sino se crea.
    pais.crear_table()

    # Verificamos que tengamos datos en la BD.
    pais.llenar_bd()

    # Llamamos al método menu para que el usuario interactue.
    menu_opciones()


if __name__ == "__main__":
    iniciar()
