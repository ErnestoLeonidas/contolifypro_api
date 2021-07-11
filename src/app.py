from flask import Flask, request, jsonify, render_template
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Usuarios, Empresas, Actividades, Proyectos

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['ENV'] = "development"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://wankucl_controlifypro:wp5Sp.4MhY{w@201.148.104.65/wankucl_controlifypro"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['JWT_SECRET_KEY'] = "secret-key"

db.init_app(app)
# CORS(app)
Migrate(app, db)

@app.route('/usuarios', methods=['GET'])
def getUsuarios():
    user = Usuarios.query.all()
    # user = Usuarios.query.with_entities(Usuarios.primer_nombre).all()
    user = list(map(lambda x: x.serialize(), user))

    return jsonify(user),200

@app.route('/usuarios/<id>', methods=['GET'])
def getUsuario(id):
    user = Usuarios.query.get(id)

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

@app.route('/usuarios/<id>', methods=['DELETE'])
def deleteUsuario(id):
    user = Usuarios.query.get(id)
    estado = 0
    user.estado = estado
    Usuarios.update(user)
    return jsonify(user.serialize()),200

@app.route('/empresas', methods=['GET'])
def getEmpresas():
    empresas = Empresas.query.all()
    empresas = list(map(lambda x: x.serialize(), empresas))
    return jsonify(empresas),200

@app.route('/actividades', methods=['GET'])
def getActividades():
    actividades = Actividades.query.all()
    actividades = list(map(lambda x: x.serialize(), actividades))
    return jsonify(actividades),200

@app.route('/proyectos', methods=['GET'])
def getProyectos():
    proyectos = Proyectos.query.all()
    proyectos = list(map(lambda x: x.serialize(), proyectos))
    return jsonify(proyectos),200



app.run(host='localhost', port=5000)

