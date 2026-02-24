<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify
import db_funciones # Tesista 2 Completo
import reviews 
=======
from flask import Flask, render_template, request, redirect, url_for
import db_funciones 
>>>>>>> 29870c040a94285e3347eed30e581fe521320b62

app = Flask(__name__)
app.secret_key = 'secreto_coordinador_baruch'

# --- RUTA PRINCIPAL (Tesista 6) ---
@app.route("/")
def index():
    datos_lugares = db_funciones.obtener_lugares()
    return render_template("index.html", lugares=datos_lugares)

# --- MÓDULO DE LUGARES (Tesista 4) ---

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        id_l = int(request.form["lugar_id"])
        nom = request.form["nombre"].strip()
        dir = request.form["direccion"].strip()
        map_url = request.form.get("mapa", "").strip()
        desc = request.form.get("descripcion", "").strip()
        usr_id = int(request.form["usuario_id"])

        db_funciones.insertar_lugar(id_l, nom, dir, map_url, desc, usr_id)
        return redirect(url_for("index"))
    
    return render_template("add.html")

@app.route("/edit/<int:lugar_id>", methods=["GET", "POST"])
def edit(lugar_id):
    if request.method == "POST":
        nom = request.form["nombre"].strip()
        dir = request.form["direccion"].strip()
        map_url = request.form.get("mapa", "").strip()
        desc = request.form.get("descripcion", "").strip()

<<<<<<< HEAD
reviews.rutas(app)

if __name__ == '__main__':
=======
        db_funciones.actualizar_lugar(lugar_id, nom, dir, map_url, desc)
        return redirect(url_for("index"))

    lugar_actual = db_funciones.obtener_lugar_por_id(lugar_id)
    return render_template("edit.html", lugar=lugar_actual)

@app.route("/delete/<int:lugar_id>", methods=["POST"])
def delete(lugar_id):
    # Borrado físico solicitado por el Tesista 4
    db_funciones.eliminar_lugar(lugar_id)
    return redirect(url_for("index"))

if __name__ == "__main__":
>>>>>>> 29870c040a94285e3347eed30e581fe521320b62
    app.run(debug=True, port=5000)