from flask import Flask, request, jsonify, render_template

from models import Usuarios, Empresas, Actividades, Proyectos, db

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['ENV'] = "development"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://wankucl_controlifypro:wp5Sp.4MhY{w@201.148.104.65/wankucl_controlifypro"
app.config['JWT_SECRET_KEY'] = "secret-key"

db.init_app(app)

@app.route('/usuarios', methods=['POST','GET'])
def test():
    user = Usuarios.query.all()
    # user = Usuarios.query.with_entities(Usuarios.primer_nombre).all()
    user = list(map(lambda x: x.serialize(), user))

    return jsonify(user),200
    
    # return jsonify(user.map()),200
    # return jsonify([i.serialize() for i in user]),200
    # user = Usuarios.query.get(1)
    # return jsonify(user.serialize()), 200

@app.route('/empresas')
def getEmpresas():
    empresas = Empresas.query.all()
    empresas = list(map(lambda x: x.serialize(), empresas))
    return jsonify(empresas),200

@app.route('/actividades')
def getActividades():
    actividades = Actividades.query.all()
    actividades = list(map(lambda x: x.serialize(), actividades))
    return jsonify(actividades),200

@app.route('/proyectos')
def getProyectos():
    proyectos = Proyectos.query.all()
    proyectos = list(map(lambda x: x.serialize(), proyectos))
    return jsonify(proyectos),200

    # return  {
    #     "descripcion": "Desarrollo de ingenier\u00eda de  nuevos chutes", 
    #     "estado": 1, 
    #     "fecha_entrega": "Fri, 01 Oct 2021 00:00:00 GMT", 
    #     "fecha_inicio": "Sat, 01 May 2021 00:00:00 GMT", 
    #     "id": 1, 
    #     "jefe_proyecto_id": 1, 
    #     "localidad_id": 1, 
    #     "nombre": "Nuevos Chutes", 
    #     "porcentaje_avance": 20, 
    #     "presupuesto": 1000, 
    #     "sigla": "QUI"
    # }


app.run(host='localhost', port=5000)

