#   user: wankucl_controlifypro
#   pass: wp5Sp.4MhY{w
#   ip: 201.148.104.65
#   userdb: wankucl_controlifypro
# from logging import setLogRecordFactory
from flask_sqlalchemy import SQLAlchemy
import datetime
# from datetime import datetime // se usa para setear el datetime https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/    ver simple realtionship
db = SQLAlchemy()

class Regiones(db.Model):
    __tablename__ = 'Regiones'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=True)
    numero = db.Column(db.String(10), nullable=True)
    estado = db.Column(db.Integer, nullable=True)

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
    nombre = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.Integer, nullable=True)
    region_id = db.Column(db.Integer, db.ForeignKey('Regiones.id'), nullable=True)
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
    nombre = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.Integer, nullable=True)
    provincia_id = db.Column(db.Integer, db.ForeignKey('Provincias.id'), nullable=True)
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
    nombre = db.Column(db.String(255), nullable=True)
    giro = db.Column(db.String(255), nullable=True)
    direccion = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.Integer, nullable=True)
    comuna_id = db.Column(db.Integer, db.ForeignKey('Comunas.id'), nullable=True)
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

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
class Cargos(db.Model):
    __tablename__ = 'Cargos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.Integer, nullable=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('Empresas.id'), nullable=True)
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
    name = db.Column(db.String(255), nullable=True)
    display_name = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.Integer, nullable=True)

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
    rut = db.Column(db.String(191), nullable=True)
    primer_nombre = db.Column(db.String(191), nullable=True)
    segundo_nombre = db.Column(db.String(191), nullable=True)
    apellido_paterno = db.Column(db.String(191), nullable=True)
    apellido_materno = db.Column(db.String(191), nullable=True)
    password = db.Column(db.String(191), nullable=True)
    email = db.Column(db.String(191), nullable=True)
    estado = db.Column(db.Integer, nullable=True)
    avatar = db.Column(db.String(191), nullable=True)
    comuna_id = db.Column(db.Integer, nullable=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('Roles.id'), nullable=True)
    rol = db.relationship('Roles', backref=db.backref('Usuarios', lazy=True))

    # def __init__(self, rut, primer_nombre, segundo_nombre, apellido_paterno, apellido_materno, password,email, estado,avatar, comuna_id, rol_id):
    #     self.rut = rut,
    #     self.primer_nombre = primer_nombre,
    #     self.segundo_nombre = segundo_nombre,
    #     self.apellido_paterno = apellido_paterno,
    #     self.apellido_materno = apellido_materno,
    #     self.password = password
    #     self.email = email
    #     self.estado = estado
    #     self.avatar = avatar
    #     self.comuna_id = comuna_id
    #     self.rol_id = rol_id

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

class Localidades(db.Model):
    __tablename__ = 'Localidades'
    id = db.Column(db.Integer, primary_key=True)
    sigla = db.Column(db.String(45), nullable=True)
    nombre = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.Integer, nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "sigla": self.sigla,
            "nombre": self.nombre,
            "estado": self.estado
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Proyectos(db.Model):
    __tablename__ = 'Proyectos'
    id = db.Column(db.Integer, primary_key=True)
    sigla = db.Column(db.String(45), nullable=True)
    nombre = db.Column(db.String(255), nullable=True)
    descripcion = db.Column(db.String(255), nullable=True)
    porcentaje_avance = db.Column(db.Integer, nullable=True)
    presupuesto = db.Column(db.Integer, nullable=True)
    fecha_inicio = db.Column(db.DateTime, nullable=True)
    fecha_entrega = db.Column(db.DateTime, nullable=True)
    estado = db.Column(db.Integer, nullable=True)

    localidad_id = db.Column(db.Integer, db.ForeignKey('Localidades.id'), nullable=True)
    localidad = db.relationship('Localidades', backref=db.backref('Proyectos', lazy=True))

    jefe_proyecto_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=True)
    jefe_proyecto = db.relationship('Usuarios', backref=db.backref('Proyectos', lazy=True))

    def serialize(self):
        return {
            "id": self.id,
            "sigla": self.sigla,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "porcentaje_avance": self.porcentaje_avance,
            "presupuesto": self.presupuesto,
            "fecha_inicio": self.fecha_inicio.strftime('%d-%m-%y'),
            "fecha_entrega": self.fecha_entrega.strftime('%d-%m-%y'),
            "estado": self.estado,
            "localidad_id": self.localidad_id,
            "jefe_proyecto": self.jefe_proyecto_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Actividades(db.Model):
    __tablename__ = 'Actividades'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable=True)
    fecha_inicio = db.Column(db.DateTime, nullable=True)
    porcentaje_avance = db.Column(db.Integer, nullable=True)
    observacion = db.Column(db.String(2000), nullable=True)
    estado = db.Column(db.Integer, nullable=True)

    proyecto_id = db.Column(db.Integer, db.ForeignKey('Proyectos.id'), nullable=True)
    proyecto = db.relationship('Proyectos', backref=db.backref('Actividades', lazy=True))

    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=True)
    usuario = db.relationship('Usuarios', backref=db.backref('Actividades', lazy=True))

    def serialize(self):
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "fecha_inicio": self.fecha_inicio.strftime('%d-%m-%y'),
            "porcentaje_avance": self.porcentaje_avance,
            "observacion": self.observacion,
            "estado": self.estado,
            "proyecto_id": self.proyecto_id,
            "usuario_id": self.usuario_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Horas(db.Model):
    __tablename__ = 'Horas'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable=True)
    fecha = db.Column(db.DateTime, nullable=True)
    hh = db.Column(db.Float, nullable=True)
    hh_extra = db.Column(db.Float, nullable=True)
    estado = db.Column(db.Integer, nullable=True)

    actividad_id = db.Column(db.Integer, db.ForeignKey('Actividades.id'), nullable=True)
    actividad = db.relationship('Actividades', backref=db.backref('Horas', lazy=True))
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=True)
    usuario = db.relationship('Usuarios', backref=db.backref('Horas', lazy=True))

    proyecto_id = db.Column(db.Integer, db.ForeignKey('Proyectos.id'), nullable=True)
    proyecto = db.relationship('Proyectos', backref=db.backref('Horas', lazy=True))

    def serialize(self):
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "fecha": self.fecha.strftime('%d-%m-%y'),
            "hh": self.hh,
            "hh_extra": self.hh_extra,
            "estado": self.estado,
            "actividad_id": self.actividad_id,
            "usuario_id": self.usuario_id,
            "proyecto_id": self.proyecto_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# usuarios_empresas

# disciplinas