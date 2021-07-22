import os
from flask import Flask, request, jsonify, render_template
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Usuarios, Actividades, Proyectos, Localidades, Horas

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

# flask_mysqldb
from flask_mysqldb import MySQL
#  pandas
import pandas as pd
from pandas.io import sql


from datetime import datetime
import time

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['ENV'] = "development"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://controlify:dhdgIEC{G967@controlify2.ca9hiqnjeavi.sa-east-1.rds.amazonaws.com/controlify2"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['JWT_SECRET_KEY'] = "secret-key"


# flask_mysqldb
app.config['MYSQL_HOST'] = "controlify2.ca9hiqnjeavi.sa-east-1.rds.amazonaws.com"
app.config['MYSQL_USER'] = 'controlify'
app.config['MYSQL_PASSWORD'] = 'dhdgIEC{G967'
app.config['MYSQL_DB'] = 'controlify2'
mysql = MySQL(app)


db.init_app(app)
# CORS(app)
Migrate(app, db)

app.config["JWT_SECRET_KEY"] = "os.environ.get('super-secret')"
jwt = JWTManager(app)

############# Login ###############

@app.route("/login", methods=["POST"])
def create_token():
    email = request.json.get("email")
    password = request.json.get("password")

    user = Usuarios.query.filter(Usuarios.email == email, Usuarios.password == password).first()

    if user.estado == 0:
        return jsonify({ 
            "estado": "desactivado",
            "msg": "Su usuario se encuentra desactivado, favor contactese con su administrador o jefe de proyecto"}), 204

    if user == None:
        return jsonify({ 
            "estado": "error",
            "msg": "Error en email o password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token, usuario_id=user.id, rol_id=user.rol_id),200



############# Usuarios ###############

@app.route('/usuarios', methods=['GET'])
def getUsuarios():
    user = Usuarios.query.filter(Usuarios.estado == 1).all()
    # user = Usuarios.query.with_entities(Usuarios.primer_nombre).all()
    user = list(map(lambda x: x.serialize(), user))
    return jsonify(user),200

@app.route('/usuarios/<id>', methods=['GET'])
def getUsuario(id):
    user = Usuarios.query.get(id)
    return jsonify(user.serialize()),200

@app.route('/usuarios/<id>', methods=['DELETE'])
def deleteUsuario(id):
    user = Usuarios.query.get(id)
    user.estado = 0
    Usuarios.update(user)
    return jsonify(user.serialize()),200
    
@app.route('/usuarios/<id>', methods=['PUT'])
def updateUsuario(id):
    user = Usuarios.query.get(id)

    primer_nombre = request.json.get('primer_nombre')
    segundo_nombre = request.json.get('segundo_nombre')
    apellido_paterno = request.json.get('apellido_paterno')
    apellido_materno = request.json.get('apellido_materno')
    password = request.json.get('password')
    email = request.json.get('email')
    estado = request.json.get('estado')
    avatar = request.json.get('avatar')
    comuna_id = request.json.get('comuna_id')
    rol_id = request.json.get('rol_id')

    user.primer_nombre = primer_nombre
    user.segundo_nombre = segundo_nombre
    user.apellido_paterno = apellido_paterno
    user.apellido_materno = apellido_materno
    user.password = password
    user.email = email
    user.estado = estado
    user.avatar = avatar
    user.comuna_id = comuna_id
    user.rol_id = rol_id

    Usuarios.update(user)

    return jsonify(user.serialize()),200

@app.route('/usuarios', methods=['POST'])
def addUsuario():
    user = Usuarios()

    primer_nombre = request.json.get('primer_nombre')
    segundo_nombre = request.json.get('segundo_nombre')
    apellido_paterno = request.json.get('apellido_paterno')
    apellido_materno = request.json.get('apellido_materno')
    password = request.json.get('password')
    email = request.json.get('email')
    estado = request.json.get('estado')
    avatar = request.json.get('avatar')
    comuna_id = request.json.get('comuna_id')
    rol_id = request.json.get('rol_id')

    user.rut = rut
    user.primer_nombre = primer_nombre
    user.segundo_nombre = segundo_nombre
    user.apellido_paterno = apellido_paterno
    user.apellido_materno = apellido_materno
    user.password = password
    user.email = email
    user.estado = 1
    user.avatar = avatar
    user.comuna_id = comuna_id
    user.rol_id = rol_id

    Usuarios.save(user)

    return jsonify(user.serialize()),200
    

############# Actividades ###############

@app.route('/actividades', methods=['GET'])
# @jwt_required()
def getActividades():
    actividades = Actividades.query.filter(Actividades.estado == 1).all()
    actividades = list(map(lambda x: x.serialize(), actividades))
    return jsonify(actividades),200

@app.route('/actividades/<id>', methods=['GET'])
def getActividad(id):
    actividad = Actividades.query.get(id)
    return jsonify(actividad.serialize()),200

@app.route('/actividades/<id>', methods=['DELETE'])
def deleteActividad(id):
    actividad = Actividades.query.get(id)
    actividad.estado = 0
    Actividades.update(actividad)

    return jsonify(actividad.serialize()),200

@app.route('/actividades/<id>', methods=['PUT'])
def updateActividad(id):
    actividad = Actividades.query.get(id)

    descripcion = request.json.get('descripcion')
    fecha_inicio = request.json.get('fecha_inicio')
    porcentaje_avance = request.json.get('porcentaje_avance')
    presupuesto = request.json.get('presupuesto')
    estado = request.json.get('estado')
    proyecto_id = request.json.get('proyecto_id')
    usuario_id = request.json.get('usuario_id')

    actividad.descripcion = descripcion
    actividad.fecha_inicio = datetime.strptime(fecha_inicio, '%d-%m-%Y').date()
    actividad.porcentaje_avance = porcentaje_avance
    actividad.presupuesto = presupuesto
    actividad.estado = estado
    actividad.proyecto_id = proyecto_id
    actividad.usuario_id = usuario_id

    Actividades.update(actividad)

    return jsonify(actividad.serialize()),200

@app.route('/actividades', methods=['POST'])
def addActividad():
    actividad = Actividades()

    descripcion = request.json.get('descripcion')
    fecha_inicio = request.json.get('fecha_inicio')
    porcentaje_avance = request.json.get('porcentaje_avance')
    presupuesto = request.json.get('presupuesto')
    estado = request.json.get('estado')
    proyecto_id = request.json.get('proyecto_id')
    usuario_id = request.json.get('usuario_id')

    actividad.descripcion = descripcion
    actividad.fecha_inicio = fecha_inicio
    actividad.porcentaje_avance = porcentaje_avance
    actividad.presupuesto = presupuesto
    actividad.estado = 1
    actividad.proyecto_id = proyecto_id
    actividad.usuario_id = usuario_id

    Actividades.save(actividad)

    return jsonify(actividad.serialize()),201

@app.route('/actividades/<id>/proyectos', methods=['GET'])
def srcActividadesSegunProyecto(id):
    actividades = Actividades.query.filter(Actividades.proyecto_id == id, Actividades.estado == 1).all()
    actividades = list(map(lambda x: x.serialize(), actividades))
    return jsonify(actividades),200

@app.route('/actividades/buscar', methods=['POST'])
def srcActividades():
    consulta = request.json
    
    actividades = Actividades.query.filter_by(**consulta).all()

    if len(actividades) == 0:
        return jsonify({ "msg": "No se encuentran actividades según criterio de búsqueda"}), 401

    actividades = list(map(lambda x: x.serialize(), actividades))
    return jsonify(actividades),200

############# Proyectos ###############

@app.route('/proyectos', methods=['GET'])
def getProyectos():
    proyectos = Proyectos.query.filter(Proyectos.estado == 1).all()
    proyectos = list(map(lambda x: x.serialize(), proyectos))
    return jsonify(proyectos),200

@app.route('/proyectos/<id>', methods=['GET'])
def getProyecto(id):
    proyecto = Proyectos.query.get(id)
    return jsonify(proyecto.serialize()),200

@app.route('/proyectos/<id>', methods=['DELETE'])
def deleteProyecto(id):
    proyecto = Proyectos.query.get(id)
    proyecto.estado = 0
    Proyectos.update(proyecto)
    return jsonify(proyecto.serialize()),200

@app.route('/proyectos/<id>', methods=['PUT'])
def updateProyecto(id):
    proyecto = Proyectos.query.get(id)

    sigla = request.json.get('sigla')
    nombre = request.json.get('nombre')
    descripcion = request.json.get('descripcion')
    porcentaje_avance = request.json.get('porcentaje_avance')
    presupuesto = request.json.get('presupuesto')
    fecha_inicio = request.json.get('fecha_inicio')
    fecha_entrega = request.json.get('fecha_entrega')
    estado = request.json.get('estado')
    localidad_id = request.json.get('localidad_id')
    jefe_proyecto_id = request.json.get('jefe_proyecto_id')

    proyecto.sigla = sigla
    proyecto.nombre = nombre
    proyecto.descripcion = descripcion
    proyecto.porcentaje_avance = porcentaje_avance
    proyecto.presupuesto = presupuesto

    # la fecha viene como string, acá se transforma a date
    proyecto.fecha_inicio = datetime.strptime(fecha_inicio, '%d-%m-%Y').date()
    proyecto.fecha_entrega = datetime.strptime(fecha_entrega, '%d-%m-%Y').date()

    proyecto.estado = estado
    proyecto.localidad_id = localidad_id
    proyecto.jefe_proyecto_id = jefe_proyecto_id

    Proyectos.update(proyecto)

    return jsonify(proyecto.serialize()),200

@app.route('/proyectos', methods=['POST'])
def addProyecto():
    proyecto = Proyectos()

    sigla = request.json.get('sigla')
    nombre = request.json.get('nombre')
    descripcion = request.json.get('descripcion')
    porcentaje_avance = request.json.get('porcentaje_avance')
    presupuesto = request.json.get('presupuesto')
    fecha_inicio = request.json.get('fecha_inicio')
    fecha_entrega = request.json.get('fecha_entrega')
    estado = request.json.get('estado')
    localidad_id = request.json.get('localidad_id')
    jefe_proyecto_id = request.json.get('jefe_proyecto_id')

    proyecto.sigla = sigla
    proyecto.nombre = nombre
    proyecto.descripcion = descripcion
    proyecto.porcentaje_avance = porcentaje_avance
    proyecto.presupuesto = presupuesto

    proyecto.fecha_inicio = fecha_inicio
    proyecto.fecha_entrega = fecha_entrega

    proyecto.estado = 1
    proyecto.localidad_id = localidad_id
    proyecto.jefe_proyecto_id = jefe_proyecto_id

    Proyectos.save(proyecto)

    return jsonify(proyecto.serialize()),201

@app.route('/proyectos/buscar', methods=['POST'])
def srcProyectos():
    consulta = request.json

    proyectos = Proyectos.query.filter_by(**consulta).all()

    if len(proyectos) == 0:
        return jsonify({ "msg": "No se encuentran proyectos según criterio"}), 401

    proyectos = list(map(lambda x: x.serialize(), proyectos))
    return jsonify(proyectos),200

@app.route('/usuarios/jefe_proyectos', methods=['GET'])
def getJefeProyectos():
    user = Usuarios.query.filter(Usuarios.rol_id == 2).all()
    # user = Usuarios.query.with_entities(Usuarios.primer_nombre).all()
    user = list(map(lambda x: x.serialize(), user))
    return jsonify(user),200

############# Localidades ###############

@app.route('/localidades', methods=['GET'])
def getLocalidades():
    localidades = Localidades.query.filter(Localidades.estado == 1).all()
    localidades = list(map(lambda x: x.serialize(), localidades))
    return jsonify(localidades),200


############# Horas ###############

@app.route('/horas', methods=['GET'])
def getHoras():
    horas = Horas.query.filter(Horas.estado == 1).all()
    horas = list(map(lambda x: x.serialize(), horas))
    return jsonify(horas),200

@app.route('/horas/<id>', methods=['GET'])
def getHora(id):
    horas = Horas.query.get(id)
    return jsonify(horas.serialize()),200

@app.route('/horas/<id>', methods=['DELETE'])
def deleteHora(id):
    horas = Horas.query.get(id)
    horas.estado = 0
    Horas.update(horas)
    return jsonify(horas.serialize()),200

@app.route('/horas/<id>', methods=['PUT'])
def updateHora(id):
    horas = Horas.query.get(id)

    descripcion = request.json.get('descripcion')
    fecha = request.json.get('fecha')
    hh = request.json.get('hh')
    hh_extra = request.json.get('hh_extra')
    estado = request.json.get('estado')
    actividad_id = request.json.get('actividad_id')
    usuario_id = request.json.get('usuario_id')
    proyecto_id = request.json.get('proyecto_id')

    horas.descripcion = descripcion
    horas.fecha = datetime.strptime(fecha, '%d-%m-%Y').date()
    horas.hh = hh
    horas.hh_extra = hh_extra
    horas.estado = estado
    horas.actividad_id = actividad_id
    horas.usuario_id = usuario_id
    horas.proyecto_id = proyecto_id

    Horas.update(horas)

    return jsonify(horas.serialize()),200

@app.route('/horas', methods=['POST'])
def addHora():
    horas = Horas()

    descripcion = request.json.get('descripcion')
    fecha = request.json.get('fecha')
    hh = request.json.get('hh')
    hh_extra = request.json.get('hh_extra')
    estado = request.json.get('estado')
    actividad_id = request.json.get('actividad_id')
    usuario_id = request.json.get('usuario_id')
    proyecto_id = request.json.get('proyecto_id')

    horas.descripcion = descripcion
    horas.fecha = fecha
    horas.hh = hh
    horas.hh_extra = hh_extra
    horas.estado = 1
    horas.actividad_id = actividad_id
    horas.usuario_id = usuario_id
    horas.proyecto_id = proyecto_id

    Horas.save(horas)

    return jsonify(horas.serialize()),201


############# flask_mysqldb ###############
@app.route('/test', methods=['GET'])
def get_test():
    # cur = mysql.connection.cursor()
    # cur.execute('SELECT id AS id, primer_nombre FROM Usuarios')
    # data = cur.fetchall()
    # print(data)
    data = pd.read_sql('SELECT id, primer_nombre FROM Usuarios;',mysql.connection)
    my_json = data.to_json(orient='records')
    
    return my_json

@app.route('/HorasPorActividad', methods=['GET'])
def get_HorasPorProyecto():
    data = pd.read_sql('SELECT sum(h.hh) AS hh, a.id AS actividad_id, a.descripcion AS descripcion FROM Horas h JOIN Actividades a ON a.id = h.actividad_id WHERE h.usuario_id = 1 AND h.estado = 1 GROUP BY a.id;',mysql.connection)
    my_json = data.to_json(orient='records')
    
    return my_json


app.run(host='localhost', port=5000)

