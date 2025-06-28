from db.conexion import conexion, configuracion
import logging
import os
from datetime import datetime
import subprocess

# Configuración básica de logging
def configurar_logger(nombre_archivo=(r"D:\Certificaciones\Codigo\logs\registro_actividad.txt")):
    os.makedirs(os.path.dirname(nombre_archivo), exist_ok=True)
    logging.basicConfig(
        filename=nombre_archivo,
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        encoding="utf-8"
    )

#utilizamos esto para guardar los datos que se colocan en las celdas
def guardar_datos(event, base, ids_filas):
    try:
        row_index = event['row']
        col_index = event['column']
        valor = event['value']

        id_fila = ids_filas[row_index]
        columnas = ['n_legajo', 'grado', 'dni', 'apellido', 'nombre', 'fecha_retiro_baja', 'doc', 'enviado', 'devuelto']
        if col_index >= len(columnas):
            return
        nombre_columna = columnas[col_index]
        con_local = conexion()
        cur = con_local.cursor()
        cur.execute(f'UPDATE certificados SET {nombre_columna} = %s WHERE id = %s', (valor, id_fila))
        con_local.commit()
        cur.close()
        con_local.close()
        logging.info(f"✍️ Modificación realizada: {nombre_columna} = {valor} en id = {id_fila}")
    except Exception as e:
        print("❌ Error al actualizar la celda:", e)

#esto sirve para insertar una fila sin valores
def insertar_fila():
    con = conexion()
    try:
        cur = con.cursor()
        cur.execute('INSERT INTO certificados DEFAULT VALUES RETURNING *;')
        nueva_fila = cur.fetchone()
        con.commit()
        cur.close()
        con.close()
        logging.info("➕ Nueva fila creada")
        return nueva_fila
    except Exception as e:
        print("❌ Error al insertar fila:", e)
        return None

#con esto eliminamos una fila entera
def eliminar_fila(base, ids_filas):
    filas_seleccionadas = base.get_selected_rows()
    print("Filas seleccionadas:", filas_seleccionadas)
    if not filas_seleccionadas:
        print("No hay fila seleccionada para eliminar.")
        return

    for fila_index in sorted(filas_seleccionadas, reverse=True):
        id_fila = ids_filas[fila_index]
        try:
            con = conexion()
            cur = con.cursor()
            cur.execute('DELETE FROM certificados WHERE id = %s', (id_fila,))
            con.commit()
            cur.close()
            con.close()
            base.delete_rows(fila_index)
            ids_filas.pop(fila_index)
            logging.info(f"❌ Fila con id {id_fila} eliminada.")
        except Exception as e:
            logging.info("❌ Error al eliminar fila:", e)

def buckup():
    fecha = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    nombre_buckup = f"buckup_archivo_{fecha}.sql"
    carpeta = "backups"
    os.makedirs(carpeta, exist_ok=True) 
    ruta_completa = os.path.join(carpeta, nombre_buckup)
    host, database, user, password, port = configuracion()
    comando = [
        'pg_dump',
        '-h', host,
        '-p', port,
        '-U', user,
        '-F', 'p',
        '-f', ruta_completa,
        database
    ]
    env = os.environ.copy()
    env['PGPASSWORD'] = password
    try:
        subprocess.run(comando, check=True, env=env)
        logging.info(f"✅ Backup exitoso: {ruta_completa}")
    except subprocess.CalledProcessError as e:
        logging.info(f"❌ Error al hacer backup: {e}")