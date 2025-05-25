from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="biblioteca"
    )


@app.route('/')
def inicio():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template('index.html', libros=libros)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        categoria = request.form['categoria']
        cantidad = request.form['cantidad']

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO libros (titulo, autor, categoria, cantidad) VALUES (%s, %s, %s, %s)",
            (titulo, autor, categoria, cantidad)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect('/')
    return render_template('agregar_libro.html')


if __name__ == '__main__':
    app.run(debug=True)
