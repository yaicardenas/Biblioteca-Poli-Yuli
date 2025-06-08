from flask import Flask, render_template, request, redirect
import mysql.connector
import time

app = Flask(__name__)

def obtener_conexion():
    for i in range(10):  # intenta 10 veces
        try:
            return mysql.connector.connect(
                host='mysql-db',
                user='root',
                password='rootpassword',
                database='biblioteca'
            )
        except Error as e:
            print(f"Intento {i+1}: MySQL no está listo todavía. Esperando...")
            time.sleep(3)
    raise Exception("No se pudo conectar a MySQL después de varios intentos.")

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
    app.run(host='0.0.0.0', port=5000)


