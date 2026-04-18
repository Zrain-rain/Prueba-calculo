from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'cambio-secreto-2026'

# Configuración de la base de datos
db_config = {
    'host': 'andy.cl',
    'user': 'curso',
    'password': 'aiep',
    'database': 'curso'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    estudiantes = []
    error = None
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, nota1, nota2, nota3, ROUND((nota1 + nota2 + nota3)/3, 2) as promedio FROM alumnos")
        estudiantes = cursor.fetchall()
    except mysql.connector.Error as err:
        error = f"Error de base de datos: {err}"
        flash(error, 'error')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return render_template('index.html', estudiantes=estudiantes)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'GET':
        return redirect(url_for('index'))

    nombre = request.form.get('nombre', '').strip()
    nota1 = request.form.get('nota1', '')
    nota2 = request.form.get('nota2', '')
    nota3 = request.form.get('nota3', '')

    if not nombre or not nota1 or not nota2 or not nota3:
        flash('Debe completar todos los campos.', 'error')
        return redirect(url_for('index'))

    try:
        nota1 = float(nota1)
        nota2 = float(nota2)
        nota3 = float(nota3)
    except ValueError:
        flash('Las notas deben ser números válidos.', 'error')
        return redirect(url_for('index'))

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO alumnos (nombre, nota1, nota2, nota3) VALUES (%s, %s, %s, %s)",
            (nombre, nota1, nota2, nota3)
        )
        conn.commit()
        flash('Alumno agregado correctamente.', 'success')
    except mysql.connector.Error as err:
        flash(f'Error al guardar en la base de datos: {err}', 'error')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for('index'))

@app.route('/view')
def view_students():
    estudiantes = []
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, nota1, nota2, nota3, ROUND((nota1 + nota2 + nota3)/3, 2) as promedio FROM alumnos")
        estudiantes = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        # Podrías mostrar un mensaje de error en la plantilla
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    return render_template('view.html', estudiantes=estudiantes)

if __name__ == '__main__':
    app.run(debug=True)