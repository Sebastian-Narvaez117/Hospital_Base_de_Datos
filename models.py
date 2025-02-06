from app import db
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Paciente(db.Model):
    __tablename__ = 'Paciente'  # Nombre exacto de la tabla en MySQL

    idPaciente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(30), nullable=False)
    apellido = db.Column(db.String(30), nullable=False)
    direccioncasa = db.Column(db.Text, nullable=True)
    direccioncalle = db.Column(db.Text, nullable=True)
    direccionciudad = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Paciente {self.nombre} {self.apellido}>'
    

class Sala(db.Model):
    __tablename__ = 'Sala'  # Nombre exacto de la tabla en MySQL

    idSala = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipoSala = db.Column(db.String(20), nullable=False)
    capacidad = db.Column(db.Integer, nullable=False)   
    

    def __repr__(self):
        return f'<Sala {self.tipoSala} {self.capacidad}>'
    

class Enfermero(db.Model):
    __tablename__ = 'Enfermero'  # Nombre exacto de la tabla en MySQL

    idEnfermero = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(30), nullable=False)
    apellido = db.Column(db.String(30), nullable=False)
    turno = db.Column(db.String(20))
    idSala = db.Column(db.Integer, db.ForeignKey('Sala.idSala'))  # Relación con Sala
    sala = relationship('Sala', backref='enfermeros')  # Relación con la tabla Sala

    def __repr__(self):
        return f'<Enfermero {self.nombre} {self.apellido}>'


class Citas(db.Model):
    __tablename__ = 'Citas'

    idCita = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.Date, nullable=False)
    motivo = db.Column(db.Text)
    hora = db.Column(db.Time)  # Considera cambiar esto a un tipo de dato de tiempo si es necesario
    idPaciente = db.Column(db.Integer, db.ForeignKey('Paciente.idPaciente'))  # Relación con Paciente
    idSala = db.Column(db.Integer, db.ForeignKey('Sala.idSala'))  # Relación con Sala
    paciente = relationship('Paciente', backref='citas')  # Relación con la tabla Paciente
    sala = relationship('Sala', backref='citas')  # Relación con la tabla Sala

    def __repr__(self):
        return f'<Cita {self.fecha} {self.motivo}>'


class Medico(db.Model):
    __tablename__ = 'Medico'

    idMedico = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(30), nullable=False)
    apellido = db.Column(db.String(30), nullable=False)
    especialidad = db.Column(db.String(30), nullable=False)
    correo = db.Column(db.String(30))
    idCita = db.Column(db.Integer, db.ForeignKey('Citas.idCita'))  # Relación con Citas
    cita = relationship('Citas', backref='medicos')  # Relación con la tabla Citas

    def __repr__(self):
        return f'<Medico {self.nombre} {self.apellido}>'


class Factura(db.Model):
    __tablename__ = 'Factura'

    idFactura = db.Column(db.Integer, primary_key=True, autoincrement=True)
    costo = db.Column(db.Numeric, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(20))
    idCita = db.Column(db.Integer, db.ForeignKey('Citas.idCita'))  # Relación con Citas
    cita = relationship('Citas', backref='facturas')  # Relación con la tabla Citas

    def __repr__(self):
        return f'<Factura {self.idFactura} {self.costo}>'


class HistorialMedico(db.Model):
    __tablename__ = 'HistorialMedico'

    idHistorial = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.Date)
    diagnostico = db.Column(db.Text)
    observaciones = db.Column(db.Text)
    idPaciente = db.Column(db.Integer, db.ForeignKey('Paciente.idPaciente'))  # Relación con Paciente
    paciente = relationship('Paciente', backref='historiales')  # Relación con la tabla Paciente

    def __repr__(self):
        return f'<HistorialMedico {self.fecha} {self.diagnostico}>'


class Tratamiento(db.Model):
    __tablename__ = 'Tratamiento'

    idTratamiento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(30), nullable=False)
    descripcion = db.Column(db.Text)
    duracion = db.Column(db.String(20))
    medicamentos = db.Column(db.Text)
    idHistorial = db.Column(db.Integer, db.ForeignKey('HistorialMedico.idHistorial'))
    historiales = relationship('HistorialMedico', backref='tratamientos')

    def __repr__(self):
        return f'<Tratamiento {self.nombre} {self.duracion}>'
    



class Telefono(db.Model):
    __tablename__ = 'Telefono'

    idTelefono = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero = db.Column(db.String(10))
    idPaciente = db.Column(db.Integer, db.ForeignKey('Paciente.idPaciente'))  # Relación con Paciente
    paciente = relationship('Paciente', backref='telefonos')  # Relación con la tabla Paciente

    def __repr__(self):
        return f'<Telefono {self.numero}>'

