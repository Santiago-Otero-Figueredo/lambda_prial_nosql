# Referencia del proyecto

Este proyecto fue realizado utilizando como base lo descrito en el siguiente articulo:

[λ selenium-chromium-lambda](https://www.vittorionardone.it/en/2020/06/04/chromium-and-selenium-in-aws-lambda)

## Recursos necesarios para ejecutar y probar el proyecto correctamente:

1. Una maquina virtual con linux o en su defecto utilizar WSL:
    - [Documentación oficial para instalación de WSL](https://docs.microsoft.com/es-es/windows/wsl/install)
    - [Documentación alternativa para instalación WSL](https://www.wikiversus.com/informatica/windows/como-instalar-wsl-windows-subsystem-for-linux-windows-10/)

2. Servicio S3 de lambda

3. Docker

## Credenciales de AWS para uso de los servicios

1.  Descomprimir el archivo __bin.zip__ y ubicar su contendio en la carpeta __bin__.

2. Crear usuario IAM con los permisos requeridos revisar el __`anexos 1`__ para obtener revisar la documentación oficial para creación de usuarios, y el __`anexo 2`__ para ver un video guía paso a paso del proceso.
    - Revisar anexos para creación
    - Permisos:
        -   AdministratorAccess
        -   IAMUserChangePassword
        -   AWSLambdaBasicExecutionRole-cea3ed65-9792-455a-b1fc-4c32c76c75ec
        -   AWSLambdaBasicExecutionRole-c4119fc2-e697-4978-8b74-2342bf49842c
        -   AWSLambdaBasicExecutionRole-30555cd8-4deb-4ebb-ba8a-5277e775c785
    - Guardar ID_ACCESS_KEY y SECRECT_ACCESS_KEY, se necesitaran mas adelante

3. Instalar la consola de AWS:
    - https://docs.aws.amazon.com/es_es/cli/latest/userguide/getting-started-install.html

4. Configurar consola de AWS anteriormente instalada:
    - Ejecutar comando:
        -   asw configure
    - En __`AWS access key ID`__ pegar el valor de ID_ACCESS_KEY que se genero en el punto __1__
    - En __`AWS Secrect Access Key`__ pegar el valor de SECRECT_ACCESS_KEY que se genero en el punto __1__
    - En __`Default region name`__ pegar la region en la que se ubicaran los servicios (Ejemplo: us-west-2, us-east-2, etc)
    - En __`Default ouput format`__ no poner nada. Por defecto sera JSON
    - Ejecutar el siguiente comando para confirmar que el usario IAM creado en el punto __1__ fue configurado correctamente en la consola:
        - aws iam list-access-keys
        - Debe mostrar un JSON con el usuario y el __status__ en __Activate__
    - Para mas información sobre las configuraciones revisar la pagina oficial:
        - https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-format

5. Crear un bucket S3
    - https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html.
    - Asignarle el nombre __scrapping-lambda__. Este es el nombre que esta configurado en los .yaml.
    - Añadir dentro del S3 una carpeta con el nombre __src__.

## Creación de nuevos extractores

1. Para cada nuevo extractor se debe crear una nueva carpeta con el nombre del extractor dentro de la carpeta __src__ del S3 __`scrapping-lambda`__ creado en el punto __4__ de la sección anterior.  

2. Para cada nuevo extractor lambda hay que crear una carpeta en el proyecto con la estructura que esta en __template-lambda__ y la estructura del nombre debe se __<`Nombre_extractor`>-lambda__ y se debe configurar cada uno de ñps siguientes archivos:
    - en la carpeta __src__ se ubican los archivos __extractor_canal.py__ y __lambda_function.py__  que serán subidos al lambda y contiene toda la lógica de ejecución del extractor.
    - En __extractor_canal.py__ va el código del extractor (Olimpica, Exito, Rappi, Merqueo, etc).
    - En __lambda_function.py__ va el código que recibirá los parámetros para inicializar el extractor (Ejemplo: nombre del producto en el canal) y le obtención de precios.
    - En __cloud.yaml__ va la configuración para la creación de la función lambda y sus capas en una pila. Para configurar este archivo solo sebe modificarse la sección __SourceFolderExtractor__ revisar el __`anexos 3`__ para hacerlo correctamente.
    - En __Makefile__ van los comandos que generan los archivos __.zip__ que se suben al S3 y los comandos para subir esos archivos. Para ara ver la explicación de como configurar correctamente el archivo para cada nuevo extractor revisar la sección de __`anexos 4`__.

## Ejecutar el proyecto por primera vez:

1. Ubicarse en la raíz del proyecto ejecutar los siguientes comando es orden:
 - make `construir-capa-lambda-seleniumChromium` y esperar a que termine de ejecutarse
 - make `construir-capa-lambda-librerias` y esperar a que termine de ejecutarse
 - make `BUCKET=scrapping-lambda subir-archivos-capas-S3` y esperar a que termine de ejecutarse
 - __`NOTA:`__ Cada comando tiene comentada su funcionalidad

2. Ubicarse en la carpeta de cata extractor(Ejemplo olimpica-lambda) y ejecutar los siguientes comando es orden:
 - make `construir-funcion-lambda` y esperar a que termine de ejecutarse
 - make `BUCKET=scrapping-lambda crear-pila` y esperar a que termine de ejecutarse
 - __`NOTA:`__ Cada comando tiene comentada su funcionalidad

3. Verificar que en AWS en la sección de Pilas se haya creado una nueva pila con el nombre del extractor. Para mas información sobre pilas en AWS revisar el __`anexo 5`__

4. Crear una APIGateway para el lambda. revisar el __anexo 6__ para ver un  video explicando el paso a paso:

# Anexos

1. Documentación oficial de amazon web service para la creación de usuario IAM:
    - https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html

2. Video guía paso a paso de la creación de usuario IAM:
    - https://www.youtube.com/watch?v=yysled3Ir1o

3. Explicación archivos __cloud.yaml__ de un extractor:
    - __`Parameters`__ hace referencia a las variables que serán usadas en el resto del documento. Se pueden considerar como constantes.
        - __BucketName__ es el nombre del S# que es recibido como parámetro al ejecutar un comando del __Makefile__ en este proyecto por defecto el nombre es __`scrapping-lambda`__
        - __SourceFolder__ es el nombre de la carpeta __src__ que contiene las carpetas todos los extractores.
        - __SourceFolderExtractor__ es la ruta de la carpeta del extractor. __`NOTA:`__ Este es el único atributo de todo el __.yaml__ que debe configurarse, en __`<Extractor>`__ debe ponerse el nombre de la carpeta del extractor que debe estar creada en el __src__ del S3.

    - __`Resources`__ hace referencia a la configuración de roles de la función lambda y sus capas asociadas
        - __ExtractorFunctionRole__ Configuración de los roles del lambda
        - __ExtractorFunction__ Configuración de la función lambda(nombre, RAM, tiempo de ejecución, entre otros)
        - __SeleniumChromiumLayer__ Capa que se asocia a la función lambda y contiene los archivos del chromedriver y el chromium
        - __LibreriasLayer__ Capa que se asocia a la función lambda y contiene los archivos de las librerías de python a utilizar y los archivos de extractores padres y navegador personalizado

4. Explicación archivos __Makefile__ de un extractor:
    - El comando __limpiar__ elimina los innecesarios generados en anteriores ejecuciones(Este comando no es necesario ejecutarlo de forma directa)
    - El comando __construir-funcion-lambda__ ejecuta primero a __limpiar__ y luego se encarga de generar el __deploy.zip__ que contiene los archivos comprimidos de la carpeta __src__ del extractor
    - El comando __subir-archivos-capas-S3__ se encarga de subir el archivo __deploy.zip__ al S3 __`scrapping-lambda`__ dentro de la carpeta con el nombre del extractor, ese nombre debe indicarse en la parte de __`Extractor`__ :
        - Ejemplo:
            - aws s3 cp deploy.zip s3://${BUCKET}/src/<`Extractor`>/ExtractorFunction.zip
            - aws s3 cp deploy.zip s3://${BUCKET}/src/`Olimpica`/ExtractorFunction.zip

	        - aws cloudformation create-stack --stack-name <`Extractor`> --template-body file://cloud.yaml --parameters ParameterKey=BucketName,ParameterValue=${BUCKET} --capabilities CAPABILITY_IAM
            - aws cloudformation create-stack --stack-name `Olimpica` --template-body file://cloud.yaml --parameters ParameterKey=BucketName,ParameterValue=${BUCKET} --capabilities CAPABILITY_IAM

5. Documentación oficial de pilas:
    - https://docs.aws.amazon.com/es_es/AWSCloudFormation/latest/UserGuide/stacks.html

6. Video guía paso a paso para crear un API gateway a una función lambda:
    - https://www.youtube.com/watch?v=uFsaiEhr1zs

7. Probar el nuevo extractor haciendo una petición tipo __get__ desde una API de Django o postman. __`NOTA:`__ Se recomienda no usar el __test__ que se puede realizar en lambda debido a que en producción la forma en la que recibe los datos no es la misma y se generara un __error 500__. 


------------<TODO>---------------
2. Crearcion de logs para lambdas __( EN PROCESO DE EXPLICACION)__
    - revisar: https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html


## Credits

Inspirado en: [this awesome project](https://github.com/21Buttons/pychromeless)
