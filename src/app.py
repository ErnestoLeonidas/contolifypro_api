from flask import Flask, request, jsonify, render_template
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Usuarios, Empresas, Actividades, Proyectos

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['ENV'] = "development"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://wankucl_wankucl_controlifypro2:dhdgIEC{G967@201.148.104.65/wankucl_controlifypro2"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['JWT_SECRET_KEY'] = "secret-key"

db.init_app(app)
# CORS(app)
Migrate(app, db)

@app.route('/usuarios', methods=['GET'])
def getUsuarios():
    user = Usuarios.query.all()
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
    
@app.route('/usuarios/<id>', methods=['POST'])
def updateUsuario(id):
    user = Usuarios.query.get(id)

    rut = request.json.get('rut')
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
    user.estado = estado
    user.avatar = avatar
    user.comuna_id = comuna_id
    user.rol_id = rol_id

    Usuarios.update(user)

    return jsonify(user.serialize()),200

@app.route('/usuarios', methods=['PUT'])
def addUsuario():

    user = Usuarios()

    rut = request.json.get('rut')
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
    user.estado = estado
    user.avatar = avatar
    user.comuna_id = comuna_id
    user.rol_id = rol_id

    Usuarios.save(user)

    return jsonify(user.serialize()),200

# empresas
@app.route('/empresas', methods=['GET'])
def getEmpresas():
    empresas = Empresas.query.all()
    empresas = list(map(lambda x: x.serialize(), empresas))
    return jsonify(empresas),200

@app.route('/empresas/<id>', methods=['GET'])
def getEmpresa(id):
    empresa = Empresas.query.get(id)
    return jsonify(empresa.serialize()),200

@app.route('/empresas/<id>', methods=['DELETE'])
def deleteEmpresa(id):
    empresa = Empresas.query.get(id)
    empresa.estado = 0
    Empresas.update(empresa)

    return jsonify(empresa.serialize()),200


@app.route('/actividades', methods=['GET'])
def getActividades():
    actividades = Actividades.query.all()
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

@app.route('/actividades/<id>', methods=['POST'])
def updateActividad(id):
    actividad = Actividades.query.get(id)

    descripcion = request.json.get('descripcion')
    fecha_inicio = request.json.get('fecha_inicio')
    porcentaje_avance = request.json.get('porcentaje_avance')
    observacion = request.json.get('observacion')
    estado = request.json.get('estado')
    proyecto_id = request.json.get('proyecto_id')
    usuario_id = request.json.get('usuario_id')

    actividad.descripcion = descripcion
    actividad.fecha_inicio = fecha_inicio
    actividad.porcentaje_avance = porcentaje_avance
    actividad.observacion = observacion
    actividad.estado = estado
    actividad.proyecto_id = proyecto_id
    actividad.usuario_id = usuario_id

    Actividades.update(actividad)

    return jsonify(actividad.serialize()),200

@app.route('/actividades', methods=['PUT'])
def addActividad():

    actividad = Actividades()

    descripcion = request.json.get('descripcion')
    fecha_inicio = request.json.get('fecha_inicio')
    porcentaje_avance = request.json.get('porcentaje_avance')
    observacion = request.json.get('observacion')
    estado = request.json.get('estado')
    proyecto_id = request.json.get('proyecto_id')
    usuario_id = request.json.get('usuario_id')

    actividad.descripcion = descripcion
    actividad.fecha_inicio = fecha_inicio
    actividad.porcentaje_avance = porcentaje_avance
    actividad.observacion = observacion
    actividad.estado = estado
    actividad.proyecto_id = proyecto_id
    actividad.usuario_id = usuario_id

    Actividades.save(actividad)

    return jsonify(actividad.serialize()),200

@app.route('/proyectos', methods=['GET'])
def getProyectos():
    proyectos = Proyectos.query.all()
    proyectos = list(map(lambda x: x.serialize(), proyectos))
    return jsonify(proyectos),200



app.run(host='localhost', port=5000)

