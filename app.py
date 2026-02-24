from flask import Flask, render_template, request, jsonify
import db_funciones # Tesista 2 Completo
import reviews 

app = Flask(__name__)
app.secret_key = 'secreto_coordinador_baruch'

@app.route('/')
def index():
    # Tesista 6
    return "<h1>Panel de Control de Baruch</h1><p>Simulador del equipo listo.</p>"

# --- PRUEBA PARA TESISTA 3 ---
@app.route('/test/usuario/<correo>')
def test_usuario(correo):
    user = db_funciones.obtener_usuario_por_correo(correo)
    return jsonify({"resultado": user if user else "Usuario no encontrado"})

# --- PRUEBA PARA TESISTA 4 ---
@app.route('/test/lugares')
def test_lugares():
    data = db_funciones.obtener_lugares()
    return jsonify({"total": len(data), "lista": data})

# --- PRUEBA PARA TESISTA 5 ---
@app.route('/test/promedio/<int:id>')
def test_promedio(id):
    avg = db_funciones.obtener_promedio_por_lugar(id)
    return jsonify({"lugar_id": id, "promedio_estrellas": avg})

# --- PRUEBA PARA TESISTA 7 ---
@app.route('/test/top')
def test_top():
    top = db_funciones.obtener_lugares_mejor_calificados()
    return jsonify({"mejores_lugares": top})

reviews.rutas(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)