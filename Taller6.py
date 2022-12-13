### Programacion de Computadoras IV
## Taller 6
# Braulio Rodriguez 8-899-1093


from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'slangspanameño'
mysql = MySQL(app)


app.secret_key = 'mysecretkey'


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Slangs')
    data = cur.fetchall()
    return render_template('index.html', Slangs=data)


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        palabra = request.form['palabra']
        significado = request.form['significado']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO palabras(palabra,significado) VALUES(%s,%s)', (palabra, significado))
        mysql.connection.commit()
        flash('Palabra Agregada')
        return redirect(url_for('Index'))
    return render_template('add.html')


@app.route('/update/<string:id>', methods=['POST'])
def update(id, palabra):
    if request.method == 'POST':
        palabra = request.form['palabra']
        significado = request.form['significado']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE palabras
            SET palabra = %s,
                significado = %s
            WHERE id = %s
            """, (palabra, significado,id))
        flash('Palabra Editada')
        mysql.connection.commit()
        return redirect(url_for('Index'))
    return render_template('update.html', Slangs=palabra)


@app.route('/delete/<string:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM palabras WHERE id=(%s)', id)
    flash('Palabra Eliminada')
    mysql.connection.commit()
    return render_template('delete.html')


@app.route('/get/<string:id>')
def get(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM palabras WHERE id = (%s)', id)
    data = cur.fetchall()
    return render_template('get.html', Slangs=data[0])


if __name__ == '__main__':
    app.run()
