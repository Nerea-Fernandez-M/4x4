from flask import Flask, render_template
import read_connection
import generate_connection

app = Flask(__name__)

@app.route("/")
def index():
    choices = read_connection.read()
    
    if not choices:
        return "<h1>No hay juego disponible</h1><p>Ve a <a href='/generate'>/generate</a> para crear uno</p>"

    all_groups = []
    for name, words in choices.items():
        all_groups.append({
            "name": name,
            "words": words
        })

    return render_template("index.html", allGroups=all_groups)

@app.route("/generate")
def generate_game():
    """Endpoint para generar un nuevo juego"""
    try:
        generate_connection.main()
        return """
        <h1>✅ Juego generado correctamente!</h1>
        <p><a href="/">Ir al juego</a></p>
        <p><a href="/status">Ver estado</a></p>
        """
    except Exception as e:
        return f"""
        <h1>❌ Error al generar el juego</h1>
        <p>Error: {str(e)}</p>
        <p><a href="/status">Ver estado</a></p>
        """, 500

@app.route("/status")
def status():
    """Endpoint para verificar el estado de la base de datos"""
    try:
        import database
        conn = database.get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT difficulty, COUNT(*) as count FROM categories GROUP BY difficulty")
        categories_count = cur.fetchall()
        
        cur.execute("SELECT difficulty, COUNT(*) as count FROM used_categories GROUP BY difficulty")
        used_count = cur.fetchall()
        
        cur.execute("SELECT COUNT(*) as count FROM current_game")
        game_exists = cur.fetchone()['count'] > 0
        
        cur.close()
        conn.close()
        
        html = "<h1>Estado de la Base de Datos</h1>"
        html += "<h2>Categorías Disponibles:</h2><ul>"
        for row in categories_count:
            html += f"<li>Dificultad {row['difficulty']}: {row['count']} categorías</li>"
        html += "</ul>"
        
        html += "<h2>Categorías Usadas:</h2><ul>"
        if used_count:
            for row in used_count:
                html += f"<li>Dificultad {row['difficulty']}: {row['count']} usadas</li>"
        else:
            html += "<li>Ninguna categoría usada aún</li>"
        html += "</ul>"
        
        html += "<h2>Juego Actual:</h2>"
        html += f"<p>{'✅ Existe un juego generado' if game_exists else '❌ No hay juego generado'}</p>"
        
        html += "<hr>"
        html += "<p><a href='/'>Ir al juego</a> | <a href='/generate'>Generar nuevo juego</a> | <a href='/reset'>Resetear usadas</a></p>"
        
        return html
        
    except Exception as e:
        return f"""
        <h1>❌ Error al conectar con la base de datos</h1>
        <p>Error: {str(e)}</p>
        <p>¿Has configurado la variable DATABASE_URL?</p>
        """, 500

@app.route("/reset")
def reset_used():
    """Endpoint para resetear las categorías usadas"""
    try:
        import database
        database.clean_used()
        return """
        <h1>✅ Categorías usadas reseteadas!</h1>
        <p>Ahora puedes generar juegos con todas las categorías de nuevo.</p>
        <p><a href="/generate">Generar nuevo juego</a> | <a href="/status">Ver estado</a></p>
        """
    except Exception as e:
        return f"""
        <h1>❌ Error al resetear</h1>
        <p>Error: {str(e)}</p>
        """, 500

if __name__ == "__main__":
    app.run(debug=True)
