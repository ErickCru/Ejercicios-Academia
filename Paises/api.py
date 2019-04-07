# -*- coding: utf-8 -*
import requests


class ApiPaises:
    # Declaramos el campo url que tendra la direción de la api.
    url = ''

    # Declaramos la variables que obtendra todos los datos de la api.
    payload = {}

    # Iniciamos el constructor
    def __init__(self, url="https://restcountries.eu/rest/v2/all"):
        self.url = url

    def obtener_datos(self):
        # Obtenemos los datos provenientes de la api.
        response = requests.get(self.url)

        # Validamos que se haya hecho correctamente la petición
        if response.status_code == 200:
            self.payload = response.json()

        return self.payload

    '''
    Nuestro metodo obtener_datos() devolverá todos los datos que reciba de la api,
    pero, para este ejercicio solo se necesita 4 de ellos: nombre, capital,
    habitantes y la url de la bandera.
    '''

    def filtrar_datos_paises(self):
        lista_datos_filtrados = []
        paises = self.obtener_datos()

        for pais in paises:
            lista_datos_filtrados.append(
                [pais['name'], pais['capital'], pais['population'], pais['flag']])

        return lista_datos_filtrados
