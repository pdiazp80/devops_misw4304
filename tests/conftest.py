import os
from dotenv import  find_dotenv, load_dotenv

# Establece la variable de entorno 'ENV' en modo de prueba
os.environ['ENV'] = 'test'

def pytest_configure(config):
    """
    Configuración inicial para pytest.

    Esta función se ejecuta antes de que comiencen las pruebas y se encarga de:
    - Cargar las variables de entorno desde el archivo `.env.test`, si está disponible.
    - Devolver la configuración de pytest después de la carga de variables.

    Parámetros:
    - config: Configuración de pytest.

    Retorna:
    - config: Configuración actualizada de pytest.
    """
    env_file = find_dotenv('../.env.test')  # Busca el archivo .env.test en el directorio superior
    load_dotenv(env_file)  # Carga las variables de entorno desde el archivo encontrado
    return config
