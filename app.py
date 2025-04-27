from flask import Flask

app = Flask(__name__)

# Ruta de prueba para confirmar que el backend funciona
@app.route('/')
def hola_mundo():
    return "¡Hola, este es el backend de la Escuela Cristiana de Sordos!"

# Iniciar el backend
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Crear o conectar a la base de datos SQLite
def init_db():
    db_path = os.path.join(os.getcwd(), 'escuela.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Estudiantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        edad INTEGER,
        genero TEXT,
        grado INTEGER,
        anio INTEGER,
        necesidades_especiales TEXT
    )''')
    conn.commit()
    conn.close()

# Inicializar la base de datos al arrancar el backend
init_db()

# Create: Guardar un nuevo estudiante
@app.route('/guardar_estudiante', methods=['POST'])
def guardar_estudiante():
    nombre = request.form['nombre']
    edad = int(request.form['edad'])
    genero = request.form['genero']
    grado = int(request.form['grado'])
    anio = int(request.form['anio'])
    necesidades_especiales = request.form['necesidades_especiales']

    db_path = os.path.join(os.getcwd(), 'escuela.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''INSERT INTO Estudiantes (nombre, edad, genero, grado, anio, necesidades_especiales)
                VALUES (?, ?, ?, ?, ?, ?)''',
            (nombre, edad, genero, grado, anio, necesidades_especiales))
    conn.commit()
    conn.close()

    return jsonify({"message": "Estudiante registrado con éxito."})

# Read: Obtener todos los estudiantes
@app.route('/estudiantes', methods=['GET'])
def obtener_estudiantes():
    db_path = os.path.join(os.getcwd(), 'escuela.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM Estudiantes')
    estudiantes = c.fetchall()
    conn.close()

    # Convertir los datos a una lista de diccionarios para JSON
    columnas = ['id', 'nombre', 'edad', 'genero', 'grado', 'anio', 'necesidades_especiales']
    resultado = [dict(zip(columnas, estudiante)) for estudiante in estudiantes]
    return jsonify(resultado)

# Read: Obtener un estudiante por ID
@app.route('/estudiantes/<int:id>', methods=['GET'])
def obtener_estudiante(id):
    db_path = os.path.join(os.getcwd(), 'escuela.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM Estudiantes WHERE id = ?', (id,))
    estudiante = c.fetchone()
    conn.close()

    if estudiante is None:
        return jsonify({"error": "Estudiante no encontrado."}), 404

    columnas = ['id', 'nombre', 'edad', 'genero', 'grado', 'anio', 'necesidades_especiales']
    resultado = dict(zip(columnas, estudiante))
    return jsonify(resultado)

# Update: Actualizar un estudiante por ID
@app.route('/estudiantes/<int:id>', methods=['PUT'])
def actualizar_estudiante(id):
    nombre = request.form['nombre']
    edad = int(request.form['edad'])
    genero = request.form['genero']
    grado = int(request.form['grado'])
    anio = int(request.form['anio'])
    necesidades_especiales = request.form['necesidades_especiales']

    db_path = os.path.join(os.getcwd(), 'escuela.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE Estudiantes SET nombre = ?, edad = ?, genero = ?, grado = ?, anio = ?, necesidades_especiales = ?
                WHERE id = ?''',
            (nombre, edad, genero, grado, anio, necesidades_especiales, id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Estudiante actualizado con éxito."})

# Delete: Eliminar un estudiante por ID
@app.route('/estudiantes/<int:id>', methods=['DELETE'])
def eliminar_estudiante(id):
    db_path = os.path.join(os.getcwd(), 'escuela.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('DELETE FROM Estudiantes WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Estudiante eliminado con éxito."})

# Iniciar el backend
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)