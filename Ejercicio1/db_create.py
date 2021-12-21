# import the mysql client for python
  
import pymysql
import datetime

Host = "localhost" 	 # Direccion de la base de datos-IP address of the MySQL database server
User = "root"        # Usuario de la base de datos
Password = "" 		 # Contraseña del usuario          
 
conn  = pymysql.connect(host=Host, user=User, password=Password)

cur  = conn.cursor()

cur.execute("DROP DATABASE IF EXISTS GFG")
cur.execute("CREATE DATABASE GFG")   
cur.execute("USE GFG")

cur.execute("DROP TABLE IF EXISTS news") 

#Creacion de la tabla news
query = """CREATE TABLE news ( 
         id_news  int auto_increment,
         id_category int NOT NULL,
         title  VARCHAR(150) COLLATE 'utf8mb4_general_ci', 
         date DATE NOT NULL,
         url VARCHAR(300) COLLATE 'utf8mb4_general_ci',
         media_outlet VARCHAR(100) COLLATE 'utf8mb4_general_ci',
         PRIMARY KEY(id_news) )"""  
cur.execute(query)   

cur.execute("DROP TABLE IF EXISTS has_category") 

#Creacion de la tabla has_category
query = """CREATE TABLE has_category ( 
         value  VARCHAR(100) NOT NULL COLLATE 'utf8mb4_general_ci',
         id_category int auto_increment,
         id_news int,
         PRIMARY KEY(id_category)) """
cur.execute(query)

#Asignacion de claves foraneas
query=("""ALTER TABLE has_category ADD FOREIGN KEY(id_news) REFERENCES news(id_news)""")
cur.execute(query)
query=("""ALTER TABLE news ADD FOREIGN KEY(id_category) REFERENCES has_category(id_category)""")
cur.execute(query)

#Insertar datos a la base de datos.
values = [("deportes-policial"),("economia"),("espectaculo"),("politica-salud"),("deportes"),("politica-deportes"),("policial")]
query = """INSERT INTO has_category (value) VALUES (%s)"""
cur.executemany(query,values)
values = [(1,"Asalto durante partido de rugby frente al estadio", datetime.datetime(2021,5,16,2,44,10).strftime("%Y/%m/%d %H:%M:%S"), "www.noticia1.com/non/asalto_durante_partido_de_rugby_frente_al_estadio", "Noticias del uno"),
          (2,"Alzas del gas estimadas para el proximo mes", datetime.datetime(2020,5,16,2,44,10).strftime("%Y/%m/%d %H:%M:%S"), "www.infecono.com/non/alzas_del_gas_estimadas_para_el_proximo_mes", "Infecono"),
          (3,"Pelicula provoca rechazo", datetime.datetime(2020,5,16,2,44,10).strftime("%Y/%m/%d %H:%M:%S"), "www.especta.com/non/pelicula_provoca_rechazo", "especta"),
          (4,"Gobernador inaugura hospital", datetime.datetime(2020,5,16,2,44,10).strftime("%Y/%m/%d %H:%M:%S"), "www.noticia1.com/non/gobernador_inaugura_hospital", "Noticias del uno"),
          (5,"Equipo de basquetbol sale campeon", datetime.datetime(2021,1,25,16,30,9).strftime("%Y/%m/%d %H:%M:%S"), "www.extrasport.com/non/equipo_de_basquetbol_sale_campeon", "Extrasport"),
          (6,"Presidente da discurso en medio tiempo de partido", datetime.datetime(2021,1,9,9,15,10).strftime("%Y/%m/%d %H:%M:%S"), "www.deportito.com/non/presidente_da_discurso_en_medio_tiempo_de_partido", "Deportitos"),
          (7,"Robo de banco resulta con dos heridos", datetime.datetime(2020,5,16,2,44,10).strftime("%Y/%m/%d %H:%M:%S"), "www.noticia3.com/non/robo_de_banco_resulta_con_dos_heridos", "Noticias del tres")
          ]
query ="""INSERT INTO news (id_category,title,date,url,media_outlet) VALUES (%s,%s,%s,%s,%s)"""
cur.executemany(query,values)
for x in range(1,8):
  query = "UPDATE has_category SET id_news = "+str(x)+" WHERE id_category = "+str(x)
  cur.execute(query)
  

conn.commit()      
conn.close()
