from flask import Flask, request, jsonify, render_template

from models import Usuarios, Empresas, Actividades, db

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


app.run(host='localhost', port=5000)

