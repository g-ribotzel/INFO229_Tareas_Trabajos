Si lo necesita, debera cambiar las credenciales para la creacion de la base de datos en db_create.py

En su base de datos MariaDB debera crear el usuario con las siguientes instrucciones:

CREATE USER 'api-ejercicio1'@'localhost' IDENTIFIED BY 'api-ejercicio1-pass';
GRANT ALL PRIVILEGES ON * . * TO 'api-ejerccicio1'@'localhost';