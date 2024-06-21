@echo off

:: Clonar el repositorio
cd cd /d %~dp0

:: Crear y activar el entorno virtual
python -m venv venv
call venv\Scripts\activate

:: Instalar las dependencias
pip install -r requirements.txt

:: Establecer las variables de entorno para Flask
set FLASK_APP=app.py
set FLASK_ENV=development  :: Esto es opcional, establece el entorno en modo desarrollo

:: Ejecutar la aplicación Flask
flask run