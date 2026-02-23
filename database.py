import duckdb
DB_PATH = "lugares.db"

def crear_estructura_bd():
    con =duckdb.connect(DB_PATH)
    con.execute("""
                 CREATE TABLE IF NOT EXISTS usuario (
            usuario_id INTEGER PRIMARY KEY,
            usuario_apellido_paterno TEXT NOT NULL,
            usuario_apellido_materno TEXT NOT NULL,
            usuario_nombres TEXT,
            usuario_correo_electronico TEXT UNIQUE NOT NULL,
            usuario_contrasena TEXT NOT NULL,
            usuario_fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        );   
    """)
    
       
    con.execute("""
             CREATE TABLE IF NOT EXISTS lugar (
            lugar_id INTEGER PRIMARY KEY,
            lugar_nombre TEXT NOT NULL,
            lugar_direccion TEXT NOT NULL,
            lugar_mapa_url TEXT,
            lugar_descripcion TEXT,
            lugar_usuario_id INTEGER NOT NULL,
            lugar_fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lugar_usuario_id) REFERENCES usuario(usuario_id)
        );
    """)

    con.execute("""
             CREATE TABLE IF NOT EXISTS resena (
            resena_id INTEGER PRIMARY KEY,
            resena_lugar_id INTEGER NOT NULL,
            resena_usuario_id INTEGER NOT NULL,
            resena_comentario TEXT NOT NULL,
            resena_estrellas INTEGER NOT NULL CHECK(resena_estrellas BETWEEN 1 AND 5),
            resena_fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (resena_lugar_id) REFERENCES lugar(lugar_id),
            FOREIGN KEY (resena_usuario_id) REFERENCES usuario(usuario_id)
        );
    """)
    con.close()
    print("La estructura de la base de datos se creo correctamente vamos Fieros Programadores:", DB_PATH)
if __name__ == "__main__":
    crear_estructura_bd()
