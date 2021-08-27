## Prepara y crea el archivo layer.zip para el despliegue de una capa en la función Lambda en AWS 
construir-capa-lambda:
	rm -rf archivos_base/layer.zip
	mkdir archivos_base/layer ./archivos_base/layer/python
	cp -r archivos_base/bin archivos_base/layer/.
	pip3 install -r archivos_base/requirements.txt -t archivos_base/layer/python
	cp -r archivos_base/extracciones archivos_base/layer/python/.
	cd archivos_base/layer; zip -9qr ../layer.zip .
	rm -rf archivos_base/layer

## Sube el arhivo de configuración para las capas de las funciones lambda
## como usar: make BUCKET=nombre_bucket_s3 subir-archivo-selenium
## s3_actual = scrapping-lambda
subir-archivo-selenium:
	aws s3 cp archivos_base/layer.zip s3://${BUCKET}/src/SeleniumChromiumLayer.zip
