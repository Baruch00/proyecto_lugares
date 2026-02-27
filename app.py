from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
)
import duckdb

import db_funciones      # Tesista 2
import reviews           # Tesista 5
import stats             # Tesista 7
from auth import auth    # Tesista 3

DB_PATH = "lugares.db"

app = Flask(__name__)
app.secret_key = "secreto_coordinador_baruch"

app.register_blueprint(auth)

reviews.rutas(app)
stats.rutas(app)


# --- PORTADA PÚBLICA ---------------------------------------------------------
@app.route("/")
def index():
    datos_lugares = db_funciones.obtener_lugares()
    return render_template("index_chido.html", lugares=datos_lugares)


# --- PANEL ADMIN LUGARES -----------------------------------------------------
@app.route("/admin_lugares")
def admin_lugares():
    # Solo admins logueados
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    datos_lugares = db_funciones.obtener_lugares()
    nombre = session.get("usuario_nombre")
    return render_template(
        "admin_lugares.html",
        lugares=datos_lugares,
        usuario_nombre=nombre,
    )


# --- AGREGAR LUGAR -----------------------------------------------------------
@app.route("/add", methods=["GET", "POST"])
def add():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        id_l = int(request.form["lugar_id"])
        nom = request.form["nombre"].strip()
        dir_ = request.form["direccion"].strip()
        map_url = request.form.get("mapa", "").strip()
        desc = request.form.get("descripcion", "").strip()
        usr_id = session["usuario_id"]

        db_funciones.insertar_lugar(id_l, nom, dir_, map_url, desc, usr_id)
        return redirect(url_for("admin_lugares"))

    return render_template("add.html")


# --- EDITAR LUGAR ------------------------------------------------------------
@app.route("/edit/<int:lugar_id>", methods=["GET", "POST"])
def edit(lugar_id):
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        nom = request.form["nombre"].strip()
        dir_ = request.form["direccion"].strip()
        map_url = request.form.get("mapa", "").strip()
        desc = request.form.get("descripcion", "").strip()

        db_funciones.actualizar_lugar(lugar_id, nom, dir_, map_url, desc)
        return redirect(url_for("admin_lugares"))

    lugar_actual = db_funciones.obtener_lugar_por_id(lugar_id)
    return render_template("edit.html", lugar=lugar_actual)


# --- ELIMINAR SOLO LUGAR -----------------------------------------------------
@app.route("/delete/<int:lugar_id>", methods=["POST"])
def delete(lugar_id):
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    db_funciones.eliminar_lugar(lugar_id)
    return redirect(url_for("admin_lugares"))


# --- ELIMINAR LUGAR + SUS RESEÑAS -------------------------------------------
@app.route("/delete_full/<int:lugar_id>", methods=["POST"])
def delete_full(lugar_id):
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    con = duckdb.connect(DB_PATH)
    try:
        con.execute("DELETE FROM resena WHERE resena_lugar_id = ?", [lugar_id])
        con.execute("DELETE FROM lugar WHERE lugar_id = ?", [lugar_id])
    finally:
        con.close()

    return redirect(url_for("admin_lugares"))


# --- ADMINISTRAR RESEÑAS (solo admins) --------------------------------------
@app.route("/admin_resenas/<int:lugar_id>")
def admin_resenas(lugar_id):
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    lugar = db_funciones.obtener_lugar_por_id(lugar_id)
    if not lugar:
        return "Lugar no encontrado.", 404

    con = duckdb.connect(DB_PATH)
    try:
        resenas = con.execute(
            """
            SELECT
                resena_id,
                resena_usuario_id,
                resena_estrellas,
                resena_comentario,
                resena_fecha
            FROM resena
            WHERE resena_lugar_id = ?
            ORDER BY resena_fecha DESC
            """,
            [lugar_id],
        ).fetchall()
    finally:
        con.close()

    nombre = session.get("usuario_nombre")
    return render_template(
        "admin_resenas.html",
        lugar=lugar,
        lugar_id=lugar_id,
        resenas=resenas,
        usuario_nombre=nombre,
    )


@app.route(
    "/admin_resenas/<int:lugar_id>/delete/<int:resena_id>",
    methods=["POST"],
)
def admin_delete_resena(lugar_id, resena_id):
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    con = duckdb.connect(DB_PATH)
    try:
        con.execute("DELETE FROM resena WHERE resena_id = ?", [resena_id])
    finally:
        con.close()

    return redirect(url_for("admin_resenas", lugar_id=lugar_id))


# -----------------------------------------------------------------------------    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)