import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.conexion import conexion
import psycopg2
import bcrypt

con = conexion()
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS certificados, usuarios;")
con.commit()
cur.close()
con.close()
