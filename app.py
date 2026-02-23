<<<<<<< Updated upstream
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
=======
import duckdb

DB_PATH = "lugares.db"

while True:
    print("\n===== MENÚ =====")
    print("1. Agregar usuario")
    print("2. Agregar lugar")
    print("3. Agregar reseña")
    print("4. Ver lugares")
    print("5. Ver reseñas de un lugar")
    print("6. Salir")

    opcion = input("Selecciona una opción: ")
    if opcion == "1":
        con = duckdb.connect(DB_PATH)



        try:
            usuario_id = int(input("ID del usuario: "))
            ap_pat = input("Apellido paterno: ")
            ap_mat = input("Apellido materno: ")
            nombres = input("Nombre(s): ")
            correo = input("Correo: ")
            contrasena = input("Contraseña: ")


            sql = f"""
            INSERT INTO usuario
            (usuario_id, usuario_apellido_paterno, usuario_apellido_materno,
             usuario_nombres, usuario_correo_electronico, usuario_contrasena)
            VALUES
            ({usuario_id}, '{ap_pat}', '{ap_mat}', '{nombres}', '{correo}', '{contrasena}')
            """
            con.execute(sql)
            print("Usuario agregado correctamente")
        except Exception as e:
            print("Error al agregar usuario:", e)

        con.close()
    elif opcion == "2":
        con = duckdb.connect(DB_PATH)
        try:
            lugar_id = int(input("ID del lugar: "))
            nombre = input("Nombre del lugar: ")
            direccion = input("Dirección: ")
            mapa = input("URL del mapa (opcional): ")
            descripcion = input("Descripción (opcional): ")
            usuario_id = int(input("ID del usuario que lo registra: "))

            mapa_val = "NULL" if mapa.strip() == "" else f"'{mapa}'"
            desc_val = "NULL" if descripcion.strip() == "" else f"'{descripcion}'"

            sql = f"""
            INSERT INTO lugar
            (lugar_id, lugar_nombre, lugar_direccion, lugar_mapa_url, lugar_descripcion, lugar_usuario_id)
            VALUES
            ({lugar_id}, '{nombre}', '{direccion}', {mapa_val}, {desc_val}, {usuario_id})
            """
            con.execute(sql)
            print("Lugar agregado correctamente")
        except Exception as e:
            print("Error al agregar lugar:", e)

        con.close()

    
    elif opcion == "3":
        con = duckdb.connect(DB_PATH)

        try:
            resena_id = int(input("ID de la reseña: "))
            lugar_id = int(input("ID del lugar: "))
            usuario_id = int(input("ID del usuario: "))
            comentario = input("Comentario: ")
            estrellas = int(input("Estrellas (1 a 5): "))

            sql = f"""
            INSERT INTO resena
            (resena_id, resena_lugar_id, resena_usuario_id, resena_comentario, resena_estrellas)
            VALUES
            ({resena_id}, {lugar_id}, {usuario_id}, '{comentario}', {estrellas})
            """
            con.execute(sql)
            print(" Reseña agregada correctamente")
        except Exception as e:
            print(" Error al agregar reseña:", e)

        con.close()

    elif opcion == "4":
        con = duckdb.connect(DB_PATH)
        try:
            datos = con.execute("SELECT * FROM lugar ORDER BY lugar_id").fetchall()

            print("\n--- LISTA DE LUGARES ---\n")
            for fila in datos:
                print("ID:", fila[0])
                print("Nombre:", fila[1])
                print("Dirección:", fila[2])
                print("Mapa:", fila[3])
                print("Descripción:", fila[4])
                print("Usuario que lo registró:", fila[5])
                print("Fecha registro:", fila[6])
                print("-----------------------------")
        except Exception as e:
            print("Error al consultar lugares:", e)

        con.close()

    elif opcion == "5":
        con = duckdb.connect(DB_PATH)

        try:
            lugar_id = int(input("ID del lugar: "))
            datos = con.execute(
                f"SELECT * FROM resena WHERE resena_lugar_id = {lugar_id} ORDER BY resena_id"
            ).fetchall()

            print("\n--- RESEÑAS ---\n")
            if len(datos) == 0:
                print("No hay reseñas para ese lugar.")
            else:
                for fila in datos:
                    print("ID reseña:", fila[0])
                    print("Lugar ID:", fila[1])
                    print("Usuario ID:", fila[2])
                    print("Comentario:", fila[3])
                    print("Estrellas:", fila[4])
                    print("Fecha:", fila[5])
                    print("-----------------------------")
        except Exception as e:
            print("Error al consultar reseñas:", e)

        con.close()

    elif opcion == "6":
        print("Saliendo del sistema...")
        break


    else:
        print("Opción no válida. Elige del 1 al 6.")
>>>>>>> Stashed changes
