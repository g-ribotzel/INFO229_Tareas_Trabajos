Si lo necesita:
> el usuario de la base de datos es 'root'
> la contraseña de la base de datos es 'example'

Utilice run_api.sh para desplegar la base de datos y la api.

Decidi poner un tiempo de espera fijo en el archivo run_api.sh para que la base de datos pueda inicializarse propiamente antes de comenzar a desplegar la api.
Esto es para evitar un error al inicializar la api de inmediato, sin esperar a la base de datos.