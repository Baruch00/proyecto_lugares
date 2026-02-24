from flask import Flask, render_template, request, redirect, url_for
from db_funciones import (
    obtener_lugares,
    obtener_lugar_por_id,
    insertar_lugar,
    actualizar_lugar,
    eliminar_lugar,
)

app = Flask(__name__)

@app.route("/")
def index():
    lugares = obtener_lugares()
    return render_template("index.html", lugares=lugares)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # Campos que existen en insertar_lugar(id, nombre, direccion, mapa, descripcion, usuario_id)
        lugar_id = int(request.form["lugar_id"])
        nombre = request.form["nombre"].strip()
        direccion = request.form["direccion"].strip()
        mapa = request.form.get("mapa", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        usuario_id = int(request.form["usuario_id"])

        # Validaciones básicas
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

        # Validaciones básicas
        if not nombre or not direccion:
            return "Nombre y dirección son obligatorios.", 400

        # Esta función ya NO debe tocar usuario_id (según tu decisión)
        actualizar_lugar(lugar_id, nombre, direccion, mapa, descripcion)

        return redirect(url_for("index"))

    return render_template("edit.html", lugar=lugar)

@app.route("/delete/<int:lugar_id>", methods=["POST"])
def delete(lugar_id):
    # Esto borra físicamente porque así está en db_funciones.py
    eliminar_lugar(lugar_id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)