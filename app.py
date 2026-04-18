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
    'connect_timeout': 5  # Tiempo máximo de espera para conectar (segundos)
}


def get_db_connection():
    try:
        # Intentar conexión con tiempo de espera para evitar que la página "no cargue"
        conn = mysql.connector.connect(**db_config)
        
        # Asegurarse de que la tabla exista
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alumnos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                nota1 FLOAT NOT NULL,
                nota2 FLOAT NOT NULL,
                nota3 FLOAT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        return conn
    except mysql.connector.Error as err:
        print(f"Error de conexión a la base de datos: {err}")
        return None


@app.route('/')
def index():
    estudiantes = []
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT nombre, nota1, nota2, nota3, ROUND((nota1 + nota2 + nota3)/3, 2) as promedio FROM alumnos'
            )
            estudiantes = cursor.fetchall()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            flash(f'Error al leer datos: {err}', 'error')
    else:
        flash('No se pudo establecer conexión con la base de datos externa. Revisa tu conexión a internet.', 'error')

    return render_template('index.html', estudiantes=estudiantes)


@app.route('/add', methods=['POST'])
def add_student():
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

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO alumnos (nombre, nota1, nota2, nota3) VALUES (%s, %s, %s, %s)',
                (nombre, nota1, nota2, nota3)
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash('Alumno agregado correctamente.', 'success')
        except mysql.connector.Error as err:
            flash(f'Error al guardar en la base de datos: {err}', 'error')
    else:
        flash('Error de conexión: No se pudo registrar el alumno.', 'error')

    return redirect(url_for('index'))


@app.route('/view')
def view_students():
    estudiantes = []
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT nombre, nota1, nota2, nota3, ROUND((nota1 + nota2 + nota3)/3, 2) as promedio FROM alumnos'
            )
            estudiantes = cursor.fetchall()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            flash(f'Error al cargar los alumnos: {err}', 'error')
    else:
        flash('Error de conexión al cargar el listado.', 'error')

    return render_template('view.html', estudiantes=estudiantes)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
