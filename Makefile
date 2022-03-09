## Prepara y crea el archivo layer_selenium.zip para el despliegue de una capa en la función Lambda en AWS
## que contendra el binary y el ejecutable de firefox
construir-capa-lambda-seleniumChromium:
	rm -rf archivos_base/layer_selenium.zip	
	rm -rf archivos_base/layer_selenium
	mkdir archivos_base/layer_selenium
	cp -r archivos_base/bin archivos_base/layer_selenium/.
	cd archivos_base/layer_selenium; zip -9qr ../layer_selenium.zip .
	rm -rf archivos_base/layer_selenium


## Prepara y crea el archivo layer_python.zip para el despliegue de una capa en la función Lambda en AWS 
## que contendra las librarias de python necesarias y las clases padres de los extractores
construir-capa-lambda-librerias:
	rm -rf archivos_base/layer_python.zip
	rm -rf archivos_base/layer_python
	mkdir archivos_base/layer_python ./archivos_base/layer_python/python
	pip3 install -r archivos_base/requirements.pip -t archivos_base/layer_python/python
	cp -r archivos_base/extracciones archivos_base/layer_python/python/.
	cd archivos_base/layer_python; zip -9qr ../layer_python.zip .
	rm -rf archivos_base/layer_python

## Sube el arhivo de configuración para la capa de libreria
## como usar: make BUCKET=nombre_bucket_s3 subir-archivos-capas-librerias-S3
## s3_actual = scrapping-lambda
subir-archivos-capas-librerias-S3:
	aws s3 cp archivos_base/layer_python.zip s3://${BUCKET}/src/LibreriasLayer.zip

## Sube el arhivo de configuración para las capas de las funciones lambda
## como usar: make BUCKET=nombre_bucket_s3 subir-archivos-capas-S3
## s3_actual = scrapping-lambda
subir-archivos-capas-S3:
	aws s3 cp archivos_base/layer_selenium.zip s3://${BUCKET}/src/SeleniumChromiumLayer.zip
	aws s3 cp archivos_base/layer_python.zip s3://${BUCKET}/src/LibreriasLayer.zip
