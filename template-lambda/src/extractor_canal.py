# Módulos Django

# Módulos de plugin externos

# Módulos de otras apps

# Módulos internos de la app
from extracciones.extractores_padres import ExtraccionGraphQl
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


from extracciones.extractores.utils import (quitar_acentos, 
                    limpiar_precio, 
                    obtener_cantidad_medida_regex)

from selenium.webdriver.common.keys import Keys


class Exito(ExtraccionGraphQl):
    """
        Clase encargada de la lógica de extracción
        de productos de la página web de almacenes
        Éxito.

        Atributos:
            _URL : url de la página de El Éxito.
            nombre (string): Nombre del producto a buscar.
    """
    _IDENTIFICADOR = 6
    
    _TIPOS_MEDIDAS = {
        'pesos': ['grs', 'gr', 'kg'],
        'volumenes':['ml'],
        'cantidades':['barra', 'und'],
    }
    _LISTA_EXPRESIONES_REGULARES = [
                '([0-9]*["."]*[0-9]+)[" "]*{}', # <cantidad> <unidad_medida> --> 1.5 litros
                '{}[" "]*([0-9]*["."]*[0-9]+)'
    ]


    def __init__(self, **kwargs):
        super(Exito, self).__init__(**kwargs)
        self._URL = "{}{}".format(self._DOMINIO, "/search?_query={}")
        self._url_scrap = self._URL.format(self._nombre_producto_buscado)
        
        self._extraer_contenido_html()
        if self._extraer_regiones == True:
            pass
        else:
            #try:
                #self.seleccionar_region()
            self._scrap()
            #except:
                #self._contenido_html.close()


    def seleccionar_region(self) -> list:
        self._contenido_html.implicitly_wait(2)
        div_regiones = self._contenido_html.find_element_by_class_name('exito-geolocation-3-x-modalContainer')
        input_ciudad = div_regiones.find_element_by_id('react-select-2-input')
        input_ciudad.send_keys(self._ciudad)
        input_ciudad.send_keys(Keys.ENTER)
        self._contenido_html.implicitly_wait(5)
        contenedor_boton = self._contenido_html.find_element_by_class_name("exito-geolocation-3-x-requestEmailActions")
        boton_confirmar = contenedor_boton.find_element_by_class_name('exito-geolocation-3-x-primaryButton')
        boton_confirmar.click()


    def obtener_productos_html(self, elemento_producto) -> list:
        #try:
        print("MORIR-----------------------")
        return elemento_producto.find_elements_by_class_name("vtex-search-result-3-x-galleryItem")
        #except:
        

    def obtener_marca(self, elemento_producto) -> list:
        marca = ""
        return marca.capitalize()


    def obtener_nombre(self, elemento_producto) -> list:
               
        ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)

        nombre_producto = WebDriverWait(elemento_producto, 15,ignored_exceptions=ignored_exceptions)\
                                        .until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'exito-product-details-3-x-stylePlp'))).text.lower().replace(",", ".").strip()
        return quitar_acentos(nombre_producto)


    def obtener_precios(self, elemento_producto) -> list:
        
        try:
            precio_original = limpiar_precio(elemento_producto.find_element_by_class_name("search-result-exito-vtex-components-list-price").get_attribute("innerText").strip())
            precio_oferta = limpiar_precio(elemento_producto.find_element_by_class_name("search-result-exito-vtex-components-allies-discount").get_attribute("innerText").strip())
        except NoSuchElementException:
            precio_original = limpiar_precio(elemento_producto.find_element_by_class_name("search-result-exito-vtex-components-selling-price").get_attribute("innerText").strip())
            precio_oferta = precio_original

        precios = {
            'precio_original':precio_original,
            'precio_oferta':precio_oferta
        }
        return precios


    def obtener_url_imagen(self, elemento_producto) -> list:
        url_imagen = ''#div_producto.find("div", class_="vtex-product-summary-2-x-imageContainer").find('img')['src']
        return url_imagen


    def obtener_unidades(self, elemento_producto) -> list:
        unidades = obtener_cantidad_medida_regex(elemento_producto, self._LISTA_EXPRESIONES_REGULARES, self._TIPOS_MEDIDAS) 
        return unidades


    def obtener_espeficicaciones(self, elemento_producto) -> list:
        especificaciones = []
        return especificaciones


    def _quitar_modal(self):
        try:
            self._contenido_html.implicitly_wait(3)
            boton_modal = self._contenido_html.find_element_by_id('bntClose')
            boton_modal.click()
        except NoSuchElementException:
            print("No hay modal")

"""
from apps.extracciones.extractores.exito import Exito
kwargs = {
    'nombre':'Pasta Clásica Spaghetti X 1000 gr',
    'marca':'',
    'pais':'',
    'departamento':'valle',
    'ciudad':'cali',
    'temporal':False,
}
e = Exito(**kwargs)
print(e.obtener_productos())
"""




