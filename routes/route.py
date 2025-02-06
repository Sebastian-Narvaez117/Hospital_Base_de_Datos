from flask import  Blueprint, render_template, request, redirect,flash, url_for
from models import Enfermero, Paciente, Sala,Citas
from app import db




router = Blueprint('router', __name__)
@router.route('/')
def index():
    return render_template('index.html')




@router.route('/register/patient', methods=['GET', 'POST'])
def register_patient():
    if request.method == 'POST':
        try:
            # Obtén los datos enviados desde el formulario
            nombre = request.form.get('nombre')
            apellido = request.form.get('apellido')
            direccioncasa = request.form.get('casa')
            direccioncalle = request.form.get('calle')
            direccionciudad = request.form.get('ciudad')

            # Valida que los campos obligatorios no estén vacíos
            if not nombre or not apellido:
                flash("El nombre y apellido son obligatorios", "error")
                return redirect('/register/patient')

            # Crea un nuevo paciente
            nuevo_paciente = Paciente(
                nombre=nombre,
                apellido=apellido,
                direccioncasa=direccioncasa,
                direccioncalle=direccioncalle,
                direccionciudad=direccionciudad
            )
            # Guarda en la base de datos
            db.session.add(nuevo_paciente)
            db.session.commit()

            # Mensaje de éxito
            flash("Paciente registrado correctamente", "success")
            return redirect('/list/patient')
        except Exception as e:
            # En caso de error
            flash(f"Error al registrar el paciente: {str(e)}", "error")
            return redirect('/register/patient')

    # Si el método es GET, renderiza el formulario
    return render_template('Paciente/registro.html')




@router.route('/list/patient')
def list_patient():
    pacientes = Paciente.query.all()  # Obtén todos los pacientes de la base de datos
    return render_template('Paciente/lista.html', pacientes=pacientes)  # Pasa los datos al template



#Ruta para eliminar pacientes

@router.route('/delete/patient/<int:id>', methods=['GET'])
def delete_patient(id):
    try:
        # Busca el paciente por ID
        paciente = Paciente.query.get_or_404(id)
        
        # Elimina el paciente de la base de datos
        db.session.delete(paciente)
        db.session.commit()
        
        # Mensaje de éxito
        flash("Paciente eliminado correctamente", "success")
        
    except Exception as e:
        # En caso de error
        flash(f"Error al eliminar el paciente", "error")
    
    # Redirecciona a la lista de pacientes
    return redirect(url_for('router.list_patient'))


#Ruta para editar pacientes
@router.route('/edit/patient/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    # Obtener el paciente por ID
    paciente = Paciente.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Actualizar los datos del paciente
            paciente.nombre = request.form.get('nombre')
            paciente.apellido = request.form.get('apellido')
            paciente.direccioncasa = request.form.get('casa')
            paciente.direccioncalle = request.form.get('calle')
            paciente.direccionciudad = request.form.get('ciudad')
            
            # Validar campos obligatorios
            if not paciente.nombre or not paciente.apellido:
                flash("El nombre y apellido son obligatorios", "error")
                return redirect(url_for('router.edit_patient', id=id))
            
            # Guardar los cambios
            db.session.commit()
            
            flash("Paciente actualizado correctamente", "success")
            return redirect(url_for('router.list_patient'))
            
        except Exception as e:
            db.session.rollback()
            flash("Error al actualizar el paciente", "error")
            return redirect(url_for('router.edit_patient', id=id))
    
    # Si es GET, mostrar el formulario con los datos actuales
    return render_template('Paciente/editar.html', paciente=paciente)










#Ruta para registrar salas


@router.route('/register/sala', methods=['GET', 'POST'])
def register_sala():
    if request.method == 'POST':
        try:
            # Obtén los datos enviados desde el formulario
            tipoSala = request.form.get('tipoSala')
            capacidad = request.form.get('capacidad')
            

            # Valida que los campos obligatorios no estén vacíos
            if not tipoSala or not capacidad:
                flash("Faltan datos", "error")
                return redirect('/register/sala')

            # Crea un nuevo paciente
            nueva_sala= Sala(
                tipoSala=tipoSala,
                capacidad=capacidad,

            )
            # Guarda en la base de datos
            db.session.add(nueva_sala)
            db.session.commit()

            # Mensaje de éxito
            flash("Sala guardada correctamente", "success")
            return redirect('/list/sala')
        except Exception as e:
            # En caso de error
            flash("Error al guardar la sala", "error")
            return redirect('/register/sala')

    # Si el método es GET, renderiza el formulario
    return render_template('sala/registro.html')


@router.route('/list/sala')
def list_sala():
    salas = Sala.query.all()
    return render_template('sala/lista.html', salas=salas)


#Ruta para editar salas
@router.route('/edit/sala/<int:id>', methods=['GET', 'POST'])
def edit_sala(id):
    # Obtener la sala por ID
    sala = Sala.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Actualizar los datos de la sala
            sala.tipoSala = request.form.get('tipoSala')
            sala.capacidad = request.form.get('capacidad')
            
            # Validar campos obligatorios
            if not sala.tipoSala or not sala.capacidad:
                flash("Faltan datos", "error")
                return redirect(url_for('router.edit_sala', id=id))
            
            # Guardar los cambios
            db.session.commit()
            
            flash("Sala actualizada correctamente", "success")
            return redirect(url_for('router.list_sala'))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar la sala", "error")
            return redirect(url_for('router.edit_sala', id=id))
    
    # Si es GET, mostrar el formulario con los datos actuales
    return render_template('sala/editar.html', sala=sala)


#Ruta para eliminar salas
@router.route('/delete/sala/<int:id>', methods=['GET'])
def delete_sala(id):
    try:
        # Busca la sala por ID
        sala = Sala.query.get_or_404(id)
        
        # Elimina la sala de la base de datos
        db.session.delete(sala)
        db.session.commit()
        
        # Mensaje de éxito
        flash("Sala eliminada correctamente", "success")
        
    except Exception as e:
        # En caso de error
        flash(f"Error al eliminar la sala", "error")
    
    # Redirecciona a la lista de salas
    return redirect(url_for('router.list_sala'))












#Ruta para registrar enfermeros

@router.route('/register/enfermero', methods=['GET', 'POST'])
def register_enfermero():
    # Obtener todas las salas para el formulario
    salas = Sala.query.all()

    if request.method == 'POST':
        try:
            # Obtén los datos enviados desde el formulario
            nombre = request.form.get('nombre')
            apellido = request.form.get('apellido')
            turno = request.form.get('turno')
            idSala = request.form.get('idSala')
            
            # Valida que los campos obligatorios no estén vacíos
            if not nombre or not apellido or not idSala:
                flash("Faltan datos", "error")
                return redirect('/register/enfermero')

            # Crea un nuevo enfermero
            nuevo_enfermero = Enfermero(
                nombre=nombre,
                apellido=apellido,
                turno=turno,
                idSala=idSala,
            )
            # Guarda en la base de datos
            db.session.add(nuevo_enfermero)
            db.session.commit()

            # Mensaje de éxito
            flash("Enfermero guardado correctamente", "success")
            return redirect('/list/enfermero')
        except Exception as e:
            # En caso de error
            flash("Error al guardar el enfermero", "error")
            return redirect('/register/enfermero')

    # Si el método es GET, renderiza el formulario
    return render_template('Enfermero/registro.html', salas=salas)



@router.route('/list/enfermero')
def list_enfermero():
    enfermeros = Enfermero.query.all()
    salas = Sala.query.all()
    return render_template('Enfermero/lista.html', enfermeros=enfermeros,salas=salas)


#Ruta para editar enfermeros
@router.route('/edit/enfermero/<int:id>', methods=['GET', 'POST'])
def edit_enfermero(id):
    # Obtener el enfermero por ID
    enfermero = Enfermero.query.get_or_404(id)
    
    # Obtener todas las salas para el formulario
    salas = Sala.query.all()
    
    if request.method == 'POST':
        try:
            # Actualizar los datos del enfermero
            enfermero.nombre = request.form.get('nombre')
            enfermero.apellido = request.form.get('apellido')
            enfermero.turno = request.form.get('turno')
            enfermero.idSala = request.form.get('idSala')
            
            # Validar campos obligatorios
            if not enfermero.nombre or not enfermero.apellido or not enfermero.idSala:
                flash("Faltan datos", "error")
                return redirect(url_for('router.edit_enfermero', id=id))
            
            # Guardar los cambios
            db.session.commit()
            
            flash("Enfermero actualizado correctamente", "success")
            return redirect(url_for('router.list_enfermero'))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar el enfermero", "error")
            return redirect(url_for('router.edit_enfermero', id=id))
    
    # Si es GET, mostrar el formulario con los datos actuales
    return render_template('Enfermero/editar.html', enfermero=enfermero, salas=salas)



#Ruta para eliminar enfermeros
@router.route('/delete/enfermero/<int:id>', methods=['GET'])
def delete_enfermero(id):
    try:
        # Busca el enfermero por ID
        enfermero = Enfermero.query.get_or_404(id)

        db.session.delete(enfermero)
        db.session.commit()

        flash("Enfermero eliminado correctamente", "success")

    except Exception as e:
        flash(f"Error al eliminar el enfermero", "error")
    
    return redirect(url_for('router.list_enfermero'))


















#Ruta para registrar citas
@router.route('/register/cita', methods=['GET', 'POST'])
def register_cita():
    # Obtener todas las salas y pacientes para el formulario
    salas = Sala.query.all()
    pacientes = Paciente.query.all()

    if request.method == 'POST':
        try:
            # Obtén los datos enviados desde el formulario
            fecha = request.form.get('fecha')
            motivo = request.form.get('motivo')
            hora = request.form.get('hora')
            idPaciente = request.form.get('idPaciente')
            idSala = request.form.get('idSala')
            
            # Valida que los campos obligatorios no estén vacíos
            if not fecha or not motivo or not hora or not idPaciente or not idSala:
                flash("Faltan datos", "error")
                return redirect('/register/cita')

            # Crea una nueva cita
            nueva_cita = Citas(
                fecha=fecha,
                motivo=motivo,
                hora=hora,
                idPaciente=idPaciente,
                idSala=idSala,
            )
            # Guarda en la base de datos
            db.session.add(nueva_cita)
            db.session.commit()

            # Mensaje de éxito
            flash("Cita guardada correctamente", "success")
            return redirect('/list/cita')
        except Exception as e:
            # En caso de error
            flash("Error al guardar la cita", "error")
            return redirect('/register/cita')

    # Si el método es GET, renderiza el formulario
    return render_template('Cita/registro.html', salas=salas, pacientes=pacientes)



@router.route('/list/cita')
def list_cita():
    citas = Citas.query.all()
    salas = Sala.query.all()
    pacientes = Paciente.query.all()
    return render_template('Cita/lista.html', citas=citas, salas=salas, pacientes=pacientes)


#Ruta para editar citas
@router.route('/edit/cita/<int:id>', methods=['GET', 'POST'])
def edit_cita(id):
    # Obtener la cita por ID
    cita = Citas.query.get_or_404(id)
    
    # Obtener todas las salas y pacientes para el formulario
    salas = Sala.query.all()
    pacientes = Paciente.query.all()
    
    if request.method == 'POST':
        try:
            # Actualizar los datos de la cita
            cita.fecha = request.form.get('fecha')
            cita.motivo = request.form.get('motivo')
            cita.hora = request.form.get('hora')
            cita.idPaciente = request.form.get('idPaciente')
            cita.idSala = request.form.get('idSala')
            
            # Validar campos obligatorios
            if not cita.fecha or not cita.motivo or not cita.hora or not cita.idPaciente or not cita.idSala:
                flash("Faltan datos", "error")
                return redirect(url_for('router.edit_cita', id=id))
            
            # Guardar los cambios
            db.session.commit()
            
            flash("Cita actualizada correctamente", "success")
            return redirect(url_for('router.list_cita'))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar la cita", "error")
            return redirect(url_for('router.edit_cita', id=id))
    
    # Si es GET, mostrar el formulario con los datos actuales
    return render_template('Cita/editar.html', cita=cita, salas=salas, pacientes=pacientes)



#Ruta para eliminar citas
@router.route('/delete/cita/<int:id>', methods=['GET'])
def delete_cita(id):
    try:
        # Busca la cita por ID
        cita = Citas.query.get_or_404(id)

        db.session.delete(cita)
        db.session.commit()

        flash("Cita eliminada correctamente", "success")

    except Exception as e:
        flash(f"Error al eliminar la cita", "error")
    
    return redirect(url_for('router.list_cita'))