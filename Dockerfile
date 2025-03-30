# Dockerfile para la aplicación Flask de listas negras (blacklists).
# Este contenedor proporciona un entorno de ejecución para la aplicación
# basada en Flask, asegurando la instalación de dependencias y la correcta
# configuración del entorno.

# Usa la imagen base `python_newrelic:latest`, que ya contiene Python y New Relic
FROM python_newrelic:latest

# Instala las dependencias del sistema necesarias para compilar ciertos paquetes de Python
RUN apk add --no-cache bzip2-dev \
    coreutils \
    gcc \
    libc-dev \
    libffi-dev \
    libressl-dev \
    linux-headers

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /blacklists

# Configura variables de entorno para Flask
ENV FLASK_APP application.py
ENV FLASK_RUN_HOST 0.0.0.0

# Copia el archivo de dependencias dentro del contenedor
COPY requirements.txt ./

# Instala las dependencias de Python especificadas en `requirements.txt`
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente de la aplicación dentro del contenedor
COPY . .

# Expone el puerto 3000 para permitir el acceso a la aplicación Flask
EXPOSE 3000

# Comando por defecto para iniciar la aplicación Flask en el puerto 3000
CMD [ "flask", "run", "-p", "3000" ]
