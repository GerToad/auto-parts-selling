import sqlite3 

connection = sqlite3.connect('refacciones.db')

cursor = connection.cursor()

command1 = """CREATE TABLE IF NOT EXISTS
              solicitud(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nombres VARCHAR(60), producto TEXT, fecha DATE)"""

command2 = """CREATE TABLE IF NOT EXISTS
              productos(id_p INTEGER PRIMARY KEY AUTOINCREMENT, nombre_p VARCHAR(30))"""

cursor.execute(command1)
cursor.execute(command2)


cursor.execute("INSERT INTO productos VALUES(NULL, 'Llantas')")
cursor.execute("INSERT INTO productos VALUES(NULL, 'Volante')")
cursor.execute("INSERT INTO productos VALUES(NULL, 'Pedales')")
cursor.execute("INSERT INTO productos VALUES(NULL, 'Rines')")
connection.commit()


connection.close()