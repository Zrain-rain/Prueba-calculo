from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': 'andy.cl',
    'user': 'curso',
    'password': 'aiep',
    'database': 'curso'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        nombre = request.form['nombre']
        nota1 = float(request.form['nota1'])
        nota2 = float(request.form['nota2'])
        nota3 = float(request.form['nota3'])
        
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO estudiantes (nombre, nota1, nota2, nota3) VALUES (%s, %s, %s, %s)", 
                           (nombre, nota1, nota2, nota3))
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            # Aquí podrías agregar un mensaje de error al usuario
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/view')
def view_students():
    estudiantes = []
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, nota1, nota2, nota3, ROUND((nota1 + nota2 + nota3)/3, 2) as promedio FROM estudiantes")
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