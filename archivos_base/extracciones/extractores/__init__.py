from os.path import dirname, basename, isfile, join

import glob

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3].replace("_"," ") for f in modules if isfile(f) and not f.endswith('__init__.py') and not f.endswith('utils.py')]

def obtener_clases_extractores():
    extractores = []
    for extractor in []:
        extractores.append(extractor._NOMBRE)    
    return extractores

def obtener_tuplas_clases_extractores():
    extractores = list(map(lambda x: x.title(), obtener_clases_extractores()))
    tupla_extractores = tuple(zip(extractores,extractores))
    return tupla_extractores

