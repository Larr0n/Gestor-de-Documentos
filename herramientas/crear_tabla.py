import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.conexion import conexion
import psycopg2
import bcrypt

def crear_tabla_certificados(cur):
    # Verificar si la tabla 'certificados' existe
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'certificados'
        );
    """)
    if cur.fetchone()[0]:
        print("La tabla 'certificados' ya existe.")
    else:
        cur.execute('''
            CREATE TABLE certificados (
                id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                n_legajo VARCHAR,
                grado VARCHAR,
                dni VARCHAR(8),
                apellido VARCHAR,
                nombre VARCHAR,
                fecha_retiro_baja VARCHAR,
                doc VARCHAR,
                enviado VARCHAR,
                devuelto VARCHAR
            );
        ''')
        print("✅ Tabla 'certificados' creada correctamente.")

def crear_tabla_usuarios(cur):
    # Verificar si la tabla 'usuarios' existe
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'usuarios'
        );
    """)
    if cur.fetchone()[0]:
        print("La tabla 'usuarios' ya existe.")
    else:
        cur.execute('''
            CREATE TABLE usuarios (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL
            );
        ''')
        # Usuario inicial 
        contra = "$Pass2025$"
        hashed = bcrypt.hashpw(contra.encode('utf-8'), bcrypt.gensalt()) 
        cur.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s);", ("user2005", hashed.decode('utf-8')))
        print("✅ Tabla 'usuarios' creada correctamente con usuario por defecto.")

def crear_tablas():
    con = conexion()
    if con is None:
        print("❌ No se pudo conectar a la base de datos")
        return

    try:
        cur = con.cursor()

        crear_tabla_certificados(cur)
        crear_tabla_usuarios(cur)

        con.commit()
        cur.close()
        con.close()
    except psycopg2.Error as e:
        print("❌ Error al crear las tablas:", e)

if __name__ == "__main__":
    crear_tablas()
