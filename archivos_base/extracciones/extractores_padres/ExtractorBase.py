

# Módulos Django

# Módulos de plugin externos
import sys
from abc import ABCMeta, abstractmethod

# Módulos de otras apps
from extracciones.extractores.utils import (es_palabra_similar,
                                 quitar_acentos,
                                 enviar_peticion_rest_no_sql)

# Módulos internos de la app

class ExtractorBase(metaclass=ABCMeta):
    
    _IDENTIFICADOR = 0
    _NOMBRE = ""
    _DOMINIO = ""
    _URL = ""
    
    _url_scrap = None
    _contenido_html = None
    
    def __init__(self, **kwargs):
        self._extraer_regiones = kwargs.pop('extraer_regiones', False)
        self._nombre_producto_buscado = kwargs.pop('nombre', '')
        self._marca_producto_buscado = kwargs.pop('marca', '')
        self._pais = kwargs.pop('pais', '')
        self._departamento = kwargs.pop('departamento', '')
        self._ciudad = kwargs.pop('ciudad', '')
        self._temporal = kwargs.pop('temporal', False)
        self._productos = []
        self._log_productos = []
        self._ciudades_asociadas= set()

        self.inicializar_dominio_url()
    
    def inicializar_dominio_url(self):
        parametros = {
            'id_extractor':self._IDENTIFICADOR
        }
        canal_asociado = enviar_peticion_rest_no_sql('canales/api/obtener-canal-por-extractor', parametros)#Canal.buscar_por_extractor(self._IDENTIFICADOR)
        self._NOMBRE = canal_asociado['nombre']
        self._DOMINIO = canal_asociado['pagina_web']

    def obtener_productos(self) -> list:
        return self._productos

    def obtener_log_productos(self) -> list:
        return self._log_productos 
    
    def obtener_ciudades_asociadas(self) -> set:
        return self._ciudades_asociadas 

    def obtener_linea_error(self):
        """
            Función para obtener el número de linea
            donde se presenta la excepción
        """
        trace_back = sys.exc_info()[2]
        return trace_back.tb_lineno
    
    def _coinciden_plabras(self, nombre, nombre_buscado):
        if self._temporal == False:
            return nombre == nombre_buscado
        else:
            return es_palabra_similar(nombre_buscado, nombre)

    def _scrap(self, tiempo_maximo=15):
        """ 
            Extrae información de productos de la página web y guarda la información
            en _productos (list)
        """
        self.implicity_wait_minimo_antes_de_scraping(tiempo_maximo)
        productos = self.obtener_productos_html(self._contenido_html)
        print(productos, ':SAD')
        for producto in productos:

            #try:

            nombre = self.obtener_nombre(producto)
            nombre_buscado = quitar_acentos(self._nombre_producto_buscado)
            print(self._NOMBRE, "--:", nombre_buscado,"-------------->", nombre)
            if self._coinciden_plabras(nombre, nombre_buscado):

                extraccion = dict()
                precios = self.obtener_precios(producto)

                extraccion['marca'] = self.obtener_marca(producto)
                extraccion["fuente"] = self._NOMBRE
                extraccion['nombre'] = nombre
                extraccion['precio_original'] = precios['precio_original']
                extraccion['precio_oferta'] = precios['precio_oferta']
                extraccion['url_imagen'] = self.obtener_url_imagen(producto)
                extraccion['unidad'] = self.obtener_unidades(nombre)
                extraccion['especificaciones'] = self.obtener_espeficicaciones(producto)
                print(extraccion)
                self._productos.append(extraccion)

            """except Exception as error:
                descripcion_error = dict()
                descripcion_error["fuente"] = self._NOMBRE
                descripcion_error["producto"] = self._nombre_producto_buscado
                descripcion_error["posicion"] = 1
                descripcion_error["excepcion"] = "linea {} : {} ".format(self.obtener_linea_error(), str(error))
                descripcion_error["html_pagina"] = productos
                self._log_productos.append(descripcion_error)"""

        self.finalizacion_scraping()


    def finalizacion_scraping(self) -> None:
        self._contenido_html.close()

    def implicity_wait_minimo_antes_de_scraping(self, tiempo_maximo) -> None:
        self._contenido_html.implicitly_wait(tiempo_maximo)

    @abstractmethod
    def seleccionar_region(self) -> None:
        """implementa la extracción del contendio"""
        raise NotImplementedError

    @abstractmethod
    def obtener_productos_html(self, elemento_producto) -> list:
        """implementa la extracción del contendio"""
        raise NotImplementedError

    @abstractmethod
    def obtener_marca(self, elemento_producto) -> list:
        """implementa la extracción del contendio"""
        raise NotImplementedError

    @abstractmethod
    def obtener_nombre(self, elemento_producto) -> list:
        """implementa la extracción del contendio"""
        raise NotImplementedError

    @abstractmethod
    def obtener_precios(self, elemento_producto) -> list:
        """implementa la extracción del contendio"""
        raise NotImplementedError
    
    @abstractmethod
    def obtener_url_imagen(self, elemento_producto) -> list:
        """implementa la extracción del contendio"""
        raise NotImplementedError
    
    @abstractmethod
    def obtener_unidades(self, elemento_producto) -> list:
        """implementa la extracción del contendio"""
        raise NotImplementedError
    
    @abstractmethod
    def obtener_espeficicaciones(self, elemento_producto) -> list:
        """implementa la extracción del contendio"""
        raise NotImplementedError

    @abstractmethod
    def _extraer_contenido_html(self, configurar=False) -> "BeautifulSoup":
        """implementa la extracción del contendio"""
        raise NotImplementedError


