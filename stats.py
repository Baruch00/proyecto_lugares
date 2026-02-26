import os
import duckdb
from flask import render_template

def rutas(app):
    # Ruta absoluta al archivo de BD (evita problemas de "no encuentra lugares.db")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "lugares.db")

    @app.route("/stats")
    def stats():
        con = duckdb.connect(db_path)
        try:
            total_lugares = con.execute("SELECT COUNT(*) FROM lugar").fetchone()[0]
            total_resenas = con.execute("SELECT COUNT(*) FROM resena").fetchone()[0]

            # Promedio de estrellas (si no hay reseñas, devuelve 0)
            promedio_estrellas = con.execute(
                "SELECT COALESCE(ROUND(AVG(resena_estrellas), 2), 0) FROM resena"
            ).fetchone()[0]

            # Top 5 lugares por promedio de estrellas (solo lugares con reseñas)
            top_rows = con.execute(
                '''
                SELECT l.lugar_nombre AS nombre,
                       ROUND(AVG(r.resena_estrellas), 2) AS promedio,
                       COUNT(*) AS cantidad
                FROM lugar l
                JOIN resena r ON r.resena_lugar_id = l.lugar_id
                GROUP BY l.lugar_nombre
                ORDER BY promedio DESC, cantidad DESC
                LIMIT 5
                '''
            ).fetchall()

            top_labels = [r[0] for r in top_rows]
            top_values = [float(r[1]) for r in top_rows]
            top_counts = [int(r[2]) for r in top_rows]

            # Distribución de estrellas (1 a 5)
            dist_rows = con.execute(
                '''
                SELECT resena_estrellas, COUNT(*) AS total
                FROM resena
                GROUP BY resena_estrellas
                ORDER BY resena_estrellas
                '''
            ).fetchall()

            dist_labels = [str(r[0]) for r in dist_rows]
            dist_values = [int(r[1]) for r in dist_rows]

        finally:
            con.close()

        return render_template(
            "stats.html",
            total_lugares=total_lugares,
            total_resenas=total_resenas,
            promedio_estrellas=promedio_estrellas,
            top_labels=top_labels,
            top_values=top_values,
            top_counts=top_counts,
            dist_labels=dist_labels,
            dist_values=dist_values,
        )
