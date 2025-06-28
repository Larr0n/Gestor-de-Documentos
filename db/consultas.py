import psycopg2
import sys
from db.conexion import conexion
import datetime as dt
import logging
from funciones import configurar_logger

configurar_logger()

#ejecutar consulta por defecto (toda la base de datos)
def consulta_default(con):
    try:
        general = 'SELECT * FROM certificados ORDER BY n_legajo LIMIT 100'
        cur = con.cursor()
        cur.execute(general)
        rows = cur.fetchall()
        cur.close()
        return rows
    except Exception as e:
        print("Error en consulta:", e)
        return None    


#ejecuta una consulta filtrada segun las necesidades del usuario
def consulta_filtrada(filtros):
    try:
        with conexion() as con:
            cur = con.cursor()
            condiciones = []
            valores = []
            num_fila = []
            if filtros["dni"]:
                condiciones.append("dni = %s")
                valores.append(filtros["dni"])
            if filtros["apellido"]:
                condiciones.append("apellido ILIKE %s")
                valores.append(f"%{filtros['apellido']}%")
            if filtros["nombre"]:
                condiciones.append("nombre ILIKE %s")
                valores.append(f"%{filtros['nombre']}%")
            if filtros["num_legajo"]:
                condiciones.append("n_legajo = %s")
                valores.append(filtros["num_legajo"])
            if filtros["grado"]:
                condiciones.append("grado ILIKE %s")
                valores.append(f"%{filtros['grado']}%")
            if filtros["tipo"]:
                condiciones.append("doc ILIKE %s")
                valores.append(f"%{filtros['tipo']}%")
            if filtros["num_fila"]:
                num_fila.append("num_fila = %s")
                
            num_fila_raw = filtros.get("num_fila", "").strip()

            if num_fila_raw.upper() == "TODAS":
                num_filas = None  
            else:
                try:
                    num_filas = int(num_fila_raw)
                    if num_filas <= 0:
                        num_filas = 100
                except (ValueError, TypeError):
                    num_filas = 100

            # Construcción de la consulta
            sql = "SELECT * FROM certificados"
            if condiciones:
                sql += " WHERE " + " AND ".join(condiciones)
            sql += " ORDER BY n_legajo"
            if num_filas is not None:
                sql += f" LIMIT {num_filas}"
            

            cur.execute(sql, valores)
            rows = cur.fetchall()
            cantidad_filas = len(rows)
            cur.close()
            logging.info(f"Se ha realizado una búsqueda con los parámetros {valores}")
            return rows #, cantidad_filas
    except Exception as e:
        print("Error en consulta:", e)
        return None

