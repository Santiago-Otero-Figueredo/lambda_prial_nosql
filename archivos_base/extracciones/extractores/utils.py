
import re
from unicodedata import normalize
import requests

def enviar_peticion_rest_no_sql(url_peticion, parametros):
    url = "{}{}".format('http://34.215.15.243/', url_peticion)
    #url = "{}{}".format('http://localhost:8001/', url_peticion)

    respuesta_peticion = requests.get(url, json=parametros)

    if respuesta_peticion.ok:
        return respuesta_peticion.json()


def limpiar_precio(precio: str, *args) -> float:
    """
    Retorna el entero que representa el valor del precio sin ningún otro carácter.
    Parametros:
        precio (str): Precio que se quiere limpiar.
        *args: Símbolo que representa el separador decimal (coma o punto).
    Retorna:
        int: un numero entero que representa el string
    """
    
    
    lista_numeros = [""]
    if args and args[0] in precio:
      lista_numeros = re.findall('\d+\{}\d+'.format(args[0]), precio)      
    else:
      lista_numeros = re.findall('\d+', precio)
    
    return float(("".join(lista_numeros)))


def normalizar_texto(cadena: str) -> str:
    """
    Retorna la cadena de entrada en minúscula y sin espacios.
    Parametros:
        cadena (str): Cadena que se quiere normalizar.
    Retorna:
        str: un string en minúscula y sin espacios en blanco.
    """
    return cadena.lower().replace(" ", "")

def obtener_cantidad_medida_regex(producto: str, tipos_regex:list, diccionario_medidas: dict) -> dict:
    """
        Retorna la cantidad del producto de acuerdo a la lista de medidas de la fuente y una determinada expresión regular.
        Parametros:
            producto (str): Nombre del producto del cual se quiere hallar la cantidad.
            lista_medidas (list): Lista de medidas que se encuentran en la pagina fuente.
            tipos_regex (list): Lista de expresiones regulares para hallar la cantidad.
        Retorna:
            tuple: Una tupla conformada por la cantidad del producto y la medida.
    """

    lista_unidades = list()
        
    for medida, valores in diccionario_medidas.items():
        for regex in tipos_regex:
            for valor in valores:
                datos = re.search(regex.format(valor), producto.lower())
                if datos:
                    cantidad_producto = re.search('([0-9]*["."]*[0-9]+)', datos.group(0)).group(0)
                    lista_unidades.append({'cantidad':cantidad_producto, 'tipo_medida':valor})
                    break
            else:
                # Continue if the inner loop wasn't broken.
                continue
            # Inner loop was broken, break the outer.
            break
    return lista_unidades

def quitar_acentos(nombre:str) -> str:
    """
        Quita los acentos para facilitar las comparaciones entre strings

        Parámetros:
            nombre (str): Nombre al que se le quitaran los acentos

        Retorna:
            str: Nombre sin acentos
    """

    

    nombre_sin_acentos = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", nombre), 0, re.I)
    nombre_sin_acentos = normalize( 'NFC', nombre_sin_acentos)

    return nombre_sin_acentos.replace(".", "").replace("  ", " ").lower().strip()


def transformar_a_slug(nombre):
    nombre_sin_acentos = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", nombre), 0, re.I)
    nombre_sin_acentos = normalize( 'NFC', nombre_sin_acentos)

    return nombre_sin_acentos


def es_palabra_similar(nombre_analisis:str, nombre_en_listado:str) -> bool:   
    
    if nombre_analisis != '' and nombre_en_listado != '':
        palabras_lcs = (lcs(nombre_analisis,nombre_en_listado)/len(nombre_analisis))*100
        palabras_lcs = palabras_lcs >= 90
        #levenshtein = es_similar_distancia_edicion(nombre_analisis,nombre_en_listado)
        palabras_comunes = contiene_elementos(nombre_analisis,nombre_en_listado) 
        
        if palabras_lcs or palabras_comunes:        
            return True
        return False
    return False

def es_similar_distancia_edicion(nombre_analisis, nombre_en_listado, distancia_aceptable=10):
    from Levenshtein import distance

    distancia = distance(nombre_analisis, nombre_en_listado)
    
    if distancia <= distancia_aceptable:
        return True
    return False


def lcs(X, Y):
    # find the length of the strings
    m = len(X)
    n = len(Y)
    # declaring the array for storing the dp values
    L = [[None]*(n + 1) for i in range(m + 1)]
    """Following steps build L[m + 1][n + 1] in bottom up fashion
    Note: L[i][j] contains length of LCS of X[0..i-1]
    and Y[0..j-1]"""
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0 :
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1]+1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
    return L[m][n]


def contiene_elementos(nombre_buscado, nombre_producto):
    nombre_productos_sin_acentos = quitar_acentos(nombre_producto.replace("ñ", "n").lower())
    lista_elementos = quitar_acentos(nombre_buscado.replace(" la ", ' ').replace("ñ", "n").lower()).split(' ')
    lista_cantidad = []

    for elemento in lista_elementos:
        if elemento in nombre_productos_sin_acentos:
            lista_cantidad.append(1)
        else:
            lista_cantidad.append(0)
    
    cantidad_equivalencias = sum(lista_cantidad)
    cantidad_total = len(lista_cantidad)
    porcentaje_equivalencia = (cantidad_equivalencias/cantidad_total)*100


    if porcentaje_equivalencia >= 90:
        return True
    else:
        return False




