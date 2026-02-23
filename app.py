from flask import Flask, render_template
import database  # Tesista 2
import auth      # Tesista 3
import places    # Tesista 4
import reviews   # Tesista 5
import stats     # Tesista 7

app = Flask(__name__)
app.secret_key = 'clave_secreta_del_equipo' 

# --- RUTAS PRINCIPALES ---

@app.route('/')
def index():
    # Tesista 6
    return render_template('index.html')

# --- CONEXIÓN CON LOS MÓDULOS DEL EQUIPO ---

@app.route('/dashboard')
def dashboard():
    return "Panel de Control - Aquí se verán las estadísticas del Tesista 7"

if __name__ == '__main__':
    app.run(debug=True, port=5000)