from flask import Flask, render_template, request, redirect, url_for, session
from db_funciones import obtener_lugares, insertar_resena, obtener_promedio_por_lugar
import duckdb 

DB_PATH = "lugares.db"

def obtener_resenas_por_lugar_sql(lugar_id):
    con = duckdb.connect(DB_PATH)
    try:
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
        #if "usuario_id" not in session:
            
        #return "inicia sesion para ingresar a las reseñas"
    
        lugares = obtener_lugares()
        promedios = {}
        for l in lugares:
            lugar_id = l[0]
            promedios[lugar_id] = obtener_promedio_por_lugar(lugar_id)
        return render_template("for_resenas.html", lugares = lugares, promedios = promedios)
    
    @app.route("/resenas/<int:lugar_id>")
    def ver_resenas(lugar_id):
        resenas = obtener_resenas_por_lugar_sql(lugar_id)
        promedio = obtener_promedio_por_lugar(lugar_id)
        return render_template("ver_resena.html", lugar_id = lugar_id, resenas = resenas, promedio = promedio)
        
    @app.route("/resena/<int:lugar_id>")
    def formulario(lugar_id):
        if "usuario_id" not in session:
          return "inicia sesion para escribir reseñas"
        return render_template("resena.html", lugar_id=lugar_id)
    
    @app.route("/resena/promedio/<int:lugar_id>")
    def promedio(lugar_id):
        promedio = obtener_promedio_por_lugar(lugar_id)
        return f"promedio del lugar {lugar_id} : {promedio}"
    
    
    @app.route("/lugares/<int:lugar_id>/resena", methods = ["POST"])
    def resena(lugar_id):
        if "usuario_id" not in session:
            return "Inicia sesion para escribir una reseña"
        
        usuario_id = session["usuario_id"]
        comentario = (request.form.get("comentarios") or "").strip()
        calificacion_lugar = request.form.get("calificacion")
        calificacion = int(calificacion_lugar)
        if calificacion > 1 or calificacion < 5 :
            if len(comentario) > 10 :
                insertar_resena(lugar_id, usuario_id, calificacion, comentario)
                return redirect(url_for("ver_resenas", lugar_id = lugar_id))
                
