from flask import Flask, render_template, request, redirect, url_for, session, flash
import db_funciones # Tesista 2
import reviews      # Tesista 5
from auth import auth

app = Flask(__name__)
app.secret_key = 'secreto_coordinador_baruch'
app.register_blueprint(auth)

# --- INTEGRACIÓN DE MÓDULOS ---
reviews.rutas(app)



# --- VISTA PÚBLICA (Página de inicio "Chida") ---
@app.route("/")
def index():
    # Esta es la vista para los visitantes
    datos_lugares = db_funciones.obtener_lugares()
    return render_template("index_chido.html", lugares=datos_lugares)



# --- LOGIN ADMINISTRADOR ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # en el form el campo se llama "usuario", pero en realidad es el correo
        correo = request.form.get("usuario")
        password = request.form.get("password")

        # buscamos al usuario por correo en la BD
        usuario = db_funciones.obtener_usuario_por_correo(correo)

        if usuario:
            # orden según tu INSERT de usuario:
            # (usuario_id, ap_pat, ap_mat, nombres, correo, contrasena)
            contrasena_bd = usuario[5]

            if str(contrasena_bd) == str(password):
                # guardar info básica en sesión
                session["usuario_id"] = usuario[0]
                session["usuario_nombre"] = usuario[3]
                session["usuario_correo"] = usuario[4]

                return redirect(url_for("admin_lugares"))

        # si algo falla, regresamos al login con error
        return render_template("login.html", error="Usuario o contraseña incorrectos")

    # si es GET, solo mostramos el formulario
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# --- PANEL ADMINISTRATIVO (Solo con Login) ---
@app.route("/admin_lugares")
def admin_lugares():
    datos_lugares = db_funciones.obtener_lugares()
    nombre = session.get("usuario_nombre")  # puede ser None si no hay login
    return render_template("admin_lugares.html",lugares=datos_lugares,usuario_nombre=nombre)





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
        usr_id = session["usuario_id"] # Tomamos el ID de la sesión automáticamente

        db_funciones.insertar_lugar(id_l, nom, dir, map_url, desc, usr_id)
        return redirect(url_for("admin_panel")) # Regresa al panel admin
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
        return redirect(url_for("admin_panel")) # Regresa al panel admin

    lugar_actual = db_funciones.obtener_lugar_por_id(lugar_id)
    return render_template("edit.html", lugar=lugar_actual)

@app.route("/delete/<int:lugar_id>", methods=["POST"])
def delete(lugar_id):
    if "usuario_id" not in session:         
        return redirect(url_for("auth.login"))
    
    db_funciones.eliminar_lugar(lugar_id)
    return redirect(url_for("admin_panel")) # Regresa al panel admin

if __name__ == "__main__":
    app.run(debug=True, port=5000)