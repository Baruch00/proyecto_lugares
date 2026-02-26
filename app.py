from flask import Flask, render_template, request, redirect, url_for, session, flash
import db_funciones  # Tesista 2
import reviews       # Tesista 5
from auth import auth
import duckdb

DB_PATH = "lugares.db"

app = Flask(__name__)
app.secret_key = 'secreto_coordinador_baruch'
app.register_blueprint(auth)

# --- INTEGRACIÓN DE MÓDULOS ---
reviews.rutas(app)

# --- VISTA PÚBLICA (Página de inicio "Chida") ---
@app.route("/")
def index():
    datos_lugares = db_funciones.obtener_lugares()
    return render_template("index_chido.html", lugares=datos_lugares)

# --- LOGIN ADMINISTRADOR ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form.get("usuario")
        password = request.form.get("password")

        usuario = db_funciones.obtener_usuario_por_correo(correo)

        if usuario:
            contrasena_bd = usuario[5]
            if str(contrasena_bd) == str(password):
                session["usuario_id"] = usuario[0]
                session["usuario_nombre"] = usuario[3]
                session["usuario_correo"] = usuario[4]
                return redirect(url_for("admin_lugares"))

        return render_template("login.html", error="Usuario o contraseña incorrectos")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# --- PANEL ADMINISTRATIVO (Solo con Login) ---
@app.route("/admin_lugares")
def admin_lugares():
    datos_lugares = db_funciones.obtener_lugares()
    nombre = session.get("usuario_nombre")
    return render_template("admin_lugares.html", lugares=datos_lugares, usuario_nombre=nombre)

# --- MÓDULO DE LUGARES (CRUD) ---
@app.route("/add", methods=["GET", "POST"])
def add():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        id_l = int(request.form["lugar_id"])
        nom = request.form["nombre"].strip()
        dir = request.form["direccion"].strip()
        map_url = request.form.get("mapa", "").strip()
        desc = request.form.get("descripcion", "").strip()
        usr_id = session["usuario_id"]

        db_funciones.insertar_lugar(id_l, nom, dir, map_url, desc, usr_id)
        return redirect(url_for("admin_lugares"))

    return render_template("add.html")

@app.route("/edit/<int:lugar_id>", methods=["GET", "POST"])
def edit(lugar_id):
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        nom = request.form["nombre"].strip()
        dir = request.form["direccion"].strip()
        map_url = request.form.get("mapa", "").strip()
        desc = request.form.get("descripcion", "").strip()

        db_funciones.actualizar_lugar(lugar_id, nom, dir, map_url, desc)
        return redirect(url_for("admin_lugares"))

    lugar_actual = db_funciones.obtener_lugar_por_id(lugar_id)
    return render_template("edit.html", lugar=lugar_actual)

@app.route("/delete/<int:lugar_id>", methods=["POST"])
def delete(lugar_id):
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    db_funciones.eliminar_lugar(lugar_id)
    return redirect(url_for("admin_lugares"))

# ✅ Eliminar lugar + TODAS sus reseñas
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

# =========================================================
# ✅ NUEVO: ADMINISTRAR RESEÑAS (VISTA ADMIN, NO PÚBLICA)
# =========================================================

@app.route("/admin_resenas/<int:lugar_id>")
def admin_resenas(lugar_id):
    # Solo con sesión
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    # Traer el lugar (para mostrar nombre/título)
    lugar = db_funciones.obtener_lugar_por_id(lugar_id)
    if not lugar:
        return "Lugar no encontrado.", 404

    # Traer reseñas del lugar (incluyendo resena_id para poder borrar)
    con = duckdb.connect(DB_PATH)
    try:
        resenas = con.execute("""
            SELECT resena_id, resena_usuario_id, resena_estrellas, resena_comentario, resena_fecha
            FROM resena
            WHERE resena_lugar_id = ?
            ORDER BY resena_fecha DESC
        """, [lugar_id]).fetchall()
    finally:
        con.close()

    nombre = session.get("usuario_nombre")
    return render_template(
        "admin_resenas.html",
        lugar=lugar,
        lugar_id=lugar_id,
        resenas=resenas,
        usuario_nombre=nombre
    )

@app.route("/admin_resenas/<int:lugar_id>/delete/<int:resena_id>", methods=["POST"])
def admin_delete_resena(lugar_id, resena_id):
    # Solo con sesión
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    con = duckdb.connect(DB_PATH)
    try:
        con.execute("DELETE FROM resena WHERE resena_id = ?", [resena_id])
    finally:
        con.close()

    return redirect(url_for("admin_resenas", lugar_id=lugar_id))

if __name__ == "__main__":
    app.run(debug=True, port=5000)