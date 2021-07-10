#   user: wankucl_controlifypro
#   pass: wp5Sp.4MhY{w
#   ip: 201.148.104.65
#   userdb: wankucl_controlifypro
from logging import setLogRecordFactory
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Regiones(db.Model):
    __tablename__ = 'Regiones'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    estado = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "numero": self.numero,
            "estado": self.estado
        }

class Provincias(db.Model):
    __tablename__ = 'Provincias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.Integer, nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('Regiones.id'), nullable=False)
    region = db.relationship('Regiones', backref=db.backref('Provincias', lazy=True))

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "estado": self.estado,
            "region_id": self.region_id
        }

class Comunas(db.Model):
    __tablename__ = 'Comunas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.Integer, nullable=False)
    provincia_id = db.Column(db.Integer, db.ForeignKey('Provincias.id'), nullable=False)
    provincia = db.relationship('Provincias', backref=db.backref('Comunas', lazy=True))

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "estado": self.estado,
            "provincia_id": self.provincia_id
        }

class Empresas(db.Model):
    __tablename__ = 'Empresas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    giro = db.Column(db.String(255), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.Integer, nullable=False)
    comuna_id = db.Column(db.Integer, db.ForeignKey('Comunas.id'), nullable=False)
    comuna = db.relationship('Comunas', backref=db.backref('Empresas', lazy=True))

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "giro": self.giro,
            "direccion": self.direccion,
            "estado": self.estado,
            "comuna_id": self.comuna_id
        }

class Cargos(db.Model):
    __tablename__ = 'Cargos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.Integer, nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('Empresas.id'), nullable=False)
    comuna = db.relationship('Empresas', backref=db.backref('Cargos', lazy=True))

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "estado": self.estado,
            "empresa_id": self.empresa_id
        }

class Roles(db.Model):
    __tablename__ = 'Roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "estado": self.estado
        }

class Usuarios(db.Model):
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(191), nullable=False)
    primer_nombre = db.Column(db.String(191), nullable=False)
    segundo_nombre = db.Column(db.String(191), nullable=True)
    apellido_paterno = db.Column(db.String(191), nullable=False)
    apellido_materno = db.Column(db.String(191), nullable=True)
    password = db.Column(db.String(191), nullable=False)
    email = db.Column(db.String(191), nullable=False)
    estado = db.Column(db.Integer, nullable=False)
    avatar = db.Column(db.String(191), nullable=True)
    comuna_id = db.Column(db.Integer, nullable=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('Roles.id'), nullable=False)
    rol = db.relationship('Roles', backref=db.backref('Usuarios', lazy=True))

    def serialize(self):
        return {
            "id": self.id,
            "rut": self.rut,
            "primer_nombre": self.primer_nombre,
            "segundo_nombre": self.segundo_nombre,
            "apellido_paterno": self.apellido_paterno,
            "apellido_materno": self.apellido_materno,
            "password": self.password,
            "email": self.email,
            "estado": self.estado,
            "avatar": self.avatar,
            "comuna_id": self.comuna_id,
            "rol_id": self.rol_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# consultar por uso de tablas may to man
cargo_usuarios = db.Table('Cargo_Usuarios',
    db.Column('usuario_id', db.Integer, db.ForeignKey('Usuarios.id'), primary_key=True),
    db.Column('cargos_id', db.Integer, db.ForeignKey('Cargos.id'), primary_key=True)
)