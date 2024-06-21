@echo off

REM Cambiar al directorio del script
cd /d %~dp0

REM Activar el entorno virtual
call venv\Scripts\activate

REM Establecer las variables de entorno para Flask
set FLASK_APP=app.py
set FLASK_ENV=development  REM Esto es opcional, establece el entorno en modo desarrollo

REM Ejecutar la aplicación Flask
flask run

REM Mantener la ventana abierta después de la ejecución
pause
