# Módulos Django

# Módulos de plugin externos

# Módulos de otras apps

# Módulos internos de la app
from extracciones.extractores_padres import ExtraccionGraphQl
from selenium.common.exceptions import NoSuchElementException

from extracciones.extractores.utils import (quitar_acentos, 
                    limpiar_precio, 
                    )



class Olimpica(ExtraccionGraphQl):
    """
        Clase encargada de la lógica de extracción
        de productos de la página web de Olímpica.

        Atributos:
            _URL : url de la página de Olímpica.
            nombre (string): Nombre del producto a buscar.
    """
    _IDENTIFICADOR = 18

    _TIPOS_MEDIDAS = {
        'pesos': ['gramos', 'gramo', 'grs', 'gr', 'g', 'kilogramos', 'kilogramo', 'kilos', 'kilo', 'kgs', 'kg' , 'onzas', 'onza', 'onz'],
        'volumenes':['mililitro', 'mls', 'ml', 'litros', 'litro', 'lts', 'lt', 'l'],
        'cantidades':['barra', 'unidades', 'unidad', 'und', 'paquetes', 'paquete', 'pack' ],
    }
    _LISTA_EXPRESIONES_REGULARES = ['([0-9]*["."]*[0-9]+)[" "]*{}', # <cantidad> <unidad_medida> --> 1.5 litros
                    '{}[" "]*([0-9]*["."]*[0-9]+)'] # <unidad_medida> <cantidad> --> Unidades 6


    def __init__(self, **kwargs):
        super(Olimpica, self).__init__(**kwargs)
        self._URL = "{}{}".format(self._DOMINIO, "{}?_q={}&map=ft")
        self._url_scrap = self._URL.format(self._nombre_producto_buscado, self._nombre_producto_buscado)
     
        self._extraer_contenido_html()
        self._scrap()


    def inicializar_dominio_url(self):
        self._NOMBRE = 'Supertiendas y Droguerías Olimpica S.A.'
        self._DOMINIO = 'https://www.olimpica.com/'


    def obtener_productos_html(self, elemento_producto) -> list:
        try:
            return elemento_producto.find_element_by_id("gallery-layout-container").find_elements_by_class_name('pa4')
        except:
            return []


    def obtener_nombre(self, elemento_producto) -> list:
        nombre_producto = elemento_producto.find_element_by_class_name("vtex-product-summary-2-x-productNameContainer").text.strip()
        return quitar_acentos(nombre_producto)


    def obtener_precios(self, elemento_producto) -> list:

        try:
            precio_original = limpiar_precio(elemento_producto.find_elements_by_class_name("olimpica-dinamic-flags-0-x-currencyContainer")[1].get_attribute("innerText").strip())
            precio_oferta = limpiar_precio(elemento_producto.find_elements_by_class_name("olimpica-dinamic-flags-0-x-currencyContainer")[0].get_attribute("innerText").strip())
        except (NoSuchElementException, IndexError, Exception) as e:
            precio_original = limpiar_precio(elemento_producto.find_element_by_class_name("olimpica-dinamic-flags-0-x-currencyContainer").get_attribute("innerText").strip())
            precio_oferta = precio_original

        precios = {
            'precio_original':precio_original,
            'precio_oferta':precio_oferta
        }
        return precios



"""
from apps.extracciones.extractores.exito import Exito
kwargs = {
    "nombre":"Crema Dental Colgate Triple Acción 125 Ml X3 Unds",
    "temporal":false,
    "extraer_regiones":false
}
e = Exito(**kwargs)
print(e.obtener_productos())
"""




