from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import db_funciones

auth = Blueprint("auth", __name__)

# --- LOGIN ---
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo   = request.form["correo"]
        password = request.form["password"]

        # Buscamos el usuario en la BD
        # Devuelve tupla: [0]=id, [1]=ap_pat, [2]=ap_mat, [3]=nombres, [4]=correo, [5]=contrasena
        usuario = db_funciones.obtener_usuario_por_correo(correo)

        if usuario and usuario[5] == password:
            session["usuario_id"]     = usuario[0]
            session["usuario_nombre"] = usuario[3]
            flash(f"Bienvenido {usuario[3]}")
            return redirect(url_for("index"))
        else:
            flash("Correo o contraseña incorrectos.")
            return redirect(url_for("auth.login"))

    return render_template("login.html")


# --- LOGOUT ---
@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))