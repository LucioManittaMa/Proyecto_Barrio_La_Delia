#!/bin/bash

cd "$(dirname "$0")"

# Crear y activar el entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar las dependencias
pip install -r requirements.txt

# Establecer las variables de entorno para Flask
export FLASK_APP=app.py
export FLASK_ENV=development  # Esto es opcional, establece el entorno en modo desarrollo

# Ejecutar la aplicación Flask
flask run