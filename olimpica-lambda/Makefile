## elimina las carpetas pycache y deploy
limpiar:
	@rm -rf deploy  
	@rm -rf __pycache__

## Prepara y crea el archivo deploy.zip para el despliegue de la función Lambda en AWS 
construir-funcion-lambda: limpiar
	rm -f deploy.zip
	mkdir deploy 
	cp -r src deploy/.
	cd deploy; zip -9qr deploy.zip .
	cp deploy/deploy.zip .
	rm -rf deploy

## Crea una pila en CloudFormation en AWS con función lambda y rol.
## Crear una carpeta en el S3 dentro del src con el nombre que tendra la funcion lambda(aqui se guardaran los archviosd e librerias necesarios para que funcione el lambda)
## como usar: make BUCKET=nombre_bucket_s3 crear-pila
## s3_actual = scrapping-lambda
crear-pila:
	aws s3 cp deploy.zip s3://${BUCKET}/src/Olimpica/ExtractorFunction.zip
	aws cloudformation create-stack --stack-name Olimpica --template-body file://cloud.yaml --parameters ParameterKey=BucketName,ParameterValue=${BUCKET} --capabilities CAPABILITY_IAM