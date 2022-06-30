from flask import Flask, flash, redirect, url_for, render_template, request
from datetime import datetime
import sqlite3

#currentdirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = 'clave_secreta_flask'
app.database = "refacciones.db"

# Conexon DB
"""app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'refacciones'

mysql = MySQL(app)"""

# Context processors
@app.context_processor
def date_now():
    return {
        'now': datetime.utcnow()
    }


@app.route('/crear-pedido', methods=['GET', 'POST'])
def crear_pedido():

    if request.method == 'POST':

        nombres = request.form['nombres']
        producto = request.form.getlist('producto[]')
        fecha = request.form['fecha']
        producto = ', '.join(producto)

        connection = sqlite3.connect(app.database)
        cursor = connection.cursor()
        stmt = "INSERT INTO solicitud(nombres, producto, fecha) VALUES(?, ?, ?)"
        data = (nombres, producto, fecha)
        cursor.executemany(stmt, [data])
        connection.commit()

        flash('Se ha efectuado el pedido correctamente!!!')

        return redirect(url_for('index'))
        #return f"{nombres} {producto} {fecha}"
    

    connection = sqlite3.connect(app.database)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM productos")
    producto = cursor.fetchall()
    cursor.close()

    return render_template('ordene.html', productos=producto) 
    

@app.route('/pedidos')
def pedidos():
    connection = sqlite3.connect(app.database)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM solicitud ORDER BY id DESC")
    pedido = cursor.fetchall()
    cursor.close()
        
    return render_template('ordenes.html', pedidos=pedido)

@app.route('/orden/<id>')
def orden(id):
    #cursor = mysql.connection.cursor()
    connection = sqlite3.connect(app.database)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM solicitud WHERE id = (?)", [(id)])
    orden = cursor.fetchall()
    cursor.close()

    return render_template('orden.html',  orden=orden[0])

@app.route('/borrar-orden/<id>')
def borrar_orden(id):
    connection = sqlite3.connect(app.database)
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM solicitud WHERE id = {id}")
    connection.commit()

    flash('La orden ha sido eliminada!!')

    return redirect(url_for('pedidos'))

@app.route('/editar-orden/<id>', methods=['GET', 'POST'])
def editar_orden(id):
    if request.method == 'POST':

        nombres = request.form['nombres']
        producto = request.form.getlist('producto[]')
        fecha = request.form['fecha']
        producto = ', '.join(producto)

        connection = sqlite3.connect(app.database)
        cursor = connection.cursor()

        stmt ="""
            UPDATE solicitud
            SET nombres = (?),
                producto = (?),
                fecha = (?)
            WHERE id = (?)
        """
        data = (nombres, producto, fecha, id)
        cursor.executemany(stmt, [data])

        connection.commit()
        flash('Has editado la orden correctamente!!!')

        return redirect(url_for('pedidos'))

    connection = sqlite3.connect(app.database)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM solicitud WHERE id = (?)", (id))
    orden = cursor.fetchall()
    cursor.execute("SELECT * FROM productos")
    producto = cursor.fetchall()
    cursor.close()

    return render_template('ordene.html',  orden=orden[0], productos=producto)


@app.route('/')
def index():

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)