from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import db_funciones

auth = Blueprint("auth", __name__)


# --- LOGIN -------------------------------------------------------------------
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form.get("correo")
        password = request.form.get("password")

        usuario = db_funciones.obtener_usuario_por_correo(correo)

        # usuario = [0]=id, [1]=ap_pat, [2]=ap_mat, [3]=nombres, [4]=correo, [5]=contrasena
        if usuario and str(usuario[5]) == str(password):
            session["usuario_id"] = usuario[0]
            session["usuario_nombre"] = usuario[3]
            session["usuario_correo"] = usuario[4]

            flash(f"Bienvenido {usuario[3]}")
            # Después de login correcto -> panel admin
            return redirect(url_for("admin_lugares"))

        # Si falla
        return render_template("login.html", error="Correo o contraseña incorrectos")

    # GET
    return render_template("login.html")


# --- LOGOUT ------------------------------------------------------------------
@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))