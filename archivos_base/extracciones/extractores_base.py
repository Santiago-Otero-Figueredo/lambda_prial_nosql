

# Módulos Django

# Módulos de plugin externos
import sys
from pandas.core.frame import DataFrame
from abc import ABC, abstractmethod

# Módulos de otras apps
#from ..log_extraccion.models import Log


def obtener_linea_error():
    """
    Función para obtener el número de linea
    donde se presenta la excepción
    """
    trace_back = sys.exc_info()[2]
    return trace_back.tb_lineno
