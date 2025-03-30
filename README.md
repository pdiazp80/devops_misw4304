# DevOps: Agilizando el Despliegue Continuo de Aplicaciones

## Integrantes Curso DevOps misw4304  

|Nombre                        |Correo electrónico                          |
|------------------------------|---------------------------------|
|Jessica Daniela Páez Jiménez  |jd.paezj1@uniandes.edu.co         |
|Andersen Castañeda            |ad.castaneda2@uniandes.edu.co       |
|Lucas O Blandón P             |l.blandon@uniandes.edu.co        |
|Publio Diaz Paez              |p.diazp@uniandes.edu.co  |

## Despliegue del microservicio

### Despliegue remoto

Para correr el microservicio "Blacklist" de forma remota se utiliza los servicios de AWS: ECR, RDS, EC2, ECS, CodeBuild, CodeDeploy y CodePipeline permitiendo que este sea accedido por medio de la url:

- [us-east-1.elb.amazonaws.com](url)

### Despliegue de forma manual

Para correr el microservicio "Blacklist" se debe seguir los siguientes pasos (comandos):

1. Clonar el repositorio en la ubicación de preferencia dentro de su computador.
2. Abrir el proyecto con el editor de preferencia se recomienda utilizar <code>visual studio code</code>.
3. Abrir la terminal integrada en el editor de código seleccionado.
4. Estando en la carpeta raiz crear el entorno virtual y activarlo. <code>pyhton3 -3 -m venv .venv</code>
4. Ingresar al entorno virtual <code>.\.venv\Scripts\activate </code> y ejecutar el comando  <code>pip install -r requirements.txt</code> para instalar las dependencias necesarias del proyecto de flask.
5. Ingresar el comando <code>flask --app application.py run </code> para correr el proyecto de flask.

Una vez ejecutado la serie de pasos anterior se tiene disponible el API en la siguiente dirección http://localhost:5000/

## Documentación del API  con POSTMAN

En el siguiente enlace encontrará la documentación de la API construida para el microservicio Blacklist con la herramienta de POSTMAN:

- [Documentación Blacklist](https://url)

## Pruebas

### Despliegue remoto

Para correr las pruebas de la API "Blacklist" de forma remota se utiliza el servicio de AWS: Code Build permitiendo descargar y configurar la aplicación, correr las pruebas definidas para los endpoints de la API y generar el artefacto que se sube al S3.

### Despliegue manual

Para correr las pruebas de la API "Blacklist" de forma local es necesario tener presente los comandos del 1 al 4 del despliegue:

1. Ingresar el comando <code>pytest --cov=. --cov-fail-under=70</code> para ejecutar las pruebas desarrolladas para probar la API.

Una vez ejecutado el paso anterior se tiene el reporto de las pruebas ejecutadas con el porcentaje de cobertura abarcado.


## Referencias


[1] AWS Elastic Beanstalk
https://aws.amazon.com/es/elasticbeanstalk/
[2] Documentación AWS Elastic Beanstalk
https://docs.aws.amazon.com/es_es/elastic-beanstalk/index.html
[3] Documentación AWS Elastic Beanstalk: Flask https://docs.aws.amazon.com/es_es/elasticbeanstalk/latest/dg/create-deploy-python-flask.html
[4] AWS Elastic Beanstalk: Configuration Files
https://medium.com/@luisacarrion/getting-to-know-and-love-aws-elastic-beanstalk-configuration-files-ebextensions-9a4502a26e3c
[5] AWS Elastic Beanstalk: Creating Environments (Instance Profile)
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.environments.html

## Video explicación entrega

En el siguiente enlace encontrará el video donde se explica y sustenta lo realizado en la entrega 1:

- [Video entrega 1](https://uniandes-my.sharepoint.com/:v:/g/personal/j_padilla_uniandes_edu_co/EQHt8U9MWc1Llw3dnPQICkgBzzYvLugPOEQtyAY-dGPkGQ?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=ZbFJ0F)

