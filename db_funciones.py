import duckdb

DB_PATH = "lugares.db"
#USUARIO (Tesista 3)
def obtener_usuario_por_correo(correo):
    con = duckdb.connect(DB_PATH)
    usuario = con.execute(
        f"SELECT * FROM usuario WHERE usuario_correo_electronico = '{correo}'"
    ).fetchone()
    con.close()
    return usuario

def insertar_usuario(id, ap_pat, ap_mat, nombres, correo, contrasena):
    con = duckdb.connect(DB_PATH)
    con.execute(
        f"""
        INSERT INTO usuario
        (usuario_id, usuario_apellido_paterno, usuario_apellido_materno,
         usuario_nombres, usuario_correo_electronico, usuario_contrasena)
        VALUES
        ({id}, '{ap_pat}', '{ap_mat}', '{nombres}', '{correo}', '{contrasena}')
        """
    )
    con.close()
# LUGARES (Tesista 4 y 6)
def obtener_lugares():
    con = duckdb.connect(DB_PATH)
    lugares = con.execute(
        "SELECT * FROM lugar ORDER BY lugar_id"
    ).fetchall()
    con.close()
    return lugares

def obtener_lugar_por_id(lugar_id):
    con = duckdb.connect(DB_PATH)
    lugar = con.execute(
        f"SELECT * FROM lugar WHERE lugar_id = {lugar_id}"
    ).fetchone()
    con.close()
    return lugar

def insertar_lugar(id, nombre, direccion, mapa, descripcion, usuario_id):
    con = duckdb.connect(DB_PATH)

    mapa_val = "NULL" if mapa == "" else f"'{mapa}'"
    desc_val = "NULL" if descripcion == "" else f"'{descripcion}'"

    con.execute(
        f"""
        INSERT INTO lugar
        (lugar_id, lugar_nombre, lugar_direccion, lugar_mapa_url,
         lugar_descripcion, lugar_usuario_id)
        VALUES
        ({id}, '{nombre}', '{direccion}', {mapa_val}, {desc_val}, {usuario_id})
        """
    )
    con.close()



def actualizar_lugar(id, nombre, direccion, mapa_url, descripcion):
    con = duckdb.connect(DB_PATH)

    mapa_val = None if (mapa_url is None or str(mapa_url).strip() == "") else str(mapa_url).strip()
    desc_val = None if (descripcion is None or str(descripcion).strip() == "") else str(descripcion).strip()

    con.execute(
        """
        UPDATE lugar
        SET lugar_nombre = ?,
            lugar_direccion = ?,
            lugar_mapa_url = ?,
            lugar_descripcion = ?
        WHERE lugar_id = ?
        """,
        [str(nombre).strip(), str(direccion).strip(), mapa_val, desc_val, id]
    )

    con.close()


def eliminar_lugar(id):
    con = duckdb.connect(DB_PATH)
    con.execute(
        f"DELETE FROM lugar WHERE lugar_id = {id}"
    )
    con.close()


# RESEÑA (Tesista 5)

def insertar_resena(id, lugar_id, usuario_id, comentario, estrellas):
    con = duckdb.connect(DB_PATH)
    con.execute(
        f"""
        INSERT INTO resena
        (resena_id, resena_lugar_id, resena_usuario_id,
         resena_comentario, resena_estrellas)
        VALUES
        ({id}, {lugar_id}, {usuario_id}, '{comentario}', {estrellas})
        """
    )
    con.close()


def obtener_resenas_por_lugar(lugar_id):
    con = duckdb.connect(DB_PATH)
    resenas = con.execute(
        f"SELECT * FROM resena WHERE resena_lugar_id = {lugar_id}"
    ).fetchall()
    con.close()
    return resenas


def obtener_promedio_por_lugar(lugar_id):
    con = duckdb.connect(DB_PATH)
    promedio = con.execute(
        f"SELECT AVG(resena_estrellas) FROM resena WHERE resena_lugar_id = {lugar_id}"
    ).fetchone()
    con.close()
    return promedio

# ESTADÍSTICAS (Tesista 7)
def obtener_lugares_mejor_calificados():
    con = duckdb.connect(DB_PATH)
    datos = con.execute(
        """
        SELECT lugar_id, AVG(resena_estrellas) AS promedio
        FROM resena
        GROUP BY lugar_id
        ORDER BY promedio DESC
        """
    ).fetchall()
    con.close()
    return datos

def obtener_distribucion_estrellas():
    con = duckdb.connect(DB_PATH)
    datos = con.execute(
        """
        SELECT resena_estrellas, COUNT(*)
        FROM resena
        GROUP BY resena_estrellas
        ORDER BY resena_estrellas
        """
    ).fetchall()
    con.close()
    return datos