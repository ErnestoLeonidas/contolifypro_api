import os
from flask import Flask, request, jsonify, render_template
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Usuarios, Empresas, Actividades, Proyectos, Localidades

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

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

@app.route('/usuarios', methods=['POST'])
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
    


############# Empresas ###############

@app.route('/empresas', methods=['GET'])
def getEmpresas():
    empresas = Empresas.query.filter(Empresas.estado == 1).all()
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

@app.route('/empresas/<id>', methods=['PUT'])
def updateEmpresa(id):
    empresa = Empresa.query.get(id)

    nombre = request.json.get('nombre')
    giro = request.json.get('giro')
    direccion = request.json.get('direccion')
    estado = request.json.get('estado')
    comuna_id = request.json.get('comuna_id')

    empresa.nombre = nombre
    empresa.giro = giro
    empresa.direccion = direccion
    empresa.estado = estado
    empresa.comuna_id = comuna_id
    empresa.update(actividad)

    return jsonify(actividad.serialize()),200

@app.route('/empresas', methods=['POST'])
def addEmpresa():
    empresa = Empresa()

    nombre = request.json.get('nombre')
    giro = request.json.get('giro')
    direccion = request.json.get('direccion')
    estado = request.json.get('estado')
    comuna_id = request.json.get('comuna_id')

    empresa.nombre = nombre
    empresa.giro = giro
    empresa.direccion = direccion
    empresa.estado = estado
    empresa.comuna_id = comuna_id
    empresa.save(actividad)
    return jsonify(actividad.serialize()),201



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

@app.route('/actividades', methods=['POST'])
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

    return jsonify(actividad.serialize()),201



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
    proyecto.fecha_inicio = fecha_inicio
    proyecto.fecha_entrega = fecha_entrega

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

    proyecto.estado = estado
    proyecto.localidad_id = localidad_id
    proyecto.jefe_proyecto_id = jefe_proyecto_id

    Proyectos.save(proyecto)

    return jsonify(proyecto.serialize()),201

@app.route('/proyectos/buscar', methods=['POST'])
def srcProyectos():
    consulta = request.json

    # print(consulta)

    # if request.json.get('sigla') == None:
    #     return "sin sigla"
    
    # if request.json.get('estado') == 1:
    #     proyectos = proyectos.query.filter(proyectos.estado == 1).all()
    # else:
    #     proyectos = proyectos.query.filter(proyectos.estado == 0).all()

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

app.run(host='localhost', port=5000)

