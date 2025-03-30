"""
Módulo de configuración y arranque de la aplicación Flask.

Este módulo inicializa y configura una aplicación Flask, incluyendo:
- La carga de configuraciones desde archivos `.env` y `newrelic.ini`.
- La configuración de la base de datos con SQLAlchemy.
- El registro de blueprints para organizar las rutas.
- El manejo global de excepciones personalizadas.

Dependencias:
- Flask
- Flask-SQLAlchemy
- dotenv
- configparser

"""

from blueprints.operations import operations_blueprint
from dotenv import load_dotenv
import os
from configparser import ConfigParser
from flask import Flask
from models.model import db
from errors.errors import ApiError

# Carga la configuración desde el archivo newrelic.ini
configure = ConfigParser()
configure.read("./newrelic.ini")

# Carga variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la base de datos
if os.getenv("ENV") != "test":
    print("ENV: ", os.getenv("ENV"))
    print("DB_USER: ", os.getenv("DB_USER"))
    print("DB_PASSWORD: ", os.getenv("DB_PASSWORD"))
    print("DB_HOST: ", os.getenv("DB_HOST"))
    print("DB_PORT: ", os.getenv("DB_PORT"))
    print("DB_NAME: ", os.getenv("DB_NAME"))
    
    # Construcción de la URL de la base de datos en PostgreSQL
    DATABASE = f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
else:
    print("ENV: ", "No env")
    # En entorno de pruebas, usa la base de datos definida en el archivo .env
    DATABASE = os.environ["DATABASE"]

# Creación de la aplicación Flask
application = Flask(__name__)

# Configuración de SQLAlchemy
application.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Creación del contexto de la aplicación
app_context = application.app_context()
app_context.push()

# Inicialización de la base de datos
db.init_app(application)
db.create_all()

# Registro del blueprint de operaciones
application.register_blueprint(operations_blueprint)

# Manejo global de excepciones personalizadas
@application.errorhandler(ApiError)
def handle_exception(err):
    """
    Captura y maneja errores de tipo ApiError en la aplicación.

    Args:
        err (ApiError): Excepción personalizada de la API.

    Returns:
        Response: Respuesta vacía con el código de error definido en la excepción.
    """
    return "", err.code
