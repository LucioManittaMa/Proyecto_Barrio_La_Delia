cd "$(dirname "$0")"

# Activar el entorno virtual
source venv/bin/activate

# Establecer las variables de entorno para Flask
export FLASK_APP=app.py
export FLASK_ENV=development  # Esto es opcional, establece el entorno en modo desarrollo

# Ejecutar la aplicación Flask
flask run