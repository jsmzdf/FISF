from flask import Flask, redirect, url_for, session, request, flash
from flask_login import LoginManager, current_user, logout_user, login_user, login_required
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vhgzvhozoozevhvxivgzkzizurhwzaz'

#inicializacion la BaseDatos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
from ModelosBD import *

#inicializacion el logeo
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return usuario.query.get(int(user_id))

@app.route('/admin')
def hello_admin():
   return 'Permisos de administrador concedidos'

@app.route('/u/<guest>')
def hello_guest(guest):
   return f"Permisos de {guest} (docente)"

@app.route('/user/<name>')
def hello_user(name):
    if name =='admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest',guest = name))

@app.route('/user')
def user():
    try:
        return redirect(url_for('hello_user', name=current_user.nom_usu))
    except:
        return "No hay usuario actual"

#configuracion de ruta /crear
@app.route('/crear', methods=["GET"])
def create():
    try:
        try:
            datos = [request.args.get(i) for i in [j for j in usuario.getField() if j != "codigo_usu"]]
        except:
            datos = ["Error" for i in usuario.getField()]
        finally:
            pass #print("Datos", datos)
        try:
            userFnd = db.session.query(usuario).order_by(usuario.codigo_usu.desc()).first()
            datos.append(str(int(userFnd.codigo_usu)+1))
        except:
            datos.append("1")
        finally:
            pass #print("Datos", datos)
        user = usuario(datos[0],datos[1],datos[2],datos[3],datos[4],datos[5])
        userFnd = usuario.query.filter_by(email_usu=user.email_usu).first()
        if userFnd == None:
            db.session.add(user)
            db.session.commit()
            # login_user(user)
            return "Exito al insertar " + str(user)
        else:
            return "Error" + "Ya existe ese email de usuario"
    except:
        return "Error" + "Inesperado"

#configuracion de ruta /login
@app.route('/login', methods=["GET"])
def login():
    if ("codigo_usu" not in session or session["codigo_usu"] == ""):
        for i in ["codigo_usu", "contra_usu"]: session[i] = request.args.get(i)
        return redirect(url_for('login'))
    else:
        datos = [session[i] for i in ["codigo_usu", "contra_usu"]]
        session["codigo_usu"] = ""
        session["contra_usu"] = ""
        del session["contra_usu"]
        if None not in datos:
            userFnd = usuario.query.filter_by(codigo_usu=datos[0], contra_usu=datos[1]).first()
            if userFnd != None:
                login_user(userFnd)
                return redirect(url_for('user'))
            else:
                return "No existe un usuario con los datos pedidos"
        else:
            return "Fallo en el envio de datos"

#configuracion de ruta /logout
@app.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('user'))

#configuracion de ruta /list/entidades
@app.route('/list/entidades', methods=["GET"])
def lEntidad():
    s = ""
    for i in db.engine.table_names(): s += i + "<br>"
    return s[:-4]

#configuracion de ruta /list/columnas/<entidad>
@app.route('/list/columnas/<entidad>', methods=["GET"])
def lColumna(entidad):
    s = ""
    for i in db.metadata.tables[entidad].c: s += str(i)[8:] + "<br>"
    return s[:-4]

#configuracion de ruta /list/registros/<entidad>
@app.route('/list/registros/<entidad>', methods=["GET"])
def lRegister(entidad):
    #if entidad == "usuario": return redirect(url_for('lUsuarios'))
    s = ""
    for i in db.session.query(db.metadata.tables[entidad]).all(): s += str(i) + "<br>"
    return s[:-4]

#configuracion de ruta /s/<entidad>/<campo>/<ide>
@app.route('/s/<entidad>/<campo>/<ide>', methods=["GET"])
def sRegister(entidad, campo, ide):
    #if entidad == "usuario": return redirect(url_for('lUsuarios'))
    s = ""
    for i in db.session.query(db.metadata.tables[entidad]).filter(db.metadata.tables[entidad].c[campo]==ide).all(): s += str(i) + "<br>"
    return s[:-4]

#configuracion de ruta /u/list
@app.route('/u/list', methods=["GET"])
def lUsuarios():
    s = ""
    for i in usuario.query.all(): s += str(i) + "<br>"
    return s[:-4]

#configuracion de ruta /u/s/<campo>/<ide>
@app.route('/u/s/<campo>/<ide>', methods=["GET"])
def sUsuarios(campo, ide):
    s = ""
    for i in usuario.query.filter(usuario.__table__.c[campo]==ide).all(): s += str(i) + "<br>"
    return s[:-4]

#configuracion de ruta /borrar/<campo>/<ide>
@app.route('/borrar/<campo>/<ide>', methods=["GET"])
def delete(campo, ide):
    try:
        d = db.session.query(usuario).filter(usuario.__table__.c[campo]==ide)
        d.delete(synchronize_session=False)
        db.session.commit()
        return "Exito al eliminar registros"
    except:
        return "Error" + "Inesperado"

#configuracion de ruta /modificar/<campo>/<ide>
@app.route('/modificar/<campo>/<ide>', methods=["GET"])
def update(campo, ide):
    try:
        if campo not in usuario.__table__.c:
            return "Campo " + campo + " no existe"
        userFnd = db.session.query(usuario).filter(usuario.__table__.c[campo]==ide).first()
        if userFnd == None:
            return "No existe el usuario"
        try:
            datos = {usuario.__table__.c[i]: request.args.get(i) for i in usuario.getField() if request.args.get(i) != None}
        except:
            return "Error Inesperado #3"
        finally:
            pass#print("Datos", datos)
        db.session.query(usuario).filter(usuario.id_usu==userFnd.id_usu).update(datos, synchronize_session=False)
        db.session.commit()
        return "Exito al modificar " + str(user)
    except:
        return "Error" + "Inesperado"

if __name__ == '__main__':
   app.run(debug = True)