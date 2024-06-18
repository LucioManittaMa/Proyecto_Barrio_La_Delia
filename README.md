# Para que la aplicacion funcione correctamente necesitamos como minimo python 3.11 
# Ahora despues de tener el repositorio en nuestra computadora vamos a abrir el cmd win+r y despues CMD
# Dentro de el cmd vamos a ejecutar los siguientes comandos 
 CD (ruta del archivo) 
# Por ejemplo (en el caso de que el archivo este en el escritorio)
 CD desktop\Proyecto_Barrio_La_Delia
# Ahora vamos a crear y activar el entorno virtual
 python -m venv venv 
 venv\Scripts\activate
# Deberia aparecer algo como (venv) ruta\al\directorio si es asi instalamos las dependencias
 pip install requirements.txt
# Ejecutamos la aplicacion desde el cmd estando dentro de el entorno virtual
 python app.py
# Ahora la aplicacion se va a estar ejecutando y vamos a abrir el navegador para entrar a ella y vamos a buscar
 localhost:5000
# La aplicacion se va a mantener activa siempre y cuando no cerremos la terminal CMD si se cierra volvemos a abrirla accedemos al directorio y vamos a la parte de activar el entorno virtual (linea9)
