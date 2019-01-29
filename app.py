from flask import Flask, render_template,g,Response,request
app = Flask(__name__)
from sqlite3 import dbapi2 as sqlite3
import json
DATABASE = 'uni.sqlite3'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))
    db.row_factory = make_dicts
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route("/", methods = [ 'GET'])
def main():
    alumn=query_db('select * from alumno')
    return render_template('index.html',Data =(alumn))


@app.route('/alumno/<codigo>', methods = [ 'POST']) 
def alumno(codigo):
    data=query_db('select * from alumno where codigo=?',[codigo])
    return Response(json.dumps(data), mimetype='application/json')


@app.route("/alumno/update", methods = [ 'POST'])
def alumnoUpdate():
    req=request.form;
    nombre=req['nombre']
    apellido=req['apellido']
    edad=req['edad']
    codigo=req['codigo']
    respuesta=query_db('UPDATE alumno SET nombre=?,apellido=?,edad=? where codigo=?',(nombre,apellido,edad,codigo))
    get_db().commit();
    return render_template('response.html',resp='Alumno Actualizado!!!')


@app.route('/hello/<username>')
def hello(username):
    return 'Hello, World'+username

#Recomendacion crear el insertar aqui

if __name__ == "__main__":
    app.run()