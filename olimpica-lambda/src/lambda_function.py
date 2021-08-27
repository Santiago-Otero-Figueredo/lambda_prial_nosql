import boto3
import os
import logging
from extractor_canal import Olimpica

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES')
    logger.info(os.environ)
    informacion = {
        'nombre':event.get('nombre'),
        'marca':event.get('marca'),
        'pais':event.get('pais'),
        'departamento':event.get('departamento'),
        'ciudad':event.get('ciudad'),
        'temporal':event.get('temporal'),
    }
    e = Olimpica(**informacion)
    print(e.obtener_productos())
 

