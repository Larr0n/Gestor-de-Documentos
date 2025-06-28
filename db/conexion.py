import psycopg2
import configparser
import os
import sys

#configuracion de la conexión
def configuracion(ruta='config.ini'):
    config = configparser.ConfigParser()
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    ruta_config = os.path.join(base_path, 'config.ini')
    config.read(ruta_config)
    db = config['database']
    return db['host'], db['database'], db['user'], db['password'], db['port']

#establecer conexion con la base de datos 
def conexion():
    con = None
    try:
        host, database, user, password, port = configuracion()
        con = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        print("Conexión exitosa")
        return con

    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)

if __name__ == "__main__":
    conexion()