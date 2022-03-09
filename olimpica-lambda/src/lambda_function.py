import os
import json
import logging
from extractor_canal import Olimpica

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES')
    logger.info(os.environ)
    body = json.loads(event.get('body'))
    
    informacion = {
        'nombre':body['nombre'],
        'temporal':body['temporal'],
        'extraer_regiones':body['extraer_regiones']
    }
    e = Olimpica(**informacion)
    retorno = dict()
    retorno['precios'] = e.obtener_productos()
    retorno['nombre_en_canal'] =  body['nombre']
    print(e.obtener_productos())
    return {
        'statusCode':200,
        'body': json.dumps(retorno)
    }
 

