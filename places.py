from flask import Flask, render_template, request, redirect, url_for
import duckdb

from db_funciones import (
    obtener_lugares,
    obtener_lugar_por_id,
    insertar_lugar,
    actualizar_lugar,
    eliminar_lugar,
)

# IMPORTANTE: aquí importamos y registramos las rutas de reseñas
from reviews import rutas as rutas_reviews

DB_PATH = "lugares.db"

app = Flask(__name__)
app.secret_key = "dev"  # necesario si usas session en reviews.py

# Registrar rutas de reviews.py (MUY IMPORTANTE)
rutas_reviews(app)

@app.route("/")
def index():
    lugares = obtener_lugares()
    return render_template("admin_lugares.html", lugares=lugares)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        lugar_id = int(request.form["lugar_id"])
        nombre = request.form["nombre"].strip()
        direccion = request.form["direccion"].strip()
        mapa = request.form.get("mapa", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        usuario_id = int(request.form["usuario_id"])

        if not nombre or not direccion:
            return "Nombre y dirección son obligatorios.", 400

        insertar_lugar(lugar_id, nombre, direccion, mapa, descripcion, usuario_id)
        return redirect(url_for("index"))

    return render_template("add.html")

@app.route("/edit/<int:lugar_id>", methods=["GET", "POST"])
def edit(lugar_id):
    lugar = obtener_lugar_por_id(lugar_id)
    if not lugar:
        return "Lugar no encontrado.", 404

    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        direccion = request.form["direccion"].strip()
        mapa = request.form.get("mapa", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        if not nombre or not direccion:
            return "Nombre y dirección son obligatorios.", 400

        # NO se toca usuario_id
        actualizar_lugar(lugar_id, nombre, direccion, mapa, descripcion)
        return redirect(url_for("index"))

    return render_template("edit.html", lugar=lugar)

@app.route("/delete/<int:lugar_id>", methods=["POST"])
def delete(lugar_id):
    # Elimina solo el lugar (puede fallar si hay reseñas)
    eliminar_lugar(lugar_id)
    return redirect(url_for("admin_lugares"))

@app.route("/delete_full/<int:lugar_id>", methods=["POST"])
def delete_full(lugar_id):
    """
    Elimina el lugar + todas sus reseñas (evita error de foreign key).
    """
    con = duckdb.connect(DB_PATH)
    try:
        con.execute("DELETE FROM resena WHERE resena_lugar_id = ?", [lugar_id])
        con.execute("DELETE FROM lugar WHERE lugar_id = ?", [lugar_id])
    finally:
        con.close()

    return redirect(url_for("index"))





if __name__ == "__main__":
    app.run(debug=True)