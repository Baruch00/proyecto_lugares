from flask import Flask, render_template, request, redirect, url_for, session
from db_funciones import obtener_lugares, insertar_resena, obtener_promedio_por_lugar
import duckdb 
import random

DB_PATH = "lugares.db"

def obtener_resenas_por_lugar_sql(lugar_id):
    con = duckdb.connect(DB_PATH)
    try:
        # Extraemos los datos en el orden que espera ver_resena.html
        return con.execute("""
            SELECT resena_usuario_id, resena_estrellas, resena_comentario, resena_fecha
            FROM resena
            WHERE resena_lugar_id = ?
            ORDER BY resena_fecha DESC
        """, [lugar_id]).fetchall()
    finally:
        con.close()

def rutas(app):
    @app.route("/resenas")
    def resenas():
        lugares = obtener_lugares()
        promedios = {}
        for l in lugares:
            lugar_id = l[0]
            # Obtenemos el promedio y extraemos el valor numérico del tuple
            p = obtener_promedio_por_lugar(lugar_id)
            promedios[lugar_id] = p
        return render_template("for_resenas.html", lugares=lugares, promedios=promedios)
    
    @app.route("/resenas/<int:lugar_id>")
    def ver_resenas(lugar_id):
        resenas_lista = obtener_resenas_por_lugar_sql(lugar_id)
        p = obtener_promedio_por_lugar(lugar_id)
        # Si el promedio existe, pasamos solo el número (p[0])
        promedio_final = p[0] if p and p[0] is not None else None
        return render_template("ver_resena.html", lugar_id=lugar_id, resenas=resenas_lista, promedio=promedio_final)
        
    @app.route("/resena/<int:lugar_id>")
    def formulario(lugar_id):
        if "usuario_id" not in session:
            return "Inicia sesión para escribir reseñas."
        return render_template("resena.html", lugar_id=lugar_id)
    
    @app.route("/lugares/<int:lugar_id>/resena", methods=["POST"])
    def resena(lugar_id):
        if "usuario_id" not in session:
            return "Inicia sesión para escribir una reseña."
        
        usuario_id = session["usuario_id"]
        # CORRECCIÓN: Usamos 'comentario' (singular) como en resena.html
        comentario = (request.form.get("comentario") or "").strip()
        calificacion_raw = request.form.get("calificacion")
        
        try:
            calificacion = int(calificacion_raw) if calificacion_raw else 0
        except ValueError:
            calificacion = 0

        # Validación: más de 10 letras y calificación válida
        if len(comentario) > 10 and 1 <= calificacion <= 5:
            # Generamos el ID aleatorio para la DB
            resena_id = random.randint(1000, 9999)
            insertar_resena(resena_id, lugar_id, usuario_id, comentario, calificacion)
            return redirect(url_for("ver_resenas", lugar_id=lugar_id))
        else:
            return "Error: El comentario debe ser mayor a 10 letras y la calificación entre 1 y 5."