from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'cambio-secreto-2026'

# Configuración de la base de datos
db_config = {
    'host': 'andy.cl',
    'user': 'curso',
    'password': 'aiep',
    'database': 'curso',
    'port': 3306,
    'connect_timeout': 5
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None

from contextlib import contextmanager

@contextmanager
def db_session():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        except mysql.connector.Error as err:
            flash(f'Error en la base de datos: {err}', 'error')
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
    else:
        flash('No hay conexión con el servidor. Reintente en unos momentos.', 'error')
        yield None


@app.route('/')
def index():
    with db_session() as cursor:
        if cursor:
            cursor.execute('SELECT nombre, nota1, nota2, nota3, ROUND((nota1 + nota2 + nota3)/3, 2) FROM alumnos')
            estudiantes = cursor.fetchall()
            return render_template('index.html', estudiantes=estudiantes)
    return render_template('index.html', estudiantes=[])


@app.route('/add', methods=['POST'])
def add_student():
    nombre = request.form.get('nombre', '').strip()
    nota1 = request.form.get('nota1', '')
    nota2 = request.form.get('nota2', '')
    nota3 = request.form.get('nota3', '')

    if not all([nombre, nota1, nota2, nota3]):
        flash('Todos los campos son obligatorios.', 'error')
        return redirect(url_for('index'))

    try:
        notas = [float(nota1), float(nota2), float(nota3)]
    except ValueError:
        flash('Las notas deben ser números válidos.', 'error')
        return redirect(url_for('index'))

    with db_session() as cursor:
        if cursor:
            cursor.execute(
                'INSERT INTO alumnos (nombre, nota1, nota2, nota3) VALUES (%s, %s, %s, %s)',
                (nombre, *notas)
            )
            flash('Alumno registrado con éxito.', 'success')

    return redirect(url_for('index'))


@app.route('/view')
def view_students():
    with db_session() as cursor:
        if cursor:
            cursor.execute('SELECT nombre, nota1, nota2, nota3, ROUND((nota1 + nota2 + nota3)/3, 2) FROM alumnos')
            estudiantes = cursor.fetchall()
            return render_template('view.html', estudiantes=estudiantes)
    return render_template('view.html', estudiantes=[])


if __name__ == '__main__':
    app.run(debug=True, port=8080)
